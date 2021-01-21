
---
title: 练手c语言算法一
catalog: true
date: 2018-5-6 11:53:07
---

大华2018年软件挑战赛初赛题

<a href="/img/uploads/2018/05/%E5%88%9D%E8%B5%9B.xlsx">初赛　十道题，题目此在</a>，主要讲讲自己的思路，这里是前五题。<!--more-->

１.不相邻最大子序和。不相邻所以奇偶分开写状态转移，然后取两者较大值。类似于leetcode中house robber。
<pre>#include "stdio.h"
#define max(a,b) ((a)&gt;(b)?(a):(b))

int calc(int *nums,int n){
    int a=0,b=0,i;
    for(i=0;i&lt;n;i++){
        if(i%2 == 0){
            a = max(b,a+nums[i]);
        }else{
            b = max(a,b+nums[i]);
        }
    }
    return max(a,b);
}

int main(){
    int T,i,n,j;
    scanf("%d",&amp;T);
    int res[T];
    for(i=0;i&lt;T;i++){
        scanf("%d",&amp;n);
        int nums[n];
        for(j=0;j&lt;n;j++){
            scanf("%d",&amp;nums[j]);
        }
        res[i] = calc(nums,n);
    }
    for(i=0;i&lt;T;i++){
        printf("%d\n",res[i]);
    }
}</pre>
2.链表部分翻转。我还是用数组实现的，翻转就是遍历前一半的长度，和后一半换一下。然后在数组分割的每部分调用这个翻转完成。
<pre>#include "stdio.h"

void reverse(int *arr,int n,int start){
    int m=(n+1)/2+start,i,j,tmp;
    for(i=start;i&lt;m;i++){
        j=n+2*start-i-1;
        tmp=arr[i];
        arr[i]=arr[j];
        arr[j]=tmp;
    }
}

int main(){
    int n,i,j,k,l,T,z=0,tmp=0;
    scanf("%d",&amp;T);
    int res[1000],kk[10];
    for(k=0;k&lt;T;k++){
        j=0;
        scanf("%d",&amp;n);
        kk[k] = n;
        int nums[n];
        for(i=0;i&lt;n;i++){
            scanf("%d",&amp;nums[i]);
        }
        scanf("%d",&amp;l);
        while(j+l&lt;=n){
            reverse(nums,l,j);
            j+=l;
        }
        reverse(nums,n-j,j);
        for(i=0;i&lt;n;i++){
            res[z+i]=nums[i];
        }
        z+=n;
    }
    for(k=0;k&lt;T;k++){
        for(i=tmp;i&lt;kk[k]+tmp;i++){
            printf("%d ",res[i]);
        }
        tmp+=kk[k];
        printf("\n");
    }
}</pre>
3.霍夫曼编码，这里有参考网上的算法代码，<a href="https://blog.csdn.net/wtfmonking/article/details/17150499">参考地址</a>，也不用造轮子啦。
<pre>#include&lt;stdio.h&gt;
#include&lt;stdlib.h&gt;

typedef int ElemType;
struct BTreeNode
{
    struct BTreeNode* left;
    struct BTreeNode* right;
    ElemType data;
};

void PrintBTree_int(struct BTreeNode* BT)
{
    if (BT != NULL)
    {
        printf("%d", BT-&gt;data);
        if (BT-&gt;left != NULL || BT-&gt;right != NULL)
        {
            printf("(");
            PrintBTree_int(BT-&gt;left);
            if (BT-&gt;right != NULL)
                printf(",");
            PrintBTree_int(BT-&gt;right);
            printf(")");
        }
    }
}

struct BTreeNode* CreateHuffman(ElemType a[], int n)
{
    int i, j;
    struct BTreeNode **b, *q;
    b = malloc(n*sizeof(struct BTreeNode));
    for (i = 0; i &lt; n; i++)
    {
        b[i] = malloc(sizeof(struct BTreeNode));
        b[i]-&gt;data = a[i];
        b[i]-&gt;left = b[i]-&gt;right = NULL;
    }
    for (i = 1; i &lt; n; i++)
    {
        int k1 = -1, k2;
        for (j = 0; j &lt; n; j++)
        {
            if (b[j] != NULL &amp;&amp; k1 == -1)
            {
                k1 = j;
                continue;
            }
            if (b[j] != NULL)
            {
                k2 = j;
                break;
            }
        }
        for (j = k2; j &lt; n; j++)
        {
            if (b[j] != NULL)
            {
                if (b[j]-&gt;data &lt; b[k1]-&gt;data)
                {
                    k2 = k1;
                    k1 = j;
                }
                else if (b[j]-&gt;data &lt; b[k2]-&gt;data)
                    k2 = j;
            }
        }
        q = malloc(sizeof(struct BTreeNode));
        q-&gt;data = b[k1]-&gt;data + b[k2]-&gt;data;
        q-&gt;left = b[k1];
        q-&gt;right = b[k2];

        b[k1] = q;
        b[k2] = NULL;
    }
    free(b);
    return q;
}

ElemType WeightPathLength(struct BTreeNode* FBT, int len)
{
    if (FBT == NULL)
        return 0;
    else
    {
        if (FBT-&gt;left == NULL &amp;&amp; FBT-&gt;right == NULL)
            return FBT-&gt;data * len;
        else
            return WeightPathLength(FBT-&gt;left,len+1)+WeightPathLength(FBT-&gt;right,len+1);
    }
}

int res[26][100];

void HuffManCoding(struct BTreeNode* FBT, int len,int n,int *idx)
{
    static int a[10];
    if (FBT != NULL)
    {
        if (FBT-&gt;left == NULL &amp;&amp; FBT-&gt;right == NULL)
        {
            int i;
            res[idx[n-FBT-&gt;data]][0]=len;
            for (i = 0; i &lt; len; i++)
                res[idx[n-FBT-&gt;data]][i+1]=a[i];
        }
        else{
            a[len] = 0;
            HuffManCoding(FBT-&gt;left, len + 1,n,idx);
            a[len] = 1;
            HuffManCoding(FBT-&gt;right, len + 1,n,idx);
        }
    }
}

const int* par = 0;

int compare(const void* p1, const void* p2)
{
    int a = *(int*)p1;
    int b = *(int*)p2;

    if (par[a] &gt; par[b])
        return 1;
    else if (par[a] == par[b])
        return 0;
    else
        return -1;
}

void sort_index(const int ar[], int index[], int num)
{
    par = ar;
    qsort(index, num, sizeof(int), &amp;compare);
}


int main()
{
    int T,k,kl=0,z=0;
    scanf("%d",&amp;T);
    int rrr[10000],lll[T];
    for(k=0;k&lt;T;k++){
        int i,l,n=0,j,tmp,midx=0,mm=0,ll=0;
        int asc[26]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
        char s[100];
        scanf("%s",s);
        for(l=0;s[l]!='\0';++l);
        for(i=0;i&lt;l;i++){
            asc[s[i]-65]++;
        }

        ElemType* a;
        struct BTreeNode* fbt;
        for(i=0;i&lt;26;i++){
            if(asc[i]!=0){
                n++;
            }
        }
        int idxs[n];
        for(j=0;j&lt;n;j++){
            mm=0;
            midx=0;
            for(i=0;i&lt;26;i++){
                if(asc[i]&gt;mm){
                    mm=asc[i];
                    midx=i;
                }
            }
            idxs[j]=midx;
            asc[midx]=0;
        }

        a = malloc(n*sizeof(ElemType));
        for (i = 0; i &lt; n; i++)
            a[i]=n-i;
        fbt = CreateHuffman(a, n);
        HuffManCoding(fbt, 0, n, idxs);
        for(i=0;i&lt;l;i++){
            tmp = s[i]-65;
            for(j=1;j&lt;res[tmp][0]+1;j++){
                rrr[kl] = res[tmp][j];
                kl++;
                ll++;
            }
        }
        lll[k] = ll;
    }
    kl=0;
    for(k=0;k&lt;T;k++){
        for(z=0;z&lt;lll[k];z++){
            printf("%d",rrr[z+kl]);
        }
        kl+=lll[k];
        printf("\n");
    }
}</pre>
４.子串出现次数。也就用比较老土的办法一个个比较过去，如果对应上count+1，对不上就再回到原来后一个位置继续比较。
<pre>#include "stdio.h"

int pp(char *s1,char *s2,int l1,int l2){
    int count=0,i,j=0;
    for(i=0;i&lt;l1;i++){
        if(s1[i]==s2[j]){
            j++;
            if(j==l2){
                count++;
                i=i-j+1;
                j=0;
            }
        }else{
            i=i-j;
            j=0;
        }
    }
    return count;
}

int main(){
    int T,k;
    scanf("%d",&amp;T);
    int res[T];
    for(k=0;k&lt;T;k++){
        int count = 0,i,l1,l2;
        char s1[100],s2[100];
        scanf("%s",&amp;s1);
        scanf("%s",&amp;s2);
        for(l1=0;s1[l1]!='\0';++l1);
        for(l2=0;s2[l2]!='\0';++l2);
        res[k] = pp(s1,s2,l1,l2);
    }
    for(k=0;k&lt;T;k++){
        printf("%d\n",res[k]);
    }
}</pre>
5.吃金币游戏。这个我也没通过。本人思路是先找第一个点，然后遍历和它连接的下一步可行点，然后每个点在递归运行，这个是dfs主要部分。剪枝的话：如果在两步以外又回到走过的点就是形成环舍去，两步以内或没走过可行；同一路同方向不重复走（考虑他下一个递归讲将和之前完全一模一样）。结果：每次求该路径的金币数，取最大值。
<pre>#include "stdio.h"
#define max(a,b) ((a)&gt;(b)?(a):(b))

int x=1;
int line_his[10000]={0};
int line_dir[10000];
int maxV=0;

int check(int n){
    int i;
    for(i=x-2;i&gt;=x-3;i--){
        if(line_his[i]==n){
            return 1;
        }
    }
    for(i=x-4;i&gt;=0;i--){
        if(line_his[i]==n){
            return 0;
        }
    }
    return 1;
}

int get_road(int *arr,int r,int n,int *tmp){
    int t=0,i;
    for(i=0;i&lt;r*3;i+=3){
        if(arr[i]==n || arr[i+1]==n){
            tmp[t]=arr[i]==n?arr[i+1]:arr[i];
            t++;
        }
    }
    return t;
}

int get_value(int *arr,int r,int n1,int n2){
    int i;
    for(i=0;i&lt;r*3;i+=3){
        if(arr[i]==n1 &amp;&amp; arr[i+1]==n2){
            return arr[i+2];
        }
        if(arr[i]==n2 &amp;&amp; arr[i+1]==n1){
            return arr[i+2];
        }
    }
}

int calc_v(int *arr,int r,int p){
    int tmp = 0,i;
    int his[10000]={};
    for(i=0;i&lt;x-1;i++){
        if(his[line_his[i]*p+line_his[i+1]]!=1){
            tmp+=get_value(arr,r,line_his[i],line_his[i+1]);
        }
        his[line_his[i]*p+line_his[i+1]]=1;
        his[line_his[i]+line_his[i+1]*p]=1;
    }
    return tmp;
}

/*int check_all(int p){
    int i,j,in=0;
    for(i=0;i&lt;p;i++){
        for(j=0;j&lt;x;j++){
            if(i==line_his[j]){
                in++;
                break;
            }
        }
    }
    if(in==p){
        return 1;
    }else{
        return 0;
    }
}*/

int dfs(int *arr,int r,int p,int n){
    int i,t,tt;
    int tmp[10000];
    //if(check_all(p)){
    tt = calc_v(arr,r,p);
    maxV = max(maxV,tt);
    t = get_road(arr,r,n,tmp);
    for(i=0;i&lt;t;i++){
        if(line_dir[n*p+tmp[i]]==1){
            continue;
        }
        line_his[x]=tmp[i];
        line_dir[n*p+tmp[i]]=1;
        x++;
        if(check(tmp[i]))
            dfs(arr,r,p,tmp[i]);
        line_his[x]=-1;
        line_dir[n*p+tmp[i]]=-1;
        x--;
    }
    return maxV;
}

int main(){
    int T,k;
    scanf("%d",&amp;T);
    int result[T];
    for(k=0;k&lt;T;k++){
        maxV=0;
        x=1;
        int p,r,i,t;
        scanf("%d",&amp;p);
        scanf("%d",&amp;r);
        int arr[r*3];
        for(i=0;i&lt;r*3;i++){
            scanf("%d",&amp;arr[i]);
        }
        result[k] = dfs(arr,r,p,0);
    }
    for(k=0;k&lt;T;k++){
        printf("%d\n",result[k]);
    }
}</pre>
