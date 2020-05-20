---
title: TABLE-MAKER
catalog: true
date: 2020-05-20 10:31:43
subtitle: 一个万能数据表格的浏览器插件
header-img: 
tags:
- CHROME插件
---

# 前言

本次依旧发布一款浏览器插件--万能表格。

说说为什么万能，其一，因为它可以接入任意的GET接口数据或其他文本(html/text...)数据来源，且无跨域限制，且一些需要cookie的接口或网站访问数据时也会带上cookie。  
其二，你可以自定义列的数量和名称，自定义数据的解析到对应的列，json解析用就直接用key，文本解析就用正则表达式。  
其三，设置的数据来源一般是一个数据的详情接口或详情页，每个会对应一个主键，比如一个股票详情接口主键为股票代码，一个订单详情页的主键为唯一订单号。添加数据行的时候就使用这个主键来添加，主键会反映到url地址上，再反映到数据上。

## 案例展示

![tablemaker_jjjz](/img/mypost/tablemaker_jjjz.jpg)

![tablemaker_weather](/img/mypost/tablemaker_weather.jpg)


# 软件使用教程

## 软件下载与导入

### 源码下载导入

软件源码的github地址为   
[https://github.com/webgjc/table_maker](https://github.com/webgjc/table_maker)

首先将代码克隆到本地

> git clone https://github.com/webgjc/table_maker.git

然后打开chrome点开右上角三个点的地方，
选择更多工具 ==> 扩展程序；

因为是源码，开启右上角的开发者模式
开发者模式，(在完毕后可以关闭开发者模式)

然后点击左上角的 **加载已解压的扩展程序**，
选择刚刚clone下来的目录

下图表示已经加载进来了

![table_maker](/img/mypost/table_maker.jpg)

然后浏览器右上角也有这个插件的小图标

就表示导入完成。

### 软件商店下载

暂不支持

## 软件使用

点开浏览器右上角的 **$** 小图标，会见到如下主页

![tablemaker_main](/img/mypost/tablemaker_main.jpg)

目前该插件只支持一个表的制作与展示。

### 导入数据体验

数据如下

``` json
{
    "data_type": "text",
    "data_url": "http://fund.eastmoney.com/{ID}.html",
    "fields": [
        {
            "data_parser": "funCur-FundName\">(.*?)</span>",
            "field_name": "基金名称"
        },
        {
            "data_parser": "gz_gszzl\">(.*?)</span>",
            "field_name": "净值估算"
        }
    ],
    "keys": [
        "110022",
        "003634"
    ],
    "table_name": "基金今日估值"
}
```

这是一个已经做好的表格，表示的是基金实时净值的表格，主键为基金代码  
(这边用的天天基金网的基金详情页面，实时数据有延迟)

可以直接复制上面的数据，然后点击主页上导入新表格，粘贴回车即可，相当于已经做完了表格。如下

![tablemaker_jjjz](/img/mypost/tablemaker_jjjz.jpg)

后面如果要关注其他基金，就直接点击新增主键，输入基金的代码即可。

每次点开这个主页会重新获取渲染一遍(页面有缓存有时不会获取到最新数据)。

### 制作自己的表格TEXT解析

接下来就是最重要的部分 -- 制作万能表格

#### 基金净值表

这里以制作上面基金实时净值表为例。

#### 确定表格数据源

首先要确定好要制作的表格的数据来源。

比如这里找到了 [天天基金网](http://fund.eastmoney.com/)，  
它查看一个基金详情的的地址页如下：
> http://fund.eastmoney.com/{ID}.html

{ID}表示基金的代码，虽然是html格式的返回，但也可以正则来解析，正合适我们这里所需要的。

点击主页上的修改表格，修改表名，数据源地址(主键的地方就写{ID})和解析方式。

#### 确定需要解析的字段

这边需要从基金详情页里获取的有(基金名称，基金实时的净值估值)

到某个基金的详情的html页面，打开浏览器调试，或查看源码。

找到这个数据的来源，这边看到在html源码里能找到数据，说明是后端渲染完了的，这边只需要在这个源码里进行正则匹配数据

基金名称源码对应
``` html
<span class="funCur-Tit">基金名称：</span><span class="funCur-FundName">易方达消费行业股票</span>
```

正则解析方式为 
>funCur-FundName\">(.*?)\</span>

基金实时估值部分源码
``` html
<div class="remindicon"><p>净值估算是按照基金历史定期报告公布的持仓和指数走势预测当天净值。预估数值不代表真实净值，仅供参考，实际涨跌幅以基金净值为准。</p></div></div><div class="fundDetail-main"><!-- 档案 start --><div class="fundInfoItem"><!--开放式基金收益率模块--><div class="dataOfFund"><dl class="dataItem01"><dt><p><span><span class="sp01">净值估算</span></span><span id="gz_gztime">(20-05-20 10:01)</span><span class="infoTips"><span class="tipsBubble" style="display: none;">净值估算每个交易日9：30-15：00盘中实时更新（QDII基金为海外交易时段）。</span></span></p></dt><dd class="dataNums"><dl class="floatleft"><span class="ui-font-large ui-color-green ui-num" id="gz_gsz">3.1764</span></dl><dl id="gz_icon" class="gzdown"></dl><dl class="floatleft fundZdf"><span class="ui-font-middle ui-color-green ui-num" id="gz_gszze">0.0086</span><span class="ui-font-middle ui-color-green ui-num" id="gz_gszzl">-0.27%</span>
```

正则解析方式为
>gz_gszzl\">(.*?)\</span>

**插件上的操作为**

主页点击修改表格，点击确定并修改列

点击新增列，输入判断出来的列名和解析方式，点击确定，加完如下

![tablemaker_lie](/img/mypost/tablemaker_lie.jpg)

当然这边也提供了测试解析的功能

点击测试解析，输入一个主键，输入对应的正则，解析结果就会展示在下方。

点击返回返回主页，列就会渲染出来。

#### 最终效果和主页操作

制作完的主页如下，没有数据但加的列已经有了

![tablemaker_kongzhu](/img/mypost/tablemaker_kongzhu.jpg)

主页上可以增加主键，表示增加一行数据

增加主键就相当于一个关注的基金。

比如增加110022, 003634这两个基金代码作为主键，就制作成了上面的直接导入数据的表格

![tablemaker_jjjz](/img/mypost/tablemaker_jjjz.jpg)

双击导出表格 就将表格配置复制到剪切板，可以复制给他人导入。

### 制作自己的表格JSON解析

#### 城市天气表

这边JSON解析举的例子为 城市天气列表

#### 数据来源

首先找到所需数据源接口

这边使用国家的
>http://www.weather.com.cn/data/cityinfo/{ID}.html

{ID}表示城市代码，代码列表在下面有
https://wenku.baidu.com/view/ea286102bb68a98271fefad8.html

天气格式如下
```
{
    "weatherinfo": {
        "city": "北京",
        "cityid": "101010100",
        "temp1": "18℃",
        "temp2": "31℃",
        "weather": "多云转阴",
        "img1": "n1.gif",
        "img2": "d2.gif",
        "ptime": "18:00"
    }
}
```

编辑表格  

表名使用 城市天气表，  
数据源填写 http://www.weather.com.cn/data/cityinfo/{ID}.html  
数据格式 json

#### 设置列解析

json解析比较简单，直接使用key.key.key

举例如下：  
要解析城市名，则新增字段，名称填城市， 解析方式就写 
> weatherinfo.city  

要解析城市天气，则新增字段，解析方式就写 
> weatherinfo.weather

#### 最终效果展示

主页操作同上 TEXT解析的表格

![tablemaker_weather](/img/mypost/tablemaker_weather.jpg)

## 软件开发说明

浏览器插件的开发不在多说，可以查看下面借鉴的友联，或者对比之前发布的插件的教程。

本次插件主要利用的是 在popup.js或者background.js可以无限跨域访问的特点，就获取到任意网站的数据，且进行自定义解析，然后渲染成表格。

至于为什么要用$符号，一开始设计时是想弄一个实时基金数据列表，然后做着做着发觉可以做一个更加通用的数据表格，插件图标便也没有再换。

### 重点关注部分代码

主要代码在popup.js中，

``` javascript
// json解析，解析格式为：key.key.key
// 根据每个key去获取对应的值
async function deal_json_parser(url, key, fields) {
    return await fetch(key_replace(url, key))
        .then(response => response.json())
        .then(data => {
            rowdata = [key];
            for (i in fields) {
                tmpdata = data;
                fields[i]["data_parser"].split(".").map(fieldkey => {
                    tmpdata = tmpdata[fieldkey];
                })
                if (Object.prototype.toString.call(tmpdata) === '[object Object]') {
                    rowdata.push(JSON.stringify(tmpdata));
                } else {
                    rowdata.push(tmpdata || "");
                }
            }
            return rowdata;
        });
}

// 正则解析，将字符串正则匹配到获取到的原始数据，返回第二个值
// 也就是(.*?)的部分
async function deal_text_parser(url, key, fields) {
    return await fetch(key_replace(url, key))
        .then(res => res.text())
        .then(data => {
            rowdata = [key];
            for (i in fields) {
                rowdata.push(data.match(new RegExp(fields[i]["data_parser"]))[1]);
            }
            return rowdata;
        });
}


// 渲染主页的数据，使用异步
async function render(data) {
    $(".mainbody").html("");
    $(".table_head").html(data["table_name"]);
    headstr = "<tr>";
    headstr += "<td>主键</td>"
    data["fields"].map(field => headstr += "<td>" + field["field_name"] + "</td>");
    headstr += "<td>操作</td></tr>";
    $(".mainhead").html(headstr);
    for (key in data["keys"]) {
        let row;
        try {
            if (data["data_type"] === "json") {
                row = await deal_json_parser(data["data_url"], data["keys"][key], data["fields"]);
            } else {
                row = await deal_text_parser(data["data_url"], data["keys"][key], data["fields"]);
            }
        } catch (e) {
            row = [data["keys"][key]];
            data["fields"].map(field => row.push(""));
        }
        htmlstr = "<tr>";
        row.map(value => htmlstr += "<td>" + value + "</td>");
        htmlstr += "<td><a href='#' id='move_up' key='" + key + "'>上移</a> <a href='#' id='delete_value' key='" + key + "'>删除</a></td>"
        htmlstr += "</tr>";
        $(".mainbody").append(htmlstr);
    }
}
```

# 感谢

- [materializecss](http://www.materializecss.cn/about.html)
- [官方轮子](https://developer.chrome.com/extensions)
- [插件教程](https://www.cnblogs.com/liuxianan/p/chrome-plugin-develop.html)