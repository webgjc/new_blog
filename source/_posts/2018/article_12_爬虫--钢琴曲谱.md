
---
title: 爬虫--钢琴曲谱
catalog: true
date: 2018-3-29 13:19:58
---

最近学钢琴，也经常会用到曲谱，但网上大多数曲谱不清晰，或者清晰的要vip。因此研究下某曲谱网站，进行爬取vip才能下载的曲谱并组合为pdf。<!--more-->

可以在<a href="http://123.206.217.190:8888">http://123.206.217.190:8888</a>试用效果

下面的是python3.x代码，在window可直接本地运行，在linux做一些注释中的修改。
<pre>#coding:utf-8
import requests
from bs4 import BeautifulSoup
import os
import sys
import io
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import time
import random
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

#输入弹琴吧所需琴谱的网址
#把网址变成手机访问的网址
req = requests.Session()
url=""
#url = "http://www.tan8.com/yuepu-58546.html"
state=True

while state:
    url = input("输入弹琴吧钢琴曲网址：\n")
    if url.find("-m.html")==-1:
        url = url.replace(".html","-m.html")
        imgdir = "tmpimgtan8/"

    if url.find("-m.html")==-1:
        print("请输入正确网址")
    else:
        imgdir = "tmpimgtan8/"
        state=False

if not os.path.exists(imgdir):
    os.mkdir("tmpimgtan8")
#爬下来解析出mp3，图片地址
#保存MP3，图片
resp = req.get(url)

soup=BeautifulSoup(resp.text,"lxml")

#windows可以用这个中文名做文件名
title = soup.find_all("title")[0].text.replace(" ","").replace("/","")
#linux用下面的随机数做文件名
#title = str(int(random.random()*8999)+1000)

mp3 = soup.find_all("source")[0]["src"]
mreq = req.get(mp3)
print(title)
with open(title+".mp3","wb") as f:
    f.write(mreq.content)
    f.close()

picul = soup.find_all("ul",{"class":"swiper-wrapper"})[0]

images = picul.find_all("img")

for i in images:
    imgurl = req.get(i['src'])
    with open(imgdir+".".join(i['src'].split(".")[-2:]),"wb") as f:
        f.write(imgurl.content)
        f.close()

files=os.listdir(imgdir)

if "Thumbs.db" in files:
    files.remove("Thumbs.db")
#把图片连接成pdf
f_pdf = title+".pdf"
(w, h) = landscape(A4)
c = canvas.Canvas(f_pdf, pagesize = (h,w))

for file in files:
    c.drawImage(imgdir+file,0,0,h,w)
    c.showPage()
    os.remove(imgdir+file)
c.save()
try:
    os.rmdir("tmpimgtan8")
except:
    print("请手动删除 tmpimgtan8")</pre>
同时，还顺手写了个web服务的代码。

可以到<a href="https://github.com/webgjc/blog">https://github.com/webgjc/blog</a>的tan8/查看。
