---
article: false
title: 音乐篇
catalog: true
date: 1020-08-23 19:31:43
subtitle: 音乐始终陪伴
header-img: "/img/header_img/archive.jpg"
---

<!-- https://github.com/newraina/mePlayer -->

<video src="#" controls="controls" style="width: 100%; max-height: 500px" id="movie" loop="loop">
您的浏览器不支持 video 标签。
</video>

<div class="music" id="ms"></div>

## [伯虎说](/music/伯虎说.mp3)

## [fallin flower](/music/fallinflower.mp3)

## [summer](/img/movie/summer.mp4)

## [秋的思念](/img/movie/qiudesinian.mp4)

## [信仰-全职高手](/img/movie/xinyang.mp4)

## [Someone like you](/img/movie/someonelikeyou.mp4)

## [梦中的婚礼](/img/movie/mengzhongdehunli.mp4)

## [烟火里的尘埃](/img/movie/yanhuolidechenai.mp4)

## [青石巷 - 片段](/img/movie/qingshixiang.mp4)

## [海底](/img/movie/haidi.mp4)

## [River flows in you](/img/movie/riverflowsinyou.mp4)

## [夜的钢琴曲11](/img/movie/yedegangqinqu11.mp4)

## [梁祝钢琴曲](/img/movie/liangzhu.mp4)

## 我的纯音乐歌单
[纯音乐歌单](https://t.kugou.com/355mda6xVV2)（打不开可以尝试手机打开）

很多歌带着一段感情与记忆，还是要经历过才会听得更有滋味

## 音乐篇必读镇楼 
- 2020-08-23
```
音乐自得其乐
1. 分享音乐与感受
2. 钢琴学习与弹奏
```

<script type="text/javascript" src="/js/jquery.min.js"></script>
<script type="text/javascript" src="/js/meplayer.min.js"></script>

<script type="text/javascript">

    let defaultPlay = "qiudesinian";
    let movie = document.getElementById("movie");
    let ms = document.getElementById("ms");
    let lks = document.querySelectorAll(".post-container > h2 > a");
    let mePlayerBuilder = mePlayer;
    let mePlayerOperater = null;
    let first = true;

    function getQueryVariable(variable){
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
            var pair = vars[i].split("=");
            if(pair[0] == variable){return decodeURI(pair[1]);}
       }
       return(false);
    }

    function playMovie(pmv, play) {
        ms.style.display = "none";
        movie.style.display = "block";
        if(document.getElementsByTagName("audio")[0]) {
            document.getElementsByTagName("audio")[0].pause()
        }
        movie.src=pmv.href;
        if(play) {
            movie.play();
        }
    }

    function playMp3(pmp, play) {
        movie.style.display = "none";
        movie.pause();
        ms.style.display = "block";
        mePlayerBuilder({
            music: {
                src: pmp.href,
                title: pmp.text,
                author: "纯音乐请欣赏",
                loop: true
            },
            target: '#ms',
            autoplay: play
        });
    }


    for(let i = 0; i < lks.length; i++) {
        if(lks[i].className == "" && lks[i].href.endsWith("mp4")) {
            lks[i].onclick = function(e){
                e.preventDefault();
                playMovie(lks[i], true);
            }
        }

        if(lks[i].className == "" && lks[i].href.endsWith("mp3")) {
            lks[i].onclick = function(e){
                e.preventDefault();
                playMp3(lks[i], true);
            }
        }
    }

    let thePlay;
    if(getQueryVariable("init")) {
        thePlay = getQueryVariable("init")
    } else {
        thePlay = defaultPlay;
    }
    let init = document.getElementById(thePlay);
    let node = init.children[0];
    if(node.href.endsWith("mp4")) {
        playMovie(node, false);
    }
    if(node.href.endsWith("mp3")) {
        playMp3(node, false);
    }
</script>