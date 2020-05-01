---
title: HIVE源码学习--实现一个自定义的HIVE序列化与反序列化
catalog: true
date: 2020-05-01 14:31:43
subtitle: 
header-img: 
tags:
- HIVE
---

## 前言

hive本身并不存储数据，它用的是hdfs上存储的文件，在与hdfs的文件交互读取和写入的时候需要用到序列化，  
hive有一个serde模块，其中就有很多的序列化器和反序列化器，
- 序列化(serialize)是将导入的数据转成hadoop的Writable格式
- 反序列化(deserialize)是select时将hadoop上的数据导入到内存object

当然也有一部分不放在serde模块里，但一样的是他们都继承自AbstractSerDe，
hive已实现的有LazySimpleSerde，ColumnarSerde，AvroSerde，ORC，RegexSerde，Thrift，Parquet，CSV，JSONSerde。且他支持添加自定义的实现，因此就来实现一个。

## 实操

### 数据准备

这边序列化一个比较简单的格式,
但对于其他的道理是一样的，一行对应于表格的一行数据。
```
id=1,name="jack",age=20
id=2,name="john",age=30
```

### 新建项目myserde

新建maven项目，引入hive-serde模块
``` xml
<dependency>
      <groupId>org.apache.hive</groupId>
      <artifactId>hive-serde</artifactId>
      <version>3.1.2</version>
</dependency>
```

``` java
package cn.ganjiacheng;

import org.apache.commons.lang3.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hive.serde.serdeConstants;
import org.apache.hadoop.hive.serde2.AbstractSerDe;
import org.apache.hadoop.hive.serde2.SerDeException;
import org.apache.hadoop.hive.serde2.SerDeStats;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspector;
import org.apache.hadoop.hive.serde2.objectinspector.ObjectInspectorFactory;
import org.apache.hadoop.hive.serde2.objectinspector.PrimitiveObjectInspector;
import org.apache.hadoop.hive.serde2.typeinfo.PrimitiveTypeInfo;
import org.apache.hadoop.hive.serde2.typeinfo.TypeInfo;
import org.apache.hadoop.hive.serde2.typeinfo.TypeInfoUtils;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Nullable;
import java.util.*;

/**
 * @description: 自定义序列化
 * @author: again
 * @email: ganjiacheng@souche.com
 * @date: 2020/4/30 1:55 下午
 */
 // 继承自AbstractSerDe，主要实现他下面的initialize，serialize，deserialize
public class MySerde extends AbstractSerDe {

    private static final Logger logger = LoggerFactory.getLogger(MySerde.class);

    // 用于存储字段名
    private List<String> columnNames;

    // 用于存储字段类型
    private List<TypeInfo> columnTypes;
    private ObjectInspector objectInspector;

    // 初始化，在serialize和deserialize前都会执行initialize
    @Override
    public void initialize(Configuration configuration, Properties tableProperties, Properties partitionProperties) throws SerDeException {
        String columnNameString = tableProperties.getProperty(serdeConstants.LIST_COLUMNS);
        String columnTypeString = tableProperties.getProperty(serdeConstants.LIST_COLUMN_TYPES);
        columnNames = Arrays.asList(columnNameString.split(","));
        columnTypes = TypeInfoUtils.getTypeInfosFromTypeString(columnTypeString);

        List<ObjectInspector> columnOIs = new ArrayList<>();
        ObjectInspector oi;
        for(int i = 0; i < columnNames.size(); i++) {
            oi = TypeInfoUtils.getStandardJavaObjectInspectorFromTypeInfo(columnTypes.get(i));
            columnOIs.add(oi);
        }
        objectInspector = ObjectInspectorFactory.getStandardStructObjectInspector(columnNames, columnOIs);
    }

    // 重载的方法，直接调用上面的实现
    @Override
    public void initialize(@Nullable Configuration configuration, Properties properties) throws SerDeException {
        this.initialize(configuration, properties, null);
    }

    @Override
    public Class<? extends Writable> getSerializedClass() {
        return null;
    }

    // o是导入的单行数据的数组，objInspector包含了导入的字段信息，这边直接就按顺序
    // 将数据处理成key=value,key1=value1的格式的字符串，并返回Writable格式。
    @Override
    public Writable serialize(Object o, ObjectInspector objInspector) throws SerDeException {
        Object[] arr = (Object[]) o;
        List<String> tt = new ArrayList<>();
        for (int i = 0; i < arr.length; i++) {
            tt.add(String.format("%s=%s", columnNames.get(i), arr[i].toString()));
        }
        return new Text(StringUtils.join(tt, ","));
    }

    @Override
    public SerDeStats getSerDeStats() {
        return null;
    }

    // writable转为字符串，其中包含了一行的信息，如key=value,key1=value1
    // 分割后存到map中，然后按照字段的顺序，放到object中
    // 中间还需要做类型处理，这边只简单的做了string和int
    @Override
    public Object deserialize(Writable writable) throws SerDeException {
        Text text = (Text) writable;
        Map<String, String> map = new HashMap<>();
        String[] cols = text.toString().split(",");
        for(String col: cols) {
            String[] item = col.split("=");
            map.put(item[0], item[1]);
        }
        ArrayList<Object> row = new ArrayList<>();
        Object obj = null;
        for(int i = 0; i < columnNames.size(); i++){
            TypeInfo typeInfo = columnTypes.get(i);
            PrimitiveTypeInfo pTypeInfo = (PrimitiveTypeInfo)typeInfo;
            if(typeInfo.getCategory() == ObjectInspector.Category.PRIMITIVE) {
                if(pTypeInfo.getPrimitiveCategory() == PrimitiveObjectInspector.PrimitiveCategory.STRING){
                    obj = StringUtils.defaultString(map.get(columnNames.get(i)));
                }
                if(pTypeInfo.getPrimitiveCategory() == PrimitiveObjectInspector.PrimitiveCategory.INT) {
                    obj = Integer.parseInt(map.get(columnNames.get(i)));
                }
            }
            row.add(obj);
        }
        return row;
    }

    @Override
    public ObjectInspector getObjectInspector() throws SerDeException {
        return objectInspector;
    }

    @Override
    public String getConfigurationErrors() {
        return super.getConfigurationErrors();
    }

    @Override
    public boolean shouldStoreFieldsInMetastore(Map<String, String> tableParams) {
        return super.shouldStoreFieldsInMetastore(tableParams);
    }
}

```


### 建表与调试

编译完刚才的项目后
打开本地hive
引入刚才开发的包
> add jar (项目路径)/target/xxx.jar

建表，这里row format改为自己的序列化器
``` sql
CREATE EXTERNAL TABLE `test_serde`(
    `id` int,
    `name` string,
    `age` int
)
ROW FORMAT SERDE 'cn.ganjiacheng.MySerde'
STORED AS TEXTFILE;
```

然后导入一份数据，这边直接本地写一份上面的样例数据导入
> load data local inpath '/本地文件地址' overwrite into table test_serde;

试着查一下结果，走的为deserialize方法，显示的为正常的表格，  
这边多了引号，到时候可以中间处理去掉即可。
```
hive> select * from test_serde;
OK
1	"jack"	20
2	"john"	30
Time taken: 0.85 seconds, Fetched: 2 row(s)
```

再尝试插入一条数据，就会走serialize方法
```
hive> insert into table test_serde values(3, "qwe", 40);
Query ID = again_20200501164049_6aa10f95-73df-41ac-a9af-9bfdcecb2f7d
Total jobs = 3
Launching Job 1 out of 3
Number of reduce tasks is set to 0 since there's no reduce operator
Job running in-process (local Hadoop)
2020-05-01 16:41:00,802 Stage-1 map = 0%,  reduce = 0%
2020-05-01 16:41:01,851 Stage-1 map = 100%,  reduce = 0%
Ended Job = job_local853094563_0001
Stage-4 is selected by condition resolver.
Stage-3 is filtered out by condition resolver.
Stage-5 is filtered out by condition resolver.
Moving data to: hdfs://master:9000/user/hive/warehouse/test_serde/.hive-staging_hive_2020-05-01_16-40-49_469_5467796518535031523-1/-ext-10000
Loading data to table default.test_serde
Table default.test_serde stats: [numFiles=2, numRows=1, totalSize=68, rawDataSize=0]
MapReduce Jobs Launched:
Stage-Stage-1:  HDFS Read: 9 HDFS Write: 87 SUCCESS
Total MapReduce CPU Time Spent: 0 msec
OK
Time taken: 13.902 seconds

hive> select * from test_serde;
OK
3	qwe	40
1	"jack"	20
2	"john"	30
Time taken: 0.229 seconds, Fetched: 3 row(s)
```

来到hadoop确认一下
```
$ hadoop fs -cat /user/hive/warehouse/test_serde/000000_0
20/05/01 17:06:20 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
id=3,name=qwe,age=40
```

## 关于开发时的debug

和部署hive后hive的hive clidriver的debug类似

首先开启
> hive --debug

会显示正监听8000端口

然后在idea上打开myserde的项目，配置一个Remote，  
host为loclahost，port为8000  
use module为当前用到的module

在代码中间比如deserialize方法中打上断点，开启remote

然后hive命令行就会进入命令行模式

> add jar (项目路径)/target/xxx.jar
> use default;  
> select * from test_serde;

就会触发进入我们打在deserialize上的断点。

## 学习借鉴
- [Hive系列之SerDe](https://www.jianshu.com/p/9c43f03b97e7)