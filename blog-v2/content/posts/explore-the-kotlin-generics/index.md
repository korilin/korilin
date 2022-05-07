---
title: 探索 Java & Kotlin 泛型
date: 2021-11-06
tags: [Kotlin, Java]
---

## Kotlin 泛型基础

泛型可以让我们在代码中声明类型参数，Kotlin 泛型最基本的使用和 Java 一样，可以声明在类上和函数上，用法也都差不多。

- 声明在函数上时，可将类型参数作为参数或返回值的类型，该函数为泛型函数
- 声明在类上时，可以用在任意一处类型声明处，该类为泛型类

```Kotlin
class GenericsDemo<T>(t: T) {
    val value = t
}


fun <T> invoke(t: T) : T {
    return t
}
```

我们可以在声明了类型参数的类中，声明一个泛型方法，但如果内部方法所声明的类型参数名称和类上所声明的相同，那么会覆盖类上所声明的类型参数。下面的代码不会报错，并会打印 `Hello` 字符串。

```Kotlin
class GenericsDemo<T>() {

    fun <T> invoke(t: T) : T {
        return t
    }
}

val demo = GenericsDemo<Int>()
println(demo.invoke("Hello"))
```

此外，我们知道在类中可通过重载来定义同名方法，但这在泛型中并不起作用，如果类中拥有以下两个方法，那么将会报错。

```Kotlin
class GenericsDemo<T>() {

    // 泛型来自类
    fun invoke(t: T) : T {
        return t
    }

    // 泛型来自方法本身
    fun <S> invoke(s: S) : S {
        return s
    }
}
```

上诉代码报错原因是因为两个方法拥有相同的 signature，也就是在 JVM 看来这两个方法的方法名和参数都是一样的，报错信息如下：

> Platform declaration clash: The following declarations have the same JVM signature (invoke(Ljava/lang/Object;)Ljava/lang/Object;):

造成上诉*参数类型覆盖*和*重载签名相同*的原因是在编译成 .class 文件后，类型参数会被擦除。

## 泛型擦除

Java 和 Kotlin 的泛型都是伪泛型，泛型所进行的类型安全检查仅在编译器进行，在进入 JVM 时这些类型参数都会被移除，运行时不会保留和类型参数相关的信息，我们称这种机制为**泛型擦除**。

> 由于泛型是在 JDK 1.5 才引入，为了兼容之前的版本，因此采用泛型擦除来移除运行时的类型参数

泛型擦除时，被擦除的类型参数都会被替换成 Object，这也是为什么上述 `invoke()` 方法的 signature 为 `invoke(Ljava/lang/Object;)Ljava/lang/Object;`。

如果该报错来自 IDEA，它可能会提示采用 `@JvmName` 注解来处理这个问题，这可以改变编译成字节码后该方法的名称。

```Kotlin
@JvmName("invoke1")
fun <S> invoke(s: S) : S {
    return s
}
```

使用 `IDEA > Tools > Kotlin > Decompile Kotlin to Java` 工具可以看到反编译后的 Java 代码如下。

```Java
public final class GenericsDemo {
   public final Object invoke(Object t) {
      return t;
   }

   @JvmName(
      name = "invoke1"
   )
   public final Object invoke1(Object s) {
      return s;
   }
}
```

## 泛型约束

在 Java 中声明类型参数时，可使用 `extends` 关键字来指定泛型上界，在 Kotlin 中指定上界的方式如下：

```Kotlin
class Demo<T : Number>() {...}
```

在 Kotlin 中如果没有指定，那么会有一个默认上界 `Any?`，在尖括号中我们只能指定一个上界，如果类型参数需要指定多个上界，那么可以使用单独的 *where* 子句。

此外，如果类型参数有多个约束，它们都需要放在'where'子句中。

```Kotlin
class Demo<T> where T : CharSequence, T : Comparable<T>
```

## 协变性和逆变性

**型变是指复杂类型（组合类型）根据组成类型的子类型关系，所确定子类型关系的相关性**

> 序关系：子类型 <= 基类型

- 协变性（covariance）：保持了子类型的序关系
- 逆变性（contravariance)：逆转了子类型的序关系
- 不变性（invariance）：不存在子类型关系

泛型类是多个类型组合的复杂类型，在代数数据类型中（ADT）中属于积类型。在编译时期，泛型类指定不同类型参数时代表了不同类型，例如 `List<String>` 和 `List<Integer>` 不是并同一个类型。

Java 和 Kotlin 的简单泛型是不型变的，也就是 `List<Integer>` 不属于 `List<Number>` 的子类型，下面的操作将会在编译时期就报错。

```Java
List<Integer> integerList = new ArrayList<>();
List<Number> numberList = integerCollection; // error
```

造成这种错误的原因，是一个能存放 Number 类型对象的 List，既可以存放 Integer 对象也可以存放 Double 对象，因为这些都是 Number 的子类，如果可以将 `List<Integer>` 赋值给 `List<Number>`，意味我们可能将一个 Double 类型的对象放到 `List<Integer>` 里，这将会出现 `ClassCastException`，因此 `List<Number>` 无法作为 `List<Integer>` 的超类。

## Java 的使用处型变

如果我们要让 Java 泛型支持型变，那么需要使用通配符类型参数：
-  `? extends E` 定义了一个上界，代表类型参数为 `E` 的子类
-  `? super E` 定义了下界，代表类型参数为 `E` 的超类

`? extends E` 和直接指定为 `E` 不同，`List<? extends Number>` 指定了 List 所存的对象类型是 Number 的某个子类型，因此 Java 也不清楚 List 具体是哪个子类型，为了安全，`? extends E` 类型并不能作为方法参数类型（我们无法传入一个符合 `capture of ? extends Number` 的类型），但可以将 Number 作为返回值类型。

这其实解决了上面 `List<Number>` 无法作为 `List<Integer>` 超类的问题，由于 `List<? extends Number>` 无法使用 `add` 添加元素，因此不用担心将其他子类型的对象添加到 `List<Integer>` 容器中，那么就不用担心会产生 `ClassCastException`，因此 `List<? extends Number>` 可以作为 `List<Integer>` 的一个超类。

```Java
List<Integer> integerList = new ArrayList<>();

// List<? extends Number> 属于 List<Integer> 的一个超类
List<? extends Number> list1 = integerList;
list1.add(1) // error
Number number = list1.get(0);
```

而对于 `? super Integer`，Integer 可以向上转型成任意父类，所以可以作为方法的参数类型。但由于无法确定通配符 `?` 代表的是哪个父类，向下转型为总是有风险，因此它无法将 Integer 作为返回值的类型，但如果我们试图去获取 `capture of ? super Number` 返回值类型的对象，则会得到一个 Object，因为 `Object` 是所有类的超类。

这代表 `List<? super Integer>` 则是可以添加 Integer 对象，但只能获得 Object 对象，因此它可以作为 `List<Number>` 的超类。

```Java
List<Number> numberList = new ArrayList<>();

// List<? super Integer> 属于 List<Number> 的一个 超类
List<? super Integer> list2 = numberList;

list2.add(1);
// Object 是所有类的超类，可作为 capture of ? super Number 类型
Object object = list2.get(0);
```

对于 Java 这种在使用类型参数时，通过通配符类型来支持型变的方式，称为**使用处型变**。

- `List<? extends Number>` 可以作为 `List<Integer>` 超类，称 `List<? extends Number>` 是**协变的（covariant）**
- `List<? super Integer>` 可以作为 `List<Number>` 超类，称为 `List<? super Integer>` 是**逆变的（contravariant）**

> 在 《Effective Java》中，Joshua Bloch 称那些只能从中读取的对象为生产者，那些只能写入的对象为消费者。

> 并提出了以下助记符：
> PECS（**P**roducer `Extends`, **C**onsumer `Super`） 生产者 -Extends、消费者 -Super

## Kotlin 的声明处型变

```Java
interface Source<T> {
  T nextT();
}
```

在 Kotlin 团队认为 `Source<Object>` 类型变量存储 `Source<String>` 实例引用是安全的，但在 Java 中必须要声明对象的类型为 `Source<? extends Object>`，这毫无意义，因此官方提供了 `out` 和 `in` 两个修饰符来向编译器解释这种情况。

`out` 标注的类型参数将只能从类的成员中返回，即被作为生产，并不被消费。
- 可用于类成员 `out` 位置
- 不可用在类成员 `in` 位置

```Kotlin
class OutDemo<out T>(t: T) {

    // 作为生产者
    fun get(): T = t

    // 方法参数为 `in` 位置，即生产者位置
    // error：类型参数 T 为 `out`，不可出现在 `in` 位置
    fun set(t: T) {
        this.t = t
    }
}
```

`out` 修饰符可以使得类型参数是**协变的（convariant）**

```Kotlin
interface Source<out T> {
    fun nextT(): T
}

val source : Source<Any> = Source<String>() // success
```

而 `in` 修饰符可以使得类型参数是 **逆变的（contravariant）**，`in` 标注的类型参数将只能被消费，而不能生产，这和 Java 的 `? super E` 相对应

```Kotlin
class InDemo<in T>(t: T) {

    // error：类型参数 T 为 `in`，不可出现在 `out` 位置
    fun get(): T = t

    // 作为消费者
    fun set(t: T) {
        this.t = t
    }
}
```

此外，成员变量会提供 getter 和 setter 使得外部可读 / 写（拥有消费或者生产功能），因此 使用 `out` 或 `in` 修饰的类型参数的泛型成员需要声明为 private

`out` 和 `in`称为**型变注解**，因为是在类型声明处提供，因此称为**声明处型变**。

## 类型投影

如果只是为了使得泛型支持型变，那么声明处型变可以满足大部分要求，但有些类我们不能限制其类型参数为只消费或返回，例如 ArrayList 需要同时具有消费和生产。

Kotlin 除了提供声明处型变，也保留了使用处型变，即**类型投影**。我们可以在声明变量时使用 `out` 和 `in`，这与 Java 中的 `? extends E` 与 `? super E` 相对应。

```Kotlin
val intList = ArrayList<Int>()
var outList: ArrayList<out Number> = ArrayList()
var inList: ArrayList<in Int> = ArrayList()
outList = intList
inList = intList
```

投影除了可以作为使用处型变，也可以让我们保证方法内不会对参数接收的对象做坏事，以下是来自 Kotlin 官网的一个例子：

*将一个 Array 对象的数据复制到另一个 Array 对象中，在方法参数中将 Array 的参数类型标注为 out，可使得 form 中的元素不会被修改，以保证原数组对象中数据的安全。*

```Kotlin
fun copy(from: Array<out Any>, to: Array<Any>) { …… }
```

### 星投影

**星投影**语法可以让我们在不确定泛型参数的时候仍然安全地使用它。

```Kotlin
class Foo<T>

// 星投影
val foo: Foo<*> = Foo<Number>()
```

星投影会对定义泛型类型进行投影，该泛型类型的每个具体实例都将会是该投影的子类型。

- 对于 `Foo<T>`，定义的 `Foo<*>` 等价于 `Foo<out Any?>`
- 对于 `Foo<out T>`，`T` 是一个协变类型参数，`Foo<*>` 等价于 `Foo<out Any?>`，*由于这里的 `out` 投影是冗余的，对应的类型参数方差相同，因此也可以等价于 Foo<Any?>*
- 对于 `Foo<in T>`，`T` 是一个逆变类型参数，`Foo<*>` 等价于 `Foo<in Nothing>` 或 `Foo<Nothing>`，这将无法进行写入 `Foo<*>`，因为 `T` 未知时，没有安全的方式可以进行写入
- 对于 `Foo<T : TUpper>`，`T` 是一个具有上界 `TUpper` 的不型变类型参数，`Foo<*>` 在读取值时等价于 `Foo<out TUpper>`，而对于写值时等价于 `Foo<in Nothing>`
- 对于 `Foo<out T : TUpper>`，`T` 是一个具有上界 `TUpper` 的协型变类型参数，`Foo<*>` 等价于 `Foo<out TUpper>` 或 `Foo<TUpper>`

如果泛型类型具有多个类型参数，每个类型参数都可以单独投影。

## 具体化类型参数

我们知道 JVM 运行时会进行泛型擦除，所有使用泛型的位置都会被替换成 `Object`，因此我们没办法将泛型当作一个具体类型使用

但 Kotlin 中的[内联函数](https://kotlinlang.org/docs/inline-functions.html)可以将函数体的代码复制替换到相应的调用位置，Kotlin 提供了 `reified` 关键字，可以具体化内联函数的类型参数。

```Kotlin
inline fun <reified T> nameOf(): String = T::class.java.name

fun main() {
    println(nameOf<Int>()) // java.lang.Integer
}
```

我们查看反编译后的代码，可以看到 `main()` 方法中调用 `nameOf()` 函数的地方被替换成了 `nameOf()` 函数内的代码，而使用泛型的地方被替换成了符合上文的实际类型。

```Java
// 简化了代码，留下关注的部分
public static final void main() {
    // 泛型 T 被替换为 Integer
    String var1 = Integer.class.getName();
    System.out.println(var2);
}

public static final String nameOf() {
    // 泛型 T 被替换为 Object
    String var1 = ((Class)Object.class).getName();
    return (String)var1;
}
```

具体化类型参数可以让我们在函数中，将泛型当作一个具体的类型来使用，以支持使用类型判断、类型转换等操作来编写更优雅的代码。

```Kotlin
if (p is T) {...} // 具体化类型参数后这是支持的

// 不需要 @Suppress("UNCHECKED_CAST") 来忽略类型转换警告
return p as T
```

## 参考

- [泛型：in、out、where - Kotlin 语言中文站 (kotlincn.net)](https://www.kotlincn.net/docs/reference/generics.html)
- [内联函数与具体化的类型参数 - Kotlin 语言中文站 (kotlincn.net) ](https://www.kotlincn.net/docs/reference/inline-functions.html)
- [Generics: in, out, where | Kotlin (kotlinlang.org)](https://kotlinlang.org/docs/generics.html)
- [Inline functions | Kotlin (kotlinlang.org)](https://kotlinlang.org/docs/inline-functions.html#reified-type-parameters)
- [Java 不能实现真正泛型的原因是什么？ | RednaxelaFX 的回答 - 知乎 (zhihu.com)](https://www.zhihu.com/question/28665443/answer/118148143)
