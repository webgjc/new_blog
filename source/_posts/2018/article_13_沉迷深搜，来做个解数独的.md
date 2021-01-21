
---
title: 沉迷深搜，来做个解数独的
catalog: true
date: 2018-4-2 09:29:14
---

还记得以前高中默默盯着数独的能看半天，然后还一个个凑，这回来彻底解决一下这个问题。顺便理清一下深度优先搜索的设计流程。<!--more-->

首先数独规则自行了解，这里做最基础的9宫格数独。

拿到数独题，分一部分已知点和一部分未知点，未知点的状态是有限的，每个点都不能与横竖加九宫格内的数重复，因此可以根据这个遍历所有状态。
<pre>深度优先搜索设计
for 上一个点的可用状态：
    尝试下点
    进入下一个点（递归）
    还原下点(回溯)</pre>
<pre>剪枝过程
一大部分都在获取可用状态中去掉了（上一步下错的话，总有下一步会出现无可用状态）
然后还要限制的是到最终点停止</pre>
<pre>判断成功
只要数独状态中全部下满了，就是成功了</pre>
<pre>class ShuDu():
    #初始化数独长度，数独空点位置
    def __init__(self,state):
        self.STATE = state
        self.N = len(self.STATE[0])
        self.ZERO = [[i,j] for i in range(self.N) for j in range(self.N) if self.STATE[i][j] == 0]
        self.hasAnswer = 0
    #获取空点的可用状态
    def get_state(self,n):
        tmp_state = []
        for i in range(self.N):
            tmp_state.append(self.STATE[self.ZERO[n][0]][i])
            tmp_state.append(self.STATE[i][self.ZERO[n][1]])
        tmp_ny = int(self.ZERO[n][0] / 3)
        tmp_nx = int(self.ZERO[n][1] / 3)
        for i in range(tmp_ny * 3, tmp_ny * 3 + 3):
            for j in range(tmp_nx * 3, tmp_nx * 3 + 3):
                tmp_state.append(self.STATE[i][j])
        '''
        if self.ZERO[n][0] == self.ZERO[n][1]:
            for i in range(self.N):
                tmp_state.append(self.STATE[i][i])
        if self.ZERO[n][0] + self.ZERO[n][1] == 8:
            for i in range(self.N):
                tmp_state.append(self.STATE[i][self.N-1-i])
        '''
        return [i for i in range(1,self.N+1) if i not in list(set(tmp_state))]
    #深度优先搜索部分
    def dfs(self,k=0):
        if "0" not in str(self.STATE):
            self.hasAnswer = 1
            for i in range(self.N):
                print(self.STATE[i])
        if k &gt;= len(self.ZERO) or self.hasAnswer == 1:
            return
        for i in self.get_state(k):
            self.STATE[self.ZERO[k][0]][self.ZERO[k][1]] = i
            self.dfs(k+1)
            self.STATE[self.ZERO[k][0]][self.ZERO[k][1]] = 0

if __name__ == "__main__":
    #据说是最难数独，0代表空的点
    state = [[8,0,0,0,0,0,0,0,0],
             [0,0,3,6,0,0,0,0,0],
             [0,7,0,0,9,0,2,0,0],
             [0,5,0,0,0,7,0,0,0],
             [0,0,0,0,4,5,7,0,0],
             [0,0,0,1,0,0,0,3,0],
             [0,0,1,0,0,0,0,6,8],
             [0,0,8,5,0,0,0,1,0],
             [0,9,0,0,0,0,4,0,0]]
    s = ShuDu(state)
    #秒秒钟解出来
    s.dfs()</pre>
<pre>结果为：
[8, 1, 2, 7, 5, 3, 6, 4, 9]
[9, 4, 3, 6, 8, 2, 1, 7, 5]
[6, 7, 5, 4, 9, 1, 2, 8, 3]
[1, 5, 4, 2, 3, 7, 8, 9, 6]
[3, 6, 9, 8, 4, 5, 7, 2, 1]
[2, 8, 7, 1, 6, 9, 5, 3, 4]
[5, 2, 1, 9, 7, 4, 3, 6, 8]
[4, 3, 8, 5, 2, 6, 9, 1, 7]
[7, 9, 6, 3, 1, 8, 4, 5, 2]</pre>
