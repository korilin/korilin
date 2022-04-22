---
title: Activity 生命周期和启动模式
date: 2021-6-25
---

Activity 是 Android 四大组件之一，用于提供绘制界面的窗口，在 Android 系统中通过在其生命周期调用特定的回调方法来启动 Activity 的代码。

Activity 在生命周期中会有多个状态，通过相对应的回调来切换状态。

<!-- more -->

![activity_lifecycle](./activity_lifecycle.png)

## 回调与状态切换

#### onCreate

系统在首次创建该 Activity 子后会进入**已创建**状态，并触发 `onCreate()` 回调，执行 Activity 的基本启动逻辑，该逻辑在 Activity 的整个生命周期中应当只发生一次，我们必须实现这个回调，确保 Activity 正常启动。该回调执行后 Activity 会进入**已开始**状态。

#### onStart

当一个 Activity 进入**已开始**状态时，系统会调用此回调，使得 Activity 对用户可见，当 `onStart()` 执行结束时，Activity 会进入进入**已恢复**状态，并来到前台。

#### onResume

当 Activity 进入了**已恢复**状态时，会调用 `onResume()`。调用结束后，Activity 会一直保持**已恢复**状态。

#### onPause

当发生中断事件，或者当前 Activity 仍然可见或部分可见，但失去焦点时，Activity 会进入**已暂停**状态，并调用 `onPause()` 回调。

#### onStop

当 Activity 不再对用户可见时，或已经结束运行即将终止时，会进入**已暂停**状态，并调用 `onStop()` 回调，释放或调整在应用对用户不可见时的无用资源，Activity 在**已暂停**状态会驻留在内存的 Activity 返回栈中。

#### onRestart

处于**已暂停**状态的 Activity 可能会返回到前台，此时会调用 `onRestart()` 来将暂停的 Activity 恢复到**已开始**状态，并重新调用 `onStart()`

#### onDestory

如果 Activity 即将结束，在 `onStop()` 完成之后就会进入**已销毁**状态，销毁之前会先调用 `onDestory()` 释放该 Activity 的所有资源。

此外如果处于**已暂停**状态的 Activity，

## 任务和返回栈

在 Android 系统中，一个应用的 Activity 会按照打开顺序存放在返回栈中，一个返回栈会对应一个任务，当应用任务处于前台时，会显示返回栈栈顶的 Activity。应用启动时，如果没有对应任务存在，那么会创建一个新的任务，启动一个主的 Activity 放到返回栈中。

![diagram_backstack](./diagram_backstack.png)

当一个 Activity 启动另一个 Activity 时，新的 Activity 会压入栈顶成为新的活动 Activity，而原本的 Activity 依旧保留在返回栈中，但会进入**已停止**状态。

当点击放回键时，当前的 Activity 会被退出栈顶并被销毁，而返回栈下一个 Activity 将会执行 `onRestart()` 回调重新进入前台，当返回栈已经没有 Activity 的时候，对应的任务将会结束。

## Activity 之间的跳转

当一个 Activity 跳转到另外一个 Activity 的时候，两个 Activity 的生命周期回调有对应的执行顺序，这通过编写一个简单的例子进行测试就可以知道其执行顺序了。

假如有 A1 通过按钮启动并跳转到 A2，那么对应的生命周期回调执行顺序如下：

1. A1:`onPause()`
2. A2:`onCreate()`
3. A2:`onStart()`
4. A2:`onResume()`
5. A1:`onStop()`

可以看到 A1 因为不可见先进入**已暂停**状态，之后是 A2 启动时的一系列回调，等 A2 启动完成后，A1 因为变得不可见进入了**已停止**状态。

假如此时按下后退键，从 A2 回退到 A1 ，对应的生命周期回调顺序如下：

1. A2:`onPause()`
2. A1:`onRestart()`
3. A1:`onStart()`
4. A1:`onResume()`
5. A2:`onStop()`
6. A2:`onDestory()`

可以看到依旧是当前 Activity A2 先进入**已暂停**状态并调用 `onPause()`，之后才是 A1 的启动回调。由于使用后退键退出 A2，因此 A2 会被销毁，因此在 `onStop()` 还会调用`onDestory()`。

假如我们是通过 A2 中的按钮，再跳转到 A1，此时的生命周期回调顺序则会是下面的样子：

1. A2:`onPause()`
2. A1:`onCreate()`
3. A1:`onStart()`
4. A1:`onResume()`
5. A2:`onStop()`

可以看到会再创建一个 A1，并且 A2 不会被销毁，这和启动一个新的 Activity 的流程一样。这代表默认情况下即便返回栈中已经有 A1 对应的 Activity 了，我们再启动 A1 时还是会再创建一个新的 Activity 放到栈顶，这是 Activit 默认的启动模式。

## 启动模式

Activity 的启动模式，可以通过应用的清单文件 `AndroidManifest.xml` 和 Intent 标记来指定。

在清单文件声明 Activity 时可以通过 launchMode 属性来指定启动模式，在清单文件中可指定的启动模式有 4 种：

- **standard** 这个是默认的启动模式，即启动一个 Activity 总会创建一个新的 Activity 实例，每个实例可以属于不同的任务，一个任务也可以有多个实例

![standard](./standard.png)

- **singleTop** 当任务返回栈顶部已经存在该 Activity 实例，那么将会直接使用该实例，而不会创建新的实例，但如果对应的 Activity 实例存在于返回栈，但不处于栈顶，那么依旧会创建一个新的 Activity 实例

![standard](./singleTop.png)

- **singleTask** 在所有任务中对应 Activity 只会存在一个实例。当已经有任务存在对应的 Activity 实例时，会将该任务调到前台，并弹出对应 Activity 实例上方的其它 Activity 并销毁，保证目标 Activity 实例处于栈顶。如果没有对应的 Activity 实例则会创建一个新实例

![singleTask](./singleTask.png)

- **singleInstance** 和 singleTask 类似，但 singleInstance 创建实例时会分配到一个独立的任务中，在该任务的返回栈中只会存在一个该 Activity 实例，不会有其它的 Activity 实例，当已经存在目标 Activity 实例时，不会再进行创建，而是将原有的任务转到前台运行

![singleInstance](./singleInstance.png)

Activity 的启动模式，也可以使用 Intent 的 flags 来指定。

```Kotlin
startActivity(Intent(this, MainActivity2::class.java).apply {
    flags = Intent.FLAG_ACTIVITY_NEW_TASK
})
```

- `FLAG_ACTIVITY_NEW_TASK` 与 launchMode 的 singleTask 相同
- `FLAG_ACTIVITY_SINGLE_TOP` 与 launchMode 的  singleTop 相同
- `FLAG_ACTIVITY_CLEAR_TOP` 在 launchMode 中没有对应行为的值，如果当前任务如果有对应的 Activity 不会创建新的实例，而是移除该 Activity 上方其它的 Activity，算是针对当前任务的简化版 singleTask
- `FLAG_ACTIVITY_CLEAR_TASK` 这个属性必须配合 `FLAG_ACTIVITY_NEW_TASK` 一起使用，这个标志会将已经存在目标 Activity 的任务清空，该任务旧的 Activity 都会被完成，成为一个空任务，新的 Activity 将会成为这个空任务的新根

## taskAffinity

**“亲和性”** 表示任务 Activity 倾向于哪个任务，在默认的情况下，所有 Activity 都具有相同的亲和性，因此同一应用所有 Activity 都会位于同一任务中。

在 `AndroidManifest.xml` 文件中可以使用 `taskAffinity` 为 Activity 修改亲和性，`taskAffinity` 使用字符串值，并且不能使用 `<manifest>` 元素中声明的默认软件包名称，因为这是默认的亲和性。

一个任务的亲和性由根 Activity 决定。

当一个 Activity 启动模式为 singleTask 时，如果已存在与新 Activity 具有相同亲和性的现有任务，那么会启动到该任务中，如果找不到亲和性相同的现有任务，则会启动一个新任务。如果我们不指定 taskAffinity，该 Activity 由于默认亲和性的原因通常会在当前任务启动。

Activity 有一个 `allowTaskReparenting` 属性，如果配置为 `true` 代表该 Activity 能被分配亲和性相同的任务中。配置了这个属性的 Activity 能通过亲和性在不同任务中重新分配。

## 返回栈清除行为

用户如果离开任务太久，返回栈除了根 Activity 外的其它 Activity 都会被清除，当用户重新回到该任务时只有根 Activity 恢复。我们可以通过啊 `AndroidManifest.xml` 声明 Activity 时使用一些属性来修改这个行为：

- `alwaysRetainTaskState` 该属性只对任务的根 Activity 有意义，当根 Activity 设置为 true 时不会发生清除行为，返回栈的 Activity 会一直保留着。
- `clearTaskOnLaunch` 该属性只对任务的根 Activity 有意义，当根 Activity 设置为 true 时，用户一离开任务，该任务就会清除掉其它的 Activity，只留下根 Activity。
- `finishOnTaskLaunch` 只会作用于一个 Activity，当某个 Activity 设置为 true 时，只要离开任务，这个 Activity 无论在哪都会被清除。

## 参考

> [\<activity>  |  Android 开发者  |  Android Developers](https://developer.android.com/guide/topics/manifest/activity-element?hl=zh-cn)
>
> [Activity 简介  |  Android 开发者  |  Android Developers](https://developer.android.com/guide/components/activities/intro-activities?hl=zh-cn)
>
> [了解 Activity 生命周期  |  Android 开发者  |  Android Developers](https://developer.android.com/guide/components/activities/activity-lifecycle?hl=zh-cn)
>
> [处理 Activity 状态更改  |  Android 开发者  |  Android Developers](https://developer.android.com/guide/components/activities/state-changes?hl=zh-cn)
>
> [了解任务和返回堆栈  |  Android 开发者  |  Android Developers](https://developer.android.com/guide/components/activities/tasks-and-back-stack?hl=zh-cn)
>
> [Android Activity启动模式图解 - 简书 (jianshu.com)](https://www.jianshu.com/p/3baa0b046813)
