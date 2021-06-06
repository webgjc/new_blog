---
article: false
title: 音乐篇
catalog: true
date: 1020-08-23 19:31:43
subtitle: 音乐始终陪伴
header-img: "/img/header_img/archive.jpg"
---

<video src="/img/movie/mengzhongdehunli.mp4" controls="controls" style="width: 100%; max-height: 500px" id="movie" loop="loop">
您的浏览器不支持 video 标签。
</video>

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

<script type="text/javascript">
    let movie = document.getElementById("movie");
    let lks = document.querySelectorAll(".post-container > h2 > a");
    for(let i = 0; i < lks.length; i++) {
        if(lks[i].className == "" && lks[i].href.endsWith("mp4")) {
            lks[i].onclick = function(e){
                e.preventDefault();
                movie.src=lks[i].href;
                movie.play();
            }
        }
    }
</script>