
---
title: yolo在windows训练自己的数据集
catalog: true
date: 2017-7-22 17:00:01
---

上次讲了配置yolo，可以<a href="https://ganjiacheng.cn/blog/?p=300">戳这里</a>看哦！

这次讲讲yolo用于训练自己的数据集。<!--more-->

首先还是数据准备，比如人脸检测，那就先准备很多包含人脸的图片。

然后需要数据标注，也就是标出人脸在图片内的位置。这里用一个叫labelImg的工具。具体下载和使用看这里<a href="https://github.com/tzutalin/labelImg">https://github.com/tzutalin/labelImg</a>。

然后在图片文件夹里运行labelImg，会有个gui界面，之后就可以对每张图片进行标注，标注完后会有一大堆xml文件产生，之后运行一个python小脚本把xml转成所需的txt。

具体操作：把xml都放到一个xml文件夹里，然后在外面新建一个obj文件夹，运行下面python代码，xml会转成txt并存入obj文件夹。
<pre>#python3.5
import os
import shutil
import xml.etree.cElementTree as ET
f=os.listdir("xml/")
for i in f:
    filename=i[0:8]
    dirname="xml/"+i
    tree=ET.parse(dirname)
    root = tree.getroot()
    shutil.copy(filename+".jpg","obj/"+filename+".jpg")
    ft=open("obj/"+filename+".txt","w")
    for obj in root.findall("object"):
        data=obj.find("bndbox")
        wh=root.find("size")
        width=int(wh.find("width").text)
        height=int(wh.find("height").text)
        xmin=int(data.find("xmin").text)
        ymin=int(data.find("ymin").text)
        xmax=int(data.find("xmax").text)
        ymax=int(data.find("ymax").text)
        xmid=(xmin+xmax)/2
        ymid=(ymin+ymax)/2
        ft.write("0 "+str(xmid/width)+" "+str(ymid/height)+" "+str((xmax-xmin)/width)+" "+str((ymax-ymin)/height)+"\n")</pre>
然后把原图片也放在obj文件里，并把obj文件夹放到<a href="https://ganjiacheng.cn/blog/?p=300">上次项目</a>的darknetx64/data文件下。

然后在data下新建obj.names和obj.data。

obj.names写类别名，obj.data如下
<pre>classes= 类别数目
train  = data/train.txt
valid  = data/test.txt
names = data/obj.names
backup = backup/</pre>
然后再在data下新建train.txt和test.txt。

运行下面的代码就能把所有训练图名放到train.txt，然后也可以分一部分到test.txt。
<pre>#python3.5
import os
f=os.listdir("obj/")
file=open("train.txt","w")
for i in f:
    if i[-3:]=='jpg':
        file.write("data/obj/"+i+"\n")</pre>
然后在x64下创建yolo-obj.cfg，内容其他同yolo-voc.2.0.cfg

要改最后一个filter(224行左右)=(类别数+ 5)*5

电脑训练不起来的话也可以把第三行的subdivisions按倍数改小(默认为64，可以改32,16)

之后就可以开始训练模型咯，运行下面的代码可以开始训练
<pre>darknet.exe detector train data/obj.data yolo-obj.cfg</pre>
训练的时候可以看avg,一般是越低越好，趋于不变时就可以停止训练了。

每一百次会保存一次模型文件在backup文件夹里。

训练完后可以运行下面代码（xxx改为具体训练次数）来对新的图片进行检测。
<pre>darknet.exe detector test data/obj.data yolo-obj.cfg backup/yolo-obj_xxx.weights</pre>
这里在讲一个批量处理图片的方法。

vs里打开项目，detector.c文件，改test_detector函数，删掉输入while1和后面的input，直接改成for循环，图片名都用拼接的方法得到，比如1.jpg之类。

然后往函数里的draw_detections最后加个参数，把图片名传过去。

改image.c中draw_detections函数的参数，在用crop_image截取检测部分，用save_image保存检测出来的图像。同时去掉draw_box_width。

然后用ctrl+f搜索draw_detections，把所有用到这个函数的参数都改一下。

运行便可以批量处理图片并截取出所需部分。
