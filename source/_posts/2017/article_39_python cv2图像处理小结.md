
---
title: python cv2图像处理小结
catalog: true
date: 2017-8-6 11:22:43
---

这里做图像处理初学的一个阶段性小结。从简单的读写到复杂点的开闭运算。还有一些用到过的边缘提取，垂直水平投影等方法。<!--more-->

首先是读写和展示
<pre>import cv2
#imread第二个参数不写默认是rgb彩色，有0读取到的就是黑白二值图
im = cv2.imread("image.jpg",0)
#写入文件
cv2.imwrite("img.jpg",im)
#展示
cv2.imshow("imageName",im)
cv2.waitKey(0)</pre>
一般复制粘贴的话可以用numpy，因为cv2本身图像保存的就是一个np矩阵。

这里的注意点就是先是y再是x。
<pre>crop = im[y:y+height,x:x+width]</pre>
改尺寸
<pre>res = cv2.resize(im,(width, height), interpolation = cv2.INTER_CUBIC)</pre>
灰度，二值（手动阀值和自动阀值）
<pre>im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#第二个参数为手动阀值
retval,im_hb = cv2.threshold(im_gray, 120, 255, cv2.THRESH_BINARY) 
#自动阀值
#这里255是二值中的高值，cv2.ADAPTIVE_THRESH_MEAN_C可以用cv2.ADAPTIVE_THRESH_GAUSSIAN_C
#cv2.THRESH_BINARY和cv2.THRESH_BINARY_INV是黑白相反的
#最后两个参数可以调整来改变黑白区域
im_hb = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 1)</pre>
膨胀，腐蚀，开闭运算，待尝试（形态学梯度、顶帽、黑帽）
<pre>#首先定义一个核，一般矩形用的多
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
#膨胀腐蚀是对图中白色部分而言，膨胀便是白色变多，腐蚀是白色变少
#腐蚀
eroded = cv2.erode(img,kernel)
#膨胀
dilated = cv2.dilate(img,kernel) 
#闭运算=先膨胀后腐蚀
closed = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel) 
#开运算=先腐蚀后膨胀
open = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)</pre>
mser连通域检测，原理貌似是把图像看做高低起伏的地形，然后往下灌水。
<pre>#图片如果底色比较单一就能用来截出内容，这里需要自己控制_min_area
mser = cv2.MSER_create(_min_area=1800)
regions, boxes = mser.detectRegions(im_hb)
for box in boxes:
    x, y, w, h = box
    cv2.rectangle(im, (x,y),(x+w, y+h), (255, 0, 0), 2)</pre>
垂直，水平投影做分割，这里没找到直接可用的接口，就自己实现
<pre>#首先需要的是一张二值图im，以白底黑字为例
division=np.array([[255.0]*width]*height)
#水平投影，可以用来确定字的上下边缘
for i in range(im.shape[0]):
     n=0
     for j in range(im.shape[1]):
         if closed[i][j]==0:
             division[i][n]=0
             n+=1
#垂直投影，可以用来确定字的左右边缘已经字符中间的空隙
for i in range(im.shape[1]):
    n=0
    for j in range(im.shape[0]):
        if division[j][i]==0:
            division[height-1-n][i]=0
            n+=1
</pre>
边缘检测，尝试了findContours和sobel算子和canny算子
<pre>#这里也需要二值图im
contours, hierarchy = cv2.findContours(im,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,(0,0,255),3)</pre>
<pre>x = cv2.Sobel(im,cv2.CV_16S,1,0)  
y = cv2.Sobel(im,cv2.CV_16S,0,1)  
absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)  
dst = cv2.addWeighted(absX,0.5,absY,0.5,0)</pre>
<pre>#最大最小阀值
canny = cv2.Canny(im, 50, 150)</pre>
入门至此把，python写起来还比较方便，至于最后还得上c++。

真实中图像各异，总的还得实践出真知！
