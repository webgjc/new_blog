
---
title: swoole初试，作为一个你画我猜的websocket server
catalog: true
date: 2017-12-7 16:57:13
---

swoole也是一个php比较强大的扩展，可以实现高性能的异步并发 TCP、UDP、Unix Socket、HTTP，WebSocket。这里实现一个WebSocket的server端的你画我猜。自我觉得还是踩坑之旅，生产环节用还是值得斟酌。<!--more-->

安装环节这里不多叙述，linux上按<a href="https://wiki.swoole.com/wiki/page/6.html">这里</a>的进行就可以，插一句修改php.ini那个只要加在第一行就行。

然后touch一个php文件，这里命名为drawguess.php。具体内容解释在代码注释中。还有结尾彩蛋。
<pre>&lt;?php
//创建全局变量表，这里用于存储用户id，1024为最大容量。
$table = new swoole_table(1024);
$table-&gt;column('fd', swoole_table::TYPE_INT);
$table-&gt;create();
//定义server
$server = new swoole_websocket_server("0.0.0.0", 9501);
$server-&gt;table = $table;
//这里定义答案
$anstr="苹果,李子,梨子,榴莲,香蕉,橙子,番茄,柿子,葡萄,水蜜桃,核桃,哈密瓜,西瓜,菠萝,蓝莓,草莓,释迦,杨桃,椰子,板栗,樱桃,荔枝,龙眼,青梅,山楂,柠檬,金桔,芒果,坚果,胡桃,枇杷";
$ansarr=split(",", $anstr);
$ran=rand(0,count($ansarr));
$ans=$ansarr[$ran];
//全局计数，不同进程之间共享
$startGame=new swoole_atomic(0);
$players=new swoole_atomic(999);
$k=new swoole_atomic(0);
//定义open事件，把用户id加入表中
//push为推送数据到客户端,这里广播需要用foreach实现。
$server-&gt;on('open', function($server, $req) {
    global $ans,$players,$startGame;
    $server-&gt;table-&gt;set($req-&gt;fd, array('fd' =&gt; $req-&gt;fd));
    if(count($server-&gt;table)==1){
        $data=json_encode(array("start"=&gt;"-2","data"));
        $server-&gt;push($req-&gt;fd,$data);
    }
    if(count($server-&gt;table)==$players-&gt;get()){
        if($startGame-&gt;get()==0){
            $startGame-&gt;set(1);
            foreach ($server-&gt;table as $u) {
                if($u['fd']==$req-&gt;fd){
                    $data=json_encode(array("start"=&gt;"-1","draw"=&gt;"1","ans"=&gt;$ans));
                    $server-&gt;push($u['fd'],$data);
                }else{
                    $data=json_encode(array("start"=&gt;"-1","draw"=&gt;"0"));
                    $server-&gt;push($u['fd'],$data);
                }
            }
        }
    }
});
//定义接受到数据触发事件。
//这里主逻辑为接受getdata数据，解析，start为状态，
/*
-4---时间到0事件
-3---第一个玩家选择人数
-2---第一个玩家进入事件
-1---玩家到齐，开始游戏事件
0----touchstart事件
1----touchmove事件
2----设置线条宽度
3----设置橡皮宽度
4----清空事件
5----设置颜色事件
6----答案提交事件，判断成功与否
*/
$server-&gt;on('message', function($server, $frame) {
    //$server-&gt;push($frame-&gt;fd, $frame-&gt;data);
    global $ans,$ansarr,$players,$k;
    $getdata=json_decode($frame-&gt;data);
    if($getdata-&gt;start==-4){
        $ran=rand(0,count($ansarr));
        $ans=$ansarr[$ran];
        $i=0;
        foreach($server-&gt;table as $u) {
            if($i&lt;$k-&gt;get()){
                $i++;
            }else{
                $player=$u["fd"];
                $k-&gt;set(($k-&gt;get()+1)%$players-&gt;get());
                break;
            }
        }
        foreach ($server-&gt;table as $u) {
                if($u['fd']==$player){
                    $data=json_encode(array("start"=&gt;"-1","draw"=&gt;"1","ans"=&gt;$ans));
                    $server-&gt;push($u['fd'],$data);
                }else{
                    $data=json_encode(array("start"=&gt;"-1","draw"=&gt;"0"));
                    $server-&gt;push($u['fd'],$data);
                }
            }
    }
    if($getdata-&gt;start==-3){
        $players-&gt;set(intval($getdata-&gt;players));
    }else{
        if($getdata-&gt;start==6){
            echo $getdata-&gt;answer;
        }
        if($getdata-&gt;start==6 &amp;&amp; $getdata-&gt;answer==$ans){
            foreach ($server-&gt;table as $u) {
                $res=array("start"=&gt;"6","win"=&gt;$frame-&gt;fd);
                $server-&gt;push($u['fd'], json_encode($res));//消息广播给所有客户端    
            }  
            $ran=rand(0,count($ansarr));
            $ans=$ansarr[$ran];
            $i=0;
            foreach($server-&gt;table as $u) {
                if($i&lt;$k-&gt;get()){
                    $i++;
                }else{
                    $player=$u["fd"];
                    $k-&gt;set(($k-&gt;get()+1)%$players-&gt;get());
                    break;
                }
            }
            foreach ($server-&gt;table as $u) {
                if($u['fd']==$player){
                    $data=json_encode(array("start"=&gt;"-1","draw"=&gt;"1","ans"=&gt;$ans));
                    $server-&gt;push($u['fd'],$data);
                }else{
                    $data=json_encode(array("start"=&gt;"-1","draw"=&gt;"0"));
                    $server-&gt;push($u['fd'],$data);
                }
            }
        }else{
            foreach ($server-&gt;table as $u) {
                $server-&gt;push($u['fd'], $frame-&gt;data);//消息广播给所有客户端
            }     
        }
    }
});
//定义关闭websocket事件
$server-&gt;on('close', function($server, $fd) {
    echo "client-{$fd} is closed\n"; 
    global $startGame;
    $server-&gt;table-&gt;del($fd);
    if(count($server-&gt;table)==1){
        $startGame-&gt;set(0);
    }
});
//开启server
$server-&gt;start();</pre>
再附上前端代码。
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no,minimum-scale=1.0" name="viewport" &gt;
    &lt;title&gt;draw and guess&lt;/title&gt;
    &lt;style type="text/css"&gt;
        html,body{
            padding: 0px;
            margin: 0px;
            -webkit-tap-highlight-color:rgba(0,0,0,0);
        }
        canvas{
            border: solid 1px black;
        }
        input{
            border: none;
            border-bottom: solid 1px black;
            line-height: 20px;
            font-size: 20px;
            height: 25px;
            outline:none;
            border-radius: 0px;
            width: 70%;
        }
        button{
            height: 30px;
            width: 20%;
            background-color: rgba(255,255,255,0.5);
            border: solid 1px black;
            border-radius: 10px;
            outline: none;
        }
        .sel li{
            list-style: none;
            display: inline-block;
            width: 23%;
        }
        .color{
            position: absolute;
            width: 100%;
            margin-top: -140px;
        }
        .red{
            width: 100%;
            position: relative;
            top: 0px;
        }
        .green{
            width: 100%;
            position: relative;
            top:30px;
        }
        .blue{
            width: 100%;
            position: relative;
            top: 60px;
        }
        .ky{
            width: 20px;
            height: 20px;
            border-radius: 20px;
            background-color: black;
            position: absolute;
        }
        .jd{
            position: absolute;
            margin-top: 4px;
            border: solid 1px black;
            width: 80%;
            height: 10px;
            border-radius: 10px;
        }
        .colorz{
            position: absolute;
            right: 10%;
        }
        .showcol{
            width: 50px;
            height: 20px;
            margin: 5px;
            border:solid 1px black;
            background-color: #000;
        }
        .bs li{
            list-style: none;
            width: 50px;
            height: 20px;
        }
        .bsdiv{
            position: absolute;
            margin-top: -140px;
            margin-left: 25%;
        }
        .ans{
            position: absolute;
            top: 0px;
            right: 5px;
        }
        .error{
            position: absolute;
            top: 0;
            left: 5px;
        }
        .showinfo{
            position: absolute;
            top: 0px;
            width: 100%;
            text-align: center;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="ans" id="answer"&gt;&lt;/div&gt;
    &lt;div class="error" id="error"&gt;&lt;/div&gt;
    &lt;div class="showinfo" id="showinfo"&gt;123&lt;/div&gt;
    &lt;canvas id="can" width="600" height="600"&gt;not support&lt;/canvas&gt;
    &lt;div class="color" id="col" style="display:none;"&gt;
        &lt;div class="showcol" id="showcolor"&gt;&lt;/div&gt;
        &lt;div class="red"&gt;
            &lt;div class="jd"&gt;&lt;/div&gt;
            &lt;div class="ky" id="redmove"&gt;&lt;/div&gt;
            &lt;div class="colorz"&gt;r&lt;/div&gt;
        &lt;/div&gt;
        &lt;div class="green"&gt;
            &lt;div class="jd"&gt;&lt;/div&gt;
            &lt;div class="ky" id="greenmove"&gt;&lt;/div&gt;
            &lt;div class="colorz"&gt;g&lt;/div&gt;
        &lt;/div&gt;
        &lt;div class="blue"&gt;
            &lt;div class="jd"&gt;&lt;/div&gt;
            &lt;div class="ky" id="bluemove"&gt;&lt;/div&gt;
            &lt;div class="colorz"&gt;b&lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="sel"&gt;
        &lt;ul&gt;
            &lt;li id="colorblock"&gt;颜色&lt;/li&gt;
            &lt;li id="bsblock" style="margin-left:-10px;"&gt;
                &lt;select name="" id="selbs"&gt;
                    &lt;option value="" disabled selected="selected"&gt;画笔&lt;/option&gt;
                    &lt;option value="1"&gt;1&lt;/option&gt;
                    &lt;option value="2"&gt;2&lt;/option&gt;
                    &lt;option value="3"&gt;3&lt;/option&gt;
                    &lt;option value="4"&gt;4&lt;/option&gt;
                    &lt;option value="5"&gt;5&lt;/option&gt;
                    &lt;option value="6"&gt;6&lt;/option&gt;
                    &lt;option value="7"&gt;7&lt;/option&gt;
                    &lt;option value="8"&gt;8&lt;/option&gt;
                &lt;/select&gt;
            &lt;/li&gt;
            &lt;li style="margin-right:10px;"&gt;
                &lt;select name="" id="xpsel"&gt;
                    &lt;option value="" disabled selected="selected"&gt;橡皮&lt;/option&gt;
                    &lt;option value="0"&gt;取消&lt;/option&gt;
                    &lt;option value="1"&gt;1&lt;/option&gt;
                    &lt;option value="2"&gt;2&lt;/option&gt;
                    &lt;option value="3"&gt;3&lt;/option&gt;
                    &lt;option value="4"&gt;4&lt;/option&gt;
                    &lt;option value="5"&gt;5&lt;/option&gt;
                    &lt;option value="6"&gt;6&lt;/option&gt;
                    &lt;option value="7"&gt;7&lt;/option&gt;
                    &lt;option value="8"&gt;8&lt;/option&gt;
                &lt;/select&gt;
            &lt;/li&gt;
            &lt;li id="clear"&gt;清空&lt;/li&gt;
        &lt;/ul&gt;
    &lt;/div&gt;
    &lt;input type="text" id="ans"&gt;
    &lt;button class="btn" id="sub"&gt;提交&lt;/button&gt;
    &lt;script type="text/javascript"&gt;
        showinfo("您已进入游戏，请等待");
        var wsServer = 'ws://123.206.217.190:9501';
        var ws = new WebSocket(wsServer);
        var can=document.getElementById("can");
        var color=document.getElementById("col");
        var rm=document.getElementById("redmove");
        var gm=document.getElementById("greenmove");
        var bm=document.getElementById("bluemove");
        var showcol=document.getElementById("showcolor");
        var bsdiv=document.getElementById("bsdiv");
        var sub=document.getElementById("sub");
        var colorclicked=0;
        var colorshow=[0,0,0];
        var lineWidth=1;
        var xpWidth=0;
        var myturn=0;
        var players=0;
        var deadtime=60;
        var timejishu;

        var cvs=can.getContext("2d");
        var whmin = window.innerWidth&gt;window.innerHeight?window.innerHeight:window.innerWidth;
        var w=can.width=whmin-2;
        var h=can.height=whmin-2;

        color.addEventListener('touchstart',stcolor,{passive:false});
        color.addEventListener('touchmove',chcolor,{passtive:false});
        rm.addEventListener('touchstart',colormove,{passive:false});
        gm.addEventListener('touchstart',colormove,{passive:false});
        bm.addEventListener('touchstart',colormove,{passive:false});

        ws.onopen=function(e){
            can.addEventListener('touchstart',sendstart,{passive:false});
            can.addEventListener('touchmove',sendmove,{passive:false});
            function sendstart(e){
                e.preventDefault();
                let data={"start":"0","coor":[e.touches[0].clientX,e.touches[0].clientY]};
                if(myturn==1){
                    ws.send(JSON.stringify(data));
                }
            }
            function sendmove(e){
                e.preventDefault();
                let data={"start":"1","coor":[e.touches[0].clientX,e.touches[0].clientY]};
                if(myturn==1){
                    ws.send(JSON.stringify(data));
                }
            }
        }

        ws.onmessage=function(e){
            var con=JSON.parse(e.data);
            switch(con.start){
                case "-2":
                    console.log(con)
                    players=prompt("请选择玩家人数");
                    let data={"start":"-3","players":players};
                    ws.send(JSON.stringify(data));
                    break
                case "-1":
                    if(con.draw=="1"){
                        console.log(timejishu)
                        showinfo("该你画咯");
                        document.getElementById("answer").innerHTML=con.ans;
                        timejishu=setInterval(function(){
                            deadtime--;
                            if(deadtime&lt;55){
                                document.getElementById("showinfo").innerHTML=deadtime;
                            }
                            if(deadtime==0){
                                let data={"start":"-4"};
                                ws.send(JSON.stringify(data));
                                deadtime=60;
                                clearInterval(timejishu);
                            }
                        },1000);
                        myturn=1;
                    }else{
                        showinfo("游戏开始");
                        document.getElementById("answer").innerHTML="";
                        if(timejishu!=undefined){
                            clearInterval(timejishu);
                        }
                        myturn=0;
                    }
                    break
                case "0":
                    tstart(con.coor[0],con.coor[1]);
                    break
                case "1":
                    move(con.coor[0],con.coor[1]);
                    break
                case "2":
                    lineWidth=con.lineWidth;
                    break;
                case "3":
                    xpWidth=con.xpWidth;
                    break;
                case "4":
                    cvs.clearRect(0,0,w,h); 
                    break;
                case "5":
                    colorshow=con.color;
                    break;
                case "6":
                    if(con.win!=undefined){
                        alert(con.win+" win!");
                        deadtime=60;
                    }else{
                        document.getElementById("error").innerHTML="error:\n"+con.answer;
                    }
            }
        }
        
        document.getElementById("colorblock").onclick=function(){
            if(color.style.display=="none"){
                color.style.display="block";
                this.innerHTML="确认";
            }else{
                color.style.display="none";
                let data={"start":"5","color":colorshow};
                if(myturn==1){
                    ws.send(JSON.stringify(data));
                }
                this.innerHTML="颜色";
            }
        }
        document.getElementById("selbs").onchange=function(){
            let data={"start":"2","lineWidth":this.value};
            if(myturn==1){
                ws.send(JSON.stringify(data));
            }
        }
        document.getElementById("xpsel").onchange=function(){
            let data={"start":"3","xpWidth":this.value};
            if(myturn==1){
                ws.send(JSON.stringify(data));
            }
        }
        document.getElementById("clear").onclick=function(){
            if(myturn==1){
                ws.send(JSON.stringify({"start":"4"}));  
            }
        }
        sub.onclick=function(){
            var ans=document.getElementById("ans").value;
            let data={"start":"6","answer":ans};
            ws.send(JSON.stringify(data));
        }

        function showinfo(info){
            document.getElementById("showinfo").innerHTML=info;
        }

        function tstart(x,y){
            //e.preventDefault();
            cvs.beginPath();
            cvs.moveTo(x,y);
        }
        function move(x,y){
            //e.preventDefault();
            if(xpWidth!=0){
                cvs.clearRect(x-xpWidth*2,y-xpWidth*2,xpWidth*4,xpWidth*4);
            }else{
                cvs.lineTo(x,y);
                cvs.lineWidth=lineWidth*2;
                cvs.lineCap='round';
                cvs.lineJoin="round";
                cvs.strokeStyle="rgb("+colorshow[0]+","+colorshow[1]+","+colorshow[2]+")";
                cvs.stroke();
            }
        }
        function stcolor(e){
            e.preventDefault();
        }
        function chcolor(e){
            e.preventDefault();
            if(e.targetTouches[0].clientX&lt;window.innerWidth*0.8){
                this.children[colorclicked].children[1].style.left=e.targetTouches[0].clientX+"px";
                colorshow[colorclicked-1]=parseInt(e.targetTouches[0].clientX/(window.innerWidth*0.8)*255)
            }
            showcol.style.backgroundColor="rgb("+colorshow[0]+","+colorshow[1]+","+colorshow[2]+")";
        }
        function colormove(e){
            e.preventDefault();
            if(this.id=="redmove"){
                colorclicked=1;
            }else if(this.id=="greenmove"){
                colorclicked=2;
            }else{
                colorclicked=3;
            }
        }
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
运行的话，服务器端
<pre>php drawguess.php</pre>
客户端，swoole的http服务器的话这里不做叙述，可使用python2.x作为http服务器
<pre>python -m SimpleHTTPServer 80</pre>
或者python3.x
<pre><span class="n">python</span> <span class="o">-</span><span class="n">m</span> <span class="n">http</span><span class="o">.</span><span class="n">server</span> <span class="mi">80</span></pre>
特别说明，这里还会有个bug，回答问题时有正确答案判断为错误，感觉是编码问题，然后这个服务器端运行的时候也是如果有输出中文的话也会输出乱码。有看到改php.ini什么为utf-8，好像也没效果。

另一个若是开发阶段，经常改服务器端，但每次去找pid并kill比较麻烦，因此可以写个shell命令来自动做一步。
<pre>#!/bin/sh
kill `lsof -t -i:此处写server的端口`
sleep 2
php 此处写绝对路径/drawguess.php
sleep 1
netstat -ntlp</pre>
swoole值得探究的可能还很多，然而确实踩坑。。。。
