
---
title: 练手c语言算法二
catalog: true
date: 2018-5-6 11:53:42
---

大华2018软件挑战赛，这里是后五题。<!--more-->

6.视频编解码。16进制的数存储，加些简单的判断（开头判断，结尾判断，中间舍去部分判断）。
<pre>#include "stdio.h"

int main(){
    int T,k,x=0,y=0,tmp=0;
    scanf("%d",&amp;T);
    int res[10000],ns[T];
    for(k=0;k&lt;T;k++){
        int n,i,start=0,t=0;
        scanf("%d",&amp;n);
        int nums[n];
        for(i=0;i&lt;n;i++){
            scanf("%x",&amp;nums[i]);
        }
        for(i=0;i&lt;n-3;i++){
            if(start==5 &amp;&amp; nums[i-2]==0 &amp;&amp; nums[i-1]==0 &amp;&amp; nums[i]==03 &amp;&amp; nums[i+1]==0){
                continue;
            }
            if(nums[i]==0 &amp;&amp; nums[i+1]==0 &amp;&amp; nums[i+2]==01 &amp;&amp; start==0){
                start=1;
            }
            if(nums[i]==0 &amp;&amp; nums[i+1]==0 &amp;&amp; nums[i+2]==01 &amp;&amp; start==5){
                start=0;
            }
            if(start&gt;=1 &amp;&amp; start&lt;=4){
                start++;
            }
            if(start==5){
                res[x]=nums[i];
                x++;
                t++;
            }
        }
        ns[k] = t;
    }
    for(k=0;k&lt;T;k++){
        for(y=0;y&lt;ns[k];y++){
            printf("%x ",res[y+tmp]);
        }
        tmp += ns[k];
        printf("\n");
    }
}</pre>
7.不重复最长子串长度。也是状态转移，一个变量指在子串左边，一个在右边移动。另外用一个数组存位置和判断值是否存在。
<pre>#include "stdio.h"
#define max(a,b) ((a)&gt;(b)?(a):(b))

int main(){
    int T,k;
    scanf("%d",&amp;T);
    int res[T];
    for(k=0;k&lt;T;k++){
        int l1,i,tmp,ml=0,left=0,m=0;
        char s[100],asc[26];
        scanf("%s",&amp;s);
        for(l1=0;s[l1]!='\0';++l1);
        for(i=0;i&lt;26;i++){
            asc[i]=-1;
        }
        for(i=0;i&lt;l1;i++){
            tmp = s[i]-97;
            if(asc[tmp]==-1 || asc[tmp]&lt;left){
                asc[tmp]=i;
            }else{
                left=asc[tmp]+1;
                asc[tmp]=i;
            }
            m = max(i-left+1,m);
        }
        res[k]=m;
    }
    for(k=0;k&lt;T;k++){
        printf("%d\n",res[k]);
    }
}</pre>
8.二进制位数和等于十进制位数和。这边就暴力的每个算过来判断是不是这种数。
<pre>#include "stdio.h"

int judge(n){
    int b=n,tmp=0;
    while(b!=0)
    {
        tmp+=b%2;
        b=b/2;
    }
    b=n;
    while(b!=0){
        tmp-=b%10;
        b=b/10;
    }
    if(tmp==0){
        return 1;
    }else{
        return 0;
    }
}

int main(){
    int T,k;
    scanf("%d",&amp;T);
    int result[T];
    for(k=0;k&lt;T;k++){
        int n,i,res=0;
        scanf("%d",&amp;n);
        for(i=1;i&lt;=n;i++){
            res+=judge(i);
        }
        result[k]=res;
    }
    for(k=0;k&lt;T;k++){
        printf("%d\n",result[k]);
    }
}</pre>
9.买卖交易。这个和leetcode上有个讲股票买卖的差不多，就每次后面比前面大的话就卖出买入就可以。
<pre>#include "stdio.h"

int calc(int *nums,int n){
    int i,res=0;
    for(i=0;i&lt;n-1;i++){
        res += nums[i+1]&gt;nums[i]?nums[i+1]-nums[i]:0;
    }
    return res;
}

int main(){
    int T,k,n,i;
    scanf("%d",&amp;T);
    int res[T];
    scanf("%d",&amp;n);
    int nums[n];
    for(k=0;k&lt;T;k++){
        for(i=0;i&lt;n;i++){
            scanf("%d",&amp;nums[i]);
        }
        res[k] = calc(nums,n);
    }
    for(k=0;k&lt;T;k++){
        printf("%d\n",res[k]);
    }
}</pre>
10.二叉树右视图，主要还是用先序构建二叉树，右视图的话就是右子树优先遍历即可。
<pre>#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;malloc.h&gt;

typedef int   ElemType;
typedef struct BiTNode{
    ElemType   data;
    struct BiTNode*lChild, *rChild;
}BiTNode, *BiTree;

int i=0,maxdepth=0,al=0;
int res[100],nums[100];

int CreateBiTree(BiTree *T,char *s)
{
    ElemType ch;
    ch = s[i];
    i++;

    if(ch=='#'){
        *T = NULL;
    }else{
        *T = (BiTree)malloc(sizeof(BiTNode));
        if (!(*T)) exit(-1);

        (*T)-&gt;data = ch-'0';
        CreateBiTree(&amp;(*T)-&gt;lChild,s);
        CreateBiTree(&amp;(*T)-&gt;rChild,s);
    }
    return 1;
}

void calc(BiTree T, int depth){
    if(depth&gt;maxdepth){
        res[maxdepth+al] = T-&gt;data;
        maxdepth = depth;
    }
    if(T-&gt;rChild!=NULL) calc(T-&gt;rChild, depth+1);
    if(T-&gt;lChild!=NULL) calc(T-&gt;lChild, depth+1);
}

int main(void)
{
    int t,k,all=0;
    scanf("%d",&amp;t);
    BiTree T;
    for(k=0;k&lt;t;k++){
        i=0;
        T = NULL;
        maxdepth=0;
        char s[1000];
        scanf("%s",&amp;s);
        CreateBiTree(&amp;T,s);
        calc(T,1);
        al+=maxdepth;
        nums[k]=maxdepth;
    }
    for(i=0;i&lt;t;i++){
        for(k=0;k&lt;nums[i];k++){
            printf("%d",res[k+all]);
        }
        all+=nums[i];
        printf("\n");
    }
}</pre>
