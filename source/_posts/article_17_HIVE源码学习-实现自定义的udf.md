---
title: HIVE源码学习--实现自定义的UDF，UDAF，UDTF
catalog: true
date: 2020-05-07 14:31:43
subtitle: 
header-img: 
tags:
- HIVE
---

# 前言

hive里有三种可以自定义实现的函数，
> 自定义函数包括三种 UDF、UDAF、UDTF
> - UDF（User-Defined-Function） 一进一出 ，既一行进一行出  
> - UDAF（User- Defined Aggregation Funcation） 聚集函数，多进一出（多行进一行出）。Count/max/min 
> - UDTF（User-Defined Table-Generating Functions）一进多出，如 explore() 