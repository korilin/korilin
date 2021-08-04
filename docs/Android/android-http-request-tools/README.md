---
title: Android HTTP 请求工具
date: 2021-8-4
category: Android
---

在开发中，调用后端的 API 通常只需要知道如何发起一个 HTTP 请求并获取响应的数据就够了，Android 中可以进行 HTTP 请求的工具也很多，这里记录 HttpURLConnection、OkHttp、Retrofit 这 3 种的使用方法。

## HttpURLConnection

HttpURLConnection 是 `java.net` 提供的工具，使用起来非常简单。我们可以使用 `URL` 对象来获得 HttpURLConnection 对象，并根据业务进行一些自定义的设置，通过 `getInputStream()` 来获取服务器返回的输入流。

```Kotlin
val url = URL("https://www.baidu.com")
val connection = url.openConnection() as HttpURLConnection

connection.requestMethod = "GET"
connection.connectTimeout = 5000

val responseStream = connection.inputStream

val responseReader= responseStream.bufferedReader()
val body = StringBuilder()

responseReader.use {
    responseReader.forEachLine {
        body.append(it)
    }
}

// 关闭连接
connection.disconnect()
println(body)
```

如果我们需要提交数据，可以使用 DataOutputStream 来为这个 HTTP 请求添加需要携带的数据。

```Kotlin
connection.requestMethod = "POST"
val data = DataOutputStream(connection.outputStream)
data.writeBytes("param1=v1&param2=v2")
```

## OkHttp

OkHttp 是一个 Square 公司开发的开源库，它有自己的一套通信实现，我们使用的时候需要按照官方的说明引入依赖。

相关链接：
- GitHub：<https://github.com/square/okhttp>
- OkHttp 文档：<https://square.github.io/okhttp/>

使用 OkHttp 需要先构建 OkHttpClient 和 Request 对象，再用 `newCall()` 方法来创建一个 Call 对象，Call 对象有一个 `execute()` 方法，会发送一个 HTTP 请求并阻塞当前线程，等请求完成响应时就会返回一个 Reponse 对象，这时我们就可以通过返回的这个响应对象来拿到响应数据。

```Kotlin
val client = OkHttpClient()
val request = Request.Builder().url("https://baidu.com").build()

val call = client.newCall(request)

val response = try {
    call.execute()
}catch (ioe : IOException) {
    TODO()
}

val body = response.body?.string()
println(body)
```

如果需要发送 POST 请求并携带数据时，我们可以构建一个 FormBody 添加请求参数，在构建 Request 对象的时候调用 `post()` 方法来指定请求类型是 POST，并把构建的 FormBody 对象传入，作为请求携带的数据。

```Kotlin
val requestBody = FormBody.Builder()
    .add("param1", "v1")
    .add("param2", "v2")
    .build()

val request = Request.Builder()
    .url("https://baidu.com")
    .post(requestBody)
    .build()
```

发送请求是一个耗时操作，大部分情况下，我们需要开启一个子线程来进行请求，如果使用 HttpURLConnection 来写这种回调将会非常麻烦，但是我们在 OkHttp 中的话就非常简单，只需要将 `execute()` 方法改成 `enqueue()` 并传入一个 okhttp3.Callback 对象。

`enqueeu()` 方法会开启一个子线程来发送请求，并把请求结果回调到 Callback 中，Callback 本身是一个接口，我们需要实现它的两个方法：

- `onResponse()` 用于请求成功时的回调方法
- `onFailure()` 用于请求失败时的回调方法

```Kotlin
call.enqueue(object : Callback {

    override fun onResponse(call: Call, response: Response) {
        println(response.body?.string())
    }

    override fun onFailure(call: Call, e: IOException) {
        e.printStackTrace()
    }
})
```

## Retrofit

Retrofit 同样是 Square 公司开发的一个开源库，它是基于 OkHttp 进行封装的，在引入依赖时就会自动引入 OkHttp。

- Retrofit 文档：<https://square.github.io/retrofit/>
- Retrofit 各个版本：<https://github.com/square/retrofit/releases>

Retrofit 会把响应的 JSON 自动解析成对象，所以我们需要引入 Retrofit 的 JSON 转换库 `converter-gson`，这个库这是基于 Gson 开发的。

使用 Retorfit 比较繁琐，和 OkHttp 一样需要先构建一个 Retrofit 对象，并设置接口的根地址和 GsonConverterFactory 来正常解析 JSON，之后我们可以根据这个 Retrofit 对象创建不同的 Service。

```Kotlin
val retrofit = Retrofit.Builder()
        .baseUrl("https://api.demo.com")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
```

在创建前，我们需要先定义好我们自己的 Service 接口，在接口中定义不同的请求方法，并使用注解来告诉 Retorift 请求类型、请求端点、参数等。

如果需要返回数据，我们需要定义对应格式的数据类，并返回一个对应的 Call 对象。

```Kotlin
interface DemoService {

    data class Data(val data1: String, val data2: String)

    @GET("demo/{pathParam}/get")
    fun get(@Path("pathParam") param: String, @Query("date") timestamp: Long): Call<Data>

    data class PostBody(val param1: String, val param2: String)

    @POST("demo/post")
    fun post(@Body body: PostBody)
}
```

之后我们调用 Retrofit 对象的 `create()` 方法，将这个接口的类型传进去，Retrofit 会使用动态代理来生成一个 Service 实例。

子后我们就可以使用这个实例，调用对应的方法来发送不同的请求，并拿到 Call 对象了。

```Kotlin
val demoService: DemoService = retrofit.create(DemoService::class.java)

val call = demoService.get("value1", 1000000000000)
```

在拿到 Call 对象时，Retrofit 还没有发送请求，我们需要创建一个 Callback 对象来进行请求响应时的回调，并在 Call 调用 `enqueue()` 方法的时候将 Callback 对象传进去，此时 Retrofit 会开启子线程发起请求，等请求响应时再切回主线程。

```Kotlin
val callback = object : Callback<DemoService.Data> {

    override fun onResponse(call: Call<DemoService.Data>, response: Response<DemoService.Data>) {
        val data: DemoService.Data? = response.body()
        println(data)
    }

    override fun onFailure(call: Call<DemoService.Data>, t: Throwable) {
        t.printStackTrace()
    }
}

call.enqueue(callback)
```

另外，我们返回的数据可能并不是 JSON 格式，如果直接将 Call 的泛型指定为 String 类型的话，Gson 会解析失败，这个时候我们将泛型指定为 ResponseBody。

```Kotlin
// DemoService
@GET("/")
fun html(): Call<ResponseBody>

// Callback<ResponseBody>
 override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
    println(response.body()?.string())
}
```

## 参考

- 《第一行代码 Android 第三版》 - 郭霖
- OkHttp 文档：<https://square.github.io/okhttp/>
- Retrofit 文档：<https://square.github.io/retrofit/>
