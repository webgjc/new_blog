---
title: '本地hadoop与hive的单节点部署和开发调试[mac]'
catalog: true
date: 2020-04-27 16:27:54
subtitle:
header-img:
tags:
- HIVE
- HADOOP
---

# 预备

这边部署的
hadoop版本为 [2.7.3](http://archive.apache.org/dist/hadoop/common/hadoop-2.7.3/)  
hive版本为 [1.2.1](http://archive.apache.org/dist/hive/hive-1.2.1/)  
注:src为源码包

# Hadoop搭建

## 解压，进入配置目录
> tar zxvf hadoop-2.7.3.tar.gz  
cd hadoop-2.7.3/etc/hadoop

## 修改配置 
core-site.xml，hdfs-site.xml， mapred-site.xml
``` xml
# core-site.xml
<configuration>
     <property>
        <name>hadoop.tmp.dir</name>
        <value>(补上绝对路径)/hadoop-2.7.3/hadoop</value>
     </property>
     <property>
        <name>dfs.name.dir</name>
        <value>(补上绝对路径)/hadoop-2.7.3/hadoop/name</value>
     </property>
     <property>
        <name>fs.default.name</name>
        <value>hdfs://master:9000</value>
     </property>
</configuration>

# hdfs-site.xml
<configuration>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>(补上绝对路径)/hadoop-2.7.3/namenode</value>
    </property>
    <property>
        <name>dfs.data.dir</name>
        <value>(补上绝对路径)/hadoop-2.7.3/data</value>
    </property>
    <property>
        <name>dfs.http.address</name>
        <value>0.0.0.0:50070</value>
    </property>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>

# mapred-site.xml
<configuration>
    <property>
        <name>mapred.job.tracker</name>
        <value>master:9001</value>
     </property>
</configuration>
```


## 配置免密登录
```
1。 设置自己的mac允许远程登录：
  首先我们打开系统偏好设置–>共享
  我们将远程登录、所有用户勾选

2. 设置免密码
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod og-wx ~/.ssh/authorized_keys
chmod 750 $HOME

执行 ssh localhost 测试
```

## 启动hadoop
>./hadoop-2.7.3/sbin/start-all.sh


## 验证安装成功
执行 WordCount  
在 hdfs 创建文件夹 hadoop fs -mkdir -p /data/input  hadoop fs -mkdir -p /data/out  
上传文本文件  
hadoop fs -put a.txt /data/input  
执行 wordcount  
hadoop jar ~/hadoop/hadoop-2.7.3/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar wordcount /data/input/a.txt /data/out/my_wordcont  

## 访问界面
Resourcemanager 界面 http://127.0.0.1:8088
hadoop提供的web页面 http://127.0.0.1:50070
查看 hdfs 界面 http://127.0.0.1:50070/explorer.html#/
访问 mapreduce 提供的任务查看页面  访问hadoop提供的web页面，通过Browse the system，可以查看hdfs中的文件。


# Hive搭建

## 解压文件
> tar -zxvf apache-hive-1.2.1-bin.tar.gz

## 修改配置

先复制一份默认的配置文件
``` shell
cd apache-hive-1.2.1-bin
cp conf/hive-env.sh.template conf/hive-env.sh
cp conf/hive-default.xml.template conf/hive-site.xml
```
修改hive-site.xml中的部分peoperty
``` xml
<property>
    <name>system:java.io.tmpdir</name>
    <value>/Users/root/hadoop/tmp</value>
</property>
<property>
    <name>system:user.name</name>
    <value>hive</value>
</property>

# mysql地址localhost
<property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://localhost:3306/hive</value>
</property>
# mysql的驱动
<property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.jdbc.Driver</value>
</property>
# 用户名
<property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>root</value>
</property>
# 密码
<property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>root</value>
</property>
<property>
    <name>hive.metastore.schema.verification</name>
    <value>false</value>
</property>
```

## 装好Mysql  
放一个mysql jdbc连接的jar包到 hive的lib下  

创建一个库用作metastore存储

## 初始化Metastore
>./bin/schematool -dbType mysql -initSchema

## 启动hive
./bin/hive

# Hive源码调试

下载hive中的src包
```
tar xvf apache-hive-1.2.1-src.tar.gz
cd apache-hive-1.2.1-src
mvn clean package -Phadoop-2 -DskipTests -Pdist
```

在刚刚装好的开启远程调试模式

>hive --debug

他会显示
Listening for transport dt_socket at address: 8000

然后在idea 打开hive源码项目，注意要把编译环境改成java1.8

添加一个Configuraiton Remote
host写127.0.0.1
port写刚刚的8000
包选择hive-cli

在org/apache/hadoop/hive/cli/CliDriver.java
中找main函数，并在run()行加上断点

点击debug就可以看到运行到断点处

## 特别感谢

- 本次文章来源特别感谢mayanbo同学。