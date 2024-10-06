---
title: 在 Compose 中自定义 Glide 图片加载
date: 2024-09-29
tags: [Kotlin, Jetpack Compose]
---

## 现有的 Compose 图片加载库

目前主流的开源 Compose 图片加载库有 [coil-compose](https://github.com/coil-kt/coil) 和 [glide-compose](https://github.com/bumptech/glide)。

coil-compose 是跨平台的，因此有很多 Compose Mutiplatfrom 的项目会选择它，而单 Android 项目由于有 glide 的使用历史，可能选择 glide-compose 的会更多。

而本篇则是不直接使用 coil 和 glide 的 Compose 版本库，自己基于 glide 去编写一个 Compose 的图片加载控件。
成品可参考 [compose-trace](https://github.com/korilin/compose-trace) 中的 glide package 下的代码。

大部分情况下，coil 和 glide 官方的 Compose 版本库已经足够基础业务的使用。但是通过验证 coil 和 glide 提供的控件，在一些情况下也会出现部分非预期的效果，以及官方库在某些方法有性能问题时，我们需要自己去做一些性能优化，因此最好还是把相关 API 的调用控制在业务项目的手上。


直接使用 Glide API 去构建一个图片加载控件，我个人尝试的方案有三种：
1. 通过 Effect 更新 Painter State
2. 自定义一个异步加载的 Painter 给 Image 控件
3. 自定义 ModiferNode 节点控制 Painter 绘制

在此之前，需要先准备好一些 Glide 加载图片的工具。

## 获取图片加载尺寸

使用 Glide 我们需要给 Target 提供一个获取图片加载尺寸的方式，例如 Glide 自带的 ViewTarget 就通过获取 View 测量后的尺寸作为加载尺寸，而 CustomTarget 则是按照传入尺寸加载（默认是原图）。

通过自定义一个 `GlideSize` 和一个 `ResolvableGlideSize` 来定义图片加载大小的获取接口，在 Compose 中通过 measure 或者其他方式获得的 Size，我们也可以通过 SharedFlow 去传递这个 Size 作为图片加载尺寸。

```Kotlin
internal data class GlideSize(val width: Int, val height: Int)

internal sealed interface ResolvableGlideSize {
    suspend fun getSize(): GlideSize
}

internal class AsyncGlideSize : ResolvableGlideSize {

    private val drawSize = MutableSharedFlow<Size>(
        replay = 1,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )

    var hasEmit = false
        private set

    suspend fun emit(size: Size) {
        hasEmit = true
        this.drawSize.emit(size)
    }

    fun tryEmit(size: Size) {
        hasEmit = true
        this.drawSize.tryEmit(size)
    }

    private fun Float.roundFiniteToInt() = if (isFinite()) roundToInt() else Target.SIZE_ORIGINAL

    override suspend fun getSize(): GlideSize {
        return drawSize
            .mapNotNull {
                when {
                    it.isUnspecified -> GlideSize(
                        width = Target.SIZE_ORIGINAL,
                        height = Target.SIZE_ORIGINAL
                    )

                    else -> GlideSize(
                        width = it.width.roundFiniteToInt(),
                        height = it.height.roundFiniteToInt()
                    )
                }
            }.first()
    }
}
```

## 将图片加载结果转化为 Flow

可以参考 glide-compose 的思路，定义一个 FlowTarget 来监听图片加载结果回调，并在合适的时机提供加载尺寸给 Target，并在 Target 使用完后关闭 Flow 并清除 Target。

> FlowTarget 中可定义一些 Glide 图片加载状态，根据不同状态返回不同的 Painter

```Kotlin
internal sealed interface GlideLoadResult {
    @JvmInline
    value class Error(val painter: Painter?) : GlideLoadResult
    @JvmInline
    value class Success(val painter: Painter) : GlideLoadResult

    object Cleared : GlideLoadResult
}

internal fun RequestBuilder<Drawable>.flow(
    size: ResolvableGlideSize
): Flow<GlideLoadResult> {
    return callbackFlow {
        val target = FlowTarget(this, size, listener)
        listener(target).into(target)
        awaitClose { manager.clear(target) }
    }
}

private class FlowTarget(
    private val scope: ProducerScope<GlideLoadResult>,
    private val size: ResolvableGlideSize
) : Target<Drawable>, RequestListener<Drawable> {

    override fun getSize(cb: SizeReadyCallback) {
        scope.launch {
            val complete = size.getSize()
            cb.onSizeReady(complete.width, complete.height)
        }
    }

    override fun onLoadCleared(placeholder: Drawable?) {
        scope.trySend(GlideLoadResult.Cleared)
    }

    override fun onLoadFailed(errorDrawable: Drawable?) {
        scope.trySend(GlideLoadResult.Error(errorDrawable?.toPainter()))
    }

    override fun onResourceReady(resource: Drawable, transition: Transition<in Drawable>?) {
        val painter = resource.toPainter()
        scope.trySend(GlideLoadResult.Success(painter))
    }

    // ... other function implements
}
```


## 方案一：通过 Effect 更新 Painter State

定义一个 `State<Painter>`，通过 Compose Effect 去使用 Glide 加载图片，并更新 State，期间也可以自定义一些加载状态，根据不同的加载状态去展示不同的 Painter 以及动画。

图片加载尺寸的获取可以使用一个空的 Box 或者默认 Painter 先进行占位，等获得 Box 大小后再传递给 Target。加载出结果的 Painter 后再更新 UI 为 Image 和指定 Painter。

```Kotlin
val state = remember(model) { mutableStateOf<Painter?>(null) }

val painter = state.value

if (painter == null) Box()
else Image(painter = painter)

LaunchedEffect(model) {
    // Use glide load image
    // and update state value.
}
```

这是最简单的实现方案，早期我们项目由于时间问题，就是采用这种方案，随之业务的复杂，也发现了这种方案的弊端：
1. 由于 Glide 的加载都是通过回调，没有直接返回内存缓存的方法，在一些场景，由于 Composition 构建和 Effect 的延迟执行，以及 Painter 更改的更新延迟，导致图片的更新总是慢一拍，在 LazyList 中为滑动时图片延迟出现（即便是有内存缓存的情况），而在 RecyclerView 中刷新单 Item 存在 Compose 编写的控件加载图片的场景，和其它控件更新不同步的问题也非常明显。
2. 底层的测量依旧用的是 PainterNode，无法解决一些指定特殊 ContentScale 进行自适应宽高时空 Painter 状态的显示问题。（这一点在 glide-compose 和 coil-compose 中各自的处理也不一样，展示的效果也不一样）
3. 由于存在节点切换，性能上也比较差。

另外由于 Glide 加载的异步在 Compose 中难以中断，使用 Effect 处理加载 model 变更的时候，会使这里 Diff model 的代码变得比较复杂。

## 方案二：自定义 Painter

自定义 Painter 可以直接加载完图片后直接修改内部 Painter 的 State，由于 onDraw 本身也在快照记录范围内，因此会自动触发重绘。

```Kotlin
@Stable
private class GlideAsyncImagePainter(
    val scale: ContentScale,
    val request: Context.() -> RequestBuilder<Drawable>,
) : Painter() {

    private var painter by mutableStateOf(loading)
    private var alpha: Float by mutableFloatStateOf(DefaultAlpha)
    private var colorFilter: ColorFilter? by mutableStateOf(null)

    override val intrinsicSize: Size
        get() = painter?.intrinsicSize ?: Size.Zero

    private val glideSize = AsyncGlideSize()

    override fun DrawScope.onDraw() {
        glideSize.tryEmit(size)
        (painter)?.apply { draw(size, alpha, colorFilter) }
    }

    private var rememberJob: Job? = null
        set(value) {
            field?.cancel()
            field = value
        }

    override fun applyAlpha(alpha: Float): Boolean {
        this.alpha = alpha
        return true
    }

    override fun applyColorFilter(colorFilter: ColorFilter?): Boolean {
        this.colorFilter = colorFilter
        return true
    }

    fun startRequest(scope: CoroutineScope, context: Context, model: Any?) {
        painter = loading
        rememberJob = (scope + Dispatchers.Main.immediate).launch {
            // Use glide load image
            // and update state value.
        }
    }
}
```

自定义 Painter 还需要提供一个被动取消 Model 加载的时机（例如节点从 UI 上移除），RememberObserver 就是个不错的选择，coil-compose 的 AsyncPainter 就是这样实现的。

```Kotlin
@Stable
private class GlideAsyncImagePainter(
    val scale: ContentScale,
    val request: Context.() -> RequestBuilder<Drawable>,
) : Painter(), RememberObserver { 

    private var remembered = false

    override fun onRemembered() {
        (painter as? RememberObserver)?.onRemembered()
        remembered = true
    }

    override fun onForgotten() {
        stopRequest()
        (painter as? RememberObserver)?.onForgotten()
    }

    override fun onAbandoned() {
        stopRequest()
        (painter as? RememberObserver)?.onAbandoned()
    }

    private fun stopRequest() {
        remembered = false
        rememberJob?.cancel()
        rememberJob = null
        // finish all flow target
        glideSize.tryEmit(Size.Unspecified)
    }
}

@Composable
fun rememberGlideAsyncImagePainter(
    model: Any?,
    scale: ContentScale,
    request: (Context) -> RequestBuilder<Drawable> = { Glide.with(it).asDrawable() },
): Painter {
    val context = LocalContext.current
    val painter = remember {
        GlideAsyncImagePainter(
            loading = loading,
            failure = failure,
            scale = scale,
            listener = listener,
            request = request
        )
    }
    LaunchedEffect(model) {
        painter.startRequest(this, context, model)
    }
    return painter
}
```

自定义 Painter 方案由于没有节点变换，性能会比方案一要好得多，更新时机也比方案一要快一些。但由于 Painter 有限的接口方法，一些操作还是有局限性，还有一些复杂的问题没办法解决，例如方案一中提到的第二个问题。

coil-compose 目前还保留了 AsyncPainter，但 glide-compose 已经把自定义 Painter 移除，改为自定义 Modifier 去实现了。

## 方案三：自定义 Modifier 节点

glide-compose 和 coil-compose 的控件目前都是基于 Modifer 节点去实现，不同的是 coil 是采用 AsyncPainter + Modifier 节点 glide 是将加载逻辑也一起放到 Modifier 节点里。

Modifier.Node 类似于我们自定义 View，本身可以像 View 一样有 attch 和 detach 周期（在 ModifierNodeElement 管理下还有 reset 和 update），也可以通过 DelegatableNode 的子接口去实现自定义 measure 和 draw。

```Kotlin
internal class GlidePainterNode(
    var tag: String?,
    var nodeModel: Any?,
    var alignment: Alignment,
    var contentScale: ContentScale,
    var alpha: Float,
    var colorFilter: ColorFilter?,
) : Modifier.Node(), DrawModifierNode, LayoutModifierNod {

    private val glideSize = AsyncGlideSize()

    private fun modifyConstraints(constraints: Constraints): Constraints {
        // Fix measure constraints
    }

    override fun MeasureScope.measure(
        measurable: Measurable,
        constraints: Constraints
    ): MeasureResult {
        val modified = modifyConstraints(constraints)
        val inferredGlideSize = modified.inferredGlideSize()
        val placeable = measurable.measure(modified)
        coroutineScope.launch { glideSize.emit(inferredGlideSize) }
        return layout(placeable.width, placeable.height) {
            placeable.placeRelative(0, 0)
        }
    }

    override fun ContentDrawScope.draw() {
        // Do somthing pre-draw
        translate(dx, dy) {
            with(painter) {
                draw(size = scaledSize, alpha = alpha, colorFilter = colorFilter)
            }
        }

        // Maintain the same pattern as Modifier.drawBehind to allow chaining of DrawModifiers
        drawContent()
    }

    // Call when update by element
    fun update(nodeModel: GlideNodeModel) {
        startRequest(nodeModel)
    }

    override fun onAttach() {
        super.onAttach()
        startRequest(nodeModel)
    }

    override fun onDetach() {
        super.onDetach()
        stopRequest()
    }

    override fun onReset() {
        super.onReset()
        stopRequest()
    }
}
```

## 处理细节问题

自定义 Modifier.Node 的目的是为了性能优化和需求支持，因此在细节上我们还需要解决几个细节问题。

TODO