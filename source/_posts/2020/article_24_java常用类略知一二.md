---
title: Java常用类略知一二
catalog: true
date: 2000-09-27 19:31:43
tags:
    - JAVA
    - 知识积累
---

## 前言

这是一篇关于 Java 部分常用类的源码和实现方法的快速记录回忆篇

### HashMap

存储结构：数组 + 链表/红黑树  
put：首先将 key 取 hashcode，移位 16 位得到 1-16 的数作为数组 index，对于不同的 key 一样的 index 存入一个单链表中，当数量比较大后存成一个红黑树，便于查找  
get：首先将 key 进行一样的操作，得到 index，获取数组 index 的链表或者树然后进行遍历找到对应 key 的 value

### ThreadLocal

维护一个 ThreadLocalMap，当前线程 Thread 作为 key，value 为存储的值

### HashSet

维护一个 HashMap 实现

### synchronized 和 volatile 区别

-   volatile 是让当前变量到主存里去读取，synchronized 则是锁定当前变量；
-   volatile 只能用在变量级别，synchronized 可以用在变量、方法和类；
-   volatile 只能实现变量修改可见性，不能保证原子性，synchronized 可以保证可见性和原子性；
-   volatile 会让线程自旋，不会阻塞。synchronized 可能会造成阻塞；
-   volatile 变量不会被编译器优化，synchronized 会被优化；
