---
title: 将单向数据流应用到 Flutter
date: 2022-02-04
tags: 
    - Flutter
---

之前写过一篇关于应用架构的文章 [《对应用架构的理解与 MVI 介绍》](https://korilin.com/blog/archive/introduction-of-mvi/)

在 Flutter 中，单向数据流思维可用于外层的业务 StatefulWidget + ViewModel 或者 Widget 组件 + 高阶函数。

在 Flutter 中也有 State 的概念，但它并不仅代表一个状态，而是 Widget + 状态的组合，并且不像在原生 Android 开发中一样可以利用 LiveData 或者 Kotlin Flow 在 ViewModel 中来定义一个可订阅 State，这里记录下在 Flutter 中实现思路。

<!-- more -->

我们可以自己创建两个 State 类来实现 MVI 中的 State 概念：
- **ValueState** 不可以修改状态值，仅提供给 UI 层监听变化
- **MutableState** 继承 ValueState，可修改状态值并执行回调列表的回调提供新值。

*这里提供一个简易版本*

```Dart
typedef Function1<T> = void Function(T);

class ValueState<T> {
  static ValueState of<T>(T value) => ValueState._(value);

  ValueState._(this._value);

  late T _value;

  T get value => _value;

  final List<Function1<T>> _listens = [];

  void observe(Function1<T> f) {
    _listens.add(f);
  }

  /// 实际开发应当添加一个 dispose 方法来提供取消观察
}

class MutableState<T> extends ValueState<T> {
  static MutableState of<T>(T value) => MutableState._(value);

  MutableState._(T value) : super._(value);

  set value(T v) {
    _value = v;
    for (var f in _listens) {
      f(_value);
    }
  }
}
```

使用方式和 MVVM / MVI 架构约束上一致，在 ViewModel 中定义一个私有的 MutableState 和一个公开的 ValueState，并提供单向的数据处理 API。

```Dart
class HomeViewModel {
  final MutableState _state = MutableState.of(1);
  late ValueState state = _state;

  void increment() {
    _state.value += 1;
  }
}
```

之后在 initState 中添加状态监听更新 `ValueNotifier` 的值，通知相关的 `ValueListenableBuilder` 重绘。

```Dart
class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;
  final HomeViewModel viewModel = HomeViewModel();

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late ValueNotifier valueNotifier;
  late HomeViewModel viewModel;

  @override
  void initState() {
    super.initState();
    viewModel = widget.viewModel;
    valueNotifier = ValueNotifier(viewModel.state.value);
    viewModel.state.observe((v) {
      valueNotifier.value = v;
    });
  }
}
```

> 除了 StatefulWidget 下相关的 Widget 组件都依赖于一个 State 外，我们应当少用 setState 来刷新 UI，这会让一些无关的 Widget 也需要重新绘制。而推荐 ValueNotifier / ChangeNotifier 的一个权衡标准是它的使用代码复杂度相比 BLoC 低，可控范围比 setState 细。
