
---
title: 用google的GAE部署kindle的自动推送
catalog: true
date: 2017-10-8 09:24:01
---

偶然在github看到一个<a href="https://github.com/cdhigh/kindleear/">kindleear</a>，发现可以在google的gea配置推送到kindle，便来试试，这里记下最简单的几步操作。<!--more-->

具体可以参考网页---<a href="https://bookfere.com/post/19.html">https://bookfere.com/post/19.html</a>

首先，到google的<a href="https://console.developers.google.com/project?hl=zh-cn">https://console.developers.google.com/project?hl=zh-cn</a>创建一个新项目。

之后在<a href="https://console.cloud.google.com/">https://console.cloud.google.com/</a>这里便可以看到已创建的项目（或者选择到已创建的项目）。

在点击右上角 &gt;_ 这个按钮打开云端shell命令行。运行下面命令
<pre class=" language-bash"><code class=" language-bash">gcloud beta app create</code></pre>
完成后，在运行下面命令
<pre class=" language-bash"><code class=" language-bash"><span class="token function">rm</span> -f uploader.sh* <span class="token operator">&amp;&amp;</span> \
<span class="token function">wget</span> https://raw.githubusercontent.com/kindlefere/KindleEar-Uploader/master/uploader.sh <span class="token operator">&amp;&amp;</span> \
<span class="token function">chmod</span> +x uploader.sh <span class="token operator">&amp;&amp;</span> \
./uploader.sh</code></pre>
输入你的 Gmail 地址和已有的项目ID，就完成了创建。

完成后打开https://项目ID.appspot.com/ 就可以访问到配置界面

用admin，admin登录，里面进行kindle以及订阅的一些设置。（可以选择每日自动推送）

<strong>注：</strong>登录不了或者订阅打不开的话喝杯咖啡等一会儿就会好。

<strong>以下两步必做</strong>

<strong>注：要在亚马逊设备---kindle---设置---已认可的发件人电子邮箱列表，把刚刚的gmail加进去</strong>

<strong>注：发送出现wrong SRC_EMAIL错误，点项目主页的左上角菜单---App引擎---设置---Email API 已获授权的发件人，添加自己的gmail即可</strong>

具体效果：

<img class="alignnone size-medium wp-image-415" src="/img/uploads/2017/10/IMG_3516-225x300.jpg" alt="" width="225" height="300" /><img class="alignnone size-medium wp-image-414" src="/img/uploads/2017/10/IMG_3517-225x300.jpg" alt="" width="225" height="300" />
