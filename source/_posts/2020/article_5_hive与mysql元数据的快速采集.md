---
title: hive与mysql元数据的快速采集
catalog: true
date: 2020-04-05 16:35:20
subtitle:
header-img: "/img/article_header/header.jpg"
tags:
- 元数据
- 大数据
- MYSQL
---

## Hive元数据采集

首先以hive举例，

hive可以在命令行执行下面命令得到大部分表和字段的元数据，  
但因为这样每个都要执行就很慢。
> DESCRIBE FORMATTED {tablename}

然后直接尝试从metastore库采集，这里不做metastore具体结构的论述，  
想了解详细结构可以移步[Hive MetaStore的结构](https://www.jianshu.com/p/420ddb3bde7f)。

因为是按库采集，首先想到的方法是先到通过库获取库下的全部表列表，  
再通过库获取全部表的字段，然后在代码里进行对应表字段的整合，  
因为要对每个表都进行比对修改和版本记录等，因此就一个个表进行处理入库。  
这样取数的过程因为就两个mysql事务的步骤，实际就很快，但入库时的效率就会偏低。

下面是Metastore获取库，表，字段的具体操作：
- 先有要采集的库名，到**dbs**表根据name查询到对应的一条数据，得到库的一些信息，记录下**db_id**;
- 根据得到的**db_id**在tbls表找到对应**db_id**的表列表，每条数据包含了表名，类型，创建时间等信息；
- 表的元数据还不够，有一部分在**table_params**表中，他的存储方式是**tbl_id, key，value，key**包含了文件数，行数，大小，备注，更新时间等(有些不一定靠谱)
- 通过**tbl_id**到**partition**，**partition_params**，**partition_keys**可以拿到分区表的分区信息和全部分区的大小
  

- 然后是取一个库的全部字段，当然字段都是要带有**tbl_id**的，这样才能与上面表列表对应。
- 通过**db_id**从**tbls**获取到对应的表列表，通过列表中的**sd_id**到表sds得到对应的**cd_id**列表
- 通过**cd_id**列表到表**columns_v2**获取到对应的字段信息
- 另外分区字段需要额外从**partition_keys**通过**tbl_id**获取

使用上述操作，将表信息和字段信息分别使用join拼接为一张大表（这里可能会产生一些慢查询，可以把这个同步放到从库里），这样就已经拿到了基本想要的信息，然后通过tbl_id对表和字段数据进行整合，在把表一张张进行处理更新或新建，同时更新相关联的项；

## Mysql元数据采集

Mysql按理来说是和上面metastore基本一样的，但这边想更快一点，且可以忽略调表、字段和其他有外键关联的项；

information_schema的结构大致见[这里](https://www.jianshu.com/p/c08fe8e01c0a)

这里以tables表为例，存了大部分表元数据，取数据比如库记录id 
> database_id = 2   
> database_name = db_test

取表数据数据

> select `TABLE_SCHEMA`, `TABLE_NAME`, `TABLE_TYPE`  
> form `TABLES` where `TABLE_SCHEMA` = 'db_test'

在往后端同步数据时，先建一个db_id 与 table_name 的唯一索引，然后使用on duplicate key update实现对插入数据还是更新数据的检查。例如下

> insert into back_table  
> (db_id, table_name, table_type)  
> values  
> ('test', 'db_test', 'test', 'test')  
> on duplicate key update  
> table_name=values(table_name),  
> table_type=values(table_type);

然后直接完成对后端元数据的同步。字段同理。

这种方式采集一般的库几百张表和字段的就非常快了，基本都3秒以内。但也要考虑在表和字段比较多的时候要进行分批处理，否则可能一个sql过大或插入过慢。

## 关于实时采集

上面讲到的方式基本都是对全部元数据进行定时采集，定时的全量采集有个缺点就很慢，建了表好久才能同步到。

一般优化的方式是定时采集也可以分为新表采集与全量采集，这样把新表采集的频率变高，全量采集不变，可以稍微优化下体验。

然后这里再来考虑一下实时采集的方案。

主要利用的是mysql的binlog，先开启MySQL的binlog；

然后使用MySQL binlog的增量订阅&消费组件，如ali的canal，将binlog的json消息发送到消息队列，如kafka；

然后写一个消费端去消费，如果消费到create语句，就根据库名，表名到源数据库进行一次单表的采集。这样就可以实现建表即实时采集到元数据系统中。

mysql开启binlog见[这里](https://www.jianshu.com/p/5870cf1affb6)

canal连接mysql接受binlog并把数据投递到kafka见[这里官方教程](https://github.com/alibaba/canal/wiki/Canal-Kafka-RocketMQ-QuickStart)(安装教程也在这里)

之后写个kafka消费端来接受json的binlog数据，并得到库表去进行采集同步，  
这里用java实现实现了一个消费kafka的demo。
``` Java
package cn.ganjiacheng;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.util.Collections;
import java.util.Properties;

/**
 * @description:
 * @author: again
 * @email: 935669873@qq.com
 * @date: 2020/3/9 11:46 上午
 */
public class KafkaConsumerTest {

    public static void main(String[] args) {
        String topic = "mysqldata";
        String groupID = "lalal";

        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", groupID);
        props.put("enable.auto.commit", "true");
        props.put("auto.commit.interval.ms", "1000");
        props.put("auto.offset.reset", "earliest");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(props);

        consumer.subscribe(Collections.singletonList(topic));
        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(1000);
                for(ConsumerRecord<String, String> record: records) {
                    System.out.println(String.format("offset = %s, key = %s, value = %s", record.offset(), record.key(), record.value()));
                }
            }
        } finally {
            consumer.close();
        }
    }
}
```

开启canal的flatMessage为true，拿到的数据为json格式，  
从value里解析json数据如下，能拿到database和table。
之后就可以进行元数据采集。
``` json
{
    "data": null,
    "database": "canal",
    "es": 1586092113000,
    "id": 1,
    "isDdl": true,
    "mysqlType": null,
    "old": null,
    "pkNames": null,
    "sql": "sql sql sql",
    "sqlType": null,
    "table": "table_name",
    "ts": 1586092904217,
    "type": "CREATE"
}
```