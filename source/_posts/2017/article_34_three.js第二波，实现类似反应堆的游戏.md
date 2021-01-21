
---
title: three.js第二波，实现类似反应堆的游戏
catalog: true
date: 2017-7-25 21:26:57
---

一开始还就迷茫呢碰撞检测比较难，后来发现了physi.js。

也是在看three.js看到的一个库，用了web worker实现各种复杂的计算。

先<a href="http://test.ganjiacheng.cn/3d/test3d6.html">点击这里看效果</a>，手机电脑支持web worker(一般都支持)的都可以运行<!--more-->

初次加载看起来快，实际一个用于计算的ammo.js也有1.2M，只是他在后台加载。所以可能得等一会儿。

这个本应该有个onload的，不过目前还没有发现这个函数，之后有机会在探索。

思路便是：创造一个物理舞台，摄像头和渲染器和之前一样，加一个物理平面（带摩擦和弹性），加一个普通cube并来回运动，监听click事件，click时获取普通cube的位置并创造一个物理cube，物理cube便会往下掉，加一个计分。

下面是具体代码，js文件的话在下面的路径可以找到

http://test.ganjiacheng.cn/3d/learning-threejs/libs/xxx.js
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;  
    &lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;
    &lt;title&gt;test3d6&lt;/title&gt;
    &lt;style type="text/css"&gt;
        body{
            margin: 0;
            overflow: hidden;
        }
        #stats{
            position: absolute;
            left: 0;
            top: 0;
        }
        #grade{
            position: absolute;
            left: 50%;
            margin-left: -28px;
            top: 0;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div id="stats"&gt;&lt;/div&gt;
    &lt;div id="grade"&gt;0&lt;/div&gt;
    &lt;div id="webgl"&gt;&lt;/div&gt;
    &lt;script type="text/javascript" src="learning-threejs/libs/three.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="learning-threejs/libs/stats.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="learning-threejs/libs/physi.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript"&gt;
        var scene;
        function init(){
            var stats=initStats();

            Physijs.scripts.worker='learning-threejs/libs/physijs_worker.js';

            var scene=new Physijs.Scene();
            scene.setGravity(new THREE.Vector3(0,-50,0));

            var camera=new THREE.PerspectiveCamera(45,window.innerWidth/window.innerHeight,0.1,1000);
            camera.position.set(-30,40,40);
            camera.lookAt(scene.position);
            
            var renderer=new THREE.WebGLRenderer();
            renderer.setClearColor(0xEEEEEE);
            renderer.setSize(window.innerWidth,window.innerHeight);
            renderer.shadowMapEnable=true;
            
            var ground_material=Physijs.createMaterial(new THREE.MeshLambertMaterial({color:0xffffff}),0.9,0.3);
            var planeGeometry=new Physijs.BoxMesh(new THREE.BoxGeometry(10,1,10),ground_material,0)            
            scene.add(planeGeometry);
            
            function addPhyCube(x=0,y=0,z=0){
                var cubeGeometry=new THREE.BoxGeometry(10,2,10);
                var cube=new Physijs.BoxMesh(cubeGeometry,Physijs.createMaterial(new THREE.MeshLambertMaterial({color:0xffffff*Math.random()}),1,0));
                cube.position.set(x,y,z);
                scene.add(cube);
            }

            function addNormalCube(x=0,y=8,z=0){
                var cubeGeometry=new THREE.BoxGeometry(10,2,10);
                var cubeMaterial=new THREE.MeshLambertMaterial({color:0xff0000});
                var cube=new THREE.Mesh(cubeGeometry,cubeMaterial);
                cube.position.set(x,y,z);
                scene.add(cube);
            }
            
            var maxy=0;
            var NorNum=2;
            var time=0
            function refreshGrade(){
                if(time==0 &amp;&amp; stats.domElement.textContent[0]==6){
                    document.getElementById("webgl").onmousedown=function(){
                        addPhyCube(scene.children[NorNum].position.x,scene.children[NorNum].position.y,scene.children[NorNum].position.z);
                        time=2;
                    }
                    time=1;
                }else if(time==1){
                    document.getElementById("grade").innerHTML="start";
                }else if(time==2){
                    var len=scene.children.length;
                    var maxy=0;
                    for(var i=NorNum+1;i&lt;len;i++){
                        maxy=scene.children[i].position.y&gt;-2&amp;&amp;Math.abs(scene.children[i].position.z)&lt;15?maxy+1:maxy;
                    }                
                    camera.position.y=maxy*2+40;
                    scene.children[NorNum].position.y=maxy*2+5;
                    document.getElementById("grade").innerHTML="score:"+maxy;
                }else{
                    document.getElementById("grade").innerHTML="waiting......";
                }
            }   

            var spotLight=new THREE.SpotLight(0xffffff);
            spotLight.position.set(-40,60,0);
            scene.add(spotLight);
            spotLight.castShadow=true;
            
            document.getElementById("webgl").appendChild(renderer.domElement);
            addNormalCube(0,8,-20);
            renderer.render(scene,camera);

            var step=0;

            function rendererScene(){
                stats.update();
                refreshGrade();
                last=scene.children.length-1;
                step+=0.05;
                scene.children[NorNum].position.z+=Math.sin(step);
                requestAnimationFrame(rendererScene);
                renderer.render(scene,camera);
                scene.simulate();
            }

            function initStats(){
                var stats=new Stats();
                stats.setMode(0);
                document.getElementById("stats").appendChild(stats.domElement);
                return stats;
            }

            rendererScene();
        }
        window.onload=init;
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
效果展示：

<img class="alignnone size-medium wp-image-355" src="/img/uploads/2017/07/IMG_3419-169x300.png" alt="" width="169" height="300" />
