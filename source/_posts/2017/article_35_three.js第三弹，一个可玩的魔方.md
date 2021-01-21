
---
title: three.js第三弹，一个可玩的魔方
catalog: true
date: 2017-7-27 21:42:09
---

魔方对于大多数人都不陌生，也是个立方体的玩意儿。

这里就简单用three.js实现一下，复杂的还是定位，毕竟是3d的还能乱转。

<a href="http://test.ganjiacheng.cn/3d/test3d2.html">点击这里先看效果哦！！</a><!--more-->

看代码前还是先来说明：基本框架还是一样----舞台，摄像头和渲染器。

之后用faceMaterial写一个6面颜色不一样的cube，并用27个这样的cube组成魔方的基本样子。

trackballControls是摄像头控制函数，加入可以用鼠标控制其中的摄像头。

监听鼠标按下事件，按下时获取点击的三维坐标，获取在最前端的cube的name。

通过坐标计算旋转方向（这里容易脑壳疼），通过name计算同一平面的其他cube。

通过方向与平面以矩阵旋转平面内9个cube，并把旋转做成动画。

听说好文章结尾都有彩蛋~
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;
    &lt;title&gt;test3d&lt;/title&gt;
    &lt;style type="text/css"&gt;
        body{
            margin: 0;
            overflow: hidden;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div id="webgl"&gt;&lt;/div&gt;
    &lt;script type="text/javascript" src="http://test.ganjiacheng.cn/3d/learning-threejs/libs/three.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="http://test.ganjiacheng.cn/3d/learning-threejs/libs/TrackballControls.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript"&gt;
        function init(){
            var scene=new THREE.Scene();

            var camera=new THREE.PerspectiveCamera(45,window.innerWidth/window.innerHeight,0.1,1000);
            camera.position.set(-20,20,20);
            camera.lookAt(scene.position);

            var renderer=new THREE.WebGLRenderer();
            renderer.setClearColor(0xdadada);
            renderer.setSize(window.innerWidth,window.innerHeight);
            renderer.shadowMapEnabled=true;

            var axes=new THREE.AxisHelper(2);
            scene.add(axes);

            var group=new THREE.Mesh();
            var mats=[];
            mats.push(new THREE.MeshBasicMaterial({color:0x009e60}));//g
            mats.push(new THREE.MeshBasicMaterial({color:0x0051ba}));//b
            mats.push(new THREE.MeshBasicMaterial({color:0xffd500}));//y
            mats.push(new THREE.MeshBasicMaterial({color:0xff5800}));//j
            mats.push(new THREE.MeshBasicMaterial({color:0xC41E3A}));//r
            mats.push(new THREE.MeshBasicMaterial({color:0xffffff}));//w
            var faceMaterial=new THREE.MeshFaceMaterial(mats);
            for(var x=0;x&lt;3;x++){
                for(var y=0;y&lt;3;y++){
                    for(var z=0;z&lt;3;z++){
                        var cubeGeom=new THREE.BoxGeometry(2.9,2.9,2.9);
                        var cube=new THREE.Mesh(cubeGeom,faceMaterial);
                        cube.position.set(x*3-3,y*3-3,z*3-3);
                        cube.name=z+3*y+9*x;
                        group.add(cube);
                    }
                }
            }
            scene.add(group);

            var trackballControls=new THREE.TrackballControls(camera);
            trackballControls.rotateSpeed=1.0;
            trackballControls.zoomSpeed=1.0;
            trackballControls.panSpeed=1.0;

            document.addEventListener('mousedown',onMouseDown,false);

            var clock=new THREE.Clock();

            document.getElementById("webgl").appendChild(renderer.domElement);
            renderer.render(scene,camera);

            var test=new THREE.MeshBasicMaterial({color:0x000000});
            var startMove=-1;
            var moveList=[];
            var rotateDirection;
            var DirectionLR=true;
            var j=0;
            function onMouseDown(event){
                if(startMove!=-1){
                    return;
                }
                var vector=new THREE.Vector3((event.clientX/window.innerWidth)*2-1,-(event.clientY/window.innerHeight)*2+1,0.5);
                vector=vector.unproject(camera);
                var raycaster=new THREE.Raycaster(camera.position,vector.sub(camera.position).normalize());
                var intersects=raycaster.intersectObjects(group.children);
                if(intersects.length&gt;0){
                    j=0;
                    moveList=[];
                    startMove=intersects[0].object.name;
                    var y=scene.children[1].children[startMove].position.y;
                    getRotateDirection(intersects[0].point.x,intersects[0].point.y,intersects[0].point.z);
                    if(rotateDirection==1){
                        for(var i=0;i&lt;27;i++){
                            if(xround(scene.children[1].children[i].position.y,2)==xround(y,2)){
                                moveList.push(i);
                            }
                        }
                    }else if(rotateDirection==2){
                        for(var i=0;i&lt;27;i++){
                            if(xround(scene.children[1].children[i].position.x,2)==xround(scene.children[1].children[startMove].position.x,2)){
                                moveList.push(i);
                            }
                        }
                    }else if(rotateDirection=3){
                        for(var i=0;i&lt;27;i++){
                            if(xround(scene.children[1].children[i].position.z,2)==xround(scene.children[1].children[startMove].position.z,2)){
                                moveList.push(i);
                            }
                        }
                    }
                }
            }

            function reset(){
                startMove=-1;
            }

            function rotationMF(moveList){
                var rotationV=DirectionLR?Math.PI/100:-Math.PI/100;
                if(rotateDirection==1){
                    if(j&lt;50){
                        for(var i in moveList){
                            var rotation = new THREE.Matrix4().makeRotationY(rotationV);
                            scene.children[1].children[moveList[i]].applyMatrix(rotation);
                        }
                        j++;
                    }else{
                        reset()
                    }
                }else if(rotateDirection==2){
                    if(j&lt;50){
                        for(var i in moveList){
                            var rotation = new THREE.Matrix4().makeRotationX(rotationV);
                            scene.children[1].children[moveList[i]].applyMatrix(rotation);
                        }
                        j++;
                    }else{
                        reset()
                    }
                }else if(rotateDirection==3){
                    if(j&lt;50){
                        for(var i in moveList){
                            var rotation = new THREE.Matrix4().makeRotationZ(rotationV);
                            scene.children[1].children[moveList[i]].applyMatrix(rotation);
                        }
                        j++;
                    }else{
                        reset()
                    }
                }
            }
            
            function xround(x, num){
                return Math.round(x * Math.pow(10, num)) / Math.pow(10, num);
            }
            function getRotateDirection(x,y,z){
                function dealxyz(axis){
                    for(var i=0;i&lt;3;i++){
                        if(xround(axis[i],2)==-4.45 || xround(axis[i],2)==4.45){
                            var fl=xround(axis.splice(i,1),2)==-4.45;
                            axis[0]=axis[0]&gt;1.5?axis[0]-3:axis[0];
                            axis[0]=axis[0]&lt;-1.5?axis[0]+3:axis[0];
                            axis[1]=axis[1]&gt;1.5?axis[1]-3:axis[1];
                            axis[1]=axis[1]&lt;-1.5?axis[1]+3:axis[1];
                            var judge;
                            if(i==0 &amp;&amp; Math.abs(axis[0])&lt;Math.abs(axis[1])){
                                rotateDirection=1;
                                judge=fl?(Math.abs(axis[0])&lt;Math.abs(axis[1]) &amp;&amp; axis[1]&lt;0):(Math.abs(axis[0])&lt;Math.abs(axis[1]) &amp;&amp; axis[1]&gt;0);
                            }else if(i==0 &amp;&amp; Math.abs(axis[0])&gt;Math.abs(axis[1])){
                                rotateDirection=3;
                                judge=!fl?(Math.abs(axis[1])&lt;Math.abs(axis[0]) &amp;&amp; axis[0]&lt;0):(Math.abs(axis[1])&lt;Math.abs(axis[0]) &amp;&amp; axis[0]&gt;0);
                            }else if(i==1 &amp;&amp; Math.abs(axis[0])&lt;Math.abs(axis[1])){
                                rotateDirection=2;
                                judge=!fl?(Math.abs(axis[0])&lt;Math.abs(axis[1]) &amp;&amp; axis[1]&lt;0):(Math.abs(axis[0])&lt;Math.abs(axis[1]) &amp;&amp; axis[1]&gt;0);
                            }else if(i==1 &amp;&amp; Math.abs(axis[0])&gt;Math.abs(axis[1])){
                                rotateDirection=3;
                                judge=fl?(Math.abs(axis[1])&lt;Math.abs(axis[0]) &amp;&amp; axis[0]&lt;0):(Math.abs(axis[1])&lt;Math.abs(axis[0]) &amp;&amp; axis[0]&gt;0);
                            }else if(i==2 &amp;&amp; Math.abs(axis[0])&gt;Math.abs(axis[1])){
                                rotateDirection=1;
                                judge=fl?(Math.abs(axis[1])&lt;Math.abs(axis[0]) &amp;&amp; axis[0]&gt;0):(Math.abs(axis[1])&lt;Math.abs(axis[0]) &amp;&amp; axis[0]&lt;0);
                                console.log(judge);
                            }else if(i==2 &amp;&amp; Math.abs(axis[0])&lt;Math.abs(axis[1])){
                                rotateDirection=2;
                                judge=!fl?(Math.abs(axis[0])&lt;Math.abs(axis[1]) &amp;&amp; axis[1]&gt;0):(Math.abs(axis[0])&lt;Math.abs(axis[1]) &amp;&amp; axis[1]&lt;0);
                            }
                            return judge;
                        }
                    }
                }
                DirectionLR=!dealxyz([x,y,z]);
            }

            function renderScene(){
                var delta=clock.getDelta();
                if(startMove!=-1){rotationMF(moveList);}
                trackballControls.update(delta);
                requestAnimationFrame(renderScene);
                renderer.render(scene,camera);
            }
            renderScene();
        }
        window.onload=init;
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
这里不预览啦，主要注明的一点就是看起来比写起来真是两码事，

一开始纠结在rotation的旋转会连带转自己的坐标轴。后来慢慢发现他转的是他的children子元素，并可以创造矩阵来旋转。

本来想的很好做一个沿y轴转四个面，然后推广到x,z，只要写一套就行。现实还是安心的做完了6个面以及每个面里9个小块的分析。

本来还想着怎么能写的系统一点，可以轻松调InOut，这样就可以做多元的魔方，说不定还能研究个魔方的随机打乱和复原，好吧继续想着吧。

还有点感悟就是three.js文档虽然齐全不过问的问题确实不多，有点难搜到相似问题。搜到的时候讲的都是欧拉角，旋转矩阵，四元数这种画风。。。

three.js完结篇，，

&nbsp;

&nbsp;

&nbsp;

才怪
