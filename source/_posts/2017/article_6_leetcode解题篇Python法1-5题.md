
---
title: leetcode解题篇Python法1-5题
catalog: true
date: 2017-3-10 15:53:28
---

具体详细题目请到<a href="https://leetcode.com/problemset/algorithms/">https://leetcode.com/problemset/algorithms/</a>查看

之下解法都属第一思路，大可改进。

悄悄自问一句：今天ac了吗？<!--more-->

1. Two Sum
<pre>class Solution(object):
    def twoSum(self, nums, target):
    l=len(nums)
    for i in xrange(l):
        for j in xrange(l):
            if(j==i):
                pass
            else:
                if((nums[i]+nums[j])==target):
                    return [i,j]
</pre>
2. Add Two Numbers
<pre>class Solution(object):
    def addTwoNumbers(self, l1, l2):
        res=[]
        jw=0
        while(hasattr(l1,'val') or hasattr(l2,'val')):
            if hasattr(l2,'val') and (not hasattr(l1,'val')):
                if l2.val+jw==10:
                    jw=1
                    res.append(0)
                else:
                    res.append(l2.val+jw)
                    jw=0
                l2=l2.next
            elif hasattr(l1,'val') and not hasattr(l2,'val'):
                if l1.val+jw==10:
                    jw=1
                    res.append(0)
                else:
                    res.append(l1.val+jw)
                    jw=0
                l1=l1.next
            else:
                if l1.val+l2.val+jw&gt;=10:
                    tmp=l1.val+l2.val+jw-10
                    jw=1
                else:
                    tmp=l1.val+l2.val+jw
                    jw=0
                res.append(tmp)
                l1=l1.next
                l2=l2.next
        if(jw):
            res.append(1)
        return res
</pre>
3. Longest Substring Without Repeating Characters
<pre>class Solution(object):
    def lengthOfLongestSubstring(self, s):
        l=len(s)
        res=0
        tmp=0
        k=1
        for i in xrange(l):
            for j in xrange(k,l+2):
                if len(set(s[i:j]))!=j-i:
                    k=j
                    tmp=j-i
                    break
            if tmp&gt;res:
                res=tmp
            tmp=0
            o=1
        if s=='':
            res=1
        return res-1</pre>
4. Median of Two Sorted Arrays
<pre>class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        c=(nums1+nums2)
        c.sort()
        l=len(c)
        if l%2==0:
            res=(c[l/2]+c[l/2-1])*1.0/2
        else:
            res=(c[l/2])*1.0
        return res</pre>
5. Longest Palindromic Substring
<pre>class Solution(object):
    def longestPalindrome(self, s):
        l=len(s)
        tmp=0
        maxl,maxr=0,0
        for i in xrange(l):
            m=i+1
            n=i
            while m&lt;l and n&gt;=0:
                if s[m]==s[n]:
                    if m-n+1&gt;tmp:
                        tmp=m-n+1
                        maxl=n
                        maxr=m
                    m+=1
                    n-=1
                else:
                    break
            j=i-1
            k=i+1
            while j&gt;=0 and k&lt;l:
                if s[j]==s[k]:
                    if k-j+1&gt;tmp:
                        tmp=k-j+1
                        maxl=j
                        maxr=k
                    j-=1
                    k+=1
                else:
                    break
        return s[maxl:maxr+1]</pre>
&nbsp;
