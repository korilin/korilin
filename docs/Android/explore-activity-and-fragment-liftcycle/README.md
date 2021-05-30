---
title: 探索 Activity 与 Fragment 生命周期
date: 2021-05-10
category: Android
---

Activity 与 Fragment 是 Android 中两个非常基础的知识点，它们是两个非常相似的东西。作为 Android 的 UI 部分，Android 提供了 Fragment 来进行模块化，让我联想到了前端组件化的开发方式。

Activity 与 Fragment 都有自己的生命周期，并且它们两个的生命周期非常像，它们只是在一些特定的地方有些区别。在 Activity 与 Fragment 的生命周期中都提供了一系列覆盖生命周期的回调方法，由于 Fragment 是嵌入在 Activity 中显示，因此它比 Activity 多了几个与相关联 Activity 生命周期的回调。

对于 Activity 与 Fragment 的生命周期，在 Android 开发者官方文档有详细的介绍，但对于彼此间切换时的状态改变顺序是什么样的，这让我很好奇！

## Activity 与 Fragment 的生命周期

首先，先来看一下 Activity 与 Fragment 的生命周期以及对应的回调方法，详细的介绍以及图示可以参考官方文档：

- Activity 生命周期：<https://developer.android.com/guide/components/activities/activity-lifecycle?hl=zh-c>
- Fragment 生命周期：<https://developer.android.com/guide/fragments/lifecycle?hl=zh-cn>

**Activity 生命周期回调**

- `onCreate()` 当一个 Activity 首次创建时会进 **已创建状态**，并调用此方法，我们可以在该方法中完成 Activity 的初始化操作。当该方法执行完，Activity 将会进入 **已开始** 状态。
- `onStart()` 当 Activity 进入 **已开始** 状态后，将会调用此方法来让 Activity 对用户可见。该过程会非常快就结束，并进入 **已恢复** 状态。
- `onResume()` 进入 **已恢复** 状态后 Activity 会来到前台，并执行 `onResume()` 回调。处于该状态的 Activity 是与用户交互的运行状态。
- `onPause()`
- `onStop()`
- `onRestart()`
- `onDestroy()`

## Activity 之间的切换

## Activity 与 Fragment 回调顺序

## Fragment 之间的切换

## 参考

> 《第一行代码 Android 第三版》 - 郭霖
>
> [了解 Activity 生命周期 - Android 开发者官方文档](https://developer.android.com/guide/components/activities/activity-lifecycle?hl=zh-cn)
>
> [Fragment lifecycle - Android 开发者官方文档](https://developer.android.com/guide/fragments/lifecycle?hl=zh-cn)

