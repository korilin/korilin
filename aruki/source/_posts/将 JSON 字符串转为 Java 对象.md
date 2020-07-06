---
title: 将 JSON 字符串转为 Java 对象
date: 2020-3-14
categories: 技术笔记
tags:
    - Java
---

目前 Java 有很多 JSON 解析库，本文记录的是在开发中项目中使用了阿里巴巴的开源 JSON 解析库 fastjson, 来解析请求中的 JSON 字符串。

<!--more-->

**fastjson GitHub 地址：<https://github.com/alibaba/fastjson>**

## 引入 fastjson

在 maven 仓库下载 fastjson: <http://repo1.maven.org/maven2/com/alibaba/fastjson/>

或者配置 maven 依赖：

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>1.2.61</version>
</dependency>
```

## 使用 JSONObject

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

## 官方例子

```Java
import com.alibaba.fastjson.JSON;

Group group = new Group();
group.setId(0L);
group.setName("admin");

User guestUser = new User();
guestUser.setId(2L);
guestUser.setName("guest");

User rootUser = new User();
rootUser.setId(3L);
rootUser.setName("root");

group.addUser(guestUser);
group.addUser(rootUser);

String jsonString = JSON.toJSONString(group);

System.out.println(jsonString);
```

**输出：**

```Text
{"id":0,"name":"admin","users":[{"id":2,"name":"guest"},{"id":3,"name":"root"}]}
```

**使用到的类：**

```Java
public class Group {

    private Long       id;
    private String     name;
    private List<User> users = new ArrayList<User>();

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

    public List<User> getUsers() {
        return users;
    }

    public void setUsers(List<User> users) {
        this.users = users;
    }

    public void addUser(User user) {
        users.add(user);
    }
}
```

```Java
public class User {

    private Long   id;
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

## 使用注解的方式

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

## 参考

**fastjson 文档：<https://github.com/alibaba/fastjson/wiki>**
**菜鸟教程 Fastjson 简明教程：<https://www.runoob.com/w3cnote/fastjson-intro.html>**
