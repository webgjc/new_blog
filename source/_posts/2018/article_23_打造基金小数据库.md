
---
title: 打造基金小数据库
catalog: true
date: 2018-6-30 16:32:13
---

买过些基金，想着也可以自己打造个管理基金的，这会儿先弄来个基金数据库。<!--more-->

基金数据来自于chinafund。

先前准备：配置好mongodb的环境和下载好pymongo库且使用默认配置

用于获取数据：jj.py
<pre>#coding:utf-8
#author:~!@#$%^&amp;*()_+ganster
import io 
import re
import sys 
import json
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
req = requests.Session()
today = datetime.datetime.today().strftime("%Y-%m-%d")

#获取单个基金历史净值
#只能用于开放基金
#返回数据dataframe
def get_jjjz(code,start="2018-01-01",end=today):
    data = {
        "startdate": start,
        "enddate": today,
        "code": code
    }
    resp = req.post("http://info.chinafund.cn/fund/"+code+"/jjjz/",data=data)
    htmlstr = resp.text
    print(htmlstr,file=open("test.html","w",encoding="utf-8"))
    arrstr = re.findall(r"fundlsjz = (.*);",htmlstr)[0].replace("\'","\"")
    jsondata = json.loads(arrstr)
    data = pd.DataFrame(jsondata,columns=["date","dwjz","ljjz"])
    return data

#代码 简称 分类 单位净值 累计净值 日增值 日增长 周增 月增 季增 半年增 年增
#获取当日所有基金净值,月增长等
#返回数据dataframe,日期string
def get_day_info():
    htmlstr = req.get("http://data.chinafund.cn/?WebShieldDRSessionVerify=b1U3PfdG5OPHxthA5c4k")
    htmlstr.encoding="gbk"
    #保存html
    #print(htmlstr.text,file=open("test.html","w",encoding="utf-8"))
    soup = BeautifulSoup(htmlstr.text,"lxml")
    date = soup.title.get_text()[10:20]
    node = soup.find_all("table",{"id":"tablesorter"})[0]
    trnode = node.find_all("tr")
    data = []
    for i in range(1,len(trnode)):
        tdnodes = trnode[i].find_all("td")
        tmp = [tdnodes[2].get_text(),tdnodes[3].get_text(),tdnodes[4].img["src"][-5],tdnodes[5].get_text(),tdnodes[6].get_text(),tdnodes[7].get_text(),tdnodes[8].get_text(),tdnodes[9].get_text(),tdnodes[10].get_text(),tdnodes[11].get_text(),tdnodes[12].get_text(),tdnodes[13].get_text()]
        data.append(tmp)
    res = pd.DataFrame(data,columns=["code","name","cate","dwjz","ljjz","rzzhi","rzzha","zhz","yz","jz","bnz","nz"])
    return res,date

#获取开放基金列表
#jj_list.csv为上面获取的当日基金code列
#注：当日基金中为全部基金，开放基金只有一部分。
def get_jj_list():
    return pd.read_csv("jj_list1.csv",index_col=0)
    #make jj_list
    '''
    res = []
    jj_list = pd.read_csv("jj_list.csv")
    resp = req.get("http://info.chinafund.cn/")
    resp.encoding="gbk"
    soup = BeautifulSoup(resp.text,"lxml")
    for n in range(1,24):
        divnode = soup.find_all("div",{"id":"kfjj_"+str(n)})[0]
        trnodes = divnode.find_all("tr")
        for i in range(1,len(trnodes)):
            tdnodes = trnodes[i].find_all("td")
            tmp = [tdnodes[0].get_text(),tdnodes[1].get_text()]
            try:
                tmp.append(int(jj_list[jj_list["code"]==int(tmp[0])]["cate"].values[0]))
            except:
                tmp.append(0)
            res.append(tmp)
    data = pd.DataFrame(res,columns=["code","name","cate"])
    '''

#保存为csv格式
def save_csv(data,filename="nofilename"):
    data.to_csv(filename+".csv",encoding='utf_8_sig')

#计算关注基金涨跌幅
#返回list
def jj_zdf(code,start):
    tmp = get_jjjz(code,start=start)
    dwjz = tmp["dwjz"]
    first = dwjz[len(tmp)-1]
    zdf = ((dwjz-first)/first).tolist()[::-1]
    return zdf

#计算关注股票的涨跌幅
#返回字典，key为基金code
def jj_follow_zdf(follow):
    zdfs = {}
    for jj in follow:
        print(jj[0])
        try:
            zdfs[jj[0]] = jj_zdf(jj[0],jj[1])
        except:
            print("error:"+jj[0])
        time.sleep(10)
    return zdfs

#以类别筛选基金
#1-股票型，2-指数型，3-混合型，4-债券型，5-QDII
def jj_select_cate(category="2"):
    jj_list,_ = get_day_info()
    return jj_list[jj_list['cate']==category]

#筛选指数型基金并获取一个月涨跌幅
def jj_test():
    jjs = jj_select_cate(2)
    follow = []
    for i in jjs["code"]:
        follow.append([str(i).zfill(6),"2018-05-07"])
    print(json.dump(jj_follow_zdf(follow),open("test.json","w")))</pre>
用于数据库插入：jjdb.py
<pre>from pymongo import MongoClient
import datetime
import jj

client = MongoClient()
DB = client.jj

#检查时间是否今天（今天是否是交易日）
def check_time(date):
    today = datetime.date.today().strftime("%Y-%m-%d")
    if date == today:
        return True
    else:
        return False

#str转换成float
def trans_float(num):
    try:
        res = float(num)
    except:
        res = float(0)
    return res

#插入日期和单位净值
def insert_data(data,date):
    for i in range(len(data)):
        collection = DB[data.iloc[i]["code"]]
        posts = {"_id":date,"value":trans_float(data.iloc[i]["dwjz"])}
        collection.insert_one(posts)

#主函数
def main():
    data,date = jj.get_day_info()
    if check_time(date):
        insert_data(data,date)
    else:
        return

if __name__ == "__main__":
    main()</pre>
为了每天定时运行，这里顺便来学一下linux的crontab
<pre>#修改crontab配置文件
crontab -e</pre>
<pre>示例：
前五个分别为分(0-59) 时(0-23) 天(1-31) 月(1-12) 星期(0-6) 
后面是命令
&gt;&gt;之后是log文件
2&gt;&amp;1表示正确错误的log都打印到log文件
* * * * * /usr/local/bin/python3 /home/jjdb.py &gt;&gt; /root/test/test.log 2&gt;&amp;1</pre>
修改完保存就能用。

这里只做了进净值存储，后期还可以做一些基金管理，统计分析之类的。
