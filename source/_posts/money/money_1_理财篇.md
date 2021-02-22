---
article: false
title: 理财篇
catalog: true
date: 1020-08-23 19:31:43
subtitle: 论如何更有钱
header-img:
---

## 查看基金数据与交易
<div id="trace_data">
    <select id="select_code"></select>
    <iframe id="ifr_data"></iframe>
</div>

## 整理基金实际操作记录
- 2020-08-29
[查看基金实际操作](/article/money_2_基金实际操作/)
```
本次的数据来源主要是支付宝查账，
地址为 https://consumeprod.alipay.com/record/standard.htm
通过搜索筛选带蚂蚁财富的近三年账单，筛选出基金的买入卖出操作，
下载为csv文件

然后通过天天基金接口，获取到基金名称与代码的对应关系(有些关系还得手动补充维护)
通过脚本转换csv到json格式，同时筛选所需的信息(基金，操作，日期)

最后通过脚本将json生成markdown文本用于hexo渲染成页面
```

## 理财篇必读镇楼 
- 2020-08-23
```
我当前的理财主要在于基金的买卖，也是第二收入(亏损)来源；
本栏是一些理财思路和方法的整合，主要包含几个方向
1. 基金买入卖出及其来源依据或直觉依据
2. 在一些节点回顾性总结
3. 发现或总结一些方法论
4. 理财工具，分析工具的创造
5. 数据挖掘和分析
6. 分享一些这个方向的文章
```


<script type="text/javascript">
    let ifr = document.getElementById("ifr_data");
    let scode = document.getElementById("select_code");
    let urlroot = "/money/fund_trace_data.html?code=";
    ifr.style.border = "none";
    ifr.style.width = "100%";
    ifr.style.minHeight = "400px";

    fetch("/money/fund.json")
    .then(res => res.json())
    .then(data => {
        let codemap = {};
        let now = new Date();
        now.setFullYear(new Date().getFullYear()-1);
        data.forEach(d => {
            if(new Date(d["datetime"]) > now) {
                codemap[d["fund_name"]] = d["fund_code"];
            }
        });
        let codes = Object.keys(codemap);
        scode.innerHTML = codes
        .map(name => `<option value=${codemap[name]}>${name}</option>`)
        .join(" ");
        ifr.src = urlroot + codemap[codes[0]];
    });
    
    scode.onchange = (e) => {
        ifr.src = urlroot + scode.value;
    }
</script>