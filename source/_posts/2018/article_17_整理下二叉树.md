
---
title: 整理下二叉树
catalog: true
date: 2018-4-22 13:16:24
---

在leetcode遇到二叉树就卡机，恶补下这种数据结构，想想都难。<!--more-->

首先是节点构建和插入，这里的插入形式用来下面排序，小的在左，大的在右。
<pre>class Node():
    def __init__(self, val=None, left= None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def add(self, val):
        if val &lt; self.val:
            if self.left is None:
                self.left = Node(val)
            else:
                self.left.add(val)
        else:
            if self.right is None:
                self.right = Node(val)
            else:
                self.right.add(val)</pre>
然后是三种遍历方式
<pre>#先序
def front(root,res=[]):
    if root == None:
        return
    res.append(root.val)
    front(root.left,res)
    front(root.right,res)
    return res
#中序（这个的得到的便是排序后的数组）
def middle(root,res=[]):
    if root == None:
        return
    front(root.left,res)
    res.append(root.val)
    front(root.right,res)
    return res
#后序
def end(root,res=[]):
    if root == None:
        return
    front(root.left,res)
    front(root.right,res)
    res.append(root.val)
    return res</pre>
下面是一些应用

1.判断二叉树是否是左右镜像的

思路：输入根节点左右两个节点，判断两节点是否相同，然后递归判断左节点的左节点和右节点的右节点 以及 左节点的右节点和右节点的左节点。
<pre>def judge(left,right):
    if left is None and right is None:
        return True
    if (left is None and right is not None) or (right is None and left is not None) or right.val != left.val:
        return False
    return judge(left.left,right.right) and judge(left.right,right.left)</pre>
2.二叉树最大深度

思路：左右节点分别设一个长度，进入深一层长度就加一，返回的是两者之间大的一方，也就的到所有路径深度中最大的一个。
<pre>def depth(root):
    if root is None:
        return 0
    l = depth(root.left)
    r = depth(root.right)
    return max([l,r])+1</pre>
3.左右翻转二叉树

思路：也就是把二叉树中所有的左右节点都换一下便可。
<pre>def invertTree(root):
    if root is None:
        return None
    if root.left:
        invertTree(root.left)
    if root.right:
        invertTree(root.right)
    root.left,root.right = root.right,root.left
    return root</pre>
4.二叉树右往左的叠加和

思路：设立一个全局的和，对于每个节点都加上这个和，然后更新和，把节点从右往左遍历便是把中序遍历反一下。
<pre>sum = 0
def bst(self,root):
    if root is None:
        return
    self.bst(root.right)
    root.val += sum
    sum = root.val
    self.bst(root.left)</pre>
5.最长子树长度，可不过根节点

思路：在最大深度的基础上，添加一个变量来计算每次的左右子树和。
<pre>res = 0
def depth(self,root):
    if root is None:
        return 0
    l = self.depth(root.left)
    r = self.depth(root.right)
    res = max(res,l+r)
    return max([l,r])+1</pre>
6.判断一个树是否是另一个的子树

思路：对主树递归所有节点，只要有一个是子树成立便可。每次在递归检查子树与主树是否相同，这里所有节点都要一样。
<pre>class Solution(object):
    def isSubtree(self, s, t):
        if not s or not t:
            return not s and not t
        if self.check(s,t):
            return True
        return self.isSubtree(s.left,t) or self.isSubtree(s.right,t)
    
    def check(self,s,t):
        if not s or not t:
            return not s and not t
        if s.val != t.val:
            return False
        return self.check(s.left,t.left) and self.check(s.right,t.right)</pre>
7.合并二叉树

思路：遍历两个二叉树的节点，把和加到一个二叉树上
<pre>def mergeTrees(self, t1, t2):
    if t1 is not None and t2 is not None:
        t1.left = self.mergeTrees(t1.left,t2.left)
        t1.right = self.mergeTrees(t1.right,t2.right)
        t1.val += t2.val
        return t1
    return t1 if t2 is None else t2</pre>
