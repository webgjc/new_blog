---
title: HttpClient的Cookie策略引发的隐藏bug定位
catalog: true
date: 2020-12-27 19:31:43
tags:
    - HTTP
    - 后端
---

## 概述

本文记录一次大概历时半年也没排查出来，时有时无的隐藏bug。  
大致现象是：**一个用户能访问到别人权限的资源(用户串/权限串)**。
中间考虑过线程不安全，包的问题，Threadlocal没清除并线程复用导致等，   
最终还是排查到是Httpclient的连接池的Cookie策略。  
这个点在开发时特别容易被人忽略。

## 场景还原

### 背景说明

首先大致说下这问题和中间涉及的系统

如下有一个业务系统，  
他依赖用户系统提供用户信息，权限系统提供权限信息
![jpg](/img/mypost/article34_1.jpg)

如下是主要流程，当访问接口时，业务系统的拦截器会去用户系统校验登录，   
将用户信息和cookie保存到threadlocal中，  
当也需要权限信息时，则将保存的cookie取出来去调用权限系统，获取这个用户的权限信息。

![jpg](/img/mypost/article34_2.jpg)

### 主要问题
 
问题就出现在这中间 ：  
**进入用户系统的是用户A，但当他访问权限系统返回的权限却是用户B的**  
**且此问题不可稳定复现，出现概率不高**

## 排查过程

### 线程不安全问题

由于这边Springboot的Bean用的是单例模式，  
所以如果一个类定义了一个Hashmap的属性，多个线程之间存取就会出现串的问题

考虑如有部分权限信息存在Hashmap，导致多线程之间取到了他人的。

这个在 review了代码 和 打印了日志 后基本可以排除掉。

### Threadlocal没清除

由于Tomcat管理线程池会复用线程，也就是你的线程在这次请求用了以后，下次还会被别的请求用到，

如果没有清除Threadlocal的话，下次请求中还会保留着你的信息。

这个在经过业务排查之后，  

可以确定在出错的场景下的请求也都会走用户校验将Threadlocal的value重新set一遍，  

因为被覆盖了，就不会存在用了上一个未清除的线程的信息。
（虽然remove确实是该加的，但并不是导致这个问题真正原因）

### 问题收紧

通过加日志看输入输出，最后将问题收缩到一个函数里，  

如下代码，在打印请求头的时候还可以看到是用户A的cookie，但打印返回却是用户B的权限信息。

```java
// 获取请求头
List<Header> headers = getHeaders();
// 打印头
logger.info(JSONObject.toJSONString(headers));
// 调用权限系统
String resp = HttpUtils.sendPostRequest("权限系统接口", headers);
// 打印返回
logger.info(resp);
```

所以最后是考虑原本最不会出问题的发送请求的util出了问题。  
（原本想一个util总不会保留啥东西吧，不就是每次封装新的header请求嘛）

不看不知道，一看还挺有东西。

### 最终定位

看下边的代码，则是HttpUtil的一部分，定义了一个多线程的http连接管理器。  

```java
private static class HttpClientHolder {
    // httpclient定义 用的是org.apache.commons.httpclient
    public static HttpClient httpClient = null;

    // 初始化一个多线程的管理器，
    // 可以设置最大连接，超时等
    static {
        MultiThreadedHttpConnectionManager connectionManager = new MultiThreadedHttpConnectionManager();
        httpClient = new HttpClient(connectionManager);
        httpClient.getHttpConnectionManager().getParams().setMaxTotalConnections(MAX_CONN);
        httpClient.getHttpConnectionManager().getParams().setSoTimeout(MAX_TIME_OUT);
    }

}
```

看到这个想必基本就会想到这个错误大概是怎么发生的了。

如下图，httpclient中有两个线程C和D，  
C处理了用户A的登录，确处理了用户B的权限  
D处理了用户B的登录，确处理用户A的权限  
由此导致了开头的问题。

![jpg](/img/mypost/article34_3.jpg)

## 真正原因与解决

经过一定上面的排查已经确定了问题出现的地方为  
**httpclient的多线程管理中保留了上次请求留下的cookie，并在下次请求时默认带上了。  
由于这个多线程并与tomcat管理的处理http请求的多线程独立管理，所以存在交叉的情况。**

这边要解决他则需要httpclient不保留cookie即可，每次使用外部带进去的cookie

看了下httpclient可配置的参数，在

> org.apache.commons.httpclient.params.HttpMethodParams

有一个CookiePolicy

> org.apache.commons.httpclient.cookie.CookiePolicy

稍微看下可以发现他可配的一些cookie策略。  
这边default是RFC2109


````java
static {
    CookiePolicy.registerCookieSpec(DEFAULT, RFC2109Spec.class);
    CookiePolicy.registerCookieSpec(RFC_2109, RFC2109Spec.class);
    CookiePolicy.registerCookieSpec(RFC_2965, RFC2965Spec.class);
    CookiePolicy.registerCookieSpec(BROWSER_COMPATIBILITY, CookieSpecBase.class);
    CookiePolicy.registerCookieSpec(NETSCAPE, NetscapeDraftSpec.class);
    CookiePolicy.registerCookieSpec(IGNORE_COOKIES, IgnoreCookiesSpec.class);
}
```

搜了下RFC2109这个是个什么鬼

它是个http状态管理协议，具体可以到这看[https://datatracker.ietf.org/doc/rfc2109/](https://datatracker.ietf.org/doc/rfc2109/)

这边引用他摘要的一段话

>This document specifies a way to create a stateful session with HTTP
   requests and responses.  It describes two new headers, Cookie and
   Set-Cookie, which carry state information between participating
   origin servers and user agents.

就是它用cookie来管理一个有状态的会话。

**所以在一个httpclient线程访问登录接口，因为在response header中有set-cookie，它将这个cookie当做一个会话保留了下来。  
然后线程并没有销毁被其他请求复用，被理解为还是同一个会话，则外部传入的header并没有被应用上。**

### 修复

修复十分方便，只要将这个cookie策略改为IGNORE_COOKIES即可
```java
httpClient.getParams().setCookiePolicy(CookiePolicy.IGNORE_COOKIES);
```

## 一句话

最致命的问题总在就在你觉得不可能有问题的地方。