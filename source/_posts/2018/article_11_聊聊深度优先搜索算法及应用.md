
---
title: 聊聊深度优先搜索算法及应用
catalog: true
date: 2018-3-31 15:45:20
---

之前看算法书对于深搜一直是一个坎，有点难以理解或者理解了一些但没法下手写，这回来重新探讨一下个人目前的理解及解决方案。文章从全排入手，到解决八皇后，和尚妖怪过河等问题。<!--more-->

首先，看一个全排序，传入一个数组（其中有n个可不等长的数组），得到的结果是其中每个数组取一个数组成的新数组的集合，如下
<pre>result=[0]*3
arr=[[1,2,3],[4,5],[7,8,9]]
res=[]
#算法部分，遍历其中每个数组，在result保存临时一个数组。
#copy是因为append只是插入了一个类似指针，而result内容会变，因此要用copy换一个地址。
def dfs(arr, depth):
    global res
    for i in range(len(arr[depth])):
        result[depth] = arr[depth][i]
        if depth != len(arr) - 1:
            dfs(arr, depth + 1)
        else:
            res.append(result.copy())
dfs(arr,0)
print(res)
#结果为
[[1, 4, 7], [1, 4, 8], [1, 4, 9], [1, 5, 7], [1, 5, 8], [1, 5, 9], [2, 4, 7], [2
, 4, 8], [2, 4, 9], [2, 5, 7], [2, 5, 8], [2, 5, 9], [3, 4, 7], [3, 4, 8], [3, 4
, 9], [3, 5, 7], [3, 5, 8], [3, 5, 9]]</pre>
在来看个升级版，一个数组如[1,2,3,4,5]的全排，这里for中递归的思路则和上次基本不一样，用的是交换，遍历完所有可能的交换值，但因为只有一个数组，所以交换完保存数后还得在交换回来，也就是递归下面一行和上面一行的区别。
<pre>COUNT=0  
res=[]

#for第一次是0和所有交换，递归后是1和所有的交换
#但运行过程则会0和0换，之后跳到递归中1和1换，直到最后，得到第一情况，也就是没换，这时begin=end
#然后回退一步，那时begin应该是end-1，所以最后两个换下，又得到一种情况。
#就这样回退到最初的for，就可以遍历所有交换情况
def perm(n,begin,end):  
    global COUNT,res
    if begin&gt;=end:  
        res.append(n)
    else:  
        i=begin  
        for num in range(begin,end):  
            n[num],n[i]=n[i],n[num] 
            perm(n.copy(),begin+1,end)
            n[num],n[i]=n[i],n[num]

N=4
n=[i for i in range(N)]
perm(n,0,len(n))
print(res)</pre>
然后看几个应用，基本也是自己学了之后用上去！

第一个，九宫格中文输入得到输入项的所有组合。用到上面第一个全排序，只需要把输入转换成已按按键的字母数组。如
<pre>arr=[[a,b,c],[c,d,e],[g,h,i]]</pre>
第二个，八皇后，也就是8*8棋盘上放8个皇后，每个皇后横竖左斜右斜都不能有其他皇后。总共有92中情况。这里的解法便是先得到长为8的数组的全排，在逐个检验，当然检验是有技巧的。
<pre>#这里把数组如[1,2,3,4,5,6,7,8]下标作为棋盘x，值作为棋盘y
#因为横竖都不在线上，所以求全排
#然后检查的就是左斜右斜便可
#全排，请看前面的讲解
COUNT=0  
def perm(n,begin,end):  
    global COUNT,res
    if begin&gt;=end:  
        res.append(n)
    else:  
        i=begin  
        for num in range(begin,end):  
            n[num],n[i]=n[i],n[num] 
            perm(n.copy(),begin+1,end)
            n[num],n[i]=n[i],n[num]
res=[]
N=8
n=[i for i in range(N)]
perm(n,0,len(n))

#检验的是数组中有没有重复值
def check(l):
    return len(set(l))==len(l)

result = []

#左斜的位置x-y相同的会在一条线上，右斜的位置x+y相同的会在一条线上。
#由此检验
for i in res:
    s = [i[j]+j for j in range(N)]
    c = [i[j]-j for j in range(N)]
    if check(s) and check(c):
        print(i)
        result.append(i)
#得到92个解
print(len(result))</pre>
最后一个应用：和尚与妖怪过河问题。

问题大致是河左岸有三个妖怪三个和尚，要全部过河到右岸，有一条能载两人的船，只要左岸或右岸妖怪数大于和尚数，妖怪就会把和尚吃掉。需得所有简单解法（中间不包括重复循环步骤）。

关键点和上面的其实是差不多，只是比较难抽象出遍历的东西，一不小心就会死在中间的死循环。
<pre>class River():
    def __init__(self):
        self.ship = 1 #1--左岸，-1--右岸
        self.left = [3,3] #和尚，妖怪
        self.right = [0,0] #和尚，妖怪
        #状态改变只有这五种和取反后的五种
        self.change = [ [-1, -1],
                        [-2, 0],
                        [0, -2],
                        [-1, 0],
                        [0, -1]]
        #保存上一个状态，直接排除一样的来回
        self.lastState = -1
        #如果遍历是一棵树，保存的则根到某个枝条
        self.lineHis = [[3, 3, 0, 0, 1]]
    #改变状态
    def move(self,n):
        self.left = [self.left[i]+self.ship*self.change[n][i] for i in range(2)]
        self.right = [self.right[i]-self.ship*self.change[n][i] for i in range(2)]
        self.ship = -self.ship
        self.lastState = n
    #获取下一步可移动点，比如只有一个怪兽在左岸，就要排除两个妖怪过河的方案，这个剪枝很重要。
    def getState(self):
        states = []
        if self.ship == 1:
            state = self.left
        else:
            state = self.right
        for i in range(len(self.change)):
            if min(state[0]+self.change[i][0],state[1]+self.change[i][1])&gt;=0:
                states.append(i)
        return states
    #主算法部分，断掉妖怪大于和尚的分支。
    #在遍历中，最重要的一步就是在这条支线上，如果这一种状态之前出现过，就不要继续深入。
    def dfs(self):
        if self.left==[0,0] and self.right==[3,3]:
            print(self.lineHis)
            return 
        elif (self.left[1]&gt;self.left[0] and self.left[0]!=0) or (self.right[1]&gt;self.right[0] and self.right[0]!=0):
            return
        else:
            states = self.getState()
            for i in states:
                if i != self.lastState:
                    self.move(i)
                    self.lineHis.append(self.left+self.right+[self.ship])
                    if self.lineHis[-1] not in self.lineHis[0:-1]:
                        self.dfs()
                    self.move(i)
                    self.lineHis.pop()
        
if __name__ == "__main__":
    s = River()
    s.dfs()
    #可得4个最简解。</pre>
总结：深度优先搜索主要部分是提炼出搜索的树，然后好坏在于剪枝。
