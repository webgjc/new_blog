---
title: chrome插件 web_robot之难点探讨
catalog: true
date: 2000-12-01 19:31:43
tags:
    - CHROME插件
    - 自动化
---

## 前言

本篇主要对 WEB-ROBOT 用到的技术点和实现的探讨

将会以一个一篇文章的粒度来探讨。

### 可视化圈选的实现

- 选中事件捕获与ui展示
- 反向选择器解析

### 从上层运行到下层事件的运行流程

- 多条事务形成联动，事务上下游，事务循环，爬虫事务（未实现）
- 一个事务的运行
- 一个事件的运行，包括前置dom检查
- js事件与chrome事件封装

### 插件的通信

- background与popup
- popup与content_script
- new_tab与content_script

### 关于运行模式的一些思路

- 一般运行
- 受控运行
