
---
title: tensorflow入门之mnist手写数字识别
catalog: true
date: 2017-4-29 11:22:31
---

这是<a href="https://www.tensorflow.org/">tensorflow官网</a>的第一个例子，按他的做就可以在测试数据集达到91%左右的识别率。之后的cnn版本就可以在测试数据集达到98%以上的正确率。

因为直接用他的写没什么感觉，然后稍微摸索了一下mnist的内容。<!--more-->

下面先将mnist的55000个测试数据变成图片的形式，直观一点。
<pre>#python3.5
#windows
#引入所需库
import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf
from PIL import Image,ImageFilter
import numpy as np
import os
#关掉警告,tensorflow会有op unknown的警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
#读取mnist数据,第一次的话会自动下载
mnist=input_data.read_data_sets("MNIST_data/", one_hot=True)
#将每个784*1的像素数据变成28*28,再生成图像
for z in range(len(mnist.train.images)):
    imgArr=mnist.train.images[z]
    im=Image.new("RGB",(28,28))
    for i in range(28):
        for j in range(28):
            r=int(imgArr[i*28+j]*255)
            im.putpixel((j,i),(r,r,r))
    num=np.argmax(mnist.train.labels[z])
    im.save("train/"+str(z)+"_"+str(num)+".jpg","jpeg")
print("finish")</pre>
之后直接读取图像来进行训练。
<pre>#python3.5
#windows
import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf
import numpy as np
from PIL import Image,ImageFilter
import os
mnists=input_data.read_data_sets("MNIST_data/", one_hot=True)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
f=os.listdir("train/")
L=len(f)-1
mnist=np.zeros((L,784))
label=np.zeros((L,10))
#读取每个图像数据存到mnist中，类别存到label中
for i in range(L):
    imgdir='train/'+str(f[i])
    img=Image.open(imgdir).convert("L")
    mnist[i]=np.array(img.getdata())/255
    label[i]=[1 if j==int(f[i].split("_")[1][:-4]) else 0 for j in range(10)]
#之后的操作和tensorflow官网一样
x=tf.placeholder(tf.float32,[None,784])
w=tf.Variable(tf.zeros([784,10]))
b=tf.Variable(tf.zeros([10]))
y=tf.nn.softmax(tf.matmul(x,w)+b)
y_=tf.placeholder(tf.float32,[None,10])
cross_entropy=-tf.reduce_sum(y_*tf.log(y))
train_step=tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
sess=tf.InteractiveSession()
tf.global_variables_initializer().run()
for _ in range(1000):
    rand=np.random.randint(0,L,(100,))
    batch_xs=mnist[rand]
    batch_ys=label[rand]
    sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys})
correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
print(sess.run(accuracy,feed_dict={x:mnists.test.images,y_:mnists.test.labels})</pre>
运行结果91%左右。也算稍稍做了改变。

cnn版的还有待研究，虽然代码也很简单。先贴在这里（网上找的，兄台没记住链接不好意思）。
<pre>import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
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


mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
print("Download Done!")

sess = tf.InteractiveSession()

# paras
W_conv1 = weight_varible([5, 5, 1, 32])
b_conv1 = bias_variable([32])

# conv layer-1
x = tf.placeholder(tf.float32, [None, 784])
x_image = tf.reshape(x, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

# conv layer-2
W_conv2 = weight_varible([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# full connection
W_fc1 = weight_varible([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
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
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.arg_max(y_conv, 1), tf.arg_max(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess.run(tf.initialize_all_variables())
for i in range(2000):
    batch = mnist.train.next_batch(50)

    if i % 100 == 0:
        train_accuacy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g"%(i, train_accuacy))
    train_step.run(feed_dict = {x: batch[0], y_: batch[1], keep_prob: 0.5})

# accuacy on test
print("test accuracy %g"%(accuracy.eval(feed_dict={x: mnist.test.images[0:2000], y_: mnist.test.labels[0:2000], keep_prob: 1.0})))</pre>
