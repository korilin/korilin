---
title: Compose Multiplatform 下图片加载支持
date: 2026-02-14
tags: [Kotlin, Compose Multiplatform, Image]
---

早期由于 Android 主要的社区图片组件库（例如 Glide、Coil）在 Google Jetpack Compose 的支持上还不算好，因此当时基于 Glide 做了一个 akit 的 Compose 图片支持库，主要用于处理社区图片库一些在 Compose 上不支持的问题和 bugfix

> 可参考 [《使用 Glide 在 Compose 中加载图片
》](https://korilin.com/posts/compose-glide-image/)。

随着公司基建的发展，开始对 Compose Multiplatform 进行支持，其中图片库就是其中的一个挑战：

1. CMP 的支持并非直接全迁移，而是迁移基础模块，业务模块保持纯 Android 模块和 iOS 模块，原生和 CMP 要求共用一套加载缓存与资源类型支持。Android 端还是使用 Glide 加载，iOS 侧主要使用 Coil，并预留打通 Kingfisher 缓存或直接接入 Kingfisher 的扩展能力。
2. 虽然可以直接 expect 图片组件，由两端各自实现，但由于类似于 `Modifier.asyncBackground` 这类需要依赖 ModifierNode 测量和绘制逻辑的场景，expect 方案并无法直接套用原生 View 实现，因此最好的方式还是统一 Compose 节点定义与逻辑，仅抽象出平台加载图片的 engine（类似于 Ktor）
3. 社交业务的图片加载需要支持许多网络图片类型，包括 ninepatch 背景、gif、lottie 动画等，因此也需要在 CMP 侧同样支持这些类型的加载。


## 从原本的纯 Android Akit 库迁移到 CMP

在早期的 Android 版本里，图片加载主要是围绕 Glide 做 Compose 适配，核心目标是“让业务能在 Compose 里继续复用已有图片能力”，所以当时的重心是 UI 侧封装（例如统一的 NetImage）和加载时机控制。

迁移到 CMP 后，目标发生了变化：不是“把 Glide 搬到多端”，而是“把图片加载协议抽象到 commonMain，平台只负责引擎实现”：

- 抽离统一的请求协议
   `AsyncRequestEngine` 只定义加载行为，不绑定 Glide/Coil：

```kotlin
interface AsyncRequestEngine<Data : AsyncLoadData> {
    val engineSizeOriginal: Int
    suspend fun flowRequest(...): Flow<AsyncLoadResult<Data>>
}
```

返回值也统一成 `AsyncLoadResult`（`Success/Error/Cleared`），这样节点层不用关心底层引擎是 callback 还是 suspend。

- `akit-image` 模块只负责请求管道和 Compose 节点定义，抽离统一的 Compose 节点
   `AkitAsyncImage` 和 `Modifier.akitAsyncBackground` 最后的请求逻辑都会落到 `AsyncRequestNode`，而请求的能力则交给 `AsyncRequestEngine`，具体的平台引擎则交给对应的 `akit-image-engine-*` 模块实现。

- `AsyncImageContext` 作为请求上下文，负责把“这次加载的策略”从业务传到 Node 与 Engine。它本身不承担解码能力，而是承担配置分发。`AsyncImageContext` 更合适：页面只描述“我希望这次请求具备什么能力”，平台引擎负责具体执行。

- 抽离图形能力到独立模块，`akit-graph` 模块负责提供图形能力：NinePatch 解析与绘制、Lottie Painter、Blur Toolkit

这样迁移完成后，业务层依旧只需要关心，并选择对应的 Engine：

```kotlin
AkitAsyncImage(model = url, engine = engine, ...)
```

## 平台抽象的 Engine 与 Context

当前默认提供的 Engine 有两个：

- `GlideRequestEngine.Normal`（Android）
- `CoilRequestEngine.Normal`（CMP，当前 iOS 主用）

它们都实现了 `AsyncRequestEngine`，但分别封装了各自平台上下文和请求构建细节。核心点在于 `EngineContext` 的注册和解析机制。

`akit-image` 内部维护了一个引擎到上下文提供器的注册表：

```kotlin
object LocalEngineContextRegister {
    private val registration = mutableMapOf<KClass<out AsyncRequestEngine<*>>, EngineContextProvider>()
    fun register(type: KClass<out AsyncRequestEngine<*>>, provider: EngineContextProvider)
    @Composable fun resolve(engine: AsyncRequestEngine<*>): EngineContext
}
```

`AkitAsyncImage` 在执行时会先 `resolve(engine)`，再把 `EngineContext` 传给引擎。这样 common 层不需要依赖任何平台 API。

两个默认引擎分别在 companion 里自注册：

- Glide：注册 `GlideRequestEngine::class -> { AndroidContext(LocalContext.current) }`
- Coil：注册 `CoilRequestEngine::class -> { CoilEngineContext(LocalPlatformContext.current) }`

这套机制的好处是“引擎扩展不需要改 UI 入口”。后续如果要接 `KingfisherEngine`，只要做三件事：

1. 实现 `AsyncRequestEngine<*>`
2. 定义 `EngineContext`（比如封装 iOS 侧上下文和 loader）
3. 在 companion/init 里 `LocalEngineContextRegister.register(KingfisherEngine::class, provider)`

业务侧依然是传 `engine = KingfisherEngine.Normal`，`AkitAsyncImage` 本身不用修改。

## Ninepatch 图片加载支持

`akit-graph` 提供跨端 NinePatch 解析的 NinePatchChunk 与绘制的 NinePatchPainter，Glide 侧通过通过 NinePatchChunk 把解码结果转成 `NinePatchDrawable`，而 Coil 侧通过则直接解码为 `NinePatchPainter`

先看解析层的 `parseNinePatch` 会优先判断 chunk，再判断 raw 边框（1px 黑线规则）：

```kotlin
val type = determineNinePatchType(source, chunkBytes)
val chunk = when (type) {
    NinePatchType.Chunk -> NinePatchChunk.parse(chunkBytes)
    NinePatchType.Raw -> NinePatchChunk.createChunkFromRawSource(source)
    else -> null
}
```

`NinePatchPainter` 则根据 chunk 的 x/y div 把图片分段，固定区保持原比例，可拉伸区按目标尺寸分配，这样能在 Compose 侧实现和原生 9-patch 一致的拉伸语义。

实现思路的关键不是某个细节分支判断，而是先把不同来源统一成同一种中间结构 `NinePatchChunk`，再按平台输出目标资源类型。  
可以把链路概括成三步：解析归一化 -> 平台映射 -> 绘制拉伸。

Coil 侧的核心解析逻辑在 `NinePatchDecoder.decode`，会把解析结果统一封装成 `NinePatchCoilImage`（内部持有 `NinePatchPainter`）：

```kotlin
val parsed = parseNinePatch(
    ImageBitmapNinePatchSource(image.asComposeImageBimap),
    image.ninePatchChunk
)
when (parsed.type) {
    NinePatchType.Raw -> cropNinePatchContent(image)
    NinePatchType.Chunk -> image
    else -> null
}?.let {
    val chunk = parsed.chunk ?: NinePatchChunk.createEmptyChunk()
    NinePatchCoilImage(
        image = it,
        content = it.asComposeImageBimap,
        chunk = chunk,
    )
}
```

这里 `NinePatchCoilImage` 本质上只是桥接容器，把解码得到的内容和 `chunk` 打包后交给 `NinePatchPainter`。  
真正决定 NinePatch 拉伸行为的是 `NinePatchPainter` 的分段与绘制逻辑。

`NinePatchPainter.onDraw` 的核心链路是：

```kotlin
override fun DrawScope.onDraw() {
    val xSegments = buildSegments(chunk.xDivs, image.width)
    val ySegments = buildSegments(chunk.yDivs, image.height)

    val destWidths = computeDestLengths(xSegments, size.width.roundToInt())
    val destHeights = computeDestLengths(ySegments, size.height.roundToInt())

    var destY = 0
    for (yIndex in ySegments.indices) {
        var destX = 0
        for (xIndex in xSegments.indices) {
            val xSeg = xSegments[xIndex]
            val ySeg = ySegments[yIndex]
            drawImageRect(
                image = image,
                src = IntRect(xSeg.start, ySeg.start, xSeg.start + xSeg.length, ySeg.start + ySeg.length),
                dst = IntRect(destX, destY, destX + destWidths[xIndex], destY + destHeights[yIndex])
            )
            destX += destWidths[xIndex]
        }
        destY += destHeights[yIndex]
    }
}
```

其中最关键的是目标尺寸分配算法 `computeDestLengths`：

```kotlin
val fixedTotal = segments.filterNot { it.stretch }.sumOf { it.length }
val stretchTotal = segments.filter { it.stretch }.sumOf { it.length }

if (destLength < fixedTotal || stretchTotal == 0) {
    // 空间不足时，所有分段按同一比例整体缩放
} else {
    // 先保留 fixed 段，再把剩余空间按比例分给 stretch 段
    val remaining = destLength - fixedTotal
    val scale = remaining.toFloat() / stretchTotal
}
```

也就是说，NinePatch 的实现核心不是“把整图放大”，而是：

1. 先按 `chunk` 把位图切成 fixed/stretch 段。
2. 再按目标尺寸把可拉伸段重新分配长度。
3. 最后按二维网格逐块映射 `src -> dst` 绘制。

这样可以保证边角等固定区域不被错误拉伸，而中间可拉伸区域按规则扩展。

Android 侧会把解析结果进一步转换为 `Drawable`：`Chunk` 直接构建 `NinePatchDrawable`，`Raw` 先做裁边与密度重算再构建：

```kotlin
val parsed = parseNinePatch(bitmap.asNinePatchSource(), bitmap.ninePatchChunk)
return when (parsed.type) {
    NinePatchType.Chunk -> {
        val chunk = parsed.chunk ?: return bitmap.toDrawable(resources)
        NinePatchDrawable(
            resources, bitmap, chunk.toBytes(), chunk.padding.toAndroidRect(), srcName
        )
    }
    NinePatchType.Raw -> {
        val chunk = parsed.chunk ?: return bitmap.toDrawable(resources)
        RawNinePatchProcessor.createDrawable(resources, bitmap, chunk, srcName)
    }
    NinePatchType.None -> bitmap.toDrawable(resources)
}
```

iOS 和 Android 的底层解码细节可以不同，但最终都会回到同一套 `parseNinePatch -> NinePatchChunk -> NinePatchPainter` 的跨端链路。

## Gif、Lottie 动画支持

Gif 和 Lottie 的支持主要是解码成对应的动画 Painter 来处理。

### Gif 支持

Glide 本身支持 Gif，因此在 Akit 里不需要单独扩展；Coil 侧则实现了 `GifDecoder`，将源数据解码成动画 `Painter`。

- `decodeGif` 在 Android/iOS 分别走不同实现

Android 端使用 `Movie.decodeByteArray`，并由 `MovieGifPainter` 在 `withFrameNanos` 中推进时间轴；循环次数会从 GIF 的 `NETSCAPE2.0/ANIMEXTS1.0` 扩展块解析（`gifRepeatCount`）。

Android 侧的核心解码逻辑：

```kotlin
val movie = Movie.decodeByteArray(bytes, 0, bytes.size) ?: error("Unable to decode GIF")
val repeatCount = gifRepeatCount(bytes)
val painter = MovieGifPainter(movie, durationMs, repeatCount, outWidth, outHeight)
val image = GifCoilImage(
    firstFrame = firstFrame.asImage(),
    painter = painter,
    width = outWidth,
    height = outHeight,
    size = outWidth.toLong() * outHeight.toLong() * 4L,
    shareable = false,
)
```

iOS 端使用 Skia `Codec` 解出帧列表和每帧时长，再用 `GifPainter` 驱动帧切换。相比 Android 的 Movie 实现，iOS 这边是显式帧动画控制。

对应的 iOS 逻辑是先拆帧，再创建 `GifPainter`：

```kotlin
val codec = Codec.makeFromData(data)
val frameInfos = codec.framesInfo
val durations = IntArray(frameCount) { index ->
    val duration = frameInfos.getOrNull(index)?.duration ?: DEFAULT_FRAME_DURATION_MS
    if (duration <= 0) DEFAULT_FRAME_DURATION_MS else duration
}
repeat(frameCount) { index ->
    val bitmap = Bitmap()
    bitmap.allocPixels(codec.imageInfo)
    codec.readPixels(bitmap, index)
    frames += bitmap.asComposeImageBitmap()
}
val painter = GifPainter(frames, durations, codec.repetitionCount)
val image = GifCoilImage(firstFrameImage, painter, width, height, size, shareable = false)
```

Gif 的动画播放逻辑在 `Painter` 内部推进帧序列，下面是 `GifPainter.startAnimation` 的关键实现：

```kotlin
override fun startAnimation(coroutineContext: CoroutineContext) {
    if (frames.size <= 1) return
    if (animationJob?.isActive == true) return
    val maxLoops = if (repeatCount < 0) Int.MAX_VALUE else repeatCount + 1
    animationJob = CoroutineScope(frameContext).launch {
        var loops = 0
        var activeFrame = frameIndex.coerceIn(frames.indices)
        var lastFrameTimeNanos = 0L
        while (isActive && loops < maxLoops) {
            withFrameNanos { frameTimeNanos ->
                val durationMs = frameDurationsMs.getOrElse(activeFrame) { DEFAULT_FRAME_DURATION_MS }
                if (frameTimeNanos - lastFrameTimeNanos >= durationMs * 1_000_000L) {
                    activeFrame++
                    if (activeFrame >= frames.size) {
                        activeFrame = 0
                        loops++
                    }
                    frameIndex = activeFrame
                    lastFrameTimeNanos = frameTimeNanos
                }
            }
        }
    }
}
```

两端最后都会落到 `GifCoilImage`，把首帧作为静态预览，把真正动画交给 `Painter` 处理。

### Lottie 支持

Lottie 同时覆盖了 Glide 与 Coil 两条链路：

1. Glide（Android）
   - `LottieLibraryGlideModule` 注册 `ModelLoader<LottieResource, InputStream>` 和 `LottieDrawableDecoder`
   - 在 `LottieDrawableDecoder.decode` 中将 JSON 输入流解析为 `LottieComposition`，再构建 `LottieDrawable`

```kotlin
val result = LottieCompositionFactory.fromJsonInputStreamSync(source, cacheKey)
val composition = result.value ?: return null
val iterations = options.get(LottieDecodeOptions.Iterations)!!
val drawable = LottieDrawable().apply {
    setComposition(composition)
    repeatMode = LottieDrawable.RESTART
    repeatCount = if (iterations < 0) LottieDrawable.INFINITE else iterations
}
return SimpleResource(drawable)
```

2. Coil（Android/iOS）
   - Android 使用 `LottieCompositionFactory + LottieDrawable` 解析
   - iOS 使用 Skia Skottie `Animation.makeFromString` 解析
   - 两端都统一封装成 `LottieCoilImage(firstFrame + painter)`

Coil 解析逻辑在 `decodeLottie`（iOS 示例），直接把 JSON 转成 Skottie 动画并构建 `LottiePainter`：

```kotlin
val json = bytes.decodeToString()
val animation = Animation.makeFromString(json)
val iterations = options.getExtra(LottieIterationsKey)
val painter = LottiePainter(animation, iterations)

animation.seekFrameTime(0f)
animation.render(firstFrameCanvas, dst)
val image = LottieCoilImage(
    firstFrame = firstFrameBitmap.asImage(),
    painter = painter,
    width = width,
    height = height,
    size = (width.toLong() * height.toLong() * 4L).coerceAtLeast(0L),
    shareable = false,
)
```

Lottie 的播放逻辑同样在 `Painter.startAnimation` 内部推进时间轴（`LottiePainter`）：

```kotlin
override fun startAnimation(coroutineContext: CoroutineContext) {
    if (animationJob?.isActive == true) return
    val maxLoops = if (iterations < 0) Int.MAX_VALUE else iterations + 1
    val duration = animation.duration.takeIf { it > 0f } ?: DEFAULT_DURATION_SEC
    animationJob = CoroutineScope(frameContext).launch {
        var startNanos = 0L
        while (isActive) {
            withFrameNanos { frameTimeNanos ->
                if (startNanos == 0L) startNanos = frameTimeNanos
                val elapsedSec = (frameTimeNanos - startNanos) / 1_000_000_000.0
                val loopsDone = (elapsedSec / duration).toInt()
                if (loopsDone >= maxLoops) {
                    stopAnimation()
                    return@withFrameNanos
                }
                frameTimeSeconds = (elapsedSec - loopsDone * duration).toFloat()
                drawTick++
            }
        }
    }
}
```

动画生命周期由 `AsyncRequestNode` 统一接管：当 painter 切换时，若实现了 `AnimatablePainter` 就自动 `startAnimation/stopAnimation`。因此页面层不需要手动管理 gif/lottie 的启动与销毁。

## Transformation 支持

Factory/Decoder 更适合解决“类型识别和解码入口”问题（例如 gif、lottie、ninepatch 识别）。

而模糊、大图修复这类能力是“解码后的像素转换”，与文件类型无关。把这些放在 Transformation 层有三个直接收益：

1. 关注点分离：解码层只做类型，转换层只做像素处理
2. 可组合：可以和 centerCrop/centerInside、业务自定义转换串联
3. 可缓存：引擎会基于 transformation key/cacheKey 参与缓存命中，避免重复计算

原本 Android 的图片库就已经对 Transformation 做了抽象隔离，因此这部分迁移到 CMP 上并不难：
- 转换逻辑只关注“已解码资源”，不关心原始来源（url/file/res）
- 保留引擎自己的 transformation cache 语义（通过 key/cacheKey）

```kotlin
interface ImageTransformation<T> {
    fun key(): String
    fun transform(context: EngineContext, resource: T, width: Int, height: Int): T
}
```

`akit-image-engine-glide` 里 `BitmapTransformation/DrawableTransformation` 同时实现了 Glide Transformation 与 `ImageTransformation`，这样既能接入 Glide pipeline，也能复用项目自己的转换抽象。

请求阶段在 `setupTransforms` 里按 `ContentScale` 组合链路，并默认加上 `LargeBitmapLimitTransformation`。这个转换用于规避 Compose 场景的 `draw too large bitmap` 问题：当尺寸或 byteCount 超阈值时主动缩放，避免大图直接进绘制管线。

另一个关键点是 `SkipNinePatchDrawableTransformation`。它会跳过 `NinePatchDrawable` 的 drawable 级变换，避免 ninepatch 被错误二次处理导致拉伸语义失真。

Coil 与 Glide 在请求入口不同，但转换层语义保持一致：都围绕 `ImageTransformation` 组织转换链，并让引擎缓存基于 key/cacheKey 生效。

### 高斯模糊实现（Toolkit.blur）

`GaussianBlurTransformation` 在转换链里主要负责参数与缓存语义，真正的像素处理集中在 `Toolkit.blur`。Android 是基于 renderscript-toolkit 的 native 库来执行。

```kotlin
fun blur(inputBitmap: Bitmap, radius: Int = 5, restriction: Range2d? = null): Bitmap {
    validateBitmap("blur", inputBitmap)
    require(radius in 1..25)
    validateRestriction("blur", inputBitmap.width, inputBitmap.height, restriction)

    val outputBitmap = createCompatibleBitmap(inputBitmap)
    nativeBlurBitmap(nativeHandle, inputBitmap, outputBitmap, radius, restriction)
    return outputBitmap
}
```

iOS 的 `actual blur` 核心流程是：先算 kernel，优先走 `vImage` 盒卷积，失败再走 Kotlin fallback，最后统一处理 restriction 区域。

```kotlin
actual fun blur(
    inputArray: ByteArray,
    vectorSize: Int,
    sizeX: Int,
    sizeY: Int,
    radius: Int,
    restriction: Range2d?
): ByteArray {
    require(vectorSize == 1 || vectorSize == 4)
    require(inputArray.size >= sizeX * sizeY * vectorSize)
    require(radius in 1..25)
    validateRestriction("blur", sizeX, sizeY, restriction)

    val kernelSize = (radius * 2 + 1).coerceAtLeast(1)
    val outputArray = ByteArray(inputArray.size)
    val success = boxConvolve(
        inputArray = inputArray,
        outputArray = outputArray,
        sizeX = sizeX,
        sizeY = sizeY,
        vectorSize = vectorSize,
        kernelSize = kernelSize
    )
    if (!success) {
        boxBlurFallback(inputArray, outputArray, sizeX, sizeY, vectorSize, radius)
    }
    if (restriction != null) {
        zeroOutsideRestriction(outputArray, sizeX, sizeY, vectorSize, restriction)
    }
    return outputArray
}
```

`boxConvolve` 负责走 Accelerate：根据 `vectorSize` 分发到 `vImageBoxConvolve_ARGB8888` 或 `vImageBoxConvolve_Planar8`，并按需申请 tempBuffer。

```kotlin
private fun boxConvolve(...): Boolean {
    val kernel = kernelSize.toUInt()
    val flags = kvImageEdgeExtend
    val tempBufferSize = requiredTempBufferSize(src.ptr, dest.ptr, kernel, vectorSize)
    ...
    error = if (vectorSize == 4) {
        vImageBoxConvolve_ARGB8888(..., kernel_height = kernel, kernel_width = kernel, flags = flags)
    } else {
        vImageBoxConvolve_Planar8(..., kernel_height = kernel, kernel_width = kernel, flags = flags)
    }
    return error == 0L
}
```

fallback 路径是两次一维滑动窗口：先横向写 `temp`，再纵向写 `outputArray`，避免直接做二维卷积。

```kotlin
private fun boxBlurFallback(...) {
    val window = radius * 2 + 1
    val temp = ByteArray(inputArray.size)
    // horizontal pass -> temp
    for (y in 0 until sizeY) { ... }
    // vertical pass -> outputArray
    for (x in 0 until sizeX) { ... }
}
```

整体上两端语义保持一致：Android 走 native blur，iOS 走 vImage + fallback，参数约束与输出约束由 `Toolkit.blur` 统一。

## 总结

这次从纯 Android 图片库迁移到 CMP，核心并不是“换个跨平台库”，而是把图片能力拆成了可演进的三层：

- `akit-image`：统一 Compose 节点与请求协议
- `akit-image-engine-*`：平台加载引擎实现（Glide/Coil）
- `akit-graph`：NinePatch/Lottie/Blur 等图形能力

这种分层最大的收益是：业务侧 API 基本稳定，平台能力可以持续替换和扩展，例如：

1. 增加新的 Engine 实现（例如 kingfisher 直连版本），并继续复用现有 `EngineContext` 注册机制
2. 有其他需要服用图形能力的库（例如 `akit-resource`）可以直接应用 `akit-graph`

源码地址： <https://github.com/szkug/akit>
