
---
title: 许愿墙效果（仿）
catalog: true
date: 2017-3-26 15:09:15
---

也不知道为什么要叫许愿墙，在<a href="http://www.qdfuns.com/">前端网</a>看到许多人实现了，便来实现一个自己的版本，顺便许个愿！

这里需要先看一下下面这张图，对于后面的理解很有帮助。<!--more-->

<a href="/img/uploads/2017/03/2014091409260873.png"><img class="alignnone wp-image-213 size-medium" src="/img/uploads/2017/03/2014091409260873-300x159.png" alt="" width="300" height="159" /></a>

使用方法：下面代码复制到一个html文件里，之后浏览器打开就行。

具体实现在代码中注释。
<pre>&lt;!doctype html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;&lt;/title&gt;
    &lt;style type="text/css"&gt;
    /*去除默认内外边距*/
    * {
        margin: 0px;
        padding: 0px;
    }
    /*背景颜色*/
    html,
    body {
        height: 100%;
        background: -webkit-linear-gradient(top, rgb(203, 235, 219) 0%, rgb(55, 148, 192) 120%);
        background: -moz-linear-gradient(top, rgb(203, 235, 219) 0%, rgb(55, 148, 192) 120%);
    }
    /*画边框曲线*/
    .item {
        width: 200px;
        height: 200px;
        -webkit-border-bottom-left-radius: 20px 500px;
        -webkit-border-bottom-right-radius: 500px 30px;
        -webkit-border-top-right-radius: 5px 100px;
        -moz-border-bottom-left-radius: 20px 500px;
        -moz-border-bottom-right-radius: 500px 30px;
        -moz-border-top-right-radius: 5px 100px;
        box-shadow: 0 2px 10px 1px rgba(0, 0, 0, 0.2);
        -webkit-box-shadow: 0 2px 10px 1px rgba(0, 0, 0, 0.2);
        -moz-box-shadow: 0 2px 10px 1px rgba(0, 0, 0, 0.2);
        position: absolute;
        background: #FF9FDC;
        cursor: move;
        z-index: 2;
    }
    /*文字位置和属性*/
    .txt {
        margin-left: 25%;
        margin-top: 10%;
        color: white;
        font-size: 20px;
        font-family: "YouYuan";
    }
    /*设置关闭链接位置*/
    .close {
        position: absolute;
        bottom: 10%;
        right: 10%;
    }
    &lt;/style&gt;
&lt;/head&gt;

&lt;body&gt;
    &lt;div class="item" id="box"&gt;
        &lt;div class="txt"&gt;2017许愿墙&lt;/div&gt;
        &lt;div class="txt"&gt;This is the best future&lt;/div&gt;
        &lt;div class="close"&gt;&lt;a href="#" id="close"&gt;关闭&lt;/a&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;script type="text/javascript"&gt;
    //理解执行函数
    (function() {
        //初始化变量，获取元素，设置动作
        var state = 0,
            X = 0,
            Y = 0;
        var box = document.getElementById("box");
        var txt = document.getElementsByClassName("txt");
        var close = document.getElementById("close");
        box.onmouseup = up;
        box.onmousedown = down;
        box.onmousemove = move;
        close.onmousedown = closeBox;
        //点击关闭链接box添加隐藏属性
        function closeBox(e) {
            e.preventDefault();
            document.getElementById("box").style.display = "none";
        }
        //鼠标按下设置开关state为1，在加上box距离左上的距离
        function down(e) {
            e.preventDefault();
            state = 1;
            X += e.offsetX;
            Y += e.offsetY;
        }
        //因为点击文字也同时点击了外面的box，所以需要在点到文字的div时进行处理，把XY赋值为文字div距离外部div的左上距离
        //这里需要理解一下浏览器点击子div的时候相当于也点击了父div，而且事件是从内而外触发的
        for (var i in txt) {
            txt[i].onmousedown = function(e) {
                X = this.offsetLeft;
                Y = this.offsetTop;
            }
        }
        //松开鼠标，恢复初始值
        function up() {
            X = 0;
            Y = 0;
            state = 0;
        }
        //移动时，判断鼠标是否为按下。实现拖动效果
        function move(e) {
            if (state) {
                document.getElementById("box").style.top = e.clientY - Y + "px";
                document.getElementById("box").style.left = e.clientX - X + "px";
            }
        }
    }());
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
效果预览：<a href="/img/uploads/2017/03/QQ截图20170326144840.jpg"><img class="alignnone wp-image-212 size-full" src="/img/uploads/2017/03/QQ截图20170326144840.jpg" alt="" width="285" height="265" /></a>

&nbsp;

&nbsp;

&nbsp;

&nbsp;
