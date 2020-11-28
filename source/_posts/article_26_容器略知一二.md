---
title: 容器略知一二
catalog: true
date: 2000-09-27 19:31:43
tags:
    - JAVA
    - 知识积累
---

## 前言

本文产出关于一些容器的知识

### tomcat 总体架构

-   server:一个 tomcat 即一个 server
-   service:包含多个 connector 和一个 container，一个 server 可以有多个 service
-   connector:链接器，监听 socket 并交给对应 container 处理
-   container:执行请求并返回响应的对象，包括 engine，host，context，wrapper
-   engine:整个 servlet 引擎，最高层级容器对象，获取目标容器入口
-   host:表示虚拟主机的概念，处理来自不同地址的请求
-   context:表示一个独立的 web 应用
-   wrapper:表示 servlet 定义
-   executor:表示可以共享的线程池

### tomcat 处理请求过程

-   endpoint 接收请求
-   processor 处理请求
-   coyoteAdapter 请求路径映射
-   mapper 获取匹配的执行
-   engine 容器入口
-   host 获取匹配的 host 执行
-   context 获取匹配的 context 执行
-   wrapper 获取匹配的 wrapper 执行
-   filterchain 执行 filter
-   servlet 执行 servlet
