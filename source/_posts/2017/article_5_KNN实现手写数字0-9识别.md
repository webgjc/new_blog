
---
title: KNN实现手写数字0-9识别
catalog: true
date: 2017-3-9 00:07:34
---

KNN：我的简单理解为计算各个点到原点的距离，对于于样本数据以相差远近排序，取前面K个，属于哪个类别比较多的就当做最后分类，样本越多就越精确。<!--more-->

举个栗子：样本点：[a,b,c,d,e,f]，类别：[1,2,3,2,3,5]，假定a-f分别为相差从近到远；

如果K取1，那分类结果属于1，如果K取值为4，拿结果便为2。

废话不多说直接上代码：
<pre>//KNN分类的主程序
from numpy import *
import operator
def classify(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0] 
    #获取行
    diffMat=tile(inX,(dataSetSize,1))-dataSet 
    #=array([行数个inX])-dataSet
    sqDiffMat=diffMat**2 
    #每个数**2
    sqDistances=sqDiffMat.sum(axis=1) 
    #.sum()--所有数相加 .sum(axis=0)--列 .sum(axis=1)--行
    distances=sqDistances**0.5
    #每个数**0.5
    sortedDistIndicies=distances.argsort()
    #.argsort()返回排好序后的索引值
    classCount={}
    for i in xrange(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        #获取由近到远的类别
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
        #.get(key,default) 对类别进行计数
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    #.iteritems()返回迭代器 operator.itemgetter(1)返回第一个域的值    reverse=True倒序
    return sortedClassCount[0][0]
    #输出频率高（靠近）的一个</pre>
这里简单在提一下图像的处理PIL，以后会详细研究
<pre>from PIL import Image
im=Image.open("xxx.jpg")
data=im.getdata()
//data里便是像素点数据</pre>
之后要做的就是手写好一大部分的图，并用文件名来标记图所代表的数字，这些用来作为训练。

再把像素点转为numpy的矩阵，并标记好每个代表的数字。

载入新来的一张图得到矩阵，带入到上面的classify()就能得出结果，至于K应该取多少，凭经验来做判断，或者用大量数据做训练得出正确率最高的K值。

&nbsp;
