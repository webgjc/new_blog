
---
title: 用node.js的socket.io实现双人五子棋对战
catalog: true
date: 2017-11-22 18:31:25
---

websocket也没啥好讲的，就一可以实现长连接的协议，其中也有三次握手之说。具体的也不去探究了，这里用node.js做后端来实现与前端js的websocket连接。并完成一个简易的联机游戏。<!--more-->

首先参考这个<a href="https://socket.io/">socket.io的网址</a>，参考get start可得到一些安装的基本步骤，这里默认已经安装好node.js以及npm，具体操作包括如下
<pre>npm init</pre>
<pre><code>npm install --save express@4.15.2</code></pre>
<pre><code>npm install --save socket.io</code></pre>
之后要进行的是服务器的编写，保存为index.js
<pre>//引入必要库
var app=require('express')();
var http=require('http').Server(app);
var io=require('socket.io')(http);
//n用于保存连接数目，now用于保存当前落子玩家
var n=0;
var now=0;
//加载html文件
app.get('/',function(req,res){
    res.sendFile(__dirname + '/index.html');
})
//websocket连接操作
io.on('connection',function(socket) {
    n++;
    //断开连接操作
    socket.on('disconnect',function(){
        n--;
        console.log('out');
    });
    //收到消息，触发指定事件，并传送得到的消息
    socket.on('msg',function(info){
        console.log(now)
        if(info[2]!=now &amp;&amp; n&gt;=2){
            io.emit('message',{for:info})
            now=info[2];
        }
    })
});
//打开http服务器
http.listen(3000,function(){
    console.log('start')
})</pre>
接下来要编辑的是html文件，同目录下保存为index.html
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;五子棋&lt;/title&gt;
    &lt;style type="text/css"&gt;
        canvas{
            border:solid 1px black;
            background-color: #5b7d7d;
            -webkit-tap-highlight-color:rgba(0,0,0,0)
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;canvas id="can" width="600" height="800"&gt;not support&lt;/canvas&gt;
    &lt;script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript"&gt;
        //获取canvas，设置宽高
        //获取屏宽和高并设置小的一方为棋盘长度
        var can = document.getElementById('can');
        var x = window.innerWidth&gt;window.innerHeight?window.innerHeight:window.innerWidth;
        var w = can.width = x-20;
        var h = can.height = x-20;
        var con = can.getContext('2d');
        var nowIn=1;
        var alreadyIn=[];
        var blackIn=[];
        var whiteIn=[];
        var local=Math.random();
        //画线，做棋盘。
        function drawline(con,color,stepx,stepy){
            con.strokeStyle=color;
            con.lineWidth=1;
            for(var i=stepx+0.5;i&lt;can.width;i+=stepx){
                con.beginPath();
                con.moveTo(i,0);
                con.lineTo(i,h);
                con.stroke();
            }
            for(var i=stepy+0.5;i&lt;can.height;i+=stepy){
                con.beginPath();
                con.moveTo(0,i);
                con.lineTo(w,i);
                con.stroke();
            }
        }
        //画棋子
        function drawqi(x,y,color){
            con.beginPath();
            con.fillStyle=color;
            con.arc(x*w/15,y*w/15,w/38,0,2*Math.PI);
            con.stroke();
            con.fill();
            con.closePath();
        }
        //判断胜利，这里采用逐子判断。
        function judgeWin(chess){
            for(var i=0;i&lt;chess.length;i++){
                sp=chess[i].split(",")
                if(sp[0]&gt;=2 &amp;&amp; sp[1]&gt;=2){
                    if($.inArray((parseInt(sp[0])-1)+","+(parseInt(sp[1])-1),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])-2)+","+(parseInt(sp[1])-2),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])+1)+","+(parseInt(sp[1])+1),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])+2)+","+(parseInt(sp[1])+2),chess)!=-1){
                        return true;
                    }
                    if($.inArray((parseInt(sp[0])-1)+","+(parseInt(sp[1])),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])-2)+","+(parseInt(sp[1])),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])+1)+","+(parseInt(sp[1])),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])+2)+","+(parseInt(sp[1])),chess)!=-1){
                        return true;
                    }
                    if($.inArray((parseInt(sp[0]))+","+(parseInt(sp[1])-1),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0]))+","+(parseInt(sp[1])-2),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0]))+","+(parseInt(sp[1])+1),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0]))+","+(parseInt(sp[1])+2),chess)!=-1){
                        return true;
                    }
                    if($.inArray((parseInt(sp[0])-1)+","+(parseInt(sp[1])+1),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])-2)+","+(parseInt(sp[1])+2),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])+1)+","+(parseInt(sp[1])-1),chess)!=-1&amp;&amp;
                    $.inArray((parseInt(sp[0])+2)+","+(parseInt(sp[1])-2),chess)!=-1){
                        return true;
                    }
                }
            }
            return false
        }
        //触发画线，连接websocket
        drawline(con,'lightgray',w/15,h/15);
        var socket=io();
        //canvas点击事件，获取最近的一个落子点坐标，发送事件。
        can.onclick=function(e){
            mx=Math.round(e.offsetX/w*15);
            my=Math.round(e.offsetY/w*15);
            if($.inArray((mx*15+my),alreadyIn)==-1){
                socket.emit('msg',[mx,my,local])
            }
        }
        //服务器返回触发事件，接收消息并展示给已连接用户
        socket.on('message',function(msg){
            mx=msg.for[0]
            my=msg.for[1]
            
            alreadyIn.push(mx*15+my);
            if(nowIn==0){
                draw=drawqi(mx,my,"#000");
                blackIn.push([mx,my].toString())
                if(judgeWin(blackIn)){
                    alert("black win");
                }
            }else{
                draw=drawqi(mx,my,"#fff");
                whiteIn.push([mx,my].toString());
                if(judgeWin(whiteIn)){
                    setTimeout(alert("white win"),500);
                }
            }
            nowIn=1-nowIn;
        })
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
效果图：<img class="alignnone size-medium wp-image-437" src="/img/uploads/2017/11/MQKABG9HRBVI2B0OE-298x300.png" alt="" width="298" height="300" />

一般看看socket.io的文档便可以get到一点websocket的灵感，之后就可以自行拓展。

当然这还是websocket最基础的一部分，之后有待进一步探索。
