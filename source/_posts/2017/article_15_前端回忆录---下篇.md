
---
title: 前端回忆录---下篇
catalog: true
date: 2017-3-20 20:14:50
---

下篇开始，对于我自己来说也就是在这边徘徊，暂时也并不能完全很好的掌握这些或深入的或新颖的知识，因为前端新东西出现的实在太快了。这里的我只大致做一个引导，如有错误请及时指出。毕竟修行在个人，还是得靠自己摸索。<!--more-->

我们还是再来学习js---js进阶。这里目前必读的一本书---泽卡斯的《js高级编程指南》，如果能啃下这本书，必定精进一大步。当初我也是略读读了几次，能感受到他的强大和对我的影响力。js进阶，一方面补充了很多之前遗漏的细节，另一方面代码风格，代码思想会发生变化。学学面向对象，函数式编程，异步编程等等编程思想，对于编程的效率甚至体验都会改变。当然你会发现当初的编一行试一行的考虑肯定不是最好的，应该要站在高处看问题。如果是一个成千上万行代码的任务时，需要有总体设计的眼光。推荐在看看《js设计模式》这本。这部分时间将会非常长，当然也有无数人或停滞不前，或退而自满。任何一个行业在深入之后都不会很简单，如果你是被那三个月培训出来10k以上工资吸引进入这个行业，那就得做好打持久战的准备了，不牢固的基础在这时候会被放大。所以建议还是慢慢来，急功近利很难成为真正nb的人。

以前你是一个引用库的人，现在，你已经有能力根据自己的需求自己写一个合适自己的库或者改写别人的库，而不是之前想也不想先引用进来。虽然不提倡自己造轮子，但懂得造轮子的原理还是需要的。比如jquery这个库，没必要再去复制实现一个，但同时可以看看他实现的方法------jquery源码。从中可以学到一些设计的思想，这才是轮子的原理。

在讲点js里有趣的东西，毕竟编程很无聊，但要从无聊中寻找美的东西。canvas指的是画布，在h5里也是一个新标签，他意味着你可以用js代码在一张白纸上创作，你可以从无到有创作一个张画出来，或者把一张画复制到canvas画板上操作，之后再用js加点动作，简单的动画或者游戏就可以实现，是不是很有趣呢!更强大的是这个标签加上webgl技术就可以实现3d的创作，甚至于创作3d的游戏。

接下来开始讲一个新东西---css预处理器sass。你可以编写sass语言，然后编译成可用的css。开始你可能会奇怪写css明明好好地为什么要多一步编译呢，因为css作为一门编程语言没有很好的嵌套，继承，函数等等，这就造成写css的时候写了很多重复的代码。sass就很好的解决了这个问题，它的具体安装和语法可以看<a href="http://sass.bootcss.com/docs/guide/">文档</a>，它完全支持css3，所以它也可以帮你解决那些需要分浏览器写的代码。

js也有一些需要编译才能用的扩展语言，比如TypeScript，CoffeeScript，jsx等。他们对于js的语法做了一些改变使得一些人更容易上手，同时也对js一些危险的语法做了保护或更改。付出的代价就是每次更改需要多一步编译的工作。

突然会发现需要编译的地方好多，同时为了网页反应速度更快还得把加载的资源比如图片之类打包起来，js文件也可以进行压缩使文件更小。这些工作都是不复杂的机械式操作，所以我们可以找一个工具把这些直接完成，那就是现在讲的<a href="http://www.gulpjs.com.cn/docs/getting-started/">gulp</a>。在用他之前你先得配置好node环境----node.js和npm(node.js的包管理器)。之后再按照gulp的教程来进行操作，这里有一份gulp完成上面那些操作的模板，<a href="http://pan.baidu.com/s/1i4CpzgD">点这里下载</a>，下载完后用npm安装对应的模块，然后在代码里设置正确的路径，之后就可以运行了。他会监听指定的文件，保存之后就会自动触发，自动化了很多麻烦机械的步骤。

对于node.js，前端可以了解，亦可以有研究，毕竟是用js来写。他可以用来写后台，虽说这统一了前后端语言，让前端也可以写后台，但在目前前后端分离的情况下实现的情形并不多。我当初用他的socket模块写过一个简单的聊天室，关于socket，可以了解一下tcp/ip，三次握手等。同时，推荐一本书<a href="http://www.kancloud.cn/kancloud/tealeaf-http/43837">《http下午茶》</a>，他是讲http协议和一些请求之类，对于写后台还是很有帮助的。反正一般后台该有的node,js也可以实现，但技术肯定是有好有坏，在准备用node写后台之前最好了解一下node的优势和劣势。

再来讲最火的三个框架---angular2，react，vue。我的感觉是angular2企业内部用的较多，react可以用来搭建大型应用，vue适合轻量级的网页。就试过react，给我的感觉就是初始上手有点困难，可能不是很适合刚入门的开发者，稍微有点经验之后再来学习框架可能会有更深刻的理解。当初是被react的全家桶吸引，react和react native，毕竟也是google工程师开发出来的。前端组件化也是在react出现之后才有的名词，很多人认为这也是前端发展的大方向，或许是吧，个人有个人的理解。总有对比这三个框架的文章见到，一般就按需求来做选择，也没必要在一个框架上吊死。虽然可能学一个框架的成本并不低，但在用熟了之后会发现再也离不开，因为多多少少会被这个框架设计的思想所束缚。个人感觉框架是用来帮助人的，而不是束缚，在学框架的同时不要忘记语言本身。

学到这儿，我相信您已经可以自己完成之后的路了，后面更加深入的可以是前端的深入研究，可以是编程提高的算法与数据结构，也可以是服务器端的复杂逻辑与数据交互等等，后面的路更是丰富多彩，希望本篇前端之路只是一个开端。
