---
article: false
title: 采坑备忘录
catalog: true
date: 2021-01-29 19:31:43
subtitle: 记录下各种采坑修复的骚操作
header-img:
---

## jetbrains破解

从官网下载idea/pycharm 2019.3前的版本。

网上搜索jetbrains-agent-latest下载。

将jar文件拖入idea、pycharm即可。

## hexo锚点失效为undefined

修改如下文件，
> node_modules/hexo-toc/lib/filter.js

将29-31替换为
> $title.attr('id', id);

## 无底洞