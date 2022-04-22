---
title: Java Collection 相关知识点记录
date: 2020-2-6 15:30
categories: 笔记
tags:
    - Java
---

### 函数参数传的数组是引用

和 Python 一样，如果把一个数组或者列表当做函数的参数传入，是传了一个地址的引用，如果在调用的函数里直接修改了数组的值，那么原本数组的值也会跟着改变

```Java

public class Hello{
    public static void(String[] args){
        int[] a = {1,2,3};
        change(a);
    }

    public static void change(int[] b){
        b[0] = 0;
        b[1] = 0;
    }
}

```

按照上面的代码执行完，数组 a 的值将会变成{0,0,3}, 可以通过克隆的方法避免这种情况，通过调用 clone() 方法来获得一个复制的数组，再传入，此时传入的数组是另一个对象的引用了。

```Java

public class Hello{
    public static void(String[] args){
        int[] a = {1,2,3};
        change(a.clone());
    }

    public static void change(int[] b){
        b[0] = 0;
        b[1] = 0;
    }
}

```

### for-each 遍历

大部分 Collection 对象都可以使用 for-each 遍历，之前学过但是又给忘记了，在这记录一下。

for-each 循环的使用方法是 for（元素类型 变量名：对象）, 这样就可以把 Collection 对象依次赋值给冒号前面的变量。

例子：

```Java

LinkList<String> slist = new LinkList();

for(String s:slist){
    System.out.println(s);
}

ArrayList<Integer> ilist = new ArrayList();

for(int i:ilist){
    System.out.println(i);
}

```

这种遍历方式效率非常高，但是在多线程的时候要考虑并发操作问题

可参考：[JAVAschool](http://www.51gjie.com/java/639.html)

### List 类的 contains 方法

List 类和子类都有一个 contains() 来判断元素是否存在列表对象中，但是这个方法的底层比较的是对象，而不是变量和元素的值。

如果列表的元素类型是 String 或者 int 等这类基本类型的话，倒是不会有影响，因为这类元素拿出来的数据都是常量，所以值相同的话，地址也是相同的。

但是如果比较的是数组或者其他对象，那就会出现匹配不到的问题，因为两个对象的值虽然是相同的，但是他们引用的地址却不一样，所以无法正常判断。

下面是 contains 的源码：

```Java
/**
* Returns <tt>true</tt> if this list contains the specified element.
* More formally, returns <tt>true</tt> if and only if this list contains
* at least one element <tt>e</tt> such that
* <tt>(o==null&nbsp;?&nbsp;e==null&nbsp;:&nbsp;o.equals(e))</tt>.
*
* @param o element whose presence in this list is to be tested
* @return <tt>true</tt> if this list contains the specified element
*/
public boolean contains(Object o) {
    return indexOf(o) >= 0;
}
```

我觉得这种设计是正确的，符合面对对象的思想，假如把列表当做一个班级，元素都是学生，刚好有两个学生的名字和年龄一模一样，但他们的的确确是不同的两个人，就应该是返回 false, 而不是 true

当然这种设计有时候并不能满足我们的开发，所以我们可以通过重写 contains 的方法来满足需求。
