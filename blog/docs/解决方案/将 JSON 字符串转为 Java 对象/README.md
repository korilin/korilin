---
title: 将 JSON 字符串转为 Java 对象
date: 2021-1-16
categories: 解决方案
tags:
    - Java
    - Json
---

目前 Java 有很多 JSON 解析库，本文记录的是阿里巴巴的开源 JSON 解析库 fastjson 以及 Google 的 Gson, 来解析请求中的 JSON 字符串。

*fastjson 这段时间被爆出很多漏洞呀，没想到我选了一个代码质量最差的和一个运行速度最慢的*

<!-- more -->

## 使用 fastjson

**fastjson GitHub 仓库：<https://github.com/alibaba/fastjson>**

### Maven 引入 fastjson

在 maven 仓库下载 fastjson: <http://repo1.maven.org/maven2/com/alibaba/fastjson/>

或者配置 maven 依赖：

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>1.2.61</version>
</dependency>
```

### 使用 JSONObject

当我们发送一个请求后获取到了 JSON 字符串，可以使用 JSONObject 把字符串转换为 JSON 对象

```Java
// 发送请求
RestTemplate connect = new RestTemplate();
// 获取响应
ResponseEntity<String> response = connect.getForEntity(url);
// 获取响应数据
String body = response.body();
// 把字符串转换为JSON对象(反序列化)
JSONObject JSONdata = JSONObject.parseObject(body);
```

JSONObject 对象有 put 和 get 方法可以来存入和获取值，使用方法和 Map 差不多，如果是嵌套的 JSON 数据（通过 key 获取到的对象本质也是一个 JSON 字符串）, 要继续获取里面的值可以转为 JSONObject 对象

```Java
JSONObject jsonObj = new JSONObject();
// 传入数据
jsonObj.put("key", "value");
jsonObj.put("name", "aruki");
// 传入上面请求获取到的JSON对象
jsonObj.put("data", JSONdata);
// 获取数据
Object name = JSONdata.get("name");
JSONObject data = (JSONObject) respond.get("data");
// 可以直接获取字符串数据(序列化)
String info = data.getString("info");
```

当然 fastjson 的功能不仅仅这些，除了使用简单和速度快之外，fastjson 还有其他序列化和反序列化方式

参考官方例子：<https://github.com/alibaba/fastjson/wiki/Samples-DataBind>

### 使用注解的方式

```Java
public class User {
    @JSONField(name = "id")
    private Long id;

    @JSONField(name = "name")
    private String name;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

```Java
ArrayList<User> userList = new ArrayList<>();

userList.add(new User(1001L,"1号"));
userList.add(new User(1002L,"2号"));

String jsonStr = JSON.toJSONString(userList);

```

**jsonStr 的打印结果：**

```Text
[
    {
        "id":1001,
        "name":1号,
    },
    {
        "id":1002,
        "name":2号,
    }
]
```

## 使用 Gson

**Gson GitHub 仓库：<https://github.com/google/gson>**

### 在项目中引入

Gradle:

```groovy
dependencies {
  implementation 'com.google.code.gson:gson:2.8.6'
}
```

Maven:

```xml
<dependency>
  <groupId>com.google.code.gson</groupId>
  <artifactId>gson</artifactId>
  <version>2.8.6</version>
</dependency>
```

### JSON 字符串转 Java 对象

拥有一个 User 类，通过 Gson 对象的`fromJson()`方法将 Json 字符串转换为 User 对象。

```Java
Gson gson = new Gson();
User user = gson.fromJson(jsonStr, User.class);
```

### Java 对象转换为 JSON 字符串

当我们拥有一个 User 对象 user，可以通过 Gson 对象的`toJson()`方法将对象转换为 Json 字符串。

```Java
gson.toJson(user)
```

如果字符串中存在 Null 的字段，那么使用这种方法将不会序列化 Null 的属性，可以通过 GsonBuilder 对象来创建自定义 Gson 对象。我们可以在 GsonBuilder 对象设置 serializeNulls 来支持 Null 字段的序列化。

```Java
GsonBuilder gsonBuilder = new GsonBuilder().serializeNulls();
Gson gson = gsonBuilder.create()
```

## 相关文档

- **fastjson GitHub wiki：<https://github.com/alibaba/fastjson/wiki>**
- **Gson Google Sites：<https://sites.google.com/site/gson/gson-user-guide>**
