
---
title: 使用ppython---实现python和php之间的通信
catalog: true
date: 2017-3-15 11:30:28
---

ppython大致是用socket来实现php和python的联络;

日常不常用，有必要时还是挺有用的。<!--more-->

先是用python的socket开一个端口监听，在这个端口来进行数据传输

之后php连接那个端口，向那个端口传输数据，python在接受到数据处理之后再返回结果。

这里介绍一下基本使用，先下载<a href="http://pan.baidu.com/s/1dEHgYgL">http://pan.baidu.com/s/1dEHgYgL</a>。

解压之后放到服务器上。

为了长久在Linux服务器里可以运行，开个screen
<pre>screen -S ppython</pre>
在screen里运行,可以看到Server Startup
<pre>python php_python.py</pre>
之后进行写各自要执行的python代码和php代码
<pre>#python
#modulename.py
def add(x,y):
    return x+y</pre>
<pre>&lt;?php
require_once("php_python.php");
$x=1;$y=2;
$result=ppython("modulename::add",x,y);
echo $result;</pre>
官方文档：<a href="https://code.google.com/archive/p/ppython/">https://code.google.com/archive/p/ppython/</a>
