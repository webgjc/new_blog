
---
title: 搭建wordpress个人博客
catalog: true
date: 2017-3-6 18:29:52
---

试着写blog啦，用以分享，记录技术和生活！

本人年方21，前端起家，在向后端的php和python前进。

本次就从安装wordpress说起：<!--more-->

注：环境：云服务器+lnmp+域名。

1.先从官网<a href="https://cn.wordpress.org/releases/">https://cn.wordpress.org/releases/</a>找了最新版本4.7.2，之后解压，复制到服务器上，打开对应域名+路径就有了。

2.在配置mysql数据库，用户名和密码。就可以生成啦！！！

3.进入也是被惊艳了，上手很快。
<p style="text-align: left;">4.本来升级需要ftp，弄不明白就找了在wp-config.php最后插入了这些代码，之后跳过了输入ftp</p>

<pre style="text-align: left;"><strong>define("FS_METHOD","direct");</strong>
<strong>define("FS_CHMOD_DIR", 0777);</strong>
<strong>define("FS_CHMOD_FILE", 0777);</strong></pre>
遇到问题：在升级翻译的时候会有------无法复制文件的错误。

在升级Akismet插件的时候会出现错误-----因为我们不能复制一些文件，升级未被安装。这通常是因为存在不一致的文件权限。
