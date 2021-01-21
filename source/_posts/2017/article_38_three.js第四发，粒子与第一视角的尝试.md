
---
title: three.js第四发，粒子与第一视角的尝试
catalog: true
date: 2017-8-1 15:52:15
---

<a href="http://test.ganjiacheng.cn/3d/test3d5.html">点这里先看效果</a>，会有点晕，毕竟第一视角。

其中的大致思路：首先是舞台， 摄像机，渲染器。然后有一个clock，用于更新摄像机位置时候。<!--more-->FirstPersonControls用于制作第一视角的，后面也设置了许多参数。createSprites函数中先是创造了点云的几何和材料，然后把向量点加进去，最后在把点云加到舞台。通过渲染持续创造点云，为所有点云改变位置。
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
        #stats{
            position: absolute;
            left: 0;
            top: 0;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div id="stats"&gt;&lt;/div&gt;
    &lt;div id="webgl"&gt;&lt;/div&gt;
    &lt;script type="text/javascript" src="learning-threejs/libs/three.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="learning-threejs/libs/stats.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="learning-threejs/libs/FirstPersonControls.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript"&gt;
        function init(){
            var clock = new THREE.Clock();
            var stats=initStats();

            var scene=new THREE.Scene();

            var camera=new THREE.PerspectiveCamera(45,window.innerWidth/window.innerHeight,0.1,1000);
            camera.position.set(0,0,0);
            camera.lookAt(scene.position);
            
            var renderer=new THREE.WebGLRenderer();
            renderer.setClearColor(0x000000);
            renderer.setSize(window.innerWidth,window.innerHeight);
            renderer.shadowMapEnable=true;

            var camControls = new THREE.FirstPersonControls(camera);
            camControls.lookSpeed = 0.4;
            camControls.movementSpeed = 20;
            camControls.noFly = true;
            camControls.lookVertical = true;
            camControls.constrainVertical = true;
            camControls.verticalMin = 1.0;
            camControls.verticalMax = 2.0;
            camControls.lon = -180;
            camControls.lat = 180;

            function createSprites(){
                pic="image/Sam"+Math.floor(Math.random()*10)+".jpg";
                var texture=THREE.ImageUtils.loadTexture(pic);
                var geom=new THREE.Geometry();
                var material=new THREE.PointCloudMaterial({
                    size:4,
                    transparent:true,
                    map: texture,
                    blending: THREE.AdditiveBlending,
                    color:0x5fe0ff,
                });
                var range=500;
                for(var i=0;i&lt;500;i++){
                    var particle=new THREE.Vector3(Math.random() * range - range / 2, Math.random() * range + range / 5, Math.random() * range - range / 2);
                    geom.vertices.push(particle);
                    var color=new THREE.Color(0x00ff00);
                    color.setHSL(color.getHSL().h,color.getHSL().s,Math.random()*color.getHSL().l);
                    geom.colors.push(color);
                }
                cloud=new THREE.PointCloud(geom,material);
                cloud.sortParticles=true;
                scene.add(cloud);
            }

            function fulldown(){
                scene.children.pop();
            }

            createSprites();
            
            document.getElementById("webgl").appendChild(renderer.domElement);
            renderer.render(scene,camera);
            
            var step=0;
            var v=0;
            function rendererScene(){
                stats.update();
                var delta = clock.getDelta();
                camControls.update(delta);
                step+=2;
                if(step%100==0){
                    createSprites();
                }
                for(var i=0;i&lt;scene.children.length;i++){
                    scene.children[i].position.y-=2;
                }
                requestAnimationFrame(rendererScene);
                renderer.render(scene,camera);
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
效果是不断有数字掉落，这种还可以模拟下雨下雪之类。
