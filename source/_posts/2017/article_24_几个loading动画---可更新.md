
---
title: 几个loading动画---可更新
catalog: true
date: 2017-5-30 10:24:53
---

因为网络等因素，有时候浏览器加载页面时间会很长，一直让用户看着白屏幕也不好。

所以需要有loading动画来挽留用户。<!--more-->

这个动画可以用css实现，也可以用js实现。

这里先举两个简单的css的例子：

<a href="https://ganjiacheng.cn/blogdemo/loading.html">点击这里看演示</a>

<a href="https://ganjiacheng.cn/blogdemo/loading1.html">另一个演示</a>
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;loading&lt;/title&gt;
    &lt;style type="text/css"&gt;
        .loading{
            position:relative;
        }
        .loading span{
            position: absolute;
            bottom:-40px;
            width: 10px;
            height: 5px;
            background-color: #000;
            -webkit-animation:loading 1s;
            -webkit-animation-iteration-count:infinite;
            animation-timing-function: linear;
        }
        .loading span:nth-child(2){
            left: 30px;
            animation-delay: .2s;
        }
        .loading span:nth-child(3){
            left: 60px;
            animation-delay: .4s;
        }
        .loading span:nth-child(4){
            left: 90px;
            animation-delay: .6s;
        }
        .loading span:nth-child(5){
            left: 120px;
            animation-delay: .8s;
        }
        @-webkit-keyframes loading
        {
            0%   {height: 5px;transform:translateY(0px);}
            50%  {height: 30px;transform:translateY(15px);}
            100% {height: 5px;transform:translateY(0px);}
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="loading"&gt;
        &lt;span&gt;&lt;/span&gt;
        &lt;span&gt;&lt;/span&gt;
        &lt;span&gt;&lt;/span&gt;
        &lt;span&gt;&lt;/span&gt;
        &lt;span&gt;&lt;/span&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Document&lt;/title&gt;
    &lt;style type="text/css"&gt;
        .loading,.loadingjs{
            font-size: 50px;
        }
        .loading span{
            position: absolute;
        }
        .loading span{
            left:-10%;
            width:100px;
            animation:mymove 5s infinite;
            animation-timing-function: cubic-bezier(0.38, 0.99, 0.45, 0.13);
        }
        .loading span:nth-child(2){
            animation-delay:0.3s;
        }
        .loading span:nth-child(3){
            animation-delay:0.6s;
        }
        .loading span:nth-child(4){
            animation-delay:0.9s;
        }
        .loading span:nth-child(5){
            animation-delay:1.2s;
        }
        @keyframes mymove{
            from {left:-10%;}
            to {left: 90%;}
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="loading" id="loading"&gt;
        &lt;span&gt;.&lt;/span&gt;
        &lt;span&gt;.&lt;/span&gt;
        &lt;span&gt;.&lt;/span&gt;
        &lt;span&gt;.&lt;/span&gt;
        &lt;span&gt;.&lt;/span&gt;
    &lt;/div&gt;
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
