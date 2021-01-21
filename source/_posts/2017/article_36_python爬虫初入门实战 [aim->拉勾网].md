
---
title: python爬虫初入门实战 [aim->拉勾网]
catalog: true
date: 2017-7-31 20:12:28
---

作为pythoner爬虫还是必备技能之一，说上手就上手。

入门选了个拉勾网（莫名躺枪，下手轻点）。<!--more-->

这次具体来讲一下爬网页走过的流程。

先在chrome打开拉勾网主页，打开开发者工具network项，点每个资源就知道他的request和reponse。主页他是直接返回的内容，所以直接去爬主页，三行搞定。
<pre>import requests
req=requests.get("https://www.lagou.com/")
print(req.text)</pre>
然后继续看具体的内容页，这里以杭州为例，网址是https://www.lagou.com/jobs/list_?px=new&amp;city=%E6%9D%AD%E5%B7%9E#filterBox

以同样的方式爬内容页，会发现内容页只有外标签而没有内容。

看console便会发现有ajax的痕迹，仔细看network便会发现几个json文件，通过看他的request和reponse便会知道数据是在某个json的链接里拿到的。链接为https://www.lagou.com/jobs/positionAjax.json?px=new&amp;city=%E6%9D%AD%E5%B7%9E&amp;needAddtionalResult=false

直接爬这个链接，会发现返回错误信息，应该还有点防护措施。

所以我们把自己伪装的和浏览器更像。构造一个request头
<pre>import requests
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_?px=new&amp;city=%\E6%\9D%\AD%\E5%\B7%\9E',
    'Accept-Encoding': 'gzip, deflate, br',
}
req=requests.post("https://www.lagou.com/jobs/positionAjax.json?px=new&amp;needAddtionalResult=false",params={"city":"杭州"},headers=header)
print(req.content)</pre>
然后能爬取到一页的数据，在进一步直接爬30页，就会发现有每分钟的每个IP5次的次数限制。ip限制就用代理呗，只要在requests里面加一个proxies的参数即可，不过好的代理确实难找，<a href="http://www.gatherproxy.com/zh/">这里的还算可以</a>。

代理要加进去的话，得先爬代理网站，然后才能时时获取最新的代理并处理。
<pre>req=requests.post(url,proxies={"https":"000.000.000.000:00","http":"000.000.000.000:00"},headers=headers,params={'city':'杭州','pn':str(page)})</pre>
因为上面那个代理网站要翻墙，这里用另一个代理网站做测试。爬到网页后用beautifulSoup4来处理html代码。
<pre>#coding:utf-8
import requests
from bs4 import BeautifulSoup

def getProxyList():
    res=[]
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    response=requests.get("http://www.xicidaili.com/nn/",headers=header)
    soup=BeautifulSoup(response.text,'html.parser')
    li=soup.find_all('tr',{'class':'odd'})
    for item in li:
        res.append(item.contents[3].string+":"+item.contents[5].string)
        itemNext=item.next_sibling.next_sibling
        res.append(itemNext.contents[3].string+":"+itemNext.contents[5].string)
    return res</pre>
爬到拉勾网的内容后得处理丫。因为是json格式，直接用json处理，下面是处理的代码：
<pre>import requests
import json
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_?px=new&amp;city=%\E6%\9D%\AD%\E5%\B7%\9E',
    'Accept-Encoding': 'gzip, deflate, br',
}
req=requests.get("https://www.lagou.com/jobs/positionAjax.json?px=new&amp;needAddtionalResult=false",params={"city":"杭州"},headers=header)
data=json.loads(req.text)
for i in data['content']['positionResult']['result']:
    print(i['positionName'],i['salary'],i['workYear'],i['jobNature'],i['companyFullName'],i['companySize'],i['district'],i['createTime'])</pre>
总结：一般的套路也就是看chrome控制台，把request和reponse弄清楚，有时候还得看他的js代码，有时候html里也会隐藏一些信息，反正无所不用。

爬网页与反爬虫总是矛和盾，作为一个写网页又爬网页的，应该能更加清楚一些套路，而在写网页的时候阻挡一些简单的爬虫入侵。
