---
title: Jetpack Compose 探索
date: 2022-07-08
tags: [Kotlin, Android, Jetpack Compose]
---
## Why compose
Compose UI 的编写只需要 Kotlin，在遵循 Android 应用架构时，这样更有利于聚合 UI Elements 的代码，不需要去区分 Kotlin 代码和 xml 布局文件，在我看来这种方式更加容易采用 Android 架构指南去控制项目架构。

但从另一方面来讲，Compose 这种嵌套的 UI 组合方式会加深代码层次，因此开发过程中需要对 UI 上各个元素做更细的区分，以增加代码的可读性。另外如果状态使用没有处理好，也会对 Compose 的重组性能带来影响。

## 完善的声明式 UI
Android View 系统设计的时候是遵循 OOP 的，虽然有 XML 可以帮我们减少下面这种命令式代码的使用，但这种声明式构建 + 命令式执行的缺点还是很明显，因为需要一个加载器把布局转化到业务逻辑代码中。

```kotlin
// 命令式
val parent = ViewGroup();
val node = View();
parent.addView(node);
```

如果按照理想的声明式 UI 编写方式去改造传统 View 系统，那呈现出的代码可能会包括下面两个特点：

- 节点的构建不应该有返回值
- 节点的连接不依赖于 API
```xml
<LinearLayout>
    <TextView>Hello World</TextView>
    <MaterialButton android:onCLick="syaHi()">hi</MaterialButton>
</LinearLayout>
```

将上面的布局代码转换为 Java/Kotlin 理想的声明式代码
```kotlin
LinearLayout {
    TextView("Hello World")
    MaterialButton("Hi") {
        syaHi()
    }
}
```

Compose 利用 Kotlin DSL 构建声明式 UI，一个 `@Composable` 相当于一个节点，在内部也可以调用其他
 `@Composable` 函数构建子节点。
```kotlin
@Composable fun Foo() {
    var text by remember { mutableStateOf(1) }
    Button(onClick = { text += 1 }) {
        Text("$text")
    }
}

@Composable fun Button()
```

Compose Compiler 与 Kotlin 的版本是绑定的，对应的版本对照表可以参考官方文档：
[https://developer.android.com/jetpack/androidx/releases/compose-kotlin?hl=zh-cn](https://developer.android.com/jetpack/androidx/releases/compose-kotlin?hl=zh-cn)

## 节点与作用域
Compose 中节点分两种：

-  Group 代表一个组合范围，属于重组的最小单位，用于构建树的结构，识别结构的变化
-  LayoutNode 是最终组成渲染树的节点，可以完成测量布局绘制等渲染过程

Group 的创建是在执行 `@Composable` 函数的过程中进行。`@Composable` 函数编译时，会在签名中会插入一个 `$composer` 参数，并调用该对象的方法，我们可以使用 jadx 对 `@Composable` 函数代码生成的字节码进行反编译。
```java
// 上面的 Foo 函数签名经过 compose.compiler 编译后会变成这样
@Composable
public static final void Foo1(@Nullable Composer $composer, int $changed) {
    Composer $composer2 = $composer.startRestartGroup(-1679608079);
    ComposerKt.sourceInformation($composer2, "C(Foo1)21@424L6:Foo.kt#a1gac0");
    if ($changed != 0 || !$composer2.getSkipping()) {
        Foo2($composer2, 0);
    } else {
        $composer2.skipToGroupEnd();
    }
    ScopeUpdateScope endRestartGroup = $composer2.endRestartGroup();
    if (endRestartGroup != null) {
        endRestartGroup.updateScope(new Foo1.1($changed));
    }
}
```

参数中的 Composer 类似于上下文的东西，会贯穿 `@Composable` 函数的调用过程。Composer 大部分方法的调用，都是由 Compose 使用 KCP 解析 `@Composable` 注解对字节码进行修改时的结果。这一步由是 compose.compiler  完成，我们不应该自己创建 Composer 对象以及使用它的方法，不然可能会对 composition 过程造成影响。
### SlotTable 和 Applier
Composer 在 Jetpack Compose 上实现类有一个 internal 的 ComposerImpl，它包含了两个操作节点的成员：

- Applier 负责 NodeLayout 操作，LayoutNode 树的根节点其实就包含在里面
- SlotTable 负责存储 composition 过程的各种数据，包括 Group 和作用域对象，以及其他一些状态
```kotlin
internal class ComposerImpl(
    override val applier: Applier<*>,
    private val slotTable: SlotTable,
    private var changes: MutableList<Change>,
    ...
) : Composer
```

SlotTable 中包含两个数组。

- groups 存储 Group，Group 不以对象形式存在，在 groups 中每 5 数值代表一个 Group，其中偏移位为0的就是 startGroup 的时候传入的 key，一般由编译器生成
- slots 用于存储相关的数据，包括作用域、内容体等
```kotlin
// Group layout
//  0     | 1             | 2             | 3         | 4             |
//  Key   | Group info    | Parent anchor | Size      | Data anchor   |

internal class SlotTable : CompositionData, Iterable<CompositionGroup> {
    var groups = IntArray(0)
        private set
    
    var slots = Array<Any?>(0) { null }
        private set
}
```

Composer 调用 `startRestartGroup` 会传入编译生成的 Key，通过识别当前 Group 的 key 是否匹配，来判断是否需要对树结构进行更改。
如果是创建一个新的 Group 或者当前位置结构发生变化时，会创建一个作用域对象 `RecomposeScopeImpl` 对象存到 slots 里，当结束一个 Group 的执行后会调用作用域对象的 updateScope 注册 `@Composable` 函数体，当作用域进行重组时会重新执行注册的 `@Composable` 函数。
```kotlin
internal class RecomposeScopeImpl(
    var composition: CompositionImpl?
) : ScopeUpdateScope, RecomposeScope {
    // ScopeUpdateScope
    override fun updateScope(block: (Composer, Int) -> Unit)
    // RecomposeScope
    override fun invalidate()   
}
```
### 延迟执行 SlotTable 的更新
SlotTable 的读写需要通过 SlotReader 和 SlotWriter 来完成，为了保证操作时不会发生冲突，两者只能打开一个，并且对 SlotTable 会把对应的更新操作不会马上执行，而是记录到 Change 列表中延迟执行。
composition 过程会把步骤拆分为2个：

1. 计算和记录 SlotTable 的变化
1. 应用 SlotTable 的修改并使用 Applier 对 LayoutNode 树做对应的更新
```kotlin
// ComposerImpl
private var changes: MutableList<Change>

internal typealias Change = (
    applier: Applier<*>,
    slots: SlotWriter,
    rememberManager: RememberManager
) -> Unit
```
SlotTable 对 Group 的操作用了类似于 [GapBuffer](https://en.wikipedia.org/wiki/Gap_buffer) 的数据结构来完成。
### LayoutNode 的创建和插入
如果使用 androidx.compose.material 的组件会发生最终都是调用 `Layout()` 函数，`Layout()` 函数分两个主要的重载类型，一个有带 `content` 参数，一个没有，但里面会调用 `ReusableComposeNode()` 函数。
```kotlin
@Composable inline fun Layout(
    modifier: Modifier = Modifier, // 样式修饰和行为定义
    measurePolicy: MeasurePolicy // 定义布局的测量和布局行为
) {
    ...
    ReusableComposeNode<ComposeUiNode, Applier<Any>>(
      ...
    )
}
```

`ReusableComposeNode` 就是将 LayoutNode 作为节点加到当前位置，节点的创建和复用也是由当前的 Composer 执行的。节点的创建是在回调中使用 `factory` 去创建，同样该回调也是在最后应用更改的时候执行。
```kotlin
@Composable inline fun <T : Any, reified E : Applier<*>> ReusableComposeNode(
    noinline factory: () -> T, // 
    update: @DisallowComposableCalls Updater<T>.() -> Unit
) {
    if (currentComposer.applier !is E) invalidApplier()
    currentComposer.startReusableNode()
    // 如果当前作用于进行的组合正在调度插入树的节点，例如第一次组合或者节点重组
    if (currentComposer.inserting) {
        currentComposer.createNode { factory() }
    } else {
        currentComposer.useNode()
    }
    currentComposer.disableReusing()
    Updater<T>(currentComposer).update()
    currentComposer.enableReusing() // 节点可复用
    currentComposer.endNode()
}

val Constructor: () -> ComposeUiNode = LayoutNode.Constructor

internal val Constructor: () -> LayoutNode = { LayoutNode() }
```

NodeLayout 的节点操作都是交给 Applier 处理，AbstractApplier 中会存着 LayoutNode 树的根节点。
Applier 对节点的插入方式由两种，两种方式插入性能和节点的通知有关，具体可以看看源码的注释。
```kotlin
abstract class AbstractApplier<T>(val root: T) : Applier<T>
// 节点插入操作
fun insertTopDown(index: Int, instance: N)
fun insertBottomUp(index: Int, instance: N)
```
## 响应式UI与快照
在 Compose 中，当 State 发生变化时，会自动进行重组，更新依赖了该 State 的 `@Composable` 函数的这种响应式布局本质也是基于观察订阅，但不需要开发者自己去做订阅和反订阅这些事情，而是交给 Snapshot 完成。Snapshot 相当于给当前程序的 State 拍个照做个记录，因此称为**快照**。
快照内部对 State 值的读取和修改，会触发 `readobserver` 和 `writeObserver` 回调，在快照内修改 State 的值不会影响到外部状态。
```kotlin
val state = mutableStateOf(1)
// 拍照
val snapshot = Snapshot.takeMutableSnapshot (
    readObserver = { println("read") },
    writeObserver = { println("write") }
)
snapshot.enter {
    println("enter state: ${state.value}")
    state.value = 2
}
println("outer state: ${state.value}")
snapshot.apply()
println("apply state: ${state.value}")

// 打印
read
enter state: 1
write
outer state: 1
apply state: 2
```

`mutableStateOf()`返回的本质是一个 `SnapshotMutableStateImpl` 对象，它的 value 值都是交给 
`StateStateRecord` 去维护。
```kotlin
override var value: T
    get() = next.readable(this).value
    set(value) = next.withCurrent {
        if (!policy.equivalent(it.value, value)) {
            next.overwritable(this, it) { this.value = value }
        }
    }

private var next: StateStateRecord<T> = StateStateRecord(value)
```

当修改或读取 State 的值时，会获取当前的快照，并通知当前的 Snapshot 触发相关回调。

- Compose 读取 State 时会记录依赖了此状态的作用域
- 当 State 被修改时，会将依赖了该状态的作用域标记为 `invalid`，在重组的时候会重新执行这些作用域的组合函数
```kotlin
internal inline fun <T : StateRecord, R> T.overwritable(
    state: StateObject,
    candidate: T,
    block: T.() -> R
): R {
    var snapshot: Snapshot = snapshotInitializer
    return sync {
        // 获取当前线程快照/全局快照
        snapshot = Snapshot.current
        this.overwritableRecord(state, snapshot, candidate).block()
    }.also {
        notifyWrite(snapshot, state)
    }
}

@PublishedApi
internal fun notifyWrite(snapshot: Snapshot, state: StateObject) {
    snapshot.writeObserver?.invoke(state)
}
```
### 全局快照
UI 的变化通常是在主线程，如果更新 State 的操作是在其它线程，那么获取到的当前快照将会是全局快照 GlobalSnapShot。
全局快照会在启动的时候就注册一个回调，通过 Kotlin 协程的 Channel 发送消息，这个消息的处理会切到主线程中进行，并 `applyObservers` 中的回调，其中有一个回调会执行`performRecompose()`执行重组。
```kotlin
private val applyObservers = mutableListOf<(Set<Any>, Snapshot) -> Unit>()

internal object GlobalSnapshotManager {
    private val started = AtomicBoolean(false)

    fun ensureStarted() {
        if (started.compareAndSet(false, true)) {
            val channel = Channel<Unit>(Channel.CONFLATED)
            CoroutineScope(AndroidUiDispatcher.Main).launch {
                channel.consumeEach {
                    Snapshot.sendApplyNotifications()
                }
            }
            Snapshot.registerGlobalWriteObserver {
                channel.trySend(Unit)
            }
        }
    }
}
```
### 重组在快照中执行
进行重组时会先拍一次快照，再让重组过程在快照中执行，此时在快照中 `@Composable` 函数中读取 State 的值时会触发读观察者，把 State 和当前的作用域绑定起来。
```kotlin
private fun performRecompose(...){
    return if (
        composing(composition, modifiedValues) {
            composition.recompose()
        }
    ) composition else null
}

private inline fun <T> composing(...): T {
    val snapshot = Snapshot.takeMutableSnapshot(
        readObserverOf(composition), writeObserverOf(composition, modifiedValues)
    )
    try {
        return snapshot.enter(block)
    } finally {
        applyAndCheck(snapshot)
    }
}
```
`applyObservers` 是一个静态变量，当主线程的 MutableSnapshot 触发写入通知的时候也会触发里面的回调进行重组。在 composition 是写入不会马上就通过写观察者进行重组，而是在 composition 过程结束后，apply 后再进行重组。
## Compose 性能优化
Compose 在更新帧的时候要经过3个阶段：

- **组合**：Compose 确定**要显示的内容** - 运行可组合函数并构建界面树。
- **布局**：Compose 确定界面树中每个元素的**尺寸和位置**。
- **绘图**：Compose 实际**渲染**各个界面元素。

Compose 对这些阶段做了许多优化，例如在组合阶段使用 SoltTable 记录树结构，通过 diff 树结构的变化来更新 LayotNode 节点，还使用 RecomposeScope 作用域标记修改状态。在布局阶段使用了固有特性测量来解决布局嵌套问题。
### 重组范围最小化
开头说过，Compose 中编写代码要尽量控制组件的细度，过多的嵌套调用这不会影响 Compose 测量效率（），但如果不控制好组件的细度，导致 Group 的范围过大，可能会影响重组效率。
```kotlin
@Composable fun Foo() {
    var text by remember { mutableStateOf(1) }
    Log.d(TAG, "Foo")
    Button(
        onClick = { text += 1 }
    ).also { Log.d(TAG, "Button") }) {
        Log.d(TAG, "Button content lambda")
        Text("$text").also { Log.d(TAG, "Text") }
    }
}
```
回到前面的例子，如果点击按钮改变状态，会发现发生重组的实际上是整个 Botton 内容体的 Lambda 表达式，如果在 Lambda 表达式中存在其它的组件，那么也会跟着重组。
如果不希望 Text 对状态的依赖影响到同级的其他 `@Composable` 组件，那么可以套一层非 inline 的函数。例如下面的例子，状态变化时，重组的就只有依赖了状态的 Text 了。
```kotlin

@Composable
fun RecomposeFoo() {
    var text by remember { mutableStateOf(0) }
    Log.d(TAG, "Foo")
    Button(onClick = {
        text += 1
    }.also { Log.d(TAG, "Button") }) {
        Log.d(TAG, "Button content lambda")
        ChangeableText {
            Text("$text").also { Log.d(TAG, "Text") } // recompose
        }.also { Log.d(TAG, "ChangeableText call") }
    }
}

@Composable
fun ChangeableText(content: @Composable () -> Unit) {
    Log.d(TAG, "ChangeableText content")
    content()
    Text(text = "Hi").also { Log.d(TAG, "Hi") }
}
```
### inline 函数不能作为重组的最小范围
由于 inline 函数的特点，会共享调用方的 Group，因此 inline 函数不能作为组合的最小范围。
例如 `Column`、`Row`、`Box` 以及 `Layout` 这些容器类。
当然如果希望缩小范围提高性能，同样可以套一层非 inline 函数来缩小 Group 的范围。
### 不做多余的重组
上面提到了，重组过程只会对 `invalid` 的作用域做重组。
例如下面的代码，当 num 发生变化时，Foo1 的内容会进行重组，Foo2 会被调用，但由于编译时 Foo2 的代码插入了 Group 的逻辑， Foo2 中的 Group 和作用域并没有发生修改，因此里面的内容并不会执行。
```kotlin
@Composable
fun Foo1(num: MutableState<Int>) {
    Log.d(TAG, "Foo1 content")
    Text(text = "${num.value}").also { Log.d(TAG, "Text") }
    Foo2().also { Log.d(TAG, "call Foo2") }
}

@Composable
fun Foo2() {
    Log.d(TAG, "Foo2 content")
    Text(text = "End").also { Log.d(TAG, "End") }
}

// Foo1 content
// Text
// call Foo2
```

但如果 Foo2 的有一个 `Int` 类型的参数，并且由 Foo1 读取后传入，那么Foo1和Foo2将会一起参与重组。
```kotlin
@Composable
fun Foo1(num: MutableState<Int>) {
    Log.d(TAG, "Foo1 content")
    Foo2(num.value).also {  Log.d(TAG, "call Foo2") }
}

@Composable
fun Foo2(num: Int) {
    Log.d(TAG, "Foo2 content")
    Text(text = "$num").also { Log.d(TAG, "Text") }
}

// Foo1 content
// Foo2 content
// Text
// call Foo2
```

因此我们需要做状态的延迟读取，以缩小读取状态的 Group 范围，避免不必要的重组参与。
```kotlin
@Composable
fun Foo1(num: MutableState<Int>) {
    Log.d(TAG, "Foo1 content")
    Foo2 { num.value }.also {  Log.d(TAG, "call Foo2") }
}

@Composable
fun Foo2(num: () -> Int) {
    Log.d(TAG, "Foo2 content")
    Text(text = "${num()}").also { Log.d(TAG, "Text") }
}

// Foo2 content
// Text
```
### 官方提出的最佳做法
官方在性能优化的一文中也提出了开发过程中的5个最佳做法
[https://developer.android.com/jetpack/compose/performance#use-remember](https://developer.android.com/jetpack/compose/performance#use-remember)

1. 尽可能从组合函数中移除计算，或使用 remember 记住计算结果，降低计算开销
1. 使用延迟布局 Key
1. 使用 derivedStaeOf 限制重组
1. 尽可能延迟读取
1. 避免向后写入
