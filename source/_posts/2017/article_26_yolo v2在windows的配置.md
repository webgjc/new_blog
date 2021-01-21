
---
title: yolo v2在windows的配置
catalog: true
date: 2017-7-22 16:04:02
---

这里讲讲yolo在windows的配置，实际操作可行，这里使用时电脑为win8.1。

开始前可以到nvidia官网先看看显卡是否支持gpu哦！<!--more-->

首先下载vs2015，cuda，cudnn并配置好，这里不多叙述，标准就是：能在vs创建一个cuda项目并运行他的默认导入的代码并得到结果。在下载个opencv2.4.9，这里2.49是项目需求，改其他版本的话得改代码。

之后使用了git下载github上某个大神改好后的代码
<pre>git clone https://github.com/AlexeyAB/darknet.git</pre>
在vs里打开项目，打开build下的darknet.sln

然后在右边项目上右键-&gt;属性，

在 vc++目录 中编辑包含目录，把opencv里的include文件夹路径添加到里面。

在 c/c++   常规    附加包含目录 中把opencv的include路径加进去，如果没有cudaToolkitIncludeDir则把cuda和cudnn的include路径加进去。

在c/c++   预处理器   预处理器定义中加上OPENCV和GPU。有报错的话也可以加上_CRT_SECURE_NO_DEPRECATE，_SCL_SECURE_NO_DEPRECATE这两个。

在链接器   常规   添加库目录中加入opencv的lib路径，如果没有cuda_Path的话加上cuda，cudnn的lib路径。

在链接器   输入   附加依赖项中加入pthreadVC2.lib（自行下载），cublas.lib，curand.lib，cudart.lib和opencv里的所有lib。

然后就可以尝试运行啦。少库的话把库的路径加进去就行。

之后就可以下载一个<a href="https://pjreddie.com/media/files/yolo.weights">yolo.weights</a>，放在x64文件夹下。

在x64文件夹下运行
<pre>darknet.exe detector test data/coco.data yolo.cfg yolo.weights -i 0 -thresh 0.2</pre>
输入图片文件路径

配置好opencv的话就会直接展示，否则会保存成prediction.png文件。

或者运行下面的代码就会调用摄像头并时时检测。
<pre>darknet.exe detector demo data/coco.data yolo.cfg yolo.weights</pre>
看data/coco.name就可以知道该模型可识别的80类。

cpu上的平均8秒一张图左右，

我的920m gpu可以达到5fps，也还达不到视频标准。

下次再具体讲讲训练自己的数据。

参考地址：<a href="https://github.com/AlexeyAB/darknet">https://github.com/AlexeyAB/darknet</a>
