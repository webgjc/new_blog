
---
title: 用python写个自动改壁纸的桌面程序
catalog: true
date: 2017-11-10 18:11:31
---

忍无可忍桌面壁纸软件的广告了，终于决定自己写个，总体逻辑上也并不复杂。

先是随机爬取某bing站的壁纸图片，调用win32接口改桌面壁纸，之后用tk的桌面程序来获取用户输入时间间隔，最后封装成exe使得更通用，在后台运行以及加个图标。<!--more-->不说了，直接上代码。

由于是python3.x，库win32api库可能下载会有问题。建议直接去<a href="https://sourceforge.net/projects/pywin32/">这里</a>手动下载安装。
<pre>#coding:utf-8
#python3.5
#windows
from PIL import Image
import win32api,win32con,win32gui  
import re,os  
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import tkinter
import random
import math
import time
import re

def set_wallpaper_from_bmp(bmp_path):  
    #打开指定注册表路径  
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)  
    #最后的参数:2拉伸,0居中,6适应,10填充,0平铺  
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")  
    #最后的参数:1表示平铺,拉伸居中等都是0  
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")  
    #刷新桌面  
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,bmp_path, win32con.SPIF_SENDWININICHANGE)  
  
def set_wallpaper(bgimg):  
    #把图片格式统一转换成bmp格式,并放在源图片的同一目录  
    #注意地址必须是绝对地址
    new_bmp_path="C:/backgroundPicture/wallpaper.bmp"
    bmpImage = Image.open(BytesIO(bgimg))
    bmpImage.save(new_bmp_path, "BMP")  
    set_wallpaper_from_bmp(new_bmp_path)  

def getPicurl():
    #爬虫部分，主要从这个网站随机取页随机取壁纸，返回图片二进制。
    req=requests.Session()
    resp=req.get("https://bing.ioliu.cn/?p=1")
    soup=BeautifulSoup(resp.text,"lxml")
    pageall=soup.find_all("span")[-1].get_text()
    maxpage=int(pageall.split("/")[1].strip())
    ran=math.floor(random.random()*maxpage)+1
    resp1=req.get("https://bing.ioliu.cn?p="+str(ran))
    soup1=BeautifulSoup(resp1.text,"lxml")
    allimg=soup1.find_all("img")
    ran1=math.floor(random.random()*len(allimg))
    resp2=req.get("https://bing.ioliu.cn"+allimg[ran1].next_sibling['href'])
    url=re.findall(r'src="http(.*?)"',resp2.text)[0]
    image=req.get("http"+url)
    return image.content

def inputint():
    #获取用户输入的时间
    global t
    try:
        t = int(var.get().strip())
    except:
        t = 30
    root.destroy()

if __name__ == '__main__':  
    t=0
    if not os.path.exists('C:/backgroundPicture/'):
        os.mkdir("C:/backgroundPicture/")
    root = tkinter.Tk(className='请输入间隔时间(按分钟计)')  # 弹出框框名
    root.geometry('350x60')     # 设置弹出框的大小 w x h
    var = tkinter.StringVar()   # 这即是输入框中的内容
    var.set(30) # 通过var.get()/var.set() 来 获取/设置var的值
    entry1 = tkinter.Entry(root, textvariable=var)  # 设置"文本变量"为var
    entry1.pack()   # 将entry"打上去"
    btn1 = tkinter.Button(root, text='确认', command=inputint)     # 按下此按钮(Input), 触发inputint函数
    btn1.pack(side='bottom')
    root.mainloop()
    #一直运行并用sleep间隔
    while True:
        bgimg=getPicurl()
        set_wallpaper(bgimg)
        time.sleep(int(t*60))</pre>
关于打包成exe，在python3有个pyinstaller，直接用pip安装就行。

使用方式是以下，-F打包单个文件，-w不显示命令窗口，-i图标
<pre>pyinstaller -F -w -i bitbug_favicon.ico filename.py</pre>
以上便是自动换桌面壁纸，另附这里添加一个功能，就是在程序运行时用按键触发换壁纸。要做的便是另写一个线程做按键监听。这里用pyHook做按键监听，关于pyhook的安装，不能简单用pip，不然用按键监听的时候会有一个bug。

参考：<a href="https://blog.csdn.net/dongfuguo/article/details/70226384#reply">https://blog.csdn.net/dongfuguo/article/details/70226384#reply</a>
<pre>from ctypes import *
import pyHook
import pythoncom
import threading
def onKeyboardEvent(event):
    global lt
    #96为1左边那个按键，这里写法是双击
    if event.Ascii==96:
        if time.time()-lt&lt;2:
            bgimg=getPicurl()
            set_wallpaper(bgimg)
        else:
            lt=time.time()
    return True
def task0():
    hm = pyHook.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
def task1():
    global t
    while True:
        bgimg=getPicurl()
        set_wallpaper(bgimg)
        time.sleep(int(t*60))
threads = []
    t1 = threading.Thread(target=task0)
    threads.append(t1)
    t0 = threading.Thread(target=task1)
    threads.append(t0)
    for i in range(2):
        threads[i].start()
    for i in range(2):
        threads[i].join()</pre>
这段代码结合上面部分便可以完成一个自动换桌面且可按键手动换桌面的程序。

最后贴一下应用程序<a href="http://pan.baidu.com/s/1c1YXoje">下载地址。</a>
