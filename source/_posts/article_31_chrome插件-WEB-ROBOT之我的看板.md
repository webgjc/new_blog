---
title: chrome插件 web_robot之我的看板
catalog: true
date: 2020-12-01 19:31:43
tags:
    - CHROME插件
    - 自动化
---

## 前言

这次是web-robot这个插件的2.0的迭代。
主要实现了基于事务的看板。也实现了简易看板模式。
（看板为浏览器新标签页）

看板截图
![dashboard](/img/mypost/web_robot_dashboard.jpg)

这几个元素分别来自于
- 百度天气：https://www.baidu.com/s?ie=UTF-8&wd=%E5%A4%A9%E6%B0%94
- 天天基金：https://fund.eastmoney.com/
- 微博热搜：https://s.weibo.com/top/summary?cate=realtimehot
- 知乎热门：https://www.zhihu.com/hot
- web_robot：https://github.com/webgjc/web_robot


## 插件的一些定义

粒度从细到广

- 事件：一个浏览器**动作**，比如点击，设值，开关页面等。
- 事务：多个**事件**的合集，可以整体运行一套流程。如打开页面，设值xx，点击xx，关闭页面/展示到看板。
- 看板：多个**事务**的合集。每个事务表示看板上一个元素。


## 看板使用

首先github上下载源码

> git clone https://github.com/webgjc/web_robot.git

chrome浏览器点击右边更多，更多工具，扩展程序  
或访问
> chrome://extensions/

开启开发者模式，点击加载已解压的扩展程序  
选择刚刚克隆下来的文件夹，确认即可

点开插件如下：

![web_robot](/img/mypost/web_robot_1201.jpg)

### 简易模式

点击 开启简单看板模式

这边以百度天气为例：

打开：https://www.baidu.com/s?ie=UTF-8&wd=%E5%A4%A9%E6%B0%94

如下：
![baidutianqi](/img/mypost/web_robot_baidutianqi.jpg)

点开插件
![jiandankanban](/img/mypost/web_robot_jiandankanban.jpg)

点击页面添加看板，鼠标在页面移动可以看到粉色边框

![web_robot_xuanze](/img/mypost/web_robot_xuanze.jpg)

点击后可以看到选择器列表，从上往下分别是子元素到父元素的选择器

![web_robot_xuanzeqi](/img/mypost/web_robot_xuanzeqi.jpg)

移动选择器可以在页面看到对应的粉色蒙版

点击后，点击确认添加到看板，则可以将对应选择的元素加到看板中  
打开新页，就可以看到刚刚加的元素。

将鼠标移到页面上面中间，则会出现排版和重置。

![web_robot_new_tab](/img/mypost/web_robot_new_tab.jpg)

点击排版可以配置一个元素框的大小。  
(不会改变内部元素的大小，只改变看的框)

可以调整位置和大小，或者删除元素。

多加几个即可达到页面初的效果。

### 复杂模式

参考
[教程1，最初教程](/article/article_18_chrome插件-网页自动化/)
[教程2，进阶教程](/article/article_21_chrome插件-WEB-ROBOT/)


添加到看板对事务的要求为
- 流程事务
- 第一个事件为当页跳转 pagejump
- 最后一个事件为唯一展示 onlyshow

中间可以添加各种点击设值事件。

定义完后，重新打开插件，可看到定义的事务有一个选项叫  
添加看板，点击后则可以将对应元素加到看板中。

![web_robot_add_dshb](/img/mypost/web_robot_add_dshb.jpg)

后续看板中的管理和上面简易模式一致。

