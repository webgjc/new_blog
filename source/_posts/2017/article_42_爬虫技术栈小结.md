
---
title: 爬虫技术栈小结
catalog: true
date: 2017-11-5 16:41:51
---

做了接近一个月爬虫，中间爬到数据多的爬过唯品会，dpchallenge，frilly。百度图片和1688也是取了一部分数据来。这里做一些爬虫技术总结记录，包括基本的requests使用，json，bs4，OrderedDict，下载图片，多进程以及post一个数组。<!--more-->

首先，基本的爬虫以唯品会（这里以女装做示范），主要用以接口获取json数据，json解析，json格式化。

首先获取一下他的分类列表，由于返回的是callback里的函数，便去掉前后一些字符然后json格式化。
<pre>req=requests.Session()
cateurl='https://category.vip.com/ajax/getCategory.php?callback=getCategory&amp;tree_id=117'
pplist=req.get(cateurl).text
ppjson=json.loads(pplist[12:-1])
pparr=ppjson['data'][0]['children'][0]['children']</pre>
之后访问分类的具体页面，用一点正则到他的js里解析出productIds，解析json，然后再通过里面的每个productid的拼接构成一个url，获取到商品服装信息（这里可得缩略图）。再进入服装详情页，得到商品大图。
<pre>for item in pparr:
    searchurl='https://category.vip.com/'+item['url']
        sec1=req.get(searchurl
        jsonpic=re.findall(r'"productIds":(.*?),"',sec1.text)
        piclist=json.loads(jsonpic[0])
        for n in range(2):
            productIds='%2C'.join(map(str,piclist[50*n:(n+1)*50]))
            resp=req.get('https://category.vip.com/ajax/mapi.php?service=product_info&amp;productIds='+productIds+'&amp;warehouse=VIP_SH')
            projson=json.loads(resp.text)
            if cate &gt; -5:
                for j in projson['data']['products']:
                    detail=req.get('https://detail.vip.com/detail-'+str(j['brandId'])+'-'+str(j['productId'])+'.html?f=ad')
                    match=re.findall(r'&lt;a href="(.*?)" class="J-mer-bigImgZoom"&gt;',detail.text)
                    for url in match:
                        print(url)</pre>
插一个从网页下载图片到本地的小技巧
<pre>img=req.get(imageurl).content
with open('test.jpg','wb') as f:
    f.write(img)
    f.close()</pre>
dpchallenge.com，这是个摄影网站，除了爬图片还得爬摄影信息及评论，主要靠beautifulsoup和正则解析html文本。

这里先爬了信息，其中也包括图片地址。之后在把所有图下载下来。

这里做一部分beautifulsoup的记录
<pre>soup=BeautifulSoup(response.text,"lxml")
source_url=soup.find_all('标签',{'属性':'值(写True则代表有这个属性)'</pre>
另一个这里要注意的便是OrderedDict，由于python的object读取显示出来时会乱序或者并不是按写入的顺序显示的。所以需要用OrderedDict作代替
<pre>from collections import OrderedDict
test=OrderedDict()
test["c"]="1"
test["b"]="2"
test["a"]="3"
print(test)</pre>
最后这里在做一下爬虫期间所用的多进程的简单使用，这里用到了进程池以及进程锁：
<pre>from multiprocessing import Pool,Manager
def func(n,lock):
    with lock:
        print(n)
if __name__=="__main__":
    pool=Pool()
    lock=Manager().Lock()
    for i in range(10):
        pool.apply_async(func, (i,lock))#这边也可以加回调
    pool.close()
    pool.join()</pre>
最后考虑一个post时发现的问题，也是平常可能会忽略而出错的。

http://test.ganjiacheng.cn/testspider/test.php是一个返回post数据的接口

在js的jquery的ajax里，
<pre>$.post("./test.php",{du:"0",data:["1","2","3"]},function(data){
    console.log(data)
})
//结果：{"du":"0","data":["1","2","3"]}</pre>
而在python里
<pre>import requests
import json
post_data={
    "du":"0",
    "data":["1","2","3"],
}
res=requests.post('http://test.ganjiacheng.cn/testspider/test.php',data=post_data)
print(res.json())
#结果：{'du': '0', 'data': '3'}</pre>
也便是数组形式如[]在post传输过程是不能保持的，上面的post_data传输的信息形式应该如du=0&amp;data%5B%5D=1&amp;data%5B%5D=2&amp;data%5B%5D=3。

后来用了拼接的方法来解决这个问题。

有待提升的地方，在有较多js操作及判断的网页中，要爬到对应信息需进行复刻同样的js操作，首先要读懂js，再来要自己实现一遍，对于综合能力要求还是比较高的。对于1688这种检测到爬虫的一些行为后会需要你登录后进行操作，虽然登录后通过chrome拿到cookie是可以使用的，但可能会有时限等限制。还有待探索！
