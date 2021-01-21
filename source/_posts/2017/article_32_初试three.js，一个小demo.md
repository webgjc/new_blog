
---
title: 初试three.js，一个小demo
catalog: true
date: 2017-7-24 19:18:45
---

之前看过一点webgl编程指南，确实很难消化。所以过段时间再来朝花夕拾。

这次直接使用webgl的一个库three.js，能更方便的实现功能。

先可以<a href="https://ganjiacheng.cn/blogdemo/threejsdemo.html">点击这里看最终效果</a>。<!--more-->

基本的几步就是：定义舞台，定义透视摄像机，定义渲染器，定义灯光，画爱心，填充爱心，向舞台中心增加爱心，随机向外扩散。

下面是html代码
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;test3d3&lt;/title&gt;
    &lt;style type="text/css"&gt;
        body{
            margin: 0;
            overflow: hidden;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div id="webgl"&gt;&lt;/div&gt;
    &lt;script type="text/javascript" src="https://threejs.org/build/three.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript"&gt;
        function init(){
            var scene=new THREE.Scene();
            scene.fog=new THREE.Fog(0xffffff,15,300);

            var camera=new THREE.PerspectiveCamera(45,window.innerWidth/window.innerHeight,0.1,1000);
            camera.position.set(100,100,100);
            camera.lookAt(scene.position);
            
            var renderer=new THREE.WebGLRenderer();
            renderer.setClearColor(0xEEEEEE);
            renderer.setSize(window.innerWidth,window.innerHeight);

            var spotLight=new THREE.DirectionalLight(0xffffff);
            spotLight.position.set(200,40,200);
            scene.add(spotLight);

            function drawShape(){
                var shape=new THREE.Shape();
                shape.moveTo(0, 0);
                shape.quadraticCurveTo(-3.8, 2, 4, 9);
                shape.quadraticCurveTo(11, 2, 8, 0);
                shape.quadraticCurveTo(5, -1.2, 4, 2);
                shape.quadraticCurveTo(3, -1.2, 0, 0);
                return shape;
            }

            function createMesh(goem){
                var meshMaterial=new THREE.MeshPhongMaterial({color:0xffffff * Math.random()});
                meshMaterial.side=THREE.DoubleSide;
                var mesh=THREE.SceneUtils.createMultiMaterialObject(goem,[meshMaterial]);
                mesh.position.set(0,0,0);
                return mesh;
            }
            
            var vx=[1],vy=[1],vpy=[1],vpx=[1], vpz=[1];

            function addinitShape(){
                vx.push(Math.random()*0.02);
                vy.push(Math.random()*0.02);
                vpy.push(-0.15+Math.random()*0.3);
                vpx.push(-0.15+Math.random()*0.3);
                vpz.push(-0.15+Math.random()*0.3);
                var shape=createMesh(new THREE.ShapeGeometry(drawShape()));
                shape.rotation.z=Math.PI;
                shape.rotation.y=Math.random()*Math.PI;
                scene.add(shape);
            }

            for(var i=0;i&lt;100;i++){
                addinitShape();
            }
            
            setInterval(function(){
                if(scene.children.length&lt;1000){
                    addinitShape();
                }else{
                    scene.children.splice(1,1);
                    vx.shift();
                    vy.shift();
                    vpx.shift();
                    vpy.shift();
                    vpz.shift();
                }
            },80)
            
            document.getElementById("webgl").appendChild(renderer.domElement);
            
            function rendererScene(){
                for(let i=1;i&lt;scene.children.length;i++){
                    scene.children[i].rotation.y += vy[i];
                    scene.children[i].rotation.x += vx[i];
                    scene.children[i].position.y -= vpy[i];
                    scene.children[i].position.x += vpx[i];
                    scene.children[i].position.z += vpz[i];
                }
                requestAnimationFrame(rendererScene);
                renderer.render(scene,camera);
            }
            rendererScene();
        }
        window.onload=init;
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
这还是three.js最基础的一部分，之后会继续加特技啦！
