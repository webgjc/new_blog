
---
title: php实现Soap调用的两种方法
catalog: true
date: 2017-3-20 00:02:31
---

php也可以通过soap（一种基于xml的协议）和webservice进行数据交互。

这里通过两种方法来讲解，一个是php的SoapClient对象，另一个是php的curl。

<!--more-->

第一种：先要做一件事就是在php.ini中把soap扩展开了。
<pre>extension=php_soap.dll</pre>
然后进行php代码的编写，这里直接讲解带有header验证的soap。没有header验证的话就不需要加设置header那几行。先查看所需的xml，这里用soap12举个栗子，关注下面xml中header和body部分。
<pre>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;soap12:Envelope 
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
  xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"&gt;
  &lt;soap12:Header&gt;
    &lt;HeaderName xxx="url"&gt;
      &lt;username&gt;<span class="value">int</span>&lt;/username&gt;
      &lt;password&gt;<span class="value">string</span>&lt;/password&gt;
    &lt;/HeaderName&gt;
  &lt;/soap12:Header&gt;
  &lt;soap12:Body&gt;
    &lt;FuncName xxx="url"&gt;
       &lt;neededData&gt;data&lt;/neededData&gt;
    &lt;/FuncName&gt;
  &lt;/soap12:Body&gt;
&lt;/soap12:Envelope&gt;</pre>
<pre>&lt;?php
//wsdl地址
$url="wsdl地址";
//出现类似于<span class="pln">SOAP</span><span class="pun">-</span><span class="pln">ERROR</span><span class="pun">:</span> <span class="typ">Parsing</span><span class="pln"> WSDL</span><span class="pun">:</span> <span class="typ">Couldn</span><span class="str">'t load from的错误时加上下面这行</span>
libxml_disable_entity_loader(false);
//调用SoapClient对象
$client=new SoapClient($url);
//查看里面的函数数组
print_r($client-&gt;__getFunctions());
//构造header
$header = new SoapHeader('上面xml里的url','HeaderName',array('username'=&gt;xxx,'password'=&gt;xxx),true);
//设置header
$client-&gt;__setSoapHeaders($header);
//调用FuncName并传入数据
$return = $client-&gt;FuncName(array('neededData'=&gt;xxx));
print_r($return);</pre>
第二种：用php的curl获取数据，之后解析xml，具体来看代码吧
<pre>&lt;?php
//用curl带着post包和header去获取数据
function getData($soap_request){
      //构造头信息，和第一种方法的header不一样，具体查看webservice说明。
      $header = array(
          "Content-type: application/soap+xml; charset=utf-8",
          "Host: xxx.xxx.xxx.xxx",
          "Content-length: ".strlen($soap_request),
        );
      $soap_do = curl_init();
      curl_setopt($soap_do, CURLOPT_URL, "wsdl地址");
      curl_setopt($soap_do, CURLOPT_RETURNTRANSFER, true );
      curl_setopt($soap_do, CURLOPT_POST,           true );
      curl_setopt($soap_do, CURLOPT_POSTFIELDS,     $soap_request);
      curl_setopt($soap_do, CURLOPT_HTTPHEADER,     $header);
      $data = curl_exec($soap_do);
      return $data;
}
//处理得到的xml数据
function handData($result,$parentNode,$childNode){
      $xml=simplexml_load_string($result);
      $result = $xml-&gt;children('http://www.w3.org/2003/05/soap-envelope')
        -&gt;children('url')
        -&gt;$parentNode
        -&gt;$childNode;
      return $result;
}
//使用方法
//下面是上面xml的字符形式，将需要传入的数据直接写成标签到xml字符里
$soap_request = "&lt;?xml version......";
$return = $this-&gt;getData($soap_request);
//后面两个参数为返回xml的body内的两个标签名
$result = $this-&gt;handData($return,FuncName,returnData);</pre>
总结：一般来说会选择上一种，也可以先根据自己的情况来选择一种理解。毕竟具体问题具体分析，这边不能做到全部问题都概括，所以有多个解法总比唯一解好！

&nbsp;

&nbsp;
