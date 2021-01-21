
---
title: 爬进数字杭电python篇
catalog: true
date: 2017-9-6 10:43:27
---

上次有的<a href="https://ganjiacheng.cn/blog/?p=63">php篇数字杭电模拟登陆</a>，不过由于如今没有了验证码，可能会出点小错误，因此用python再来进进出出一遍。

此次主要还是熟悉一下python requests的使用以及对网站cookie变化的准确捕捉。post的参数以及header也是这里的重点部分，其他还能加点简单的正则。<!--more-->

具体细节在代码注释里：
<pre>import requests
import re

#先访问一次登录网站得到lt（lt后面必须，且一次性使用）
def getHduCookie():
    resp=requests.get('http://cas.hdu.edu.cn/cas/login')
    m = re.search(r'name=\"lt\" value=(.*?) /&gt;', resp.text)
    lt=m.group()[17:-4]
    return lt

#模拟登陆用户名为学号，密码为md5加密后的密码，返回跳转链接
def simLogin(lt):
    password=hashlib.md5(psd.encode('utf-8')).hexdigest()
    params={
        'encodedService':'http%3a%2f%2fi.hdu.edu.cn%2fdcp%2findex.jsp',
        'service':'http://i.hdu.edu.cn/dcp/index.jsp',
        'username':xh,
        'password':password,
        'lt':lt
    }
    resp=requests.post('http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/index.aspx',params=params)
    m=re.search(r'href="(.*?)"',resp.text)
    return m.group()[6:-1]

#去临时链接获取一次cookie并保存请求
def jxglPage(url):
    req=requests.Session()
    resp0=req.get(url)
    req.headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer':'http://jxgl.hdu.edu.cn/xf_xsqxxxk.aspx?xh='+xh+'&amp;xm=%25%5cB8%25%5cCA%25%5cBC%25%5cD2%25%5cB3%25%5cC7&amp;gnmkdm=N121113',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type':'application/x-www-form-urlencoded',
    }
    return req

#这里的例子是获取选课列表
def classList(req):
    data=''#这里是post的一大串字符，可从浏览器获取
    url='http://jxgl.hdu.edu.cn/xf_xsqxxxk.aspx?xh='+xh+'&amp;xm=%25%5cB8%25%5cCA%25%5cBC%25%5cD2%25%5cB3%25%5cC7&amp;gnmkdm=N121113'
    resp=req.post(url,data=data)
    resp.encoding='gbk'
    print(resp.text)

#主程序，设置学号密码并运行
if __name__=='__main__':
    xh='学号'
    psd='密码'
    lt=getHduCookie()
    tmpurl=simLogin(lt)
    req=jxglPage(tmpurl)
    classList(req)</pre>
学习为主，连我都不信。

温馨提醒：此片不要与<a href="https://ganjiacheng.cn/blog/?p=368">hack验证二维码篇</a>结合搞事情啦！
