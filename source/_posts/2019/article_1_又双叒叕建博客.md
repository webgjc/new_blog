---
title: "又双叒叕建博客"
catalog: true
toc_nav_num: true
date: 2019-11-13 17:05:00
subtitle: "讲讲本次建博客中间那些事"
header-img: "/img/article_header/header.jpg"
tags:
- OTHER
---

## 前言

第二次搭建博客了，第一次是用的自己的服务器搭建了wordpress博客，写了两年左右60+篇，在服务器废弃后也不再维护了。

本次又心血来潮，使用node的hexo和github的gh-pages来搭建。

开篇就以博客搭建过程为主要内容。

## 工具准备

> git, node, github账号, vscode(非必备), 域名(非必备)

这里需要自行搜索学习安装了

## 动手搭建

> 贴个官方地址
> https://hexo.io/zh-cn/

这里就不跟着官方教程走了，不过大同小异

先到 [主题页](https://hexo.io/themes/) 找个喜欢的主题

这里选了 [A-Boy](https://github.com/huweihuang/hexo-theme-huweihuang) 这个主题，🙄主要是他比较像我之前的博客风格。

```
# 下载hexo命令行工具
npm install hexo-cli -g

# 创建文件夹
mkdir blog

# 下载主题到该文件夹
git clone https://github.com/huweihuang/hexo-theme-huweihuang.git ./blog

# 下载依赖包
cd blog
npm install
```

文件组织结构大致如下
```
/_config.xml
主要配置文件

/source
存放文章 ./_posts
图片 ./img

/themes
主题的一些模板文件

/scaffolds
一些脚手架，原生就在

/node_modules
外部依赖的模块

/db.json
存储服务器解析出来的临时文章数据

/还有一些暂时用不到的文件
```

先到github建立自己的仓库，就长下面这样
![github](/img/mypost/github.png)

然后对主题的_config.xml一些配置项
```
# 配置刚才的github仓库, 一般使用gh-pages分支
deploy:
  type: git
  repo: https://github.com/<yourAccount>/<repo>
  branch: <your-branch>
```

```
# 配置路由，这里使用域名的绝对路径，相对路径会有个坑->图片写绝对路径时不会把root路径加上
url: http://ganjiacheng.cn/
root: /
```

```
# 配置主题，/theme/下的子目录文件夹
theme: huweihuang
```

```
# 侧边栏的一些配置
sidebar: true    
sidebar-about-description: "<your description>"
sidebar-avatar: img/<your avatar path>
widgets:  
- featured-tags
- short-about
- recent-posts
- friends-blog
- archive
- category
```

```
# markdown编译器的一些配置
markdown:
  render:
    html: true
    xhtmlOut: false
    breaks: true
    linkify: true
    typographer: true
    quotes: '“”‘’'
```

这里有配置背景图
推荐一个常用的[壁纸网站](https://bing.ioliu.cn/)


下面是一些命令行命令
```
# 新建文章
hexo new post "<post name>" 

# 删除临时数据库
hexo clean

# 编译为html
hexo generate 

# 开启server
hexo server

# 上传到github，第一次要写账号密码，后面就不用了
hexo deploy 
```

## 使用vscode写文章

打开建立的项目文件夹

在/source/_posts/下新建md文件为新文章

由于文章都是markdown格式，用一般文本编辑器比较困难，故而选则vscode，因为它带markdown插件，  
其他可选择的也有写文章的hexo插件 [hexo-admin](https://github.com/jaredly/hexo-admin)

command+shift+p 搜索markdown open preview to the side

就可以在左边写右边实时查看效果了

推荐一个自己记录最简markdown手册 [markdown手册](https://github.com/webgjc/ApiTestToMd/blob/master/md/markdown.md)

在markdown文件开头加上一些文章的必备信息
```
---
title: "标题"
date: 1999-01-01 00:00:00
subtitle: "副标题"
header-img: "/img/图片.jpg"
tags:
- 标签
---
```

然后开始写文章
```
此处省略一万字
```

## 介绍一些插件

原生的博客不带插件，少了很多功能，比如统计访问次数，评论系统等。

也有一些主题也内置了一些插件，直接配置即可。

由于这些功能都得带后端存储，自己做个又麻烦，因此使用一些别人做的免费的。

### 访问次数插件

这里试用下 [不蒜子](http://busuanzi.ibruce.info/) 来做访问次数。

编辑 /_config.yml 在最后加上
```
busuanzi:
  enable: true
```

找到/themes/主题名/layout/_partial/footer.ejs

在底部\</footer>标签前加上，就是网站次数统计，或者自己想加哪加哪
```
<% if (theme.busuanzi && theme.busuanzi.enable){ %>
    <script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
    <div style="text-align: center;">
        <span>
            本站总访问量<span id="busuanzi_value_site_pv"></span>次
            </span>
            <span class="post-meta-divider">|</span>
        <span>
            本站访客数<span id="busuanzi_value_site_uv"></span>人
        </span>
    </div>
<% } %>
```
下面这个是页面访问次数
```
<% if (theme.busuanzi && theme.busuanzi.enable){ %>
    <span>
        Viewed <span id="busuanzi_value_page_pv"></span> times
    </span>
<% } %>
```

### 评论插件

这里使用的是[valine](https://valine.js.org/) 和 [leancloud](https://leancloud.cn/)

valine是前端部分嵌入组件，leancloud来存储信息

注册等步骤就不贴了,看[这里](https://valine.js.org/quickstart.html)

说下嵌入的部分，在/themes/主题名/post.ejs

找个合适的标签下面加入，基本就和上面文章对齐就行

```
<script src='//unpkg.com/valine/dist/Valine.min.js'></script>
<h5>COMMENT</h5>
<div id="vcomments"></div>
<script>
    new Valine({
        el: '#vcomments',
        appId: '<AppId>', #这个要注册后拿到
        appKey: '<AppKey>', #这个同上
        notify:false, 
        verify:false, 
        avatar:'mp', 
        placeholder: '来了老弟 #markdown格式'
    })
    setTimeout(() => {
        document.getElementsByClassName("info")[0].style.display="none";
    }, 1000)
</script>
```
特地说下加settimeout那步是为了隐藏自带的power信息🙃

评论，然后就可以在leancloud 存储->结构化数据->comment看到评论信息


敲黑板，下面是重点👇😁😁

> 左边妹子的插件就搜下 [hexo live2d](https://www.baidu.com/s?ie=UTF-8&wd=hexo%20live2d) 


## 域名配置

最后来了解一下上传到github后域名配置。

在 hexo deploy 前

配置 /source/CNAME, 写解析后的域名

在买域名的域名管理处进行域名解析 

记录类型CNAME => github账号.github.io

就可以通过域名访问啦！

## 多终端同步

这个也很常见，就是在多个地方写博客，想这边写完同步到各个客户端。

如果是有自己服务器的，就装个hexo-admin的插件，开启hexo server后监听到公网端口，不放心的话入口加个认证，就可以在线编辑。

一般的做法是使用刚才建的github仓库的master分支作为文章源码，gh-pages分支作为静态博客。

```
项目根目录下/
# 引入git
git init

# 设置远程地址
git remote add origin git地址

# pull一下远程的提交，有冲突就解决下/文件备份/重命名
git pull origin master --allow-unrelated-histories

# 添加.gitignore，加入
public/
.vscode
node_modules

# git三连
git add .
git commit -m ""
git push origin master
```

终端使用写博客前先clone / pull一下，

写完deploy后 再 git三连就行

## 拓展内容

自建主题

别人的主题要自定义的话还是改很多，有想法可以自行开发主题

从上面基本也可以知道主题的就是在 /theme/下创建的文件夹,  
然后修改_config.yml的主题配置

```
主题下主要文件结构
/layout # 主要布局，样式文件
/source # 外部js css等
_config.yml # 配置文件
```
数据主要靠模板的方式加载，其他还是和原生js差不多

贴个不错的[教程](https://www.cnblogs.com/yyhh/p/11058985.html)

## 最后一席话

github有时会被墙，有时会访问慢，这个国内不一定稳定🤔

体验来说相比于简书等来说，搭建过程还是需要一定基础，写起来也都markdown，

但胜在可以自定义花里胡哨的东西(装逼万岁)。

为了坚持写博客之前一直用的是先立标题文章，几星期过去有想法和方法了再去填充完成剩下的文章内容，这个一直都还不错。

希望这个博客可以坚持久一些~