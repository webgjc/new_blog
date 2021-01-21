---
title: 利用Hadoop-MapReduce实现稀疏矩阵乘法
catalog: true
date: 2020-05-24 10:31:43
subtitle:
header-img:
tags:
    - HADOOP
---

# 前言

之前关于 hadoop，也就试过一个 wordcount，这次来学习一下用 mapreduce 实现矩阵乘法，体会一下里面的思路过程。

# 预备

## 开发环境准备

第一次开发 MapReduce 程序可以看下这边的环境准备
[开发环境准备](#mapreduce开发环境)

## MapReduce

关于 MapReduce 这边只用到最基础的，因此了解一下[wordcount](http://hadoop.apache.org/docs/r1.0.4/cn/mapred_tutorial.html)也就能知道最基础的思想。

-   Map 将每行数据转为 key,value 的格式;
-   shuffle 会将相同 key 的 value 放到一个数组迭代器里变为 key，values[];
-   Reduce 读取数据并做计算处理;

## 数据存储

因为针对的是稀疏的大矩阵，直接按矩阵格式存储会产生很多 0，  
因此这边采用了 x, y ,v 的格式，x，y 表示坐标(从 0，0 开始)，v 表示数值

## 测试数据

为了方便这边就用 int 的数据来测试，且只准备了一个小矩阵，但原理一样

```
// matA 4x3
1  2  3
4  5  0
7  8  9
10 11 12

// matB 3x2
10 15
0  2
11 9
```

转为 x, y, v 的格式后

```
// matA
0,0,1
0,1,2
0,2,3
1,0,4
1,1,5
2,0,7
2,1,8
2,2,9
3,0,10
3,1,11
3,2,12

// matB
0,0,10
0,1,15
1,1,2
2,0,11
2,1,9

// 计算结果数组C
0,0	43
0,1	46
1,0	40
1,1	70
2,0	169
2,1	202
3,0	232
3,1	280
```

将两个文件存到项目根目录/input 下

# 三种实现

这边要讨论三种实现，思想上稍稍不同。

下面矩阵名以 A，B，C 替代，表示 AxB=C。  
A 为 mxl  
B 为 lxn  
C 为 mxn

## 基础的矩阵相乘

关于矩阵相乘，一般的就会考虑到 A 的行点乘以 B 的列为 C 的一个值，  
所以最先考虑的是将 A 的第 i 行和 B 的第 i 列的数据放到一个 mapreduce 的 key 中，key 值为计算结果在 C 中的坐标。  
然后考虑 A 的每行数据需要在 B 的每列用到，用到的地方都需要拷贝一份数据到对应 key 中，B 同样，就是 map 部分逻辑。  
例如 A 的第一格数据 0,0,1，他会在与 B 的第一列，第二列点乘的时候用到成为 C 的第一行的一部分，就将它加到 key(0,0)(0,1)中。

例如上面的测试数据，这么做以后得到的 key,value 为，就是 map 部分  
value 的第一个区分矩阵，第二个是 A 的列\B 的行，第三个表示值。

```
0,0
matB,2,11
matB,0,10
matA,0,1
matA,1,2
matA,2,3

0,1
matA,0,1
matA,1,2
matA,2,3
matB,0,15
matB,2,9
matB,1,2
...
```

在 reduce 阶段，将 A 的列与 B 的行相等的计算乘积并相加的到 C 的一格的结果。

盗一张图，可以很清楚的表示这个过程，他这个的定义 1，1 为开始点
![mapreduce_show](/img/mypost/mapreduce_show.jpg)

来看具体代码

```java
package cn.ganjiacheng;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

import java.io.IOException;
import java.util.Iterator;

/**
 * @description: CALC A*B
 * @author: again
 * @email: ganjiacheng@souche.com
 * @date: 2020/5/23 10:57 上午
 */
public class Matrix {

    private static String MATA = "matA"; // 矩阵名
    private static String MATB = "matB";
    private static int MATRIXA_R = 4; // A矩阵行
    private static int MATRIXA_C = 3; // A矩阵列
    private static int MATRIXB_C = 2; // B矩阵列

    // Map部分
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {

        @Override
        public void map(LongWritable longWritable, Text text, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            String line = text.toString();
            String[] lineData = line.split(",");
            String fileName = ((FileSplit) reporter.getInputSplit()).getPath().getName(); // 矩阵分别存两个文件，获取文件名判断是哪个矩阵
            if(MATA.equals(fileName)){
                // A矩阵时，遍历B的列，将值放到点乘会用到的对应key中
                for(int i = 0; i < MATRIXB_C; i++) {
                    // 返回key value的结果
                    outputCollector.collect(
                            new Text(String.format("%s,%s", lineData[0], i)),
                            new Text(String.format("%s,%s,%s", MATA, lineData[1], lineData[2])));
                }
            }

            if(MATB.equals(fileName)) {
                // B同样
                for(int i = 0; i < MATRIXA_R; i++) {
                    outputCollector.collect(
                            new Text(String.format("%s,%s", i, lineData[1])),
                            new Text(String.format("%s,%s,%s", MATB ,lineData[0], lineData[2])));
                }
            }
        }
    }

    // Reduce部分
    public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {

        @Override
        public void reduce(Text text, Iterator<Text> iterator, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            // 初始化0数组存储对应相乘的值
            int[] valA = new int[MATRIXA_C];
            int[] valB = new int[MATRIXA_C];
            for(int i = 0; i < MATRIXA_C; i++) {
                valA[i] = 0;
                valB[i] = 0;
            }
            // 将value按第二个值的index存入数组
            while(iterator.hasNext()) {
                String item = iterator.next().toString();
                String[] itemData = item.split(",");
                if(MATA.equals(itemData[0])) {
                    valA[Integer.parseInt(itemData[1])] = Integer.parseInt(itemData[2]);
                }
                if(MATB.equals(itemData[0])) {
                    valB[Integer.parseInt(itemData[1])] = Integer.parseInt(itemData[2]);
                }
            }
            // 数组乘积求求和得到C一个位置的值
            int result = 0;
            for(int i = 0; i < MATRIXA_C; i++) {
                result += valA[i] * valB[i];
            }
            // 写入结果
            outputCollector.collect(text, new Text(Integer.toString(result)));
        }
    }

    public static void main(String[] args) throws Exception {
        // 这个是为了重复运行自动删除输出目录
        Configuration conf = new Configuration();
        Path outpath = new Path(args[1]);
        FileSystem fileSystem = outpath.getFileSystem(conf);
        if(fileSystem.exists(outpath)){
            fileSystem.delete(outpath, true);
        }

        // 定义任务
        JobConf jobConf = new JobConf(Matrix.class);
        jobConf.setJobName("matrix");

        // 定义输入输出类型
        jobConf.setOutputKeyClass(Text.class);
        jobConf.setOutputValueClass(Text.class);

        // 定义mapreduce过程
        jobConf.setMapperClass(Map.class);
        jobConf.setReducerClass(Reduce.class);

        // 定义输入输出路径
        FileInputFormat.addInputPath(jobConf, new Path(args[0]));
        FileOutputFormat.setOutputPath(jobConf, new Path(args[1]));

        // 运行任务
        JobClient.runJob(jobConf);
    }
}
```

## 分块矩阵乘法

上面的方法有个问题是在 Map 过程中 A 的每个数据要扩大 B 列倍，B 的每个数据要扩大 A 行倍，数据较为冗余。

一种优化方式是将矩阵分块。
分块的计算原理如下
![juzhengfenkuai](/img/mypost/juzhengfenkuai.jpg)

分块后如果是 k 个分为一块，数据大致可以减少 k 倍，

map 的时候按 C 的结果大块进行取 key，同时将需要进行对应计算的 A 列块和 B 行块划分到一起，reduce 的时候进行对应的块的矩阵计算。

这边举例以 2 个为一块，矩阵切分后如下，A 为 2x2，B 为 2x1  
C 即为 2x1，shuffle 后的的 key 原本会有 6 个，现在只需要 4 个，且每个数量也减少了

如下将 1 2 4 5 和 10 15 0 2 （DIV \*_ 2 _ 2）的块划到一起并在第一层 reduce 做计算，返回的 key 为对应行列
然后第二层 mapreduce 将计算结果合并累加

```
1  2  | 3
4  5  | 0
---------
7  8  | 9
10 11 | 12


10 15
0  2
-----
11 9

// shuffle后的数据格式
0,0,0
matB,0,0,10
matB,0,1,15
matB,1,1,2
matA,0,0,1
matA,0,1,2
matA,1,0,4
matA,1,1,5
0,1,0
matA,0,2,3
matB,2,0,11
matB,2,1,9
1,0,0
matB,0,0,10
matB,0,1,15
matB,1,1,2
matA,2,0,7
matA,2,1,8
matA,3,0,10
matA,3,1,11
1,1,0
matA,2,2,9
matA,3,2,12
matB,2,0,11
matB,2,1,9
```

上代码

```java
package cn.ganjiacheng;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

import java.io.IOException;
import java.util.*;

/**
 * @description:
 * @author: again
 * @email: ganjiacheng@souche.com
 * @date: 2020/5/24 10:29 上午
 */
public class BlockMatrix {

    private static String MATA = "matA";
    private static String MATB = "matB";
    private static int MATRIXA_R = 4; // A矩阵行
    private static int MATRIXA_C = 3; // A矩阵列
    private static int MATRIXB_C = 2; // B矩阵列
    private static int DIV = 2; // 每多少个分块

    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {

        @Override
        public void map(LongWritable longWritable, Text text, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            String line = text.toString();
            String[] lineData = line.split(",");
            int row = Integer.parseInt((lineData[0]));
            int col = Integer.parseInt((lineData[1]));
            String fileName = ((FileSplit) reporter.getInputSplit()).getPath().getName();
            if(MATA.equals(fileName)){
                // 分块后key只需要存分好的大块的位置和A列B行对应值，
                // value需要全部位置和值
                // 保证每块shuffle后数据量都只有 DIV**2 * 2
                for(int i = 0; i < Math.ceil(1.0 * MATRIXB_C / DIV); i++) {
                    outputCollector.collect(
                            new Text(String.format("%s,%s,%s", row/DIV, col/DIV, i)),
                            new Text(String.format("%s,%s,%s,%s", MATA, row, col, lineData[2])));
                }
            }

            if(MATB.equals(fileName)) {
                for(int i = 0; i < Math.ceil(1.0 * MATRIXA_R / DIV); i++) {
                    outputCollector.collect(
                            new Text(String.format("%s,%s,%s", i, row/DIV, col/DIV)),
                            new Text(String.format("%s,%s,%s,%s", MATB, row, col, lineData[2])));
                }
            }
        }
    }

    public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {

        @Override
        public void reduce(Text text, Iterator<Text> iterator, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            // 将A和B的x,y,v分别存储
            List<List<Integer>> listA = new ArrayList<>();
            List<List<Integer>> listB = new ArrayList<>();
            while(iterator.hasNext()){
                String value = iterator.next().toString();
                String[] data = value.split(",");
                if(MATA.equals(data[0])) {
                    listA.add(Arrays.asList(Integer.parseInt(data[1]), Integer.parseInt(data[2]), Integer.parseInt(data[3])));
                }
                if(MATB.equals(data[0])) {
                    listB.add(Arrays.asList(Integer.parseInt(data[1]), Integer.parseInt(data[2]), Integer.parseInt(data[3])));
                }
            }
            // 遍历A和B A的y和B的x相等的做乘积存入map，
            // key为A的x和B的y，value为乘积或乘积的累积
            HashMap<String, Integer> valueMap = new HashMap<>();
            for(List<Integer> itemA: listA) {
                for(List<Integer> itemB: listB) {
                    if(itemA.get(1).equals(itemB.get(0))) {
                        String key = String.format("%s,%s", itemA.get(0), itemB.get(1));
                        if(!valueMap.containsKey(key)) {
                            valueMap.put(key, itemA.get(2) * itemB.get(2));
                        }else{
                            valueMap.put(key, valueMap.get(key) + itemA.get(2) * itemB.get(2));
                        }
                    }
                }
            }
            // 每个key都取一遍就是C
            for(String key: valueMap.keySet()) {
                outputCollector.collect(new Text(key), new Text(Integer.toString(valueMap.get(key))));
            }
        }
    }
    // 后续需要接一个累加的mapreduce，这个与下面的列行乘法相同，见下方。
}
```

## 列行相乘

这个的思想基本和第二种的 reduce 部分差不多，但这个不是利用 hashmap 来自己合并，而用两次 mapreduce 来实现。找到 A 的列与 B 的行值相等的两个值进行乘积作为值，取 A 的行与 B 的列作为 Key，然后将同样 key 的 value 相加就可以得到结果。

这个需要分两步 MapReduce，  
第一步 Mapreduce 是取相等的列行相乘得值，key 为对应的行列
第二步 MapReduce 是将相等的 key 相加，得到 C 的结果。

```java
package cn.ganjiacheng;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.*;

import java.io.IOException;
import java.util.*;

/**
 * @description:
 * @author: again
 * @email: ganjiacheng@souche.com
 * @date: 2020/5/24 1:46 下午
 */
public class LhMatrix {
    private static String MATA = "matA";
    private static String MATB = "matB";
    private static int MATRIXA_R = 4; // A矩阵行
    private static int MATRIXA_C = 3; // A矩阵列
    private static int MATRIXB_C = 2; // B矩阵列

    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {

        @Override
        public void map(LongWritable longWritable, Text text, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            String line = text.toString();
            String[] lineData = line.split(",");
            String fileName = ((FileSplit) reporter.getInputSplit()).getPath().getName();
            if(MATA.equals(fileName)){
                // 将A的y作为key
                outputCollector.collect(
                        new Text(lineData[1]),
                        new Text(String.format("%s,%s,%s", MATA, lineData[0], lineData[2])));
            }

            if(MATB.equals(fileName)) {
                // 将B的x作为key
                outputCollector.collect(
                        new Text(lineData[0]),
                        new Text(String.format("%s,%s,%s", MATB, lineData[1], lineData[2])));
            }
        }
    }

    public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {

        @Override
        public void reduce(Text text, Iterator<Text> iterator, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            List<List<Integer>> listA = new ArrayList<>();
            List<List<Integer>> listB = new ArrayList<>();
            while(iterator.hasNext()){
                String value = iterator.next().toString();
                System.out.println(value);
                String[] data = value.split(",");
                if(MATA.equals(data[0])) {
                    listA.add(Arrays.asList(Integer.parseInt(data[1]), Integer.parseInt(data[2])));
                }
                if(MATB.equals(data[0])) {
                    listB.add(Arrays.asList(Integer.parseInt(data[1]), Integer.parseInt(data[2])));
                }
            }
            // shuffle同样key的AB全排列并做乘积，
            // 返回key为C的坐标，value为一部分乘积，后续要做累加
            for(List<Integer> itemA: listA) {
                for(List<Integer> itemB: listB) {
                    outputCollector.collect(
                            new Text(String.format("%s,%s", itemA.get(0), itemB.get(0))),
                            new Text(Integer.toString(itemA.get(1) * itemB.get(1))));
                }
            }
        }
    }

    // 下面的mapreduce做累加
    public static class SumMap extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {

        @Override
        public void map(LongWritable longWritable, Text text, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            // 取出第一次输出的结果
            String[] line = text.toString().split("\t");
            outputCollector.collect(new Text(line[0]), new Text(line[1]));
        }
    }

    public static class SumReducer extends MapReduceBase implements Reducer<Text, Text, Text, Text> {

        @Override
        public void reduce(Text text, Iterator<Text> iterator, OutputCollector<Text, Text> outputCollector, Reporter reporter) throws IOException {
            // 累加
            int sum = 0;
            while(iterator.hasNext()) {
                sum += Integer.parseInt(iterator.next().toString());
            }
            outputCollector.collect(text, new Text(Integer.toString(sum)));
        }
    }

    // 这边跑了两个mapreduce
    // 需要有第三个参数 第二次输出的路径
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Path outpath = new Path(args[1]);
        FileSystem fileSystem = outpath.getFileSystem(conf);
        if(fileSystem.exists(outpath)){
            fileSystem.delete(outpath, true);
        }
        Path outpath1 = new Path(args[2]);
        FileSystem fileSystem1 = outpath1.getFileSystem(conf);
        if(fileSystem1.exists(outpath1)){
            fileSystem1.delete(outpath1, true);
        }

        JobConf jobConf = new JobConf(LhMatrix.class);
        jobConf.setJobName("block matrix");

        jobConf.setOutputKeyClass(Text.class);
        jobConf.setOutputValueClass(Text.class);

        jobConf.setMapperClass(LhMatrix.Map.class);
        jobConf.setReducerClass(LhMatrix.Reduce.class);

        FileInputFormat.setInputPaths(jobConf, new Path(args[0]));
        FileOutputFormat.setOutputPath(jobConf, new Path(args[1]));

        JobClient.runJob(jobConf);


        JobConf jobConf1 = new JobConf(LhMatrix.class);
        jobConf1.setJobName("block matrix sum");
        jobConf1.setOutputKeyClass(Text.class);
        jobConf1.setOutputValueClass(Text.class);
        jobConf1.setMapperClass(LhMatrix.SumMap.class);
        jobConf1.setReducerClass(LhMatrix.SumReducer.class);

        FileInputFormat.addInputPath(jobConf1, new Path(args[1]));
        FileOutputFormat.setOutputPath(jobConf1, new Path(args[2]));
        JobClient.runJob(jobConf1);
    }
}

```

# 小结

-   第一种基本的矩阵乘法，实现比较直接，主要问题在于 map 的时候数据复制了 n 份，导致 shuffle 的数据过大；另一个是每个 reduce 的时候获得的数据量为 m+n，且需要转存到内存中，可能会导致存储不下。
-   第二种分块相乘，将数据复制分数减少了 DIV 倍，同时一个 reduce 的数据量在 DIV\*_2 _ 2 的大小；麻烦的是需要控制的就是 DIV 取合适的值。
-   第三种列行相乘，这边实现的是直接在全集上进行列行分，其实也可以在分块后进行列行，这边的每个 reduce 也是会有 m+n 的数据进来内存中，分块后再按列行划分就是步骤会多了点，也是可以的。

**感觉最为关键的一步是在 map 的时候对数据进行合理的计算划分与分发，就如同这边对矩阵的分块/列行对应分发(什么作为 key)，不同的 key 划分对应的计算量和中间过程数据完全不同。划分完后的每块 reduce 的计算基本是水到渠成的事情，都是一些累加或点乘的事情。**

# MapReduce 开发环境

这边因为本地装的 hadoop2.7.3 版本，  
因此新建 maven 项目，使用了 2.7.3 的依赖包，不过运行可以不依赖本地

```xml
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-core</artifactId>
    <version>1.2.1</version>
</dependency>
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-common</artifactId>
    <version>2.7.3</version>
</dependency>
```

打开 idea 的运行配置，  
新建 Application 的配置，

Main class 填写如下；
arguments 参数填写如下，第一个为 mvn 打包后的 jar，  
第二个为运行的类，  
后面两个为类的参数，表示输入输出路径(这边相对路径是相对项目根目录)
![mapreduce_configure](/img/mypost/mapreduce_configure.jpg)

然后直接点运行即可，debug 也可以

# 感谢

-   [MapReduce 官方教程](http://hadoop.apache.org/docs/r1.0.4/cn/mapred_tutorial.html)
-   [MapReduce 实现大矩阵乘法](https://blog.csdn.net/xyilu/article/details/9066973)
-   [一些算法的 MapReduce 实现——矩阵分块乘法计算](https://blog.csdn.net/wzhg0508/article/details/17475573)
-   [列行相乘法](https://www.cnblogs.com/Decmber/p/5491920.html)
-   [高度可伸缩的稀疏矩阵乘法](https://wenku.baidu.com/view/bd3da325cf84b9d528ea7a96.html)
