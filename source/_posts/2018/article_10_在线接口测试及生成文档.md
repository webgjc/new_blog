
---
title: 在线接口测试及生成文档
catalog: true
date: 2018-3-14 17:31:20
---

由于每次更改后端接口都要经过测试，然后又要去修改接口文档，就想着能不能整合这两步，为了自己能灵活修改，便自己来写个。

<a href="https://github.com/webgjc/ApiTestToMd">https://github.com/webgjc/ApiTestToMd</a><!--more-->

这次的代码有点多，就不直接展示了，放在github上，也可方便下载使用。

&nbsp;

写写思路及主要用到的工具：

后端使用flask框架，requests作为接口测试，增加了百度翻译api作为参数翻译，另外写了一些文件的接口。

前端使用bootstrap4作为测试接口页面的主要ui。测试记录存在sessionStorage里，只是刷新标签并不会使记消失。

前端接口文档编辑主要从sessionStorage获取到记录，用固定格式产生md文本，参数使用百度api翻译一下，再用了marked.js把md转成html文件，md和html分居左右也可以边改边看效果。

之后又增加了文件保存读取的效果，可以复用上次改下的接口文档。

html的效果就是css，借鉴于<a href="http://coolaf.com/tool/md">http://coolaf.com/tool/md</a>

就这么多功能，前前后后改了一星期左右，没有很多难点，但有些细节也是实际用了才发现去改，可能功能还能完善，差不多作为一个日常小工具也足够啦。
