
---
title: python实现简单时时打印桌面程序
catalog: true
date: 2017-3-31 00:01:39
---

这里的需求是用户在某个网页下单之后，需要打印机打出票据。

实现：用python访问一个网络接口获取需要打印的数据（json格式），之后调用系统win32print的打印接口打印出来。

时时打印的话下面用轮询并定时sleep实现。<!--more-->

再用Tkinter写一个桌面程序可以用来提醒并可以使程序长久运行。

之后再用py2exe把python文件变成一个exe文件方便在后台执行。
<pre>#coding:utf-8
#python2.7
#引入需要的库
from tkMessageBox import *
from Tkinter import *
import hashlib
import urllib2
import json
import win32ui  
import win32print  
import win32con  
import time
import socket
#定义打印机，获取内容，定义样式，打印
def send_to_printer(title,txt,txt1,txt2,txt3,txt4,txt5): 
    hDC = win32ui.CreateDC()  
    hDC.CreatePrinterDC(win32print.GetDefaultPrinter())  
    hDC.StartDoc(title)
    hDC.StartPage()
    hDC.SetMapMode(win32con.MM_TWIPS)
    #定义位置
    ulc_x = 1000  
    lrc_x = 11500  
    lrc_y = -11500 
    ulc_y = -100  
    hDC.DrawText(txt,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT)
    ulc_x = 100
    ulc_y = -400  
    hDC.DrawText(txt1,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT) 
    ulc_x = 100
    ulc_y = -2300  
    hDC.DrawText(txt1,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT)
    ulc_x = 150 
    ulc_y = -700  
    hDC.DrawText(txt2,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT) 
    ulc_x = 150 
    ulc_y = -1000  
    hDC.DrawText(txt3,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT) 
    #修改字体大小
    font = win32ui.CreateFont({
        "name": "Lucida Console",
        "height": 400,
        "weight": 400,
    })
    hDC.SelectObject(font) 
    ulc_x = 150 
    ulc_y = -1400  
    hDC.DrawText(txt4,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT) 
    ulc_x = 150 
    ulc_y = -1800  
    hDC.DrawText(txt5,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT) 
    hDC.EndPage()  
    hDC.EndDoc()
#开一个桌面程序，提醒并在后台运行
root = Tk()
#设置socket超时时间
socket.setdefaulttimeout(20)
showinfo('信息', '打印机已成功运行')
root.destroy()
#下面轮询调用接口并处理数据，导入打印
while 1:
    #捕获所有错误，使中间不会中断
    try:
        #调用接口获取json并处理
        response = urllib2.urlopen('http://test.com') 
        ret = response.read()
        #print ret
        res=json.loads(ret)
        #处理数据这部分自定义
        txt="1";txt2="2";txt3="3";txt4="4";txt5="5"
        send_to_printer("title",txt,txt1,txt2,txt3,txt4,txt5)
        response.close()
        #5秒调用一次
        time.sleep(5)
    except Exception,e:  
        #错误处理，可以打印在log上，这里只简单的捕获
        print Exception,":",e</pre>
在用py2exe之前还得写另一个setup.py
<pre>from distutils.core import setup
import py2exe
#filename是上面写的那个python文件的文件名
setup(windows=["filename.py"])</pre>
把两个文件放在同目录下，用shift+右键，在此处打开命令行，运行
<pre>python setup.py py2exe</pre>
在产生的dist文件夹里有相同文件名的exe文件，可以双击直接执行，会先报一个成功运行，之后就在后台运行。

因为他会在后台一直运行着，所以关闭的话也得到任务管理器-&gt;进程里找到那个文件名的exe后台进程，把它结束掉就行。
