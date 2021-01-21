---
title: 分布式略知一二
catalog: true
date: 2000-09-27 19:31:43
tags:
    - JAVA
    - 知识积累
---

## 前言

本文涉及分布式情况下会产生的各种问题；

### celery 多个 comsumor 如何实现一致性

当 celery 配合 redis，将 redis 作为消息队列时，redis 内部使用 list 的 lpush，brpop 来实现入队出队。  
当多个 celery 消费进程来取任务时，由于 redis 内部是单线程的，不会导致消息的重复读，brpop 在没任务时会阻塞。

### cap 理论

-   一致性
-   可用性
-   分区容错性

### zk 如何保证一致性

客户端的写请求都由 Leader 接收，Leader 将请求转成事务 Proposal，并向集群所有 Follower 节点发送广播请求，  
只要有一半以上的 Follower 进行了正确的反馈 ACK，Leader 再向所有 Follower 发送 commit 请求，将上一个事务进行提交。
