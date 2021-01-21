
---
title: python数据分析之基础画图
catalog: true
date: 2018-1-3 16:49:12
---

之前由于每次有数据用python画图都要找找其他资料和手册，顾这里做一些总结，用于方便查找与快捷使用！这里主要用matplotlib.pyplot。<!--more-->
<pre>import numpy as np
import matplotlib.pyplot as plt
#得到测试点
x=np.linspace(-5,5,50)
y=np.sin(x)
z=2*x

#设置画板大小
plt.figure(figsize=(6,6))
#用plot画图,前两个参数为数据的x和y值
#第三个参数为三个属性的结合：颜色如(b，g，r)+标记如(.，o，,)+连线如(-，--，-.)
#label为线条说明，markersize为标记大小，linewidth为连线大小
plt.plot(x,y,"go-",label="yyy",markersize=2,linewidth=1)
plt.plot(x,z,"b.-",label="zzz")

#坐标轴显示范围
plt.axis([-5,5,-5,5])
#设置坐标轴刻度
plt.xticks([-5,0,5])
plt.yticks([-5,0,5],["bad","normal","good"])
#坐标轴说明
plt.xlabel("x axis")
plt.ylabel("y axis")
#图标题
plt.title("this is title")
#显示线条说明
plt.legend()
#显示网格
plt.grid(True)
#做标注
plt.annotate("con",xy=(0,0),xycoords='data',xytext=(+30,-30),textcoords='offset points',fontsize=16,arrowprops=dict(arrowstyle='-&gt;', connectionstyle="arc3,rad=.2"))
#做注释
plt.text(x,y,"con",fondict={'size':16,'color':'r'})
#画图
plt.show()</pre>
上面的plot可做散点也可作连线图，要做复杂的散点图也可以用plt.scatter

下面再试一试常用的柱状图
<pre>import numpy as np
import matplotlib.pyplot as plt
#得到测试点
x=np.linspace(0,5,10)
y=np.sin(x)
z=2*x
#画柱状图
plt.bar(x,z,width=0.1,bottom=None,align='center')
#画柱状大小的描述
for i,j in zip(x,z):
    plt.text(i,j,"%.2f"%j,ha='center',va='bottom')
plt.show()</pre>
再来尝试绘制一个饼图，这里引用<a href="https://www.jianshu.com/p/0a76c94e9db7">https://www.jianshu.com/p/0a76c94e9db7</a>
<pre>from matplotlib import pyplot as plt 

#调节图形大小，宽，高
plt.figure(figsize=(6,9))
#定义饼状图的标签，标签是列表
labels = [u'第一部分',u'第二部分',u'第三部分']
#每个标签占多大，会自动去算百分比
sizes = [60,30,10]
colors = ['red','yellowgreen','lightskyblue']
#将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
explode = (0.05,0,0)

patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
 labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
 startangle = 90,pctdistance = 0.6)

#labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
#autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
#shadow，饼是否有阴影
#startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
#pctdistance，百分比的text离圆心的距离
#patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

#改变文本的大小
#方法是把每一个text遍历。调用set_size方法设置它的属性
for t in l_text:
    t.set_size=(30)
for t in p_text:
    t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend()
plt.show()</pre>
先用matplotlib做这些基础的图形，之后亦可用seaborn做些更好看的。
