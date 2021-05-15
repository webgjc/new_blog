---
article: false
title: 理财篇
catalog: true
date: 1020-08-23 19:31:43
subtitle: 论如何更有钱
header-img:
---

## 切换基金

<div>
    <select id="select_code"></select>
</div>

### 查看基金数据与交易
<div>
    <iframe id="ifr_data" style="border: none; width: 100%; min-height: 400px"></iframe>
</div>

### 点位分布数量
<div>
    <div style="display: flex; margin-bottom: 20px">
        <div style="flex: 0 0 80px">步长</div>
        <input type="number" id="step" value=10 />
    </div>
    <div style="display: flex; margin-bottom: 20px">
        <div style="flex: 0 0 80px">开始时间</div>
        <input type="date" id="start" value="2020-01-01" />
    </div>
    <div style="display: flex; margin-bottom: 20px">
        <div style="flex: 0 0 80px">结束时间</div>
        <input type="date" id="end" value="2021-05-01" />
    </div>
    <div style="color: red">注：除指数外，其他净值均放大了1000倍，当前位置显示为紫色</div>
    <iframe id="analyse_ifr_data" style="border: none; width: 100%; min-height: 400px"></iframe>
</div>

## 下跌在稳住
- 2021-03-15
年初挣的钱在年后都还回去了，现在还亏了不少，仓位也比较高  

主要还是集中在半导体，还有不多的一些其他行业的，传媒/证券  

但也想逐步转换到沪深300，做做指数比较香

黄金最近也入手了一些，主要从之前的400跌倒了350，买时成本价在365左右，  
现在价格差不多基本持平，个人觉得跌的差不多了，也可能最低在320。

## 整理基金实际操作记录
- 2020-08-29
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
    Date.prototype.format = function(fmt) { 
        var o = { 
            "M+" : this.getMonth()+1,                 //月份 
            "d+" : this.getDate(),                    //日 
            "h+" : this.getHours(),                   //小时 
            "m+" : this.getMinutes(),                 //分 
            "s+" : this.getSeconds(),                 //秒 
            "q+" : Math.floor((this.getMonth()+3)/3), //季度 
            "S"  : this.getMilliseconds()             //毫秒 
        }; 
        if(/(y+)/.test(fmt)) {
                fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
        }
        for(var k in o) {
            if(new RegExp("("+ k +")").test(fmt)){
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
            }
        }
        return fmt; 
    }

    let zhishu_data = [
        {
            code: "000001",
            name: "上证指数"
        }
    ]

    let ifr = document.getElementById("ifr_data");
    let analyse_ifr = document.getElementById("analyse_ifr_data");

    let scode = document.getElementById("select_code");
    let analyse_step = document.getElementById("step");
    let analyse_start = document.getElementById("start");
    let analyse_end = document.getElementById("end");

    let urlroot = "/money/fund_trace_data.html?code=";
    let analyes_url = "/money/fund_analyse_distribution.html?";

    let analyse_data = {
        code: "000001",
        step: 100,
        start: `${new Date().getFullYear()-1}-${new Date().format("MM-dd")}`,
        end: new Date().format("yyyy-MM-dd")
    }

    function init() {
        ifr.src = urlroot + analyse_data.code;
        analyse_step.value = analyse_data.step;
        analyse_start.value = analyse_data.start;
        analyse_end.value = analyse_data.end;
    }

    init()

    function render_analyse() {
        analyse_ifr.src = analyes_url + `code=${analyse_data.code}&step=${analyse_data.step}&start=${analyse_data.start}&end=${analyse_data.end}`
    }

    fetch("/money/fund.json")
    .then(res => res.json())
    .then(data => {
        let codemap = {};
        zhishu_data.forEach(item => {
            codemap[item["name"]] = item["code"]
        })
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
        analyse_data.code = codemap[codes[0]];
        render_analyse();
    });

    analyse_step.onchange = function(e){
        analyse_data.step = e.target.value
        render_analyse();
    }

    analyse_start.onchange = function(e){
        analyse_data.start = e.target.value
        render_analyse();
    }

    analyse_end.onchange = function(e){
        analyse_data.end = e.target.value
        render_analyse();
    }
    
    scode.onchange = (e) => {
        analyse_data.code = scode.value;
        render_analyse();
        ifr.src = urlroot + scode.value;
    }
</script>