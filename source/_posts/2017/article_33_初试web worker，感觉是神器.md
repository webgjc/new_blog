
---
title: 初试web worker，感觉是神器
catalog: true
date: 2017-7-25 21:02:15
---

在做3d的时候偶然发现其中用了web worker，因为要做大量的运算，如果放在js的主单线程里就会让页面卡的不行。

不信可以运行下面的Fibonacci<!--more-->
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;web worker&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;button id="btn"&gt;click me&lt;/button&gt;
    &lt;script type="text/javascript"&gt;
        btn.onclick=function(){
            alert('you clicked');
        }
        function fb(n){
            if(n==1||n==2){
                return 1;
            }else{
                return fb(n-1)+fb(n-2);
            }
        }
        alert(fb(45))
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
上面代码至少让浏览器卡上个10秒，也就是按钮事件没法触发。

然后就用得到web worker咯，他创造了类似于后台运行的“多线程”，在保证主线程正常运行的情况下在后台运行计算代码。

一些限制貌似是web worker有同源限制，也无法访问主线程的dom。

下面是web worker的代码，因为要同源，要放在服务器上运行，否则会报错。

主文件index.html
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;web worker&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;button id="btn"&gt;click me&lt;/button&gt;
    &lt;script type="text/javascript"&gt;
        var worker=new Worker("worker.js");
        worker.postMessage(45);
        worker.onmessage=function(e){
            alert(e.data)
        }
        var btn=document.getElementById("btn");
        btn.onclick=function(){
            alert('you clicked');
        }
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
然后是worker.js，在同目录下
<pre>onmessage=function(e){
    function fb(n){
        if(n==1||n==2){
            return 1;
        }else{
            return fb(n-1)+fb(n-2);
        }
    }
    postMessage(fb(e.data));
}</pre>
通过服务器运行index.html就可以啦。

比对上面的情况，效果很明显。
