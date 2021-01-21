
---
title: flask+mongodb+gunicron初试
catalog: true
date: 2017-12-21 13:37:52
---

最近接触些python后端开发，记录下所用到的一些技术。<!--more-->

flask，这个在他的官网里也有详细文档，这里简单论述一个登录+后台管理的例子。
<pre>#引入一个蓝图，蓝图封装一些接口
from lantu import simple_page
from flask import Flask,render_template,request,session,redirect,url_for
import json
import hashlib
#定义app，secret_key主要在生成session时候用
app=Flask(__name__)
app.secret_key='gjc'
#绑定蓝图
app.register_blueprint(simple_page)
#主页跳转到登录
@app.route('/')
def index():
    return redirect(url_for('login'))
#登录判断session，有则跳转到主页
@app.route("/login")
def login():
    if "username" not in session:
        return render_template('login.html')
    else:
        return redirect(url_for('simple_page.main'))
#登录验证接口
@app.route("/login/loginYz",methods=['POST'])
def loginyz():
    psd=hashlib.sha256()
    psd.update('root'.encode('utf-8'))
    if request.form['username']!='root':
        res={
            "state":"1001",
            "result":"username error"
        }
        return json.dumps(res)
    elif psd.hexdigest()!=request.form['password']:
        res={
            "state":"1002",
            "result":"password error"
        }
        return json.dumps(res)
    else:
        session['username'] = request.form['username']
        res={
            "state":"1000",
            "result":"success",
            "linkTo":"/main"
        }
        return json.dumps(res) 
#登出接口，删除session
@app.route("/loginout")
def loginout():
    session.pop('username', None)
    return redirect(url_for('login'))
#开始出程序
if __name__=='__main__':
    app.run("0.0.0.0",debug=True)</pre>
上面绑定的蓝图
<pre>from flask import Blueprint,render_template,abort,session,request
from jinja2 import TemplateNotFound
from pymongo import MongoClient
import json
#连接mongodb数据库
client=MongoClient()
db=client.test_database
posts=db.posts
#定义一个蓝图
simple_page=Blueprint('simple_page',__name__,template_folder='templates')
#管理主页
@simple_page.route("/main")
def main():
    if "username" in session:
        data={}
        data['username']=session['username']
        data['info']=[post for post in posts.find()]
        return render_template("main.html",data=data)
    else:
        return render_template('login.html')
#增加数据
@simple_page.route("/main/add",methods=['POST'])
def add():
    post={
        "name":request.form['name'],
        "email":request.form['email'],
        "phone":request.form['tel'],
        "more":request.form['more']
    }
    if posts.insert_one(post).inserted_id!="":
        return json.dumps({"state":"1000","result":"success"})
    else:
        return json.dumps({"state":"1004","result":"insert error"})
#删除数据
@simple_page.route("/main/dele",methods=['POST'])
def dele():
    result=posts.delete_one({"name":request.form['name']})
    if result.deleted_count&gt;0:
        return json.dumps({"state":"1000","result":request.form['name']})
    else:
        return json.dumps({"state":"1005","result":"delete error"})
#修改数据
@simple_page.route("/main/edit",methods=['POST'])
def edit():
    result=posts.update_one({"name":request.form['org_name']},{"$set":{
        "name":request.form['ch_name'],
        "email":request.form['ch_email'],
        "phone":request.form['ch_phone'],
        "more":request.form['ch_more']
    } })
    if result.matched_count!=0:
        return json.dumps({"state":"1000","result":request.form['ch_name']})
    else:
        return json.dumps({"state":"1006","result":"edit error"})
    #return json.dumps({"state":"1000","result":result.matched_count})</pre>
关于前端页面这里不做展示了，接下来使用gunicorn运行该flask程序

首先可以配置一下gunicorn的config，flask项目touch一个config.py，复制如下内容，当然也可以自行修改配置，内容也可以在<a href="https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py">这里</a>下载。
<pre>bind = '0.0.0.0:8000'
backlog = 2048
workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2
spew = False
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
proc_name = None
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")</pre>
然后运行
<pre>gunicorn -c config.py main:app</pre>
就可以多线程运行flask程序啦！
