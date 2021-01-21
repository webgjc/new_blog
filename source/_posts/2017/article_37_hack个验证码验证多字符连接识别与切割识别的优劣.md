
---
title: hack个验证码验证多字符连接识别与切割识别的优劣
catalog: true
date: 2017-7-31 21:26:27
---

有个多个字符识别的需求，想是要切割还是字符连接整个一起识别，所以就找了一个验证码来做对比尝试。这个验证码很简单，<a href="http://jxgl.hdu.edu.cn/CheckCode.aspx">验证码链接</a>，<!--more-->就中规中矩<img class="alignnone size-full wp-image-379" src="/img/uploads/2017/07/00126-1.png" alt="" width="60" height="22" />，

简单贴一下验证码爬下来的代码
<pre>import requests
from PIL import Image
from io import BytesIO
from threading import Thread
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
class Mythread(Thread):
    def __init__(self,num):
        Thread.__init__(self)
        self.num=num
    def run(self):
        while True:  
            req = requests.get("http://jxgl.hdu.edu.cn/CheckCode.aspx",headers=headers)
            im=Image.open(BytesIO(req.content))
            im.save("croptest/"+str(self.num)+".png")
threads=[]
for j in range(10):
    for i in range(10):
        t=Mythread(i+10*j)
        t.start()
        print(i+10*j)</pre>
之后做了去重，标记，测试正式开始

首先用不切割整体识别的方法，像素转换成黑白二值整个作为输入，输出为5个数，每个数10类的拼接，总共50类，每十个数中的1值为图中所对应的数。

先用tensorflow构建了cnn，对于cnn模型，中间并没有做很多改动，只进行了输入输出的调整。写了个输入函数把图像转换成输入数据，写了个训练函数对模型进行训练，由于样本较少，也只进行了不多的训练次数。又写了个测试函数用来爬取新图片对模型进行测试
<pre>import tensorflow as tf
import os
import numpy as np
import cv2

number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
char_Len=5*len(number)
dirname=os.listdir('dealyzm/')
dirname.remove('Thumbs.db')

def weight_varible(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
# paras
W_conv1 = weight_varible([5, 5, 1, 32])
b_conv1 = bias_variable([32])

# conv layer-1
x = tf.placeholder(tf.float32, [None, 1320])
x_image = tf.reshape(x, [-1, 22, 60, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

# conv layer-2
W_conv2 = weight_varible([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# full connection
shape = h_pool2.get_shape().as_list()
dim = 1
for d in shape[1:]:
    dim *= d
W_fc1 = weight_varible([dim, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, dim])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# output layer: softmax
W_fc2 = weight_varible([1024, char_Len])
b_fc2 = bias_variable([char_Len])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
y_ = tf.placeholder(tf.float32, [None, char_Len])

# model training
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv+ 1e-10))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
sess=tf.InteractiveSession()
tf.global_variables_initializer().run()

def getRanPic(num):
    image=[]
    name=[]
    for i in range(num):
        tmpname=[0]*char_Len
        filename=dirname[int(np.random.random()*len(dirname))]
        im=cv2.imread("dealyzm/"+filename,0)/255.0
        im=im.reshape(-1)
        for i in range(5):
            tmpname[number.index(filename[i])+len(number)*i]=1
        image.append(im)
        name.append(tmpname)
    return image,name
def trainFirst():
    saver = tf.train.Saver()
    for _ in range(400):
        batch_xs,batch_ys=getRanPic(20)
        tmp,loss=sess.run([train_step,cross_entropy],feed_dict={x:batch_xs,y_:batch_ys,keep_prob: 1.0})
        if _%20==0:
            batch_xs,batch_ys=getRanPic(20)
            correct_prediction=tf.equal(tf.argmax(tf.reshape(y_conv, [-1, 5, 10]),2),tf.argmax(tf.reshape(y_, [-1, 5, 10]),2))
            accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
            acc_test=sess.run(accuracy,feed_dict={x:batch_xs,y_:batch_ys,keep_prob: 1.0})
            print("loss:"+str(loss)+" acc_train:"+str(acc_test))
    saver.save(sess, 'model/testyzm-cnn.model', global_step=_)
def test():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    req = requests.get("http://jxgl.hdu.edu.cn/CheckCode.aspx",headers=headers)
    im=np.array(Image.open(BytesIO(req.content)))
    ret,im_hb=cv2.threshold(im,127,255,cv2.THRESH_BINARY)
    img=[im_hb.reshape(-1)/255]
    name=[[0]*50]
    saver = tf.train.Saver()
    with tf.Session() as sess:
        batch_xs,batch_ys=img,name
        path = 'model/testyzm-cnn.model-' + str(399)
        saver.restore(sess, path)
        predict = tf.argmax(tf.reshape(y_conv, [-1, 5, 10]), 2)
        pre = sess.run(predict, feed_dict={x:batch_xs,y_:batch_ys,keep_prob: 1.0})
        res=''.join(map(str,pre[0]))
        print(res)
    cv2.imshow("image",im)
    cv2.waitKey(0)
train=0
if train==0:
    trainFirst()
else:
    test()</pre>
测试结果便是整个对于自身的拟合效果还算可以，能达到90%以上，而对于test时的外来数据的表现不是很好，只有30%左右。

第二个模型，首先对样本进行了分割，把每张图的5个数分开来。
<pre>from PIL import Image
import os
d=os.listdir("dealyzm/")
k=0
for i in d:
    file=Image.open("dealyzm/"+i)
    for j in range(5):
        crop=file.crop((9*j+5,4,9*j+14,18))
        crop.save("crop/"+i[j]+str(k)+".png")
    k+=1</pre>
然后继续构建模型，只是调整了输入输出基本原理和上面一样
<pre>import tensorflow as tf
import numpy as np
import os
import cv2
import requests
from PIL import Image
from io import BytesIO

def weight_varible(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
# paras
W_conv1 = weight_varible([5, 5, 1, 32])
b_conv1 = bias_variable([32])

# conv layer-1
x = tf.placeholder(tf.float32, [None, 126])
x_image = tf.reshape(x, [-1, 9, 14, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

# conv layer-2
W_conv2 = weight_varible([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# full connection
shape = h_pool2.get_shape().as_list()
dim = 1
for d in shape[1:]:
    dim *= d
W_fc1 = weight_varible([dim, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, dim])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# output layer: softmax
W_fc2 = weight_varible([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
y_ = tf.placeholder(tf.float32, [None, 10])

# model training
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv+ 1e-10))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.arg_max(y_conv, 1), tf.arg_max(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess=tf.InteractiveSession()
tf.global_variables_initializer().run()

dirname=os.listdir("crop/")
dirname.remove("Thumbs.db")

def getRanPic(num):
    image=[]
    name=[]
    for i in range(num):
        tmpname=[0]*10
        filename=dirname[int(np.random.random()*len(dirname))]
        im=cv2.imread("crop/"+filename,0)/255.0
        im=im.reshape(-1)
        tmpname[int(filename[0])]=1
        image.append(im)
        name.append(tmpname)
    return image,name

def trainFirst():
    saver = tf.train.Saver()
    for _ in range(1000):
        batch_xs,batch_ys=getRanPic(50)
        train_step.run(feed_dict={x:batch_xs,y_:batch_ys,keep_prob: 1.0})
        if _%50==0:
            batch_xs,batch_ys=getRanPic(50)
            loss,acc=sess.run([cross_entropy,accuracy],feed_dict={x:batch_xs,y_:batch_ys,keep_prob: 1.0})
            print("loss:"+str(loss)+" acc_train:"+str(acc))
    saver.save(sess, 'model/next-crop-yzm-cnn.model', global_step=_)

def test(file):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    req = requests.get("http://jxgl.hdu.edu.cn/CheckCode.aspx",headers=headers)
    im=Image.open(BytesIO(req.content))
    img=[]
    name=[]
    for i in range(5):
        crop=np.array(im.crop((9*i+5,4,9*i+14,18)))
        ret,im_hb=cv2.threshold(crop,127,255,cv2.THRESH_BINARY)
        img.append(im_hb.reshape(-1)/255)
        name.append([0]*10)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        batch_xs,batch_ys=img,name
        path = 'model/testcropyzm-cnn.model-' + str(999)
        saver.restore(sess, path)
        predict = tf.arg_max(y_conv, 1)
        pre = sess.run(predict, feed_dict={x:batch_xs,y_:batch_ys,keep_prob: 1.0})
    im.save("croptest/"+"".join(map(str,pre))+".png")

train=1
if train==0:
    trainFirst()
else:
    test()</pre>
结果：第二次测试的正确率能达到99%以上，对于测试数据，也能有较高的正确率（测试了100个，没错）。

对比：

元数据一样是小样本，两种方法只做了输入输出的改变，但效果对比差别很明显。后者好很多。

猜测是多元连接的参数比分割后数字的参数多得多，所以训练所需的样本也会成倍增加，其中可能会有一定的关系。

猜测由于多个连接后反向传播的时候会对所有参数进行调整，所以很难训练起来。

对于小样本的模型训练还可以继续探究。可以尝试学习到一定特征然后用生成器创造大样本从而训练多个输出模型。
