
---
title: nginx+php下配置https
catalog: true
date: 2017-3-30 22:10:50
---

本来以为配置https应该和配置http是差不多的，没想到还是出了许多问题，分享给大家。

现在市面有许多免费的ssl证书，可以找一个，本人使用了<a href="https://www.qcloud.com/product/ssl">腾讯云的免费dv证书</a>。<!--more-->

之后就会得到两个文件，分别为test.com_bundle.crt和test.com.key

本人配置的环境是在centos，php集成环境lnmp下

先在服务器找到文件usr/local/nginx/conf/nginx.conf

之后把上述两个文件放到同一目录下，在原本的server listen 80下面新开一个server listen 443，代码如下
<pre>server {
        listen 443;
        server_name test.com; #填写绑定证书的域名
        ssl on;
        ssl_certificate test.com_bundle.crt;
        ssl_certificate_key test.com.key;
        ssl_session_timeout 5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2; #按照这个协议配置
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;#按照这个套件配置
        ssl_prefer_server_ciphers on;
        location / {
            root   /home/wwwroot/default;
            index  index.html index.htm index.php;
        }
        location ~ [^/]\.php(/|$)
            {
                #这个root必须加上.
                root   /home/wwwroot/default;
                # comment try_files $uri =404; to enable pathinfo
                try_files $uri =404;
                fastcgi_pass  unix:/tmp/php-cgi.sock;
                fastcgi_index index.php;
                include fastcgi.conf;
                #include pathinfo.conf;
                #开启https
                include fastcgi_params;
                fastcgi_param HTTPS on;
            }
    }</pre>
之后如果想要把http的都转到https去，可以在server listen 80里面location最上面加如下一段
<pre>location / {
                rewrite ^(.*) https://$host$1 permanent;
        }</pre>
之后需要远程连接服务器到命令行输入
<pre>nginx -s reload</pre>
最后打开浏览器访问看看效果
