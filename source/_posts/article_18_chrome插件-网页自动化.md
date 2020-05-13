---
title: WEB-ROBOT
catalog: true
date: 2020-05-11 19:31:43
subtitle: 一个管理网页自动化执行的chrome插件
header-img: 
tags:
- CHROME插件
---

# 前言

这边主要介绍一款个人自行开发的chrome插件 web-robot，  
包括它的开始设计，使用教程，实现思路和细节。  
源码的github地址是在[https://github.com/webgjc/web_robot](https://github.com/webgjc/web_robot)

# 软件设计

关于这个软件的初始设计定位，这边将他定位为**网页自动化链路管理执行**；  
类似模拟自动化测试，但不会有结果校验。

创建事务和流程的用户主要针对的用户是稍微了解一点点html的用户，当然小白可以用他人分享的事务流程享受自动运行的快感。

软件主要要包括的有以下一些：
- 网页元素的可视化筛选；
- 筛选的元素加上动作与延时变成一个事件；
- 多个事件形成一个事务流程；
- 主界面可以管理多个事务，进行事务的运行、轮播、分享等；

软件风格大致按使用的前端ui框架的极简风格走；

# 软件使用教程

## 下载与导入

### 源码下载导入

源码github地址：[https://github.com/webgjc/web_robot](
https://github.com/webgjc/web_robot)

首先到github上将源码clone到本地 / 下载解压也可以
> git clone https://github.com/webgjc/web_robot.git

然后打开chrome点开右上角三个点的地方，  
选择更多工具 ==》扩展程序；

因为是源码，开启右上角的开发者模式
![开发者模式](/img/mypost/kaifazhemoshi.jpg)

然后点击左上角的加载已解压的扩展程序，  
选择刚刚clone下来的目录

下面表示已经加载进来了
![robot](/img/mypost/robot.jpg)

且右上角出现这个小图标
![robot](/img/mypost/robot_small.jpg)

**重要：右键这个小图标，**  
**可读取和更改的网站数据，**  
**选择 在所有网站上；**

至此已经完成下载和导入啦！😋

### 从chrome商店下载导入

暂时没有上线chrome应用商店

## 软件使用

### 新建事务

首先新建一个事务
![robot](/img/mypost/robot_shiwu.jpg)

这边建一个test为例子
![robot](/img/mypost/robot_main.jpg)

### 筛选器

点击 test 进入 过程添加页

点击添加过程，进入筛选器页面
![robot](/img/mypost/robot_shaixuanqi.jpg)

这边支持按 html标签 / class / id 筛选

下面都进行举例

#### html标签筛选

选择一个html标签，a(链接), body, div等  
下方会展示一个列表，表示页面中该元素有几个。  
鼠标移到列表每个上面，  
页面对应元素将会渲染一个蒙版到以便正确定位选择。

这是选择body的时候
![robot](/img/mypost/robot_htmltag.jpg)

这是选择div的时候
![robot](/img/mypost/robot_htmltag2.jpg)


#### class / id 筛选

首先在选择标签列表的下列菜单中  
选择 第一个 class/id选择器   
然后会出现一个输入框输入对应的class或id  

class选择器需要以.开头，如：.xxx  
id选择器需要以#开头，如：#xxx

选好后按回车，如果有对应的选择器，将会展示一个列表, 
后续操作同html标签，鼠标移到列表上会渲染蒙版
![robot](/img/mypost/robot_classtag.jpg)

### 单个事件

用筛选器选中好一个元素后  
将会进入事件编辑页面
![robot](/img/mypost/robot_shijian.jpg)

(如想改变元素，可以按最上面的元素返回)

这边的选择操作可以选的有：
- click -- 点击
- value -- 设值
- refresh -- 刷新
- pagejump -- 当页url跳转

然后输入 执行前等待时间 / 和上一步执行中间间隔时间

可以测试运行当前事件，也可以把事件添加到事务流程中。

### 流程事件管理

添加后会返回流程页，  
如下加了一条，等待一秒后，(click)点击第一个\<a\>标签

![robot](/img/mypost/robot_liuch.jpg)

如下表示，  
等待一秒后，(click)点击第一个\<a\>标签的链接，  
再等待一秒后，往第一个input输入框里赋值 你好

![robot](/img/mypost/robot_liuch2.jpg)

可以选择继续添加，  
可以选择返回主页，  
可以测试运行单个事件，  
可以删除单个事件；

### 事务管理

继续到主页

事务支持新增，删除，运行，轮播，导出，导入

![robot](/img/mypost/robot_main.jpg)

#### 运行事务

运行主要是按定好的流程运行每个事件，  
运行会放在浏览器后台中，中间关闭这个页面并不会切断运行。

#### 轮播事务

轮播表示的是循环运行，运行完一次后立即进行下一次。  
中间的间隔是第一个事件的等待时间。  
由于在浏览器后台轮播可能会导致大量吃资源，因此轮播限制了只能前台运行，也就是关闭了这个管理页后就会断掉轮播。

#### 导入导出事务

点击导出，事务的信息会自动保存到剪切板，复制给他人即可；

点击导入，将他人复制的事务信息导入即可；

### 常见问题说明

>筛选器失效

有时候页面与浏览器插件的连接会失效或过期，  
这个时候可以刷新页面，然后重新打开这个插件页面。

# 软件开发过程

## 其他准备知识

关于chrome插件的开发，请看[官网教程](https://developer.chrome.com/extensions)或[其他教程](https://www.cnblogs.com/liuxianan/p/chrome-plugin-develop.html)

## 软件开发设计

这个浏览器插件包括以下几部分：
```
配置文件
manifest.json

样式文件夹
/css

html文件，主要放了popup.html，也就是这个插件管理页
/html

存放图片
/images

存放js
主要实现的包括popup.js(管理页的后端)
和background.js(浏览器的后端)
/js
```

## 部分代码说明

``` javascript
// 获取数据存储
function get_my_robot(callback) {
    chrome.storage.local.get(["my_robot"], function(res) {
        if (callback) callback(res.my_robot)
    })
}

// 设置数据存储
function set_my_robot(new_robot, callback) {
    chrome.storage.local.set({ "my_robot": new_robot }, function() {
        if (callback) callback()
    })
}

// 连接
function connect(callback) {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var port = chrome.tabs.connect(tabs[0].id, { name: "robot" });
        callback(port)
    })
}

// 当前tab执行
function exectab(callback) {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        callback(tabs[0].id)
    })
}


// 拼接要执行的js代码
function jscode(process) {
    let exec_code = "(function(){ \n";
    if(process["tag"].startsWith(".")) {
        exec_code += 'var robot_node = document.getElementsByClassName("' + process["tag"].substring(1) + '")[' + process["n"] + '];'
    }else if(process["tag"].startsWith("#")) {
        exec_code += 'var robot_node = document.getElementById("' + process["tag"].substring(1) + '");'
    }else{
        exec_code += 'var robot_node = document.getElementsByTagName("' + process["tag"] + '")[' + process["n"] + '];'
    }
    if (process["opera"] == "click") {
        exec_code += "robot_node.click();"
    } else if (process["opera"] == "value") {
        /**
         * 为react兼容
         */
        exec_code += "let lastValue = robot_node.value;"
        exec_code += "robot_node.value=\"" + process["value"] + "\";";
        exec_code += "let event = new Event('input', { bubbles: true });";
        exec_code += "event.simulated = true;";
        exec_code += "let tracker = robot_node._valueTracker;";
        exec_code += "if (tracker) { tracker.setValue(lastValue); }\n";
        exec_code += "robot_node.dispatchEvent(event);";
    } else if (process["opera"] == "refresh") {
        exec_code += "window.location.reload();";
    } else if (process["opera"] == "pagejump") {
        exec_code += "window.location.href=\"" + process["value"] + "\";";
    }
    exec_code += "\n})();";
    console.log(exec_code)
    return exec_code;
}

// 根据存储数据更新主页
function refresh_cases() {
    get_my_robot(my_robot => {
        if (my_robot == undefined) {
            set_my_robot({})
        } else {
            var cases = "";
            for (let i in my_robot) {
                let one_case = {}
                one_case["case_name"] = i;
                one_case["content"] = my_robot[i];
                let tr = '<tr id=' + i + '> \
                            <td> \
                                <a href="#" class="case_name">' + i + '</a> \
                            </td> \
                            <td> \
                                <a href="#" class="run_case">运行</a> \
                                <a href="#" class="del_case">删除</a> \
                                <a href="#" class="lun_case">轮播</a> \
                                <a href="#" class="export_case" data-clipboard-text=' + JSON.stringify(one_case) + '>导出</a> \
                            </td> \
                        </tr>';
                cases = cases + tr;
            }
            $("#cases").html(cases);
        }
    })
    new ClipboardJS('.export_case');
}


// 更新单个事务的流程
function refresh_process(case_name) {
    get_my_robot(my_robot => {
        var data = my_robot[case_name];
        var process_li = "";
        for (let i = 0; i < data.length; i++) {
            let lili = '<li class="collection-item" id="process-' + i + '"> \
                            <div class="row "> \
                                <div class="col s6 ">标签：' + data[i]["tag"] + '</div> \
                                <div class="col s6 ">#：' + data[i]["n"] + '</div> \
                            </div> \
                            <div class="row "> \
                                <div class="col s6 ">操作：' + data[i]["opera"] + '</div> \
                                <div class="col s6 ">等待：' + data[i]["wait"] + '秒</div> \
                            </div> \
                            <div class="row "> \
                                <div class="col s12 ">赋值：' + data[i]["value"] + '</div> \
                            </div> \
                            <div class="row "> \
                                <a href="# "> \
                                    <div class="col s6" id="process_test_run" >test</div> \
                                </a> \
                                <a href="# "> \
                                    <div class="col s6 " id="process_del">删除</div> \
                                </a> \
                            </div> \
                        </li> ';
            process_li = process_li + lili;
        }
        $("#process_list").html(process_li);
    })
}

// 主要
$(document).ready(function() {

    // 筛选器
    var tag_types = ["class/id选择器", "a", "body", "button", "div", "i", "img", "input", "li", "p", "span", "td", "textarea", "tr", "ul", "h1", "h2", "h3", "h4", "h5"];
    // 操作
    var operas = ["click", "value", "refresh", "pagejump"];
    var case_name = "";
    var init_select = 1;

    refresh_cases();

    $('.modal').modal();

    // 连接当前页面
    exectab(tab_id => {

        // 运行事务，调用background
        $("#cases").on("click", ".run_case", function() {
            var case_name = $(this).parent().parent().attr("id");
            var save_run = $(this).parent().html();
            var that = $(this).parent();
            that.html("运行中");
            get_my_robot(my_robot => {
                var bg = chrome.extension.getBackgroundPage();
                bg.execute(my_robot[case_name], tab_id);
                var process_wait = 0;
                for (let i = 0; i < my_robot[case_name].length; i++) {
                    process_wait = process_wait + my_robot[case_name][i]["wait"] * 1000;
                }
                setTimeout(function() {
                    that.html(save_run);
                }, process_wait)
            })
        })

        // 轮播事务
        $("#cases").on("click", ".lun_case", function() {
            var case_name = $(this).parent().parent().attr("id");
            var save_run = $(this).parent().html();
            var that = $(this).parent();
            that.html("运行中");
            get_my_robot(my_robot => {
                var process_wait = 0;
                for (let n = 0; n < 100; n++) {
                    for (let i = 0; i < my_robot[case_name].length; i++) {
                        process_wait = process_wait + my_robot[case_name][i]["wait"] * 1000;
                        setTimeout(function() {
                            chrome.tabs.executeScript(tab_id, { code: jscode(my_robot[case_name][i]) });
                        }, process_wait);
                    }
                }
                setTimeout(function() {
                    that.html(save_run);
                }, process_wait);
            })
        })

        // 导入事务
        $("#cases").on("click", ".export_case", function() {
            $(this).html("导出成功");
            var that = $(this);
            setTimeout(function() {
                that.html("导出");
            }, 1000);
        })

    })
})
```

# 感谢

- [materializecss](http://www.materializecss.cn/about.html)
- [官方轮子](https://developer.chrome.com/extensions)
- [插件教程](https://www.cnblogs.com/liuxianan/p/chrome-plugin-develop.html)