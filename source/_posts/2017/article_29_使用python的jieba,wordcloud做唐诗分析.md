
---
title: 使用python的jieba,wordcloud做唐诗分析
catalog: true
date: 2017-7-13 09:56:37
---

首先安装好python3.x以及jieba,wordcloud库,这是前提。

然后搜罗了一份唐诗的txt文档，<a href="/img/uploads/2017/07/poetry.txt">具体看这里</a>。

思路：先用<a href="https://github.com/fxsjy/jieba">jieba</a>把每首诗标题去掉，提取出正文。再jiaba.cut做分词，分完的词保存下来，再用worcloud作词云，具体可以看<a href="http://amueller.github.io/word_cloud/index.html">wordcloud文档</a>。<!--more-->

具体代码：
<pre>#coding:utf-8
#python3.5
#引入库文件
from wordcloud import WordCloud
import jieba
ss=""
f=open('poetry.txt',encoding='utf-8')
#读取每首诗并去掉标题
#进行分词并存储
for i in f.readlines():
    l=i[i.find(':')+1:-1]
    s=jieba.cut(l,cut_all=False)
    for j in s:
        if j==':' or j=='，' or j=='。':
            continue
        else:
            ss+=j+" "
#引入中文字体文件
font="C:/Windows/Fonts/simfang.ttf"
#构建词云并保存
#如需展示的话可以用matplotlib，具体可以看wordcloud文档
word=WordCloud(width=4000,height=2000,font_path=font,max_words=2000,max_font_size=500).generate(ss)
word.to_file('filename.png')</pre>
效果展示：

<a href="/img/uploads/2017/07/xxn.png"><img class="alignnone wp-image-319 size-large" src="/img/uploads/2017/07/xxn-1024x512.png" alt="" width="525" height="263" /></a>

&nbsp;
