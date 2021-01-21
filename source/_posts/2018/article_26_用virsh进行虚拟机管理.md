
---
title: 用virsh进行虚拟机管理
catalog: true
date: 2018-8-21 19:49:16
---

最近做运维，觉得学得比较实用点的技能就是管理虚拟机了。<!--more-->

这里使用的环境是已经装了centos的物理机上。

首先配置所需库，用yum下载就可以
<pre>yum -y install qemu-kvm qemu-key-tools virt-manager libvirt virt-install python-virtinst bridge-utils
yum -y install kvm qemu libvirt virt-viewer qemu-system
yum -y install libguestfs-tools</pre>
在/home下mkdir创建一个vm文件夹用于存放img镜像
<pre>qemu-img create -f qcow2 /home/vm/名称.img 容量(例：100G)</pre>
当然还得有需要准备要装的系统的iso镜像

下面命令为安装虚拟机，参数分别为：虚拟机名称，cpu，内存，iso镜像路径，img镜像路径，vnc端口
<pre>virt-install \
--name name \
--vcpus=2 \
--ram 2048 \
--cdrom=/home/CentOS-7-x86_64-DVD-1511.iso –disk \
path=/home/gjc/CentOS7_DVD1511.img \
--graphics vnc,listen=0.0.0.0,port=5910</pre>
安装完的虚拟机配置文件在/etc/libvirt/qemu/xxx.xml，可以修改配置文件在virsh define xxx一下就可以更新配置。

下载打开软件tightVNC，输入对应的ip和port，连接进行对应系统的图形化安装。

这里以linux centos7.2图形安装为例：

选择Install Centos Linux7 进入下一步

配置时间为北京时间，看左下角时间可能有偏差，调整一下

进入Software Selection，左边选择Virtualization Host，右边选择virtualization Platform和Development Tools。

下面一个是磁盘分区，在物理机装的话分一下
<pre>/boot 分 2g，/swap 分 16g，/ 分 100g，其他给/home</pre>
虚拟机的话自动分配就行。

然后是配置网络，IPv4 Setting中add一个写ip（写和主机ip最后一个端不同就行），子网掩码（255.255.255.0），网关(和主机网关一样)。写一个常用的dns服务器。

IPV6设置ignore

点击install就开始安装

然后设置root用户的密码，就可以等待安装完成。

虚拟机和主机通过桥连。

主机网络配置：在/etc/sysconfig/network-scripts/下加一个ifcfg-br0网卡，配置连接方式为桥连，其他与之前配置的网卡一样。

改之前的网卡的BRIDGE为br0，其他ipv4设置的一些都可以去掉。

虚拟机的话就之前安装时写的网络配置就行。

以下是virsh日常管理操作
<pre>列出running的虚拟机 (--all)为所有虚拟机
virsh list
开关虚拟机
virsh start name
virsh shutdown name/num
virsh destroy name/num
删除虚拟机，删除前需关闭
virsh undefine name
虚拟机快照(很有用)
virsh snapshot-list name/num
虚拟机快照回退，回退后要到具体的机器上校准时间
virsh snapshot-revert name/num snapid
删除快照
virsh snapshot-delete name/num snapid
克隆虚拟机
virt-clone -o 克隆虚拟机名称 -n 目标虚拟机名称 -f 路径/name.img</pre>
下面是克隆虚拟机的全部过程脚本
<pre>name=clone1 #虚拟机名称
port=5901 # vnc端口
ip=192.168.199.63 #虚拟机网卡ip
dir=/home/vm/ #img路径
virsh destroy base #基础虚拟机叫base
rm -rf $dir$name.img
virt-clone -o base -n $name -f $dir$name.img #克隆
virt-copy-out -d $name /etc/sysconfig/network-scripts/ifcfg-eth0 ./
sed -i "s/IPADDR=.<em>/IPADDR=\"$ip\"/" ifcfg-eth0 #改网卡
virt-copy-in -d $name ./ifcfg-eth0 /etc/sysconfig/network-scripts/
rm -rf ./ifcfg-eht0
sed -i "s/&lt;graphics.</em>//" /etc/libvirt/qemu/$name.xml #改配置
virsh define /etc/libvirt/qemu/$name.xml
virsh start $name #重启
virsh start base</pre>
其中用的较多的就是克隆和快照，一个方便复制机器，一个方便回到过去。

掌握这两个日常虚拟机管理就基本无压力咯。
