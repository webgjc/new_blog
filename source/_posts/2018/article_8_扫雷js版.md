
---
title: 扫雷js版
catalog: true
date: 2018-2-27 11:05:12
---

是老早之前写的，今天整理系统文件发现了这个扫雷，也是小惊喜，小看了下还挺有趣哈！<!--more-->

直接上代码，具体在代码中注释。

主要看点有两块，一个是从n个整数随机产生不重复的m个随机整数,m&lt;n

另一个就是自动搜寻周边不是雷的区域，也就是点了一个不是雷有时会显现一大片。
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta content="text/html; charset=utf-8" http-equiv="Content-Type"&gt;
    &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=2.0, user-scalable=no" /&gt;
    &lt;title&gt;扫雷&lt;/title&gt;
    &lt;style type="text/css"&gt;
        *{
            color: black;
            margin:0px;
            padding:0px;
        }
        html,body{
            -webkit-tap-highlight-color: transparent;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            text-decoration: none;
            height: 100%;
        }
        .con div{
            height: 40px;
            margin-left: 0.2%;
            width: 11%;
            display: inline-block;
            border: solid 1px #000;
            position: absolute;
            line-height: 50px;
            text-align: center;
            color:red;
        }
        .ti{
            position: absolute;
            bottom: 12%;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div id="contain" class="con"&gt;&lt;/div&gt;
    &lt;div class="ti"&gt;已花时间：&lt;span id="time"&gt;0&lt;/span&gt;秒&lt;/div&gt;
    &lt;script type="text/javascript"&gt;
        var leiRes=new Array(),nums=new Array();
        var Lei=1,i,jk,G=81,res=1,clickNum=0,num=0;
        //随机产生区间内的随机数
        function setRandomNum(min,max){
            return Math.floor(Math.random()*(max-min+1)+min);
        }
        //搜寻周边8个点
        function NotLeiNum(n){
            var z=Math.floor(n/9),x=n%9,leiNum=0;
            var arr=new Array();
            if(z-1&gt;=0){
                arr.push((z-1)*9+x);
            }
            if(z+1&lt;9){
                arr.push((z+1)*9+x);
            }
            if(x-1&gt;=0){
                arr.push(z*9+x-1);
            }
            if(x+1&lt;9){
                arr.push(z*9+x+1);
            }
            if(x-1&gt;=0&amp;&amp;z-1&gt;=0){
                arr.push((z-1)*9+x-1);
            }
            if(x-1&gt;=0&amp;&amp;z+1&lt;9){
                arr.push((z+1)*9+x-1);
            }
            if(x+1&lt;9&amp;&amp;z-1&gt;=0){
                arr.push((z-1)*9+x+1);
            }
            if(x+1&lt;9&amp;&amp;z+1&lt;9){
                arr.push((z+1)*9+x+1);
            }
            for(i=0;i&lt;arr.length;i++){
                if(leiRes[arr[i]]==1){
                    leiNum++;
                }
            }
            return leiNum;
        }
        //搜寻周边四个点
        function NotLei(n){
            var z=Math.floor(n/9),x=n%9,leiNum=0;
            var arr=new Array();
            if(z-1&gt;=0){
                arr.push((z-1)*9+x);
            }
            if(z+1&lt;9){
                arr.push((z+1)*9+x);
            }
            if(x-1&gt;=0){
                arr.push(z*9+x-1);
            }
            if(x+1&lt;9){
                arr.push(z*9+x+1);
            }
            for(i=0;i&lt;arr.length;i++){
                if(leiRes[arr[i]]==1){
                    leiNum++;
                }
            }
            if(leiNum&lt;1){
                if(NotLeiNum(n)==0){
                    document.getElementById(n).innerHTML=0;
                    document.getElementById(n).style.backgroundColor="#84EFFF";
                    document.getElementById(n).style.color="#000";
                    return 1;
                }
            }
            return 0;
        }
        //递归判断周边四个点
        function judgeLei(n,dir){
            var z=Math.floor(n/9),x=n%9,leiNum=0;
            var arr=new Array();
            switch(dir){
                case 1:
                if(z-1&gt;=0&amp;&amp;leiRes[(z-1)*9+x]==0){
                    if(NotLei((z-1)*9+x)){
                        judgeLei((z-1)*9+x,1);
                    }
                }
                
                case 2:
                if(z+1&lt;9&amp;&amp;leiRes[(z+1)*9+x]==0){
                    if(NotLei((z+1)*9+x)){
                        judgeLei((z+1)*9+x,2);
                    }
                }
                
                case 3:
                if(x-1&gt;=0&amp;&amp;leiRes[z*9+x-1]==0){
                    if(NotLei(z*9+x-1)){
                        judgeLei(z*9+x-1,3);
                    }
                }
                
                case 4:
                if(x+1&lt;9&amp;&amp;leiRes[z*9+x+1]==0){
                    if(NotLei(z*9+x+1)){
                        judgeLei(z*9+x+1,4);
                    }
                }
            }
        }
        //初始化
        for(i=0;i&lt;G;i++){
            nums[i]=i;
            j=Math.floor(i/9),k=i%9;
            leiRes[i]=0;
            var ele=document.createElement("div");
            ele.setAttribute("id",i);
            document.getElementById("contain").appendChild(ele);
            document.getElementById(i).setAttribute("style","top:"+j*40+"px;"+"left:"+k*11+"%");
        }
        //n个整数获取m个不相等整数
        //思路为例存有0-100的数组，首先随机获取一个整数，然后这个整数作为下标与数组下标0的数交换位置，进行下一步从数组下标1-100中在获取数
        for(i=0;i&lt;Lei;i++){
            r=setRandomNum(i,G-1);
            var temp=nums[i];
            nums[i]=nums[r];
            nums[r]=temp;
            leiRes[nums[i]]=1;
        }
        //主游戏环节，为所有节点绑定事件
        var sl=document.getElementById("contain").childNodes;
        for(i=0;i&lt;sl.length;i++){
            sl[i].onclick=function(){
                for(j=0;j&lt;Lei;j++){
                    if(this.id==nums[j]){
                        res=0;
                        document.getElementById(this.id).innerHTML="雷";
                        alert('游戏失败');
                        if(confirm("确认重新开始游戏?")){
                            window.location.reload();
                        }
                    }
                }
                if(res==1){
                    var n = NotLeiNum(this.id);
                    document.getElementById(this.id).innerHTML=n;
                    document.getElementById(this.id).style.backgroundColor="#84EFFF";
                    document.getElementById(this.id).style.color="#000";
                    if(n==0){
                        judgeLei(this.id,1);
                        /*judgeLei(this.id,2);
                        judgeLei(this.id,3);
                        judgeLei(this.id,4);*/
                    }
                }
                seledNum=document.getElementById("contain").childNodes;
                for(i=0;i&lt;seledNum.length;i++){
                    if(seledNum[i].innerHTML==""){
                        num++;
                    }
                }
                if(num==Lei){
                    alert("你成功啦");
                }else{
                    num=0;
                }
            }
        }
        //计时器
        var n=0;
        function addtime(){
            n++;
            document.getElementById("time").innerHTML=n;
        }
        setInterval("addtime()",1000);
        &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
