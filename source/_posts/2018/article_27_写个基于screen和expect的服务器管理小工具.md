
---
title: 写个基于screen和expect的服务器管理小工具
catalog: true
date: 2018-8-29 20:14:06
---

日常管理的服务器如果很多，总会感觉连完这个连那个，要么要重复输入用户密码，要么在如xshell中的一个长列表中找寻所需的服务器。比较难受就自己写个工具来连接多台服务器，并用screen保持会话。<!--more-->

先配环境，此处默认centos咯。
<pre>yum install -y screen
yum install -y expect</pre>
由于ssh连接要输入用户密码，因此得写expect脚本。

先创建一个ssh.conf用来放需要连接的服务器,格式为
<pre>name1 root@192.168.1.1 password1
name2 root@192.168.1.2 password2</pre>
同目录下写个expect脚本screen.sh，修改其权限为755.
<pre>chmod 755 screen.sh</pre>
主要功能为创建screen，登录用户名密码。
<div class="highlight">
<pre> 1 #!/bin/expect -f 
 2 
 3 set timeout 30
 4 
 5 set fid [open screen.conf r]
 6 while {[gets $fid line] &gt;= 0} {
 7     set name [lindex $line 0]
 8     set port [lindex $line 1]
 9     set pwd [lindex $line 2]
10     spawn screen -S $name ssh $port
11     expect {
12         "*yes/no" { send "yes\r"; exp_continue }
13         "*password:" { send "$pwd\r" } 
14     }
15     expect { 
16         "Last login*" {
17             send "\01d"
18         }
19     }
20     puts "$name | $port added"
21 }</pre>
再在同目录下创建个start.sh

用于检测有哪些会话没起来写入screen.conf,再调用screen.sh重启一遍。
<div class="highlight">
<pre> 1 #!/bin/bash
 2 
 3 while true
 4 do
 5 
 6     rm -rf screen.conf
 7 
 8     n=0
 9 
10     while read ll
11     do
12         name=`echo $ll |awk '{print $1}'`
13         ss=`screen -ls |grep "\.$name"`
14         if [ ${ #ss} -lt 5 ];then
15             echo $ll &gt;&gt; screen.conf
16             n=`expr $n + 1`
17         fi
18     done &lt; ssh.conf
19 
20     if [ $n -gt 0 ];then
21        ./screen.sh
22     fi
23 
24     rm -rf screen.conf
25     sleep 10
26 done</pre>
运行：
<pre>nohup start.sh &gt;&gt; screen.log 2&gt;&amp;1 &amp;</pre>
</div>
<div class="highlight">

以前嫌弃没机器，性能不行，现在手头机器太多也都是烦恼呢。

</div>
</div>
