
---
title: 解决各种问题集
catalog: true
date: 2017-11-30 17:45:55
---

python篇：

1.windows上，在pip install xxx失败的时候怎么办？

答：<a href="http://www.lfd.uci.edu/~gohlke/pythonlibs/">http://www.lfd.uci.edu/~gohlke/pythonlibs/</a>到这里面寻找whl，下载之后用 pip install xxx.whl 来安装。

<!--more-->

2.解决pip3报错Fatal error in launcher: Unable to create process using '"'。

一种：
<pre>import pip
pip.main(['install','ModuleName'])</pre>
另一种：
<pre class="lang-py prettyprint prettyprinted"><code><span class="pln">python3 </span><span class="pun">-</span><span class="pln">m pip install whlName
</span></code></pre>
3.linux上python3中文会显示UnicodeEncodeError: 'ascii' codec can't encode character。
<pre>import io 
import sys 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')</pre>
4.requests爬到的中文网页输出在windows cmd会出错
<pre>res=requests.get(url)
res.encoding='gbk'
print(res.text)</pre>
5.cv2.imread读取中文路径出错
<pre>#读取
im = cv2.imdecode(np.fromfile(file,dtype=np.uint8),-1)
#写入
cv2.imencode('.jpg',res)[1].tofile(file)</pre>
6.sublime字体高低不齐

下载安装字体 http://cloud.alphadn.com/blog/yahei-consolas.zip
修改user_setting中的font_face为
<pre>"font_face": "YaHei Consolas Hybrid",</pre>
7.windows上编写的shell文件在linux运行报错
<pre>vim file.sh
:set ff=unix</pre>
