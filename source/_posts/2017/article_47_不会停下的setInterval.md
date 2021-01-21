
---
title: 不会停下的setInterval
catalog: true
date: 2017-12-7 22:38:35
---

关于定时器，如果把浏览器最小化或者看其他页面的时候，页面都会处于未激活状态，也就是对于chrome定时器会变1s运行一次，手机定时器则会直接暂停。<!--more-->

比如运行如下代码，页面切到后台的话，定时器chrome会变一秒变一次，手机则会暂停。
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;test js&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;script type="text/javascript"&gt;
        var time=0;
        setInterval(function(){
            time++;
            document.write(time+" ");
            document.title=time+" ";
        },100);
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
然后先尝试一个web worker实现的不停下的setInterval，类似于让定时器部分js在后台运行，这样就可以一直运行定时器，前台收到msg展示即可。下面是html部分
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Document&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;script type="text/javascript"&gt;
        var worker = new Worker("worker.js");

        // 向worker.js发送信息
        worker.postMessage( 'hello world' );

        // 接收从worker.js发送的信息，存储在event.data中
        worker.onmessage = function(event){
            document.write(event.data+" ");
            document.title=event.data+" ";
        }

        // 报错信息
        worker.onerror=function(error){
            console.log(error.filename,error.lineno,error.message);
        }
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
下面是web worker的js部分。
<pre>onmessage = function(event){
    var data = event.data;
    var time=0;
    setInterval(function(){
        // 向前端页面发送信息
        postMessage(time);
        time++;
    }, 100)
}</pre>
再来一种比较奇妙的实现，主要参考<a href="https://imququ.com/post/ios-none-freeze-timer.html">这里</a>。

通过mate的refresh和setInterval的配合实现。不过这个好像最小只能实现一秒。
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta http-equiv="refresh" content="2" id="refresh"&gt;
    &lt;title&gt;123&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;script type="text/javascript"&gt;
        var meta = document.getElementById("refresh");
        var time = 0;
        setInterval(function() {
            meta.content = meta.content;
            document.title=time+" ";
            document.write(time+" ");
            time++;
        }, parseInt(meta.content / 2) * 1000);
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
最后再扯扯这个问题的初衷，一次面试被问到页面定时器显示时间由于会停止，后台运行（最小化）后回来时间不对了怎么办。

这个容易调入上面的陷阱，想着怎么让定时器持续运行，其实只要setInterval获取系统时间便可以。即使停了回来也会运行一次获取到系统时间。代码如下
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;time&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div id="time"&gt;&lt;/div&gt;
    &lt;script type="text/javascript"&gt;
        setInterval(function(){
            document.getElementById("time").innerHTML=new Date().toString();
        },1000);
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
That's all；
