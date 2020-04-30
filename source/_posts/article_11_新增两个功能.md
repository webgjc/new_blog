---
title: 博客新增两个功能模块
catalog: true
date: 2020-04-29 21:31:43
subtitle: 
header-img: 
tags:
- OTHER
---

## 入口

在主页侧边栏的FRIENDS模块中，

新增了[我的钢琴屋](http://piano.ganjiacheng.cn/) 和 [我的阅读室](/book/)

下面分别来阐述

## 我的钢琴屋

这个是挂在github上的一个静态页面，github地址为
> [https://github.com/webgjc/tan8](https://github.com/webgjc/tan8)【如侵权可下线】

主要功能为练习和收听钢琴曲

### 实现

其中包括一个flash播放器和一个数据列表

flash播放器主要参考某琴吧的实现，并引用了他们的文件存储直接获取到源地址

数据列表也主要来自某琴吧，这边用爬虫获取到了钢琴的全部列表，并做展示和过滤搜索，

数据存储为json格式，在打开页面时直接加载

表单使用的是bootstrap-table

## 我的阅读室

这个主要是为了能催自己多看看书，不迷茫。

每次看一本书也会记录下看书的笔记和感想。

### 实现

这个是在原博客基础上的进行的一部分改造，

在主题源文件下layout/
新增book.ejs

在source/下新增book/ book/index.md  
在头上加上
> layout: "book"

这样就可以新增一个页面和路由到/book/

然后在_posts中主动区分一下一般页面和书评页面，  
我这边实现是在头部加上
> book: true

然后在book.ejs中,  
对于每个post的处理前加上过滤,  
然后就可以自己对书籍文章进行排版和构建，  
比如我在文章头部加上book-cover: /img/xxx.jpg表示封面图片
```
<% site.posts.each(function(post){ %>
    <% if (post.book){ %>
    <% } %>
<% }); %>
```

同时在主题下/layout/index.ejs  
也加上过滤
```
<% page.posts.each(function(post){ %>
    <% if(!post.book) { %>
    <% } %>
<% }); %>
```