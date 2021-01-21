
---
title: node+express+mongodb初试
catalog: true
date: 2018-2-26 18:44:10
---

新尝试另一个语言node.js和框架express，记录一些基本的操作与技巧。<!--more-->

此次最大的不同是node.js是异步的，有些操作就不那么直观。

这里在linux centos做测试。前提先安装好node.js和npm。

这里也类似上次flask完成一个登陆与增删改操作的接口。

先用命令行直接生成一个项目
<pre class="language-sh"><code class="language-sh" translate="no">npm install express-generator -g
express --view=pug myapp
</code>cd myapp &amp;&amp; npm install npm start<code class="language-sh" translate="no"></code></pre>
app.js主文件
<pre>//最后两个为session所需库，还有mongodb库，需自行下载
//npm install --save express-session,session-file-store,mongodb
var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('express-session');
var FileStore = require('session-file-store')(session);

#引入路由文件
var RetInfo = require("./common/retinfo");
var index = require('./routes/index');
var users = require('./routes/users');
var manage = require('./routes/manage');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

//解析请求body
// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
//开启并设置session
app.use(session({
    secret: 'chyingp',
    store: new FileStore(),
    saveUninitialized: false,
    resave: false,
    cookie: {
        maxAge: 24*60*60*1000
    }
}));
//绑定路由，中间件
app.use('/', index);
app.use('/users', users);
//不设置的则下面的路由都会运行这个函数
app.use(function(req,res,next) {
    var sess = req.session;
    var loginUser = sess.loginUser;
    if(loginUser===undefined) return res.json(RetInfo.error("login out"));
    next();
});
//绑定另一个中间件，需登录后
app.use('/manage',manage);
//错误处理
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;</pre>
根目录下 新建一个文件夹common/用于存放通用函数，下面写了两种形式。

common/retinfo.js 用于接口返回数据
<pre>module.exports = {
    response : function(sts,msg) {
        return {"sts":sts,"msg":msg}
    },
    success : function() {
        return this.response(1,"success")
    },
    error : function(msg) {
        return this.response(-1,msg)
    },
    dberr : function(msg) {
        return this.response(-1,"db error");
    }
}</pre>
common/mongodb.js 用于数据库操作,这里使用了promise，因为mongodb操作后会有回调函数，不方便调用，写成promise就可以用then进行下去。
<pre>//use for mongodb database 

var MongoClient = require('mongodb').MongoClient;

function Mongodb(dbName, colName){

    this.dbName = dbName;
    this.colName = colName;
    this.url = 'mongodb://localhost:27017/';

    this.fetch = function(params){
        //回调函数里没法获取到外部的this，所以再定义一下that
        var that = this;
        return new Promise(function(resolve, reject, notufy) {
            MongoClient.connect(that.url, function(err, db){
                if(err) reject(err);
                var dbo = db.db(that.dbName);
                dbo.collection(that.colName).find(params).toArray(function(err, res){
                    if(err) reject(err);
                    resolve(res);
                    db.close();
                });
            });
        });
    };

    this.save = function(params){
        var that = this;
        return new Promise(function(resolve, reject, notufy){
            MongoClient.connect(that.url, function(err, db){
                if(err) reject(err);
                var dbo = db.db(that.dbName);
                dbo.collection(that.colName).insertOne(params, function(err, res){
                    if(err) reject(err);
                    resolve(res);
                    db.close();
                });
            });
        });
    };

    this.delete = function(params){
        var that = this;
        return new Promise(function(resolve, reject, notufy){
            MongoClient.connect(that.url, function(err, db){
                if(err) reject(err);
                var dbo = db.db(that.dbName);
                dbo.collection(that.colName).deleteOne(params, function(err, res){
                    if(err) reject(err);
                    resolve(res);
                    db.close();
                });
            });
        });
    }

    this.update = function(whparams,params){
        var that = this;
        return new Promise(function(resolve, reject, notufy){
            MongoClient.connect(that.url, function(err, db){
                if(err) reject(err);
                var dbo = db.db(that.dbName);
                dbo.collection(that.colName).updateOne(whparams, {$set:params}, function(err, res){
                    if(err) reject(err);
                    resolve(res);
                    db.close();
                });
            });
        });
    }
}

module.exports = Mongodb;</pre>
然后编写中间件routes/users.js
<pre>var express = require('express');
var router = express.Router();
var RetInfo = require("../common/retinfo");
//登录
router.get('/login', function(req, res, next) {
    username = req.query.username;
    password = req.query.password;
    
    if(!username || !password) return res.json(RetInfo.error("lack of params"));

    if(username == "admin" &amp;&amp; password == "admin"){
        
        req.session.regenerate(function(err) {
            if(err) return res.json(RetInfo.error("login error"));
            req.session.loginUser = username;
            return res.json(RetInfo.success());
        });

    }else{
        return res.json(RetInfo.error("username or password error"));
    }
});
//登出
router.get("/loginout", function(req, res, next) {
    req.session.destroy(function(err) {
        if(err) return res.json(RetInfo.error("login out error"));
        return res.json(RetInfo.success());
    });
})

module.exports = router;</pre>
routes/manage.js  这里写了一般的增删改操作
<pre>var express = require('express');
var router = express.Router();
var RetInfo = require("../common/retinfo");

var Mongo = require("../common/mongodb");
DB_POSTS = new Mongo("test_database","posts");
//获取数据
router.get("/",function(req, res, next){
    DB_POSTS.fetch({}).then((data)=&gt;{
        return res.send(data);
    },(err)=&gt;{
        return res.send(RetInfo.error(err.message));
    });
})
//增加
.post("/",function(req, res, next){
    DB_POSTS.save(req.body).then((data)=&gt;{
        return res.send(RetInfo.success());
    },(err)=&gt;{
        return res.send(RetInfo.error(err.message));
    });
})
//删除
.delete("/",function(req, res, next){
    data={"_id":req.query.id}
    DB_POSTS.delete(data).then((data)=&gt;{
        return res.send(data)
    },(err)=&gt;{
        return res.send(RetInfo.error(err.message))
    });
})
//修改
.put("/",function(req, res, next){
    const params = req.body;
    DB_POSTS.update({"_id":params.id},params).then((data)=&gt;{
        return res.send(RetInfo.success());
    },(err)=&gt;{
        return res.send(RetInfo.error(err.message));
    })
})

module.exports = router;</pre>
运行的话可以有很多方法
<pre>一般运行
npm start
debug模式
DEBUG=myapp:* npm start
开发修改后自动重启
nodemon app.js
后台一直运行
forever start ./bin/www</pre>
后言：对于js语法 es6等还比较生疏，并没有涉及，可能有待改进，但总怕麻烦。。。。
