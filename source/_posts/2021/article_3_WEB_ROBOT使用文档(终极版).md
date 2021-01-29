---
title: Web Robot使用教程(终极版)
catalog: true
date: 2021-01-22 10:31:43
tags:
    - CHROME插件
    - 自动化
---

# 前言

本文为[Web Robot](https://github.com/webgjc/web_robot)插件使用教程终极版

融合所有前面版本迭代的功能，包括有用的没用的

当前文档教程的Web Robot版本 V2.2.0

![image](/img/mypost/2021/1-1.jpg)

# 教程

## 下载与安装

因为一些权限因素，本插件目前没有上到chrome商店，需通过源码安装

### 下载

首先到github的仓库 [https://github.com/webgjc/web_robot](https://github.com/webgjc/web_robot)

将仓库克隆到本地

> git clone https://github.com/webgjc/web_robot.git

### 安装

打开chrome浏览器，访问 [chrome://extensions/](chrome://extensions/)

点击开启开发者模式（右上角）

加载已解压的扩展程序，选择本地的仓库代码，即可完成。

完成后可关闭开发者模式。

## 事务相关操作

事务在Web Robot中表示一系列浏览器操作的集合。

如自动化表单填写，自动化签到，自动化去广告。

配置事务/导入事务是使用插件的第一步。

### 导入事务

![image](/img/mypost/2021/1-2.jpg)

如果有别人已经配置好的并导出的成熟事务，  
或者想直接体验一下github上的演示用例[Web Robot演示用例](https://github.com/webgjc/web_robot#%E6%BC%94%E7%A4%BA%E7%94%A8%E4%BE%8B)

可以直接导入即可体验浏览器自动化的乐趣。

点开插件面板，点击 导入事务 

复制如上面演示用例中的一长json字符串。点击确认即可。

### 新增事务

![image](/img/mypost/2021/1-3.jpg)

如果要自己进行自定义的配置，首先第一步是新增事务。

点击 新增事务，填写事务的名称（不能有重复）

选择事务的类型

- 流程事务：通过页面元素定义事件，支持运行，受控运行，添加看板等；
- 并发爬虫事务：页面级的爬虫，支持并发，定时运行，数据添加看板等；
- 源码事务：源码注入，支持自定义代码，自定义注入地址；
- 受控事务：键盘鼠标的录制，支持录制，回放；

选择好后 点击确认 即创建了一个空的事务。

### 重命名/上移/删除

![image](/img/mypost/2021/1-4.jpg)

一些一般性的操作

- 重命名已创建的事务

点击事务右边操作列表中的 重命名

输入新的名字 确认即可。

- 移动事务在列表中的上下位置

点击上移，即可与上面一个事务交换位置

- 删除事务

点击删除，二次确认后即可删除。(删除不可复原)

### 导出事务

如果想要讲一个已经制作完成的事务分享给别人

点击导出，出现导出成功。

表示已经复制到 **剪切板**，再其他地方直接粘贴即可。

## 本地客户端相关，启动与使用

**重点：本地客户端只影响部分插件功能的使用。**  
**大部分情况下不需要用到！详情看[受控概念](#受控概念)，[爬虫本地相关](#爬虫本地相关)**

为了实现浏览器插件能与本地进行**数据交互**，  
同时在一些插件无法实现的功能（如控制键盘鼠标）上通过本地python来实现。

这边写了一个简单的**python web**服务，插件通过 **HTTP** 访问接口来交互。

### 启动与使用

![image](/img/mypost/2021/1-5.jpg)

首先机器上需要有python3的环境，或者创建一个python3的虚拟环境。

到插件仓库的跟目录

有一个依赖库的文件在 **py/requirements.txt**

下载依赖
> pip install -r py/requirements.txt

启动web服务
> bash main.sh start

或
> python py/web.py

**注**：main.sh中还有一些可配置操作，可用下面命令查看
> bash main.sh

### 受控概念

插件中一直穿插一个名词受控，包括受控事务，流程事务的受控运行。

这边受控表示对鼠标键盘进行控制。

- 受控事务：录制鼠标键盘操作，控制鼠标键盘还原操作
- 流程事务受控运行：流程事务是由浏览器元素定义的事件，通过控制鼠标键盘来还原事件（一般运行是通过js还原事件）

由于Chrome插件本身不能实现这个操作，

因此这边都由本地python来实现控制鼠标键盘。

由此受控相关的都会用到与本地进行数据交互。

**注**：Mac中控制键鼠需要进行 **安全与隐私** 的配置  
如用iTerm开的web服务，则需要配置 **隐私 - 辅助功能 - 支持iTerm控制您的电脑**

### 爬虫本地相关

具体爬虫信息可到 [并发爬虫事务](#并发爬虫事务) 查看

这边由于页面爬虫在完成数据获取之后需要将数据发出去。

这边是在web服务中开了一个数据接收的接口，

插件爬到的数据按一定的切割数量分批次进行接口发送。

web服务受到数据后，存储到本地文件，并进行整合。

**数据存储于 /py/crawler/**

## 流程事务

![image](/img/mypost/2021/1-6.jpg)

创建一个流程事务后，点击事务的名称即进入事务的详情配置页

流程事务由 **多个浏览器事件** 组成。

每个事件可以是如开关某页面，点击某元素，输入某值。

### 事件详情

![image](/img/mypost/2021/1-7.jpg)

一个事件包含 
- 元素：唯一选择器；
- 操作：点击，设值，开关页面；
- 等待时间：与前一个事件中间间隔的时间；
- dom检查：由于一些元素是异步/延时创建的，开启dom检查则在运行前可以保证这个元素一定存在，否则自旋。
- 其他一些不固定选项(一些特殊事件有)

#### 事件操作说明
click：点击某个元素

value：可以在一般浏览器输入框中设值（输入需要设值的值）  
如果你需要在运行前才设值这边的输入值，可以将这边设值为${value}，则在点击运行会弹出让你输入value的值

mouseover：鼠标移动到上面事件

refresh：刷新当前页面

pagejump：当前页面跳转，需要设值页面url

newpage：打开一个新页面，需要设值页面url  
**注**：第一个事件如果是新开页面且选择在后台打开，这样整个事务都会在后台运行

getvalue：取页面元素的文本，取到后保留在运行参数中，可用来后续设值，也可作为爬虫的数据。（需要设值一个取到后保存的key）
（如取到第一个页面的元素设为 title(key)，然后打卡第二个页面，设值输入框为title值，则会用刚才设值的title）

getcustomvalue：取document结果，或js函数结果，用处同上。（需要设值两个，一个作为取值key，一个为表达式）  
如取document.title可以取到页面的标题。

closepage：关闭当前页面

onlyshow：看板特殊事件操作，将当前页面只保留选择的元素，其他所有都隐藏。

sendmessgae: 发送消息，默认为发送系统消息，也可以走浏览器alert消息。

### 确定唯一元素

定义页面事件的第一步都是确定一个页面元素。

这边有多种方法，通用的为 **一般选择器 + 第n个** 来表述唯一元素(如 body&0)

#### 添加事件

![image](/img/mypost/2021/1-8.jpg)

点击添加事件，进入一般选择器配置页，可配置 **标签选择器** 或 **自由选择器**

- 标签选择器 
选择一个标签：如body，div

然后会出现一个列表，表示页面中有多少个这样的标签。（div&0，div&1）

鼠标移动上去后，页面会相应定位到这个元素上，并出现红色蒙版。

点击确认一个想要的元素。

![image](/img/mypost/2021/1-10.jpg)

- 自由选择器
选择了自由选择器，会出现一个输入框，可以自己输入想要的选择器，

回车之后也会出现一个相同的列表，(选择器&0，选择器&1)

鼠标移动和点击确认同上。

#### 页面录制（不推荐）

点击页面录制，这边暂时只支持单页面中的 **英文设值** 和 **点击事件**的录制。

录制完成后，可以点击完成录制

事件列表页会出现已经录制的所有事件。

#### 页面添加事件（推荐使用）

![image](/img/mypost/2021/1-9.jpg)

打开一个页面，点击页面添加事件。

然后在鼠标移回页面可以看到在移动到每个元素上时，都会出现一个粉色边框。

单机之后，会出现一个列表，表示当前最子元素，和其父元素，一直到跟元素。

点击选择一个想要的元素选择器

进入事件配置页，进行事件的配置。

### 运行说明

![image](/img/mypost/2021/1-11.jpg)

流程事务包含：运行，定时运行，受控运行，轮播 四种模式

#### 运行

采用后台运行模式，使用js和chrome接口还原事件。

可直接点击运行，无其他依赖。

#### 定时运行

![image](/img/mypost/2021/1-12.jpg)

配置模式分两种：每日hh:mm，每隔n分钟

如写 15:00 表示每日15点运行一次。

写 5m 则表示每5分钟运行一次。

运行按当天开始算。

运行具体会有一些时间上的出入。

运行可以配置失败重试。（失败重试有多次运行的风险）

#### 受控运行

采用控制本地鼠标键盘还原事件。（事件操作为 点击，设值）

需依赖本地web服务开启。

#### 轮播

运行完一次后直接进行下一次运行。

## 并发爬虫事务

![image](/img/mypost/2021/1-13.jpg)

顾名思义这个事务要做的事情就是页面级的爬虫，适合爬一些小批量数据，同时可以突破一些反扒限制(因为就和人打开没啥区别)

这边对于爬虫配置的抽象为：

- 一批需要爬的地址：可以自己填，批量填，或接口获取；
- 每个页面中需要爬的信息配置：配置一个流程事务，getvalue等的作为爬取数据事件；
- 并发量配置：这边使用iframe实现；
- 是否后台运行配置：后台运行则是新开chrome，并最小化的运行；
- 发送数据/保存数据：可发送到本地接收，或就存在插件信息存储中；

### 配置爬虫

点击爬虫事务的名称，进入爬虫配置页

#### url配置

两种配置方式

可自行配置地址，一行一个，  
也可直接配置成批量模式，如下的地址，则表示pn=0 到 pn=10的是个页面  
https://www.baidu.com/s?wd=test&pn={0-10}

可从接口获取
在本地web服务这边写了一个demo。具体外部接口获取地址需要自行实现一个接口。

接口调用时返回地址，如果没有了则返回空即可。

兼容场景如地址上带有一些时间戳，加密字符等特殊符号

#### 爬取数据配置

类似于配置流程事务，先通过一个方式选择一个唯一元素选择器。

然后配置事件操作，延时，dom检查等。

这边一般用getvalue，getcustomvalue事件操作。

（一般可以设置延时为0，开启dom检查）

#### 其他

后台运行：不开启使用当前浏览器开一个新tab来爬取数据，
开启后使用新开一个chrome，并最小化来运行，并在结束后关闭。

定时运行：同上流程事务定时运行

## 源码事务

![image](/img/mypost/2021/1-14.jpg)

提供源码注入的基本实现。

注：代码中可以获取document，但不能获取原页面中的js变量。

另附可以自定义在哪些页面注入。

同时也支持运行，定时运行，开启注入。

### 配置事务

点击事务名称进入配置页，

首先选择注入的 **匹配地址**，默认为全地址。

然后**写要注入的代码**，可以使用jquery。

保存后，**开启注入**则是生效。

## 受控事务

![image](/img/mypost/2021/1-15.jpg)

实现了鼠标键盘的录制和还原。

由本地python实现，插件提供数据交互。

### 配置事务

点击事务名称，进入配置页

首先配置要打开的网页。

点击 **录制操作**，进入录制

录制完，键盘按esc结束录制

点击 **受控运行** 则是回放刚刚的录制

## 我的看板

![image](/img/mypost/2021/1-16.jpg)

我的看板这边默认覆盖使用的是浏览器的新tab页。  

当然也可以主动关闭，使用命令
> bash main.sh close_dashboard

要在开启的话
> bash main.sh close_dashboard

目前看板包含两种内容：
- 单独一个页面元素的展示；
- 爬虫数据表格的展示；

添加页面元素到看板，实际使用的是流程事务，  
条件则为 事务的第一个事件为 **当前页跳转**， 最后一个事件为 **元素唯一展示**

符合条件的在主页会出现添加到看板选项。

并发爬虫事务也有一个操作是添加看板，点击则可以将爬到的数据到看板以表格展示。

### 看板操作与排版

![image](/img/mypost/2021/1-18.jpg)

将鼠标移动到看板中间的最上面，会出现排版，重置操作

点击排版，每块元素都会变成绿色，可以调整大小与位置，或者点击删除

调整完后点击保存按钮可以保存。

点击重置则会还原到最初的位置与大小。

### 简单看板模式

![image](/img/mypost/2021/1-17.jpg)

在主页点击开关开启，开启简单看板模式后，就不可以自己配置事务。

点击页面添加看板，就可以到页面中选择元素。

同上粉色边框展示选中元素。

点击确认后，选择一个选择器。

选择器列表还是从 最子元素，往上的所有父元素。

已到选择器上会出现红色蒙版。

在点击后，则会出现确认添加到看板，

确认则可以直接将这个元素添加到看板。

同时也会生成一个流程事务（只是看不到）


# 演示用例

复制下面的json字符串，走导入事务的流程即可

### 基本操作
实现效果：打开百度，设置搜索为天气，点击搜索
```json
{"case_name":"基本操作","case_process":[{"n":"0","opera":"newpage","tag":"body","value":"https://www.baidu.com/s?ie=UTF-8&wd=test","wait":"1"},{"n":"0","opera":"value","tag":"INPUT#kw","value":"天气","wait":"2"},{"n":"0","opera":"click","tag":"INPUT#su","value":"","wait":"1"}],"case_sourcecode":"","case_type":"process","control_url":"","sourcecode_url":".*"}
```

### 取值事件
实现效果：打开我的博客主页，获取标题，打开百度，搜索获取到的标题
```json
{"case_name":"取值事件用例","case_process":[{"n":"0","opera":"newpage","tag":"body","value":"http://blog.ganjiacheng.cn/","wait":"1"},{"n":"0","opera":"getvalue","tag":"HTML.macos.desktop.landscape > BODY > NAV.navbar.navbar-default.navbar-custom.navbar-fixed-top > DIV.container-fluid > DIV.navbar-header.page-scroll > A.navbar-brand","value":"title","wait":"3"},{"n":"0","opera":"pagejump","tag":"body","value":"https://www.baidu.com/s?ie=UTF-8&wd=test","wait":"2"},{"n":"0","opera":"value","tag":"INPUT#kw","value":"title","wait":"1"},{"n":"0","opera":"click","tag":"INPUT#su","value":"","wait":"1"}],"case_sourcecode":"","case_type":"process","control_url":"","sourcecode_url":".*"}
```

### 百度去广告(源码事务)
实现效果：百度去广告
```json
{"case_name":"百度去广告","case_process":[],"case_sourcecode":"Array.from(\n            document.querySelectorAll('#content_left>div'))\n            .forEach(el => \n                />广告</.test(el.innerHTML) && el.parentNode.removeChild(el)\n        );\nsetInterval(() => {\n    try{\n        Array.from(\n            document.querySelectorAll('#content_left>div'))\n            .forEach(el => \n                />广告</.test(el.innerHTML) && el.parentNode.removeChild(el)\n        )\n    } catch(e){}\n}, 1000)\n","case_type":"sourcecode","control_url":"","sourcecode_url":"baidu.com.*","start_inject":true}
```

### 定时喝水(源码事务)
实现效果：每60分钟发出alert提醒喝水
```json
{"case_name":"定时喝水","case_process":[],"case_sourcecode":"alert(\"你该喝水咯\")","case_type":"sourcecode","control_url":"","last_runtime":1599706892179,"runtime":"60m","sourcecode_url":".*"}
```

### 值选择器用例
实现效果：div{xx}可以选择值为xx的div标签，适用于页面元素匹配的补充
```json
{"case_name":"值选择器用例","case_process":[{"n":"0","opera":"newpage","tag":"body","value":"http://blog.ganjiacheng.cn/","wait":"1"},{"n":"0","opera":"click","tag":"a{About}","value":"","wait":"2"},{"n":"0","opera":"click","tag":"a{Archives}","value":"","wait":"2"},{"n":"0","opera":"click","tag":"a{Home}","value":"","wait":"2"}],"case_sourcecode":"","case_type":"process","control_url":"","sourcecode_url":".*"}
```

### 并发爬虫事务用例(爬取百度搜索前10页的每页前三条结果)
实现效果：爬取百度搜索test前10页的前三条标题
```json
{"case_name":"爬虫用例","case_process":[],"case_sourcecode":"","case_type":"paral_crawler","control_url":"","paral_crawler":{"api":"http://127.0.0.1:12580/crawler/","apicb":false,"cc":5,"data":[],"fetch":[{"check":true,"expr":"new Date()","n":"0","opera":"getcustomvalue","tag":"body","value":"时间","wait":"0"},{"check":true,"expr":"","n":"0","opera":"getvalue","tag":"h3","value":"标题1","wait":"0"},{"check":true,"expr":"","n":"1","opera":"getvalue","tag":"h3","value":"标题2","wait":"0"},{"check":true,"expr":"","n":"2","opera":"getvalue","tag":"h3","value":"标题3","wait":"0"}],"freq":1,"send":false,"urlapi":"http://127.0.0.1:12580/crawler/url/","urls":["https://www.baidu.com/s?wd=test&pn={0-10}0"]},"sourcecode_url":".*"}
```

### 后台运行流程事务 + 消息通知用例
实现效果：流程事务在后台运行，打开百度，搜索天气，点击搜搜，获取到天气的框中的值，发送系统消息
```json
{"case_name":"后台运行+消息发送","case_process":[{"bgopen":true,"check":false,"expr":"","n":"0","opera":"newpage","sysmsg":false,"tag":"body","value":"https://www.baidu.com/s?ie=UTF-8&wd=test","wait":"0"},{"check":true,"expr":"","n":"0","opera":"value","tag":"INPUT#kw","value":"天气","wait":"0"},{"check":true,"expr":"","n":"0","opera":"click","tag":"INPUT#su","value":"","wait":"0"},{"bgopen":false,"check":true,"expr":"","n":"0","opera":"getvalue","tag":"DIV#content_left > DIV.result-op.c-container.xpath-log > DIV.op_weather4_twoicon_container_div > DIV.op_weather4_twoicon > A.op_weather4_twoicon_today.OP_LOG_LINK","value":"key","wait":"1"},{"bgopen":false,"check":true,"expr":"","n":"0","opera":"sendmessage","sysmsg":true,"tag":"DIV#wrapper_wrapper","value":"天气：${key}","wait":"0"}],"case_sourcecode":"","case_type":"process","control_url":"","fail_rerun":false,"last_runtime":1611820796375,"runtime":"","sourcecode_url":".*"}
```


# asd