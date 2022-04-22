---
title: 获取字符排列组合
date: 2019-11-10
categories: 算法
tags:
    - Python
---

**假如有一串字符串，要对字符串里所有字符进行排列，列出所有排列组合的可能**

对于这种获取所有可能性的问题我第一想到的就是用树结构进行深度遍历来实现

对于这种问题，我们知道遍历到最后的树叶就是其中的一种结果，所以我们定义一个全局列表来储存全部树叶的结果。

所以我们定义一个 Tree 类来对第一次传入节点进行操作；

定义一个节点类来作为树节点，并直接把向下添加的节点写在构造函数里面，只要符合要求就一直向下传入节点，直到全部字符都遍历完，到达树叶的时候将该结果存储起来。

<!-- more -->

```Python
# 存储树叶结果
result = []

# 树结构
class Tree:

    def __init__(self,strings):
        # 树根节点
        self.nodes = []
        if strings != []:
            for index in range(0,len(strings)):
                # 把字符传入节点
                node = Node(index,strings[index],strings)
                # 添加子节点到树根
                self.nodes.append(node)


# 节点结构
class Node:
    def __init__(self,index,string,strings):
        # 树节点的值
        self.value = string
        # 树节点的子节点
        self.nodes = []
        # 复制新的字符列表
        self.strings = strings[:]
        # 将已拼接入节点值的字符从字符列表里删除
        self.strings.pop(index)
        # 如果字符列表为空, 则结束添加节点, 将当前树叶节点保存的值存进result
        if len(self.strings) == 0:
            result.append(self.value)
        # 不为空, 继续将字符存入新节点添加到当前节点的子节点中
        else:
            for i in range(0,len(self.strings)):
                node = Node(i,self.value+self.strings[i],self.strings)
                self.nodes.append(node)
```

以下是执行的主方法
先从键盘获取字符串，再将字符串转成列表以便进行遍历，然后将字符列表传入树进行操作
最后按照不同字符开头分段打印出结果

```Python
if __name__ == "__main__":
    string = str(input())

    strings = list(string)
    tree = Tree(strings)

    for i in range(0,len(strings)):
        length = int(len(result)/len(strings))
        print(result[i*length:i*length+length])

```

对于遍历所有可能的问题，树结构往往会是我考虑的解决方法之一，因为这种结构基本可以将需要的可能都列出来，即使会有累赘的元素，但是所有可能往往都可以很好的列出来，有时实现起来也比其它方式方便。
