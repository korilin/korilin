---
title: 基于operator构建的Nested-List
date: 2020-1-30 21:30
categories: 技术文章
tags:
    - Python
---

## [简介](#简介)

Nested-List是一个使用operator库构建的一个嵌套列表操作库，主要用于对元素不是基本数据类型的列表进行排序、删除等操作，里面的大多函数使用了operator库，可以简化项目代码编写量。

## [使用与示例](#使用与示例)

Nested-List可以使用pip进行安装：`pip install Nested-List`

Nested-List-1.0.x有4个可用函数，分别是排序、删除元素、最大值和最小值，Nested-List会自动判断传入的列表的元素是什么类型，并调用相应的处理函数，无论进行哪些操作，都要保证列表里的元素是同一类型，这是这个库的工作基础。

```Python
def sort(nl, *key, order=False):
    ...

def delete_items(dl, keys, values, compare=None):
    ...

def max(nl, *keys):
    ...

def min(nl, *keys):
    ...
```

每个函数使用时都需要传入需要操作的列表。

### [排序](#排序)

排序可根据列表中元素的属性来对元素进行排序，排序顺序默认是升序，当order字段设置为True或者"DESC"时，将会降序排序，当传入值不符合规定时将会按照默认排序处理，有一个注意点是如果要设置order的值，要在全部参数传入完成后再传入order的值。

```Python
import nested_list as ntls

dict_list = [
    {'name':'one', 'age':11},
    {'name':'two', 'age':5},
    {'name':'three','age':26},
    {'name':'four','age':19}
]

ntls.sort(dict_list,'age',order=False)
print(dict_list)

# 排序完的输出将会是[{'name': 'two', 'age': 5}, {'name': 'one', 'age': 11}, {'name': 'four', 'age': 19}, {'name': 'three', 'age': 26}]
```

当然列表里的元素也可以是对象，但是你要确保你的对象都是同一类型的对象，并可以指定可排序属性

```Python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __repr__(self):
        return 'User({})'.format(self.age)

user_list = [
    User('one',18),
    User('two',9),
    User('three',7),
    User('four',15)
]

ntls.sort(user_list, 'age')
print(user_list)

# 排序完的输出将会是[User(7), User(9), User(15), User(18)]，如果你不重写__repr__，那么将会打印的列表里将会是对象信息，你将看不到排序效果
```

你可以传入多个参数来进行多次排序，如下

```Python
ntls.sort(user_list, 'id', 'age',order="DESC")
```

此时sort函数将会先根据id进行降序排序，排序完再根据age排序一次

### [删除元素](#删除元素)

delete_items可根据列表的中元素的属性值来删除元素，同样的，delete_items处理的列表元素类型也可以是对象，但使用delete_items的时候传入参数有两个个注意点：

1、无论要根据的属性有多少个，传入时只能存为一个可迭代对象传入，在Python里，虽然字符串可以被迭代，传入字符串也不会报错，但会得出错误的执行结果，所以建议传入一个tuple或者list

2、当传入属性值只有一个时，传入的判断值不需要存入可迭代对象，直接传入即可，否则会出现错误的执行结果；当传入属性值有多个时，传入的判断值**只能**存为tuple对象传入

**以下是例子：**

```Python
# 单个属性时正确的使用方式
ntls.delete_items(user_list, ['age'], 7)
# 或者可以这样
ntls.delete_items(user_list, ('age'), 7)

# 单个属性时错误的使用方式
ntls.delete_items(user_list, ['age'], (7))
ntls.delete_items(user_list, 'age', 7)

# 传入多个属性时正确的使用方式
ntls.delete_items(user_list, None, ['age','name'],(7,'four'))

# 传入多个属性时错误的使用方式
ntls.delete_items(user_list, None, ['age','name'],7,'four')
ntls.delete_items(user_list, None, ['age','name'],[7,'four'])
```

### [最大值与最小值](#最大值与最小值)

如果要根据元素中某个属性来找出最值，可以调用max传入key来处理，Nested-List底层也是这么使用，对于Nested-List来说，只是引入了operator的attrgetter和itemgetter来传入key并进行了简单的包装，Nested-List的max和min也是返回了Python内置的max和min函数的工作结果。

对于Nested-List的max和min的使用方法如下

```Python
ntls.max(user_list, "age")
```

当有多个判断属性时，可直接传入多个属性名称

```Python
ntls.max(user_list, "age", "id")
```

## [致谢](#致谢)

感谢《Python Cookbook》3rd Edition的作者和翻译者，本项目的开发离不开Python Cookbook 3rd Edition Documentation里面的内容带给我的帮助和启发。

Nested-List起初的开发是针对项目中对列表中字典的排序，但随后的开发中在《Python Cookbook》3rd Edition的翻译文档中学习到了更加方便且有效率的方法，按照其中的思路将功能打包在一起供给其它人使用，同时Nested-List变得不再只能对列表中的字典进行操作，也可以对列表或者其他对象使用。

## [链接](#链接)

**Nested-List GitHub仓库主页：**[https://github.com/arukione/Nested-List](https://github.com/arukione/Nested-List)

**Python Cookbook 3rd Edition Documentation：**[https://python3-cookbook.readthedocs.io/zh_CN/latest/index.html](https://python3-cookbook.readthedocs.io/zh_CN/latest/index.html)

[闲着没事造轮子](https://www.arukione.com/2020/01/30/%E9%97%B2%E7%9D%80%E6%B2%A1%E4%BA%8B%E9%80%A0%E8%BD%AE%E5%AD%90/)
