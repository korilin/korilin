---
title: 为什么选择 Kotlin？（kt note）
date: 2021-8-3
category: Hi! Kotlin
---

当和其他人谈到 Kotlin 时，可能经常会遇到以下问题

- 你为什么选择 Kotlin？
- Kotlin 相比 Java 有什么优点？

大家总会和 Java 做对比，个人在学习交流、面试的时候也经常被问到类似的问题。因此我打算写一篇文章，记录一些 Kotlin 和 Java 不同的地方，以及对一些特性的思考，同时也可以作为一篇笔记，这篇文章会随着我的学习不断增加和改动内容。

对于比较基础的语法就不介绍太多了，毕竟语言最终也只是工具，语法层面的问题对于开发者而言也不是什么难点。

## 个人对这些问题的回答

Kotlin 提供了很多方便有用的特性，在这些特性的基础上，我们也可以去编写一些方便我们程序开发的工具，来加快我们的开发效率。

并且它可以和 Java 相互交互，我们不需要担心我们经常使用的 Java 库到 Kotlin 会用不了。

我是一个喜欢自己制造工具给自己用的人，因此偶尔会一个人负责一整个程序的开发，包括前端、后端、脚本。

而 Kotlin 这一门语言所支持的平台比我想象的要多，虽然目前用的比较多的还只是Android，但我很期待它在其它领域的发展。

如同官方所描述的那样：

> A modern programming language that makes developers happier.

Kotlin 确实加快了我开发的效率，并且我可以在这门语言上扩展各个方向。这就是我选择 Kotlin 的原因。

## 相关特性

### 空安全

讲到 Kotlin 的特性，大家肯定会想到**空安全**，毕竟在 Java 程序运行时出现的 Exception，NPE 占了不少的比例。

在 Kotlin 中，默认不允许一个变量为空，一个变量被声明的时候，意味着它应当是有一个有效值的，当一个不为空的变量被赋予一个可能为空的值时，编译将会报错。

有时候我们也需要一个可空的变量，像是一些 Java 第三方库的 API 可能会返回一个 `null`，因此在 Kotlin 我们可以在变量类型后面加上 `?` 来代表这个变量是可空的。

对于一个可能为空的值，在使用的过程中，可能会因为空安全的机制出现很多问题，因此 Kotlin 提供了空安全调用和 Eivis 操作符来让我们可以安全地使用一个可能为空的值。

```Kotlin
val nullableName:String? = map["name"]

val name:String = map["name"] ?: ""

val nullableInt:Int? = nullableName?.length
```

### 参数默认值

在 Kotlin 中，函数和类的参数，在声明时都可以指定默认参数，这样可以避免不必要的重载。

在使用的时候我们需要和 Java 一样按照顺序去进行赋值，也可以指定参数的名称来给对应的参数赋值。

定义参数的时候，应当把拥有默认的参数定义到后面，而需要在调用时创建对象 / 调用函数时指定的参数放到前面，这样就可以在按顺序赋值时候就可以先为那些需要指定值得参数进行赋值。

```Kotlin
data class DefaultParam(val param1:String = "", val param2:Int = 0)

fun default(require1: String, require2: Int, default: Boolean = false)
```

## 参考

- 《Kotlin 核心编程》 - 水滴团队
- [Kotlin 语言中文站文档](https://www.kotlincn.net/docs/reference/)
- [Kotlin 官方文档](https://kotlinlang.org/docs/home.html)
