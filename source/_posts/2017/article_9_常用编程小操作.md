
---
title: 常用编程小操作
catalog: true
date: 2017-11-30 17:45:47
---

包括，批量重命名，待更新。。。

1.批量重命名  changeName.py
<pre>import os
f=os.listdir("./")
f.remove("changeName.py")
j=0
for i in f:
 os.renames(i,str(j)+".jpg")
 j+=1</pre>
2.实现数组next并循环---js版
<pre>(now+1)%array.length</pre>
3.python字典自动初始化为0
<pre>from collections import defaultdict
d=defaultdict(int)
d['count']+=1</pre>
4.linux+windows 查看端口监听并kill
<pre>#linux
netstat -apn|grep 8000
或者
ps -aux|grep 8000
kill -9 pid

#windows
netstat -ano|findstr 3000
netstat -ano</pre>
5.linux开启防火墙
<pre>firewall-cmd --zone=public --add-port=8892/tcp --permanent
systemctl restart firewalld</pre>
6.linux下python后台运行
<pre>nohup python -u filename.py &gt; filename.out 2&gt;&amp;1 &amp;
tail -f filename.out</pre>
7.git add，git commit提交错误
<pre>git status
git reset HEAD</pre>
<pre>git log
git reset --soft commit_id</pre>
如果使用hard reset 了
<pre>git reflog
git reset --hard 前面的id</pre>
8.linux查看文件行数（windows可用git bash）
<pre>cat code.py | wc -l</pre>
