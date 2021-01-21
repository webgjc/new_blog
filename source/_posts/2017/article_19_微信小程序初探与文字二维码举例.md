
---
title: 微信小程序初探与文字二维码举例
catalog: true
date: 2017-4-7 11:33:34
---

最近，微信小程序开放了个人开发者，所以立刻申请了一个来试试。

小程序从之前刚出来时在开发者圈火极一时，而现在却用的不多，也有限制多的缘故，所以在开放了部分限制之后再来看他的发展吧。<!--more-->

这里讨论一下初探小程序的一点想法。

在<a href="https://mp.weixin.qq.com/debug/wxadoc/dev/">小程序手册</a>中也已经很明白了，把视图和逻辑分开，有点类似于react的虚拟dom，不直接去操作dom，而是改变数据之后自动刷新页面的渲染，使改动最小化。最初的试验感觉他的数据应该是单向绑定，也就是m-v而没有v-m。

另外，微信写了各种接近微信ui的组件供直接调用。html代替用的是wxml，这个可以看手册了解。关于css，他用的是wxss，wxss基本和css是相同的。js的话就是变化最大的地方，因为完全dom没有关系，直接操作数据就可以改变页面内容。所以在了解之后其实开发速度是很快的。

使用过后的感觉便是比起一般的网页流畅一些，但相较于app可能还有距离。

开发的话，先在微信公众平台新注册一个，选择小程序。下载开发者工具，再本地新建一个空文件夹，之后添加项目到这里面，就会自动创建一个示例demo。

这里简单做一个文字二维码的功能的小程序。

wxml部分基本直接用组件就行 ，然后绑定一下事件，如bindtap，{ {} }是从js里传入的数据。
<pre>&lt;!--index.wxml--&gt;
&lt;view class="container"&gt;
  &lt;form bindsubmit="formSubmit"&gt;
    &lt;view class="section"&gt;
      &lt;input placeholder="请输入想说的话" auto-focus name="input"/&gt;
    &lt;/view&gt;
    &lt;view class='btn'&gt;
      &lt;button formType="submit"&gt;提交&lt;/button&gt;
    &lt;/view&gt;
  &lt;/form&gt;
  &lt;view class="img"&gt;
    &lt;image src="{ {imgurl} }" bindtap="ch"&gt;&lt;/image&gt;
  &lt;/view&gt;
&lt;/view&gt;</pre>
wxss因为和css基本一样就不写太多了，而且ui的话很多组件已经做好了。
<pre>/**index.wxss**/
.btn{
  margin-top: 10%;
}
.section{
  border-bottom:solid 1px lightgrey;
  font-size:50rpx;
}</pre>
js里，getApp()从app.js和app.json获取配置信息，data便是可以传入wxml里的数据下面是两个事件，一开始的话会自动创建几个默认事件---开始加载，加载完成等等。然后可以自己添加事件。wx.xxx就是调用接口，接口具体也可以看文档。wx.request是获取服务器数据，这里首先需要到微信公众平台--设置里配置一下服务器域名，否则会报错。写多了容易发现有各种回调，所以要很清晰每一步。
<pre>//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    imgult:'',
    imgfile:''
  },
  ch:function(e){
    var that=this
    if(that.data.imgfile==''){
      return
    }
    wx.previewImage({
      current: that.data.imgfile,
      urls: [that.data.imgfile] 
    })
  },
  formSubmit: function(e) {
    var that = this
    wx.request({
      url: 'https://xxx.cn/test.php',
      data: {
        data: e.detail.value.input ,
      },
      header: {
          'content-type': 'application/json'
      },
      success: function(res) {
        that.setData({
          imgurl:res.data
        }),
        wx.downloadFile({
          url: 'https://xxx.cn/EXAMPLE_TMP_SERVERPATHtest.png',
          success: function(res) {
            var tempFilePaths = res.tempFilePath
            that.setData({     
              imgfile:res.tempFilePath
            })
            console.log(that.data.imgfile)
          }
        })
      }
    })
  },
})</pre>
服务器端用了<a href="http://phpqrcode.sourceforge.net/">phpqrcode</a>来生成二维码。下面是参考代码。效果：如果是数字便生成添加联系人的二维码，如果是文字，就产生文字二维码。然后通过base64编码到返回，小程序获取到64编码的图片字符放到img中就可以直接展示。
<pre>&lt;?php
include('phpqrcode/qrlib.php');
include('config.php'); 
$tempDir = EXAMPLE_TMP_SERVERPATH; 
$a=$_GET['data'];
if(!is_numeric($a)){
    QRcode::png($a,$tempDir.'test.png',QR_ECLEVEL_L, 10);
    $str = file_get_contents($tempDir.'test.png');
    echo "data:image/png;base64,".base64_encode($str);
}else{
    $name = ''; 
    $phone = $a;
    $codeContents  = 'BEGIN:VCARD'."\n"; 
    $codeContents .= 'FN:'.$name."\n"; 
    $codeContents .= 'TEL;WORK;VOICE:'.$phone."\n"; 
    $codeContents .= 'END:VCARD'; 
    QRcode::png($codeContents, $tempDir.'test.png', QR_ECLEVEL_L, 10); 
    $str = file_get_contents($tempDir.'test.png');
    echo "data:image/png;base64,".base64_encode($str);
}</pre>
效果展示：<a href="/img/uploads/2017/04/QQ截图20170407112928.jpg"><img class="alignnone wp-image-239 size-thumbnail" src="/img/uploads/2017/04/QQ截图20170407112928-150x150.jpg" alt="" width="150" height="150" /></a>
