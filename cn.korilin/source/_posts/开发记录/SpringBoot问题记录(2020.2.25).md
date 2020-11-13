---
title: SpringBoot 问题记录 (2020.2.25)
date: 2020-2-25 23:44
categories: 开发记录
tags:
    - Java
    - Spring Boot
---

## 用 IDEA 新建一个带数据库依赖的 spring boot web 项目后运行出错

**运行报错内容如下：**

```Java
Description:

Failed to configure a DataSource: 'url' attribute is not specified and no embedded datasource could be configured.

Reason: Failed to determine a suitable driver class


Action:

Consider the following:
 If you want an embedded database (H2, HSQL or Derby), please put it on the classpath.
 If you have database settings to be loaded from a particular profile you may need to activate it (no profiles are currently active).
```

上面的报错内容是说 DataSource（数据源）配置错误：url 没有配置并且嵌入数据源没有配置
其实就是没有在配置文件里面配置数据库信息

<!--more-->

**解决方法：**

在 SpringBoot 配置文件里面配置数据源就好了，但是刚开始学习不知道怎么配置数据源，可以使用另外一种方法，忽略 web 项目的数据库依赖，也就是项目入口注解那里加上 exclude 传输，如下：

```Java
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
```

## 配置 thymeleaf3 无法正常使用

修改 thymeleaf 版本是在 properties 里修改 thymeleaf.version 和 thymeleaf-layout-dialect.version, 但是配置完发现没办法正常使用模板引擎

后来去 GitHub 查了一下依赖的版本，把版本都改成新的才解决了这个问题，所以我认为应该是 thymeleaf 的布局依赖的版本的问题

```xml
<thymeleaf.version>3.0.11.RELEASE</thymeleaf.version>
<thymeleaf-layout-dialect.version>2.4.0</thymeleaf-layout-dialect.version>
```

GitHub 发行地址
<https://github.com/thymeleaf/thymeleaf/releases>
<https://github.com/ultraq/thymeleaf-layout-dialect/releases>

## 访问外部文件

SpringBoot 的静态资源文件都放在 resource/static 下面，在 SpringBoot 里面可以直接访问到这个文件下的内容，但是，在部署的时候，会打包成 jar 包，这时这个文件夹在 jar 包里面，如果用户上传文件是无法上传到这里的，所以只能存在 jar 外部。
当文件保存在 jar 包外部的时候，springboot 想要访问这些资源，需要在配置文件里面指定静态资源目录，让 springboot 根据静态资源的规则去找到这个目录，这样在 jar 包外部的文件夹也可以在 springboot 内部或者通过浏览器访问到了。

**在配置文件指定静态资源目录：**

```propreties

spring.resources:static-locations: classpath:static/,file:static/

```

上面那个配置可以让 springboot 访问 jar 包同级目录下的 static 目录内的文件，或者是本地项目根目录下 static 目录内的文件
