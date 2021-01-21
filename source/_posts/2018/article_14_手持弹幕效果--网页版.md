
---
title: 手持弹幕效果--网页版
catalog: true
date: 2018-4-6 10:39:27
---

看到抖音上手持弹幕的效果，想想应该不复杂，也可以自己在浏览器实现一个。主要问题在于怎么把浏览器上面的搜索框去掉而实现一种伪全屏。结尾有彩蛋。<!--more-->

效果暂时可以在<a href="https://ganjiacheng.cn/danmu.html">https://ganjiacheng.cn/danmu.html</a> 查看。

直接上代码，在其中论述方法。
<pre> &lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="utf-8"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"&gt;
    &lt;title&gt;手持弹幕&lt;/title&gt;
    &lt;style type="text/css"&gt;
        *{
            margin: 0px;
            padding: 0px;
        }
        html,body{
            height: 100%;
            width: 100%;
            overflow: hidden;
            background: #000;
        }
        #txt{
            overflow: visible;
            white-space: nowrap;
            transform-origin: 0% 0%;
            transform: rotate(90deg);
        }
        #config{
            position: absolute;
            bottom: 0px;
            width: 100%;
        }
        #config input{
            display: block;
            width: 100%;
            padding: .375rem .75rem;
            font-size: 1rem;
            line-height: 1.5;
            color: #495057;
            background-color: #fff;
            background-clip: padding-box;
            border: 1px solid #ced4da;
            border-radius: .25rem;
            transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out;
        }
        #config button{
            width: 23.5%;
            display: inline-block;
            font-weight: 400;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            border: 1px solid transparent;
            padding: .375rem .75rem;
            font-size: 1rem;
            line-height: 1.5;
            border-radius: .25rem;
            transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
            color: #fff;
            background-color: transparent;
            background-image: none;
            border-color: #343a40;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div id="txt"&gt;点一下屏幕进入设置&lt;/div&gt;
    &lt;div id="config" style="display:none;"&gt;
        &lt;input type="text" placeholder="输入文本,tip:上拉一下就可全屏" id="txtContent"&gt;
        &lt;input type="text" placeholder="输入颜色rgb，格式如:125 125 125" id="color"&gt;
        &lt;button id="turnLeft"&gt;左移&lt;/button&gt;
        &lt;button id="turnRight"&gt;右移&lt;/button&gt;
        &lt;button id="bigger"&gt;增大&lt;/button&gt;
        &lt;button id="smaller"&gt;减小&lt;/button&gt;
        &lt;button id="quicker"&gt;加快&lt;/button&gt;
        &lt;button id="slower"&gt;减慢&lt;/button&gt;
        &lt;button id="changeFont"&gt;字体&lt;/button&gt;
        &lt;button id="stunt"&gt;特技&lt;/button&gt;
    &lt;/div&gt;
    &lt;script type="text/javascript"&gt;
        //获取到所需dom
        var txt = document.getElementById("txt");
        var config = document.getElementById("config");
        var txtContent = document.getElementById("txtContent");
        var color = document.getElementById("color");
        var turnLeft = document.getElementById("turnLeft");
        var turnRight = document.getElementById("turnRight");
        var bigger = document.getElementById("bigger");
        var smaller = document.getElementById("smaller");
        var quicker = document.getElementById("quicker");
        var slower = document.getElementById("slower");
        var changeFont = document.getElementById("changeFont");
        var stunt = document.getElementById("stunt");
        var height = document.body.clientHeight;
        var width = document.body.clientWidth;
        var state = 0;
        var v = 10;
        var k = 0;
        //初始化设置，下面改起来方便些
        txt.style.marginTop = height+"px";
        txt.style.fontSize = "380px";
        txt.style.marginLeft = "450px";
        txt.style.color = "rgba(255,255,255,1)"

        config.onclick = function(){
            state = 1;
        }
        //显隐设置栏，消除搜索框也是无意间发现。
        //由于加了设置栏大于一屏然后可以上拉，上拉后搜索框会折叠。
        //然后在点击消除设置栏，一些浏览器就会自动占满屏，有些浏览器好像下面会有一栏空。
        document.body.onclick = function(e){
            if(state != 1){
                config.style.display = config.style.display == "none" ? "block" : "none";
            }
            state = 0;
        }
        //绑定设置输入框和按钮操作
        txtContent.onchange = function(){
            txt.innerHTML = this.value
            txt.style.marginTop = height + "px";
        }

        color.onchange = function(){
            colors = this.value.split(" ");
            txt.style.color = "rgba("+colors[0]+","+colors[1]+","+colors[2]+",1)";
            txt.style.marginTop = height + "px";
        }

        turnLeft.onclick = function(){
            txt.style.marginLeft = parseInt(txt.style.marginLeft) - 10 + "px";
        }

        turnRight.onclick = function(){
            txt.style.marginLeft = parseInt(txt.style.marginLeft) + 10 + "px";
        }

        bigger.onclick = function(){
            txt.style.fontSize = parseInt(txt.style.fontSize) + 10 + "px";
        }

        smaller.onclick = function(){
            console.log(txt.style.fontSize)
            txt.style.fontSize = parseInt(txt.style.fontSize) - 10 + "px";
            console.log(txt.style.fontSize)
        }

        quicker.onclick = function(){
            v += 2
        }

        slower.onclick = function(){
            v -= 2
        }

        changeFont.onclick = function(){
            fonts = ["SimSun","SimHei","Microsoft YaHei","Microsoft JhengHei","NSimSun","PMingLiU","MingLiU","DFKai-SB","FangSong","KaiTi","FangSong_GB2312","KaiTi_GB2312","：STHeiti","STKaiti","STSong","STFangsong","LiSu","YouYuan","STXihei","STKaiti","STKaiti","STSong","STZhongsong","STZhongsong","STFangsong","FZYaoti","STZhongsong","STCaiyun","STHupo","STLiti","STXingkai","STXinwei"]
            txt.style.fontFamily = fonts[k];
            k+=1;
        }

        stunt.onclick = function(){
            alert("要什么特技呢");
            return
        }
        //设置字体移动
        function move(){
            txt.style.marginTop = parseInt(txt.style.marginTop) - v + "px";
            if(parseInt(txt.style.marginTop) &lt;= -parseInt(txt.style.fontSize)*txt.innerHTML.length) txt.style.marginTop = height + "px";
            window.requestAnimationFrame(move);
        }
        window.requestAnimationFrame(move);
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
效果展示：<a href="/img/uploads/2018/04/微信图片_20180406103608.png"><img class="alignnone wp-image-595 size-medium" src="/img/uploads/2018/04/微信图片_20180406103608-150x300.png" alt="" width="150" height="300" /></a>

再来聊聊我对于自身前端的发展意向；

自身没有太多精力去看一些工程上的问题（比如浏览器适配，框架，css预处理等），所以大部分我会专注于效果的实现（由于网页展示起来比较方便）。

使用的多数也会在原生js行列，偶尔用个jquery，必要时看一些包的使用（如之前markdown解析器）。

随性写些启发性前端代码，可能是逻辑上的sao操作，可能是效果上的模仿或涂鸦，，可能是我未知新技术上的demo，and so on；我自己的手机跑的动就好啦。

就这样了吗，恩，然后就没有然后了。
