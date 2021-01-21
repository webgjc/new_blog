
---
title: php实现RSA加密
catalog: true
date: 2017-7-14 11:49:45
---

RSA加密具体细节这里就不说了可以自行搜索。这里做php实现的例子。

思路：在服务器端php先产生一个公钥给js用于加密，同时产生一个私钥用于解密并保存在session中，js获取用户输入并用公钥加密，然后将加密的字符串提交到后端，后端php用私钥解密后得到实际用户输入。<!--more-->

这里主要安全的一点就是信息传输过程中始终是加密后的字符串，即使被抓包也无法得到实际用户输入。

首先下载用于rsa加密的一些文件，<a href="http://pan.baidu.com/s/1o84ZXDw">点击这里下载</a>。

将这个文件夹与下面的php文件放在服务器中的同目录。

下面编写文件file1.php
<pre>&lt;?php
//产生公钥与私钥
@session_start();
set_include_path('rsa/classes/phpseclib/');
include_once('Crypt/RSA.php');
$rsa = new Crypt_RSA();
$rsa-&gt;setPrivateKeyFormat(CRYPT_RSA_PRIVATE_FORMAT_PKCS1);
$rsa-&gt;setPublicKeyFormat(CRYPT_RSA_PUBLIC_FORMAT_RAW);
$key = $rsa-&gt;createKey(1024);
$privatekey = $key['privatekey'];
$_SESSION['privatekey'] = $privatekey;
$publickey = $key['publickey']['n']-&gt;toHex();
?&gt;
&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;test&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;input type="text" placeholder="要加密字符串" id="str"&gt;
    &lt;button id="sub"&gt;submit&lt;/button&gt;
    &lt;div id="encrypted"&gt;&lt;/div&gt;
    &lt;div id="decrypted"&gt;&lt;/div&gt;
    &lt;script src="//cdn.bootcss.com/jquery/3.1.0/jquery.min.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="rsa/jsbn/jsbn.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="rsa/jsbn/prng4.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="rsa/jsbn/rng.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" src="rsa/jsbn/rsa.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript"&gt;
    //js获得公钥进行加密
    var publickey = "&lt;?=$publickey?&gt;";
    var rsakey = new RSAKey();
    rsakey.setPublic(publickey, "10001");
    $("#sub").click(function(){
        var enc = rsakey.encrypt($("#str").val());
        $('#encrypted').html("加密后\n"+enc);
        $.post('file2.php', {enc: enc}, function(data) {
            $('#decrypted').html("解密后\n"+data);
        });
    });
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
下面是file2.php
<pre>&lt;?php
//获取私钥与加密后字符串进行解密
@session_start();
set_include_path('rsa/classes/phpseclib/');
include_once('Crypt/RSA.php');
$encrypted = $_POST['enc'];
$rsa = new Crypt_RSA();
$encrypted=pack('H*', $encrypted);
$rsa-&gt;loadKey($_SESSION['privatekey']);
$rsa-&gt;setEncryptionMode(CRYPT_RSA_ENCRYPTION_PKCS1);
$decrypted = $rsa-&gt;decrypt($encrypted);
echo $decrypted;</pre>
效果展示：

<img class="alignnone size-medium wp-image-323" src="/img/uploads/2017/07/QQ截图20170714114735-300x93.jpg" alt="" width="300" height="93" />

完成rsa加密咯，目前还算比较安全的一种加密，可以在一些比较重要的信息传递中使用。
