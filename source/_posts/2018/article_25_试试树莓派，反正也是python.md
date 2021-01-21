
---
title: 试试树莓派，反正也是python
catalog: true
date: 2018-7-15 14:55:54
---

学校一个课程用到，在linux实现一个qt界面来控制几个硬件功能：摄像头，温湿度，超声波测距，红绿灯。<!--more-->

安装对应库，运行代码前就是要把器件连到对应的引脚上。
<pre>#coding:utf-8
#author:!@#$%^&amp;*()_+ganster
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication,QLCDNumber,QVBoxLayout,QGridLayout,QCheckBox,QPushButton
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtCore import QThread,Qt,pyqtSignal
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import sys
import time
import cv2
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)  #红
GPIO.setup(20,GPIO.OUT)  #黄
GPIO.setup(21,GPIO.OUT) #绿

#超声波测距端口
Trig_Pin = 5
Echo_Pin = 6
GPIO.setup(Trig_Pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)

#温湿度端口
channel = 4

#温湿度
def get_temp():
    data = []
    j = 0
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(channel, GPIO.HIGH)
    GPIO.setup(channel, GPIO.IN)
    while GPIO.input(channel) == GPIO.LOW:
        continue
    while GPIO.input(channel) == GPIO.HIGH:
        continue
    while j &lt; 40:
        k = 0
        while GPIO.input(channel) == GPIO.LOW:
            continue
        while GPIO.input(channel) == GPIO.HIGH:
            k += 1
            if k &gt; 100:
                break
        if k &lt; 8:
            data.append(0)
        else:
            data.append(1)
        j += 1
    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]
    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0
   
    for i in range(8):
        humidity += humidity_bit[i] * 2 ** (7-i)
        humidity_point += humidity_point_bit[i] * 2 ** (7-i)
        temperature += temperature_bit[i] * 2 ** (7-i)
        temperature_point += temperature_point_bit[i] * 2 ** (7-i)
        check += check_bit[i] * 2 ** (7-i)
   
    tmp = humidity + humidity_point + temperature + temperature_point
   
    if check == tmp:
        return [temperature,humidity]
    else:
        return [0,0]
    GPIO.cleanup()

#超声波测距
def get_dis():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    return round((t2-t1)*340*100/2,2)

#qt视图模块
class Example(QWidget):

    def __init__(self):
        super().__init__()
        #初始化视图
        self.initUI()
        #线程，用于更新摄像头图像
        self.sum = Sum()
        self.sum.sinOut.connect(self.update_img)
        self.sum.start()  

        self.r = 0
        self.g = 0
        self.y = 0
        self.show()      


    def initUI(self):      
        #加入按钮，复选框，lcd，并绑定事件
        hbox = QGridLayout(self)
        self.lbl = QLabel(self)

        self.lcd1 = QLCDNumber(self)
        self.lcd2 = QLCDNumber(self)

        self.cb1 = QCheckBox('red',self)
        self.cb2 = QCheckBox('yellow',self)
        self.cb3 = QCheckBox('green',self)
        self.cb1.stateChanged.connect(self.changecb1)
        self.cb2.stateChanged.connect(self.changecb2)
        self.cb3.stateChanged.connect(self.changecb3)

        self.btn = QPushButton(self)
        self.btn.setText("start")
        self.btn.clicked.connect(self.update_num)


        self.lcd3 = QLCDNumber(self)
        self.btn1 = QPushButton(self)
        self.btn1.setText("dis start")
        self.btn1.clicked.connect(self.update_dis)

        hbox.addWidget(self.lbl,0,0,1,3)
        hbox.addWidget(self.lcd1,1,0,1,1)
        hbox.addWidget(self.lcd2,1,1,1,1)
        hbox.addWidget(self.cb1,3,0,1,1)
        hbox.addWidget(self.cb2,3,1,1,1)
        hbox.addWidget(self.cb3,3,2,1,1)
        hbox.addWidget(self.btn,1,2,1,1)
        hbox.addWidget(self.lcd3,2,0,1,2)
        hbox.addWidget(self.btn1,2,2,1,1)

        self.setLayout(hbox)

    #更新图像
    def update_img(self,im):
        height, width, bytesPerComponent= im.shape
        bytesPerLine = bytesPerComponent* width
        cv2.cvtColor(im, cv2.COLOR_BGR2RGB,im)
        self.image= QImage(im.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.lbl.setPixmap(QPixmap.fromImage(self.image))
    #更新温湿度
    def update_num(self):
        #res = os.popen("python temp.py")
        #li = list(map(int,res.read().strip().split(",")))
        li = get_temp()
        print(li)
        self.lcd1.display(li[0])
        self.lcd2.display(li[1])
    #更新距离
    def update_dis(self):
        self.lcd3.display(get_dis())
    #更新复选框
    def changecb1(self):
        if self.r == 0:
            GPIO.output(16,GPIO.HIGH)
            self.r = 1
        else:
            GPIO.output(16,GPIO.LOW)
            self.r = 0
    def changecb2(self):
        if self.y == 0:
            GPIO.output(20,GPIO.HIGH)
            self.y = 1
        else:
            GPIO.output(20,GPIO.LOW)
            self.y = 0
    def changecb3(self):
        if self.g == 0:
            GPIO.output(21,GPIO.HIGH)
            self.g = 1
        else:
            GPIO.output(21,GPIO.LOW)
            self.g = 0

#线程，用于更新图像
class Sum(QThread):
    sinOut = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))

    def run(self):   
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            self.sinOut.emit(image)
            self.rawCapture.truncate()
            self.rawCapture.seek(0)
            time.sleep(0.2)
#主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())</pre>
作为电子专业，单片机，FPGA，树莓派都玩了，也差不多无憾了。

但也说不定是最后一次接触硬件方面的东西了呢。
