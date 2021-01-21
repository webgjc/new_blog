
---
title: 用python完成文本转音频(tts)
catalog: true
date: 2018-2-7 19:52:28
---

用 python完成tts的话一般会用pyttsx库，但一般pip下载的话会有各种报错。所以这里找了实际试了可用的github上几个改编的库。<!--more-->

对于python3.x版本，选择 <a href="https://github.com/jpercent/pyttsx">https://github.com/jpercent/pyttsx</a> ，来完成tts，但python3版本的目前还没发现有保存为音频文件的，只能直接发出声音。代码如下：
<pre>import pyttsx
engine = pyttsx.init()
engine.say("你好")
engine.runAndWait()</pre>
对于python2.7版本，可以选择<a href="https://github.com/hick/pyttsx">https://github.com/hick/pyttsx</a>来完成tts，他可以让文本转为声音并且可以下载保存为wav文件。

完成tts还需要pywin32，可以到这里下载对应版本，<a href="https://github.com/mhammond/pywin32/releases">https://github.com/mhammond/pywin32/releases</a>，试过目前没错。

这里使用的环境是在windows8，python2.7版本。如果要读中文的话可以在 控制面板--轻松使用--语音识别--文本到语音转换，看看有没有中文语音库。

当然还需要准备一个文本文件，在windows，首先把文本转为utf-8格式，具体做法是用记事本打开txt文件，文件--另存为--在编码里选utf-8，保存；

前戏完成，然后运行下面代码：
<pre>#coding:utf-8
import pyttsx

#读取txt文件(txt必须为utf-8编码)
s=open("filename.txt").read()

#解码为unicode
c=s.decode("utf-8")

#初始化tts
engine = pyttsx.init()

#直接发出声音
#engine.say(u"你好")

#保存为文件
engine.rec(c,"filename.wav")</pre>
