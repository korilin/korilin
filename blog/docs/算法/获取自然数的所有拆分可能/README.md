---
title: 获取自然数的所有拆分可能
date: 2019-11-10
categories: 算法
tags:
    - Python
---

**任何一个大于 1 的自然数 n, 都可以拆分成若干个小于 n 的自然数相加，现在输入一个数 n, 列出该数的所有拆分可能**

像这种获取所有可能性的问题，可以使用树遍历来解决

这次其实我第一次想到的不是树结构，而是 for 循环，其实就是被那么规律的排列给误导了~

但是最后还是靠树来实现了。

算法的思路是定义了 Node 类传入列表进行计算存储，从 1 到 n-1 开始遍历，将遍历到的数存到列表里面，每次存完 1 个数将列表传入下一个节点，再从 1 开始存，直到列表的和等于 n 的值，把这个列表进行排序然后存入全局列表 result 里面，最后再打印出来。

<!-- more -->

以下是 Python 实现代码

```Python
# 储存结果
result = []

# 定义全局变量n
n=0

class Node:
    def __init__(self,num_list):
        # 计算列表里值的和
        list_sum = sum(num_list)
        # 遍历1到当前可储存的最大值
        for i in range(1,n-list_sum+1):
            # 复制已存储自然数的列表
            new_num_list = num_list[:]
            # 将可存储的值添加进列表
            new_num_list.append(i)
            # 如果添加新值后列表里全部元素的和等于n, 则该节点为尾节点
            if list_sum+i == n:
                # 判断存的自然数是否全都小于n
                if len(new_num_list)!=1:
                    # 对存储的自然数进行排序
                    new_num_list.sort()
                    # 判断该结果是否已存在
                    if new_num_list not in result:
                        result.append(new_num_list)
            # 如果不是尾节点, 继续添加节点
            if list_sum+i < n:
                Node(new_num_list)

if __name__ == "__main__":
    print("Enter a number greater than two")
    # 设置n的值
    n = int(input())
    # 开始拆分
    num_list = []
    Node(num_list)
    # 展示结果
    for i in result:
        print(i)

```

其实无论是拆分还是组合，只要是求全部可能性的问题，用树结构都可以很好的解决。
