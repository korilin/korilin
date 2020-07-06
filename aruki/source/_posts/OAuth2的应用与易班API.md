---
title: OAuth 2.0 框架与易班 API
date: 2020-7-6
categories: 技术笔记
tags:
    - OAuth 2.0
---

OAuth 是用于授权的行业开放标准协议，在这个标准中，用户可以在第三方应用访问该用户在某一平台上存储的资源，也就是我们经常看到的某些平台可以使用第三方账号登陆。
例如我们在学校中的一些平台可以使用易班账号进行登陆，登陆之后该平台能拿到我们存储在易班上的学生信息或对账号在易班平台上的资源进行其它操作。

该标准目前使用的版本是 2.0，目前网上关于该标准的介绍有很多，尤其是 okta 平台上的文章，对于 OAuth 2.0 的每个知识点几乎都有一篇文章来介绍，当然也因为 okta 本身就是一个面向开发者的授权认证平台。

<!-- more -->

## [文章声明](#文章声明)

- 由于 OAuth 是用于认证授权的，和客户端架构关系不大，所以本篇文章基于 B/S 架构的应用来讲解
- 为方便理解，我们在此声明一个例子，为下面的介绍提供具体对象的例子。例子：我们去访问知乎网站时，使用微博账号进行登陆
- 由于客户端和平台的界线在一部分人中存在模糊性，所以进行特殊声明：**在本文章中**的客户端可以理解为一个提供服务的应用个体，例如知乎的网站（包括后台），平台为承载服务的整体，两者关系为平台包含客户端，例如知乎的网站是知乎的一个应用，但在大部分情况下两者可理解为同一样东西
- 对于用户浏览的平台来说，用户登陆的账号所在的平台是第三方，所以有些页面显示其它登陆方式的时候会显示第三方账号登陆，但是对于用户来说授不授权取决于自己，完成授权操作的是用户，而提供授权和用户数据操作权限的是账号所在的平台，所以在 OAuth 的授权流程中，用户浏览的平台才是第三方

## [名词概念](#名词概念)

学习 OAuth 2.0 首先要理清楚一些相关的名词概念。

### User-Agent

用户代理，在 B/S 架构下的整个授权流程中，由于用户是使用浏览器进行操作，所以在这里用户代理指的是浏览器

### Client

指的是第三方客户端，也就是我们浏览的平台，相对于上面例子中的知乎，在授权认证流程中通常指的是第三方客户端的服务器

### Resource Owner

资源所有者，也就是用户（User）

### Authorization Server

授权服务器（认证服务器），用来对 Resource Owner 的身份进行验证，颁发 code（授权码）和 access token（授权令牌 / 访问令牌）

### Resource Server

资源服务器，服务商提供存放用户资源的服务器，资源服务器和授权服务器可以为同一台服务器，也可以是不同服务器。

## [授权类型](#授权类型)

在 OAuth 2.0 框架中多个授权方式，其中通用的有 4 种授权方式：
- 授权码模式（Authorization Code Grant）
- 隐式授权模式（Implicit Grant）
- 密码授权模式（Resource Owner Password Credentials Grant）
- 客户端凭证模式（Client Credentials Grant）

### [授权码模式](#授权码模式)

在所有授权模式中，授权码模式是流程最严密的一个授权模式了，由于用户在浏览器方面只需要获取一个授权码，获取访问令牌的过程是在服务器进行，用户是不可见的。

```md
    Authorization Code Flow (来自 RFC 6749)

    +----------+
    | Resource |
    |   Owner  |
    |          |
    +----------+
         ^
         |
        (B)
    +----|-----+          Client Identifier      +---------------+
    |         -+----(A)-- & Redirection URI ---->|               |
    |  User-   |                                 | Authorization |
    |  Agent  -+----(B)-- User authenticates --->|     Server    |
    |          |                                 |               |
    |         -+----(C)-- Authorization Code ---<|               |
    +-|----|---+                                 +---------------+
      |    |                                         ^      v
     (A)  (C)                                        |      |
      |    |                                         |      |
      ^    v                                         |      |
    +---------+                                      |      |
    |         |>---(D)-- Authorization Code ---------'      |
    |  Client |          & Redirection URI                  |
    |         |                                             |
    |         |<---(E)----- Access Token -------------------'
    +---------+       (w/ Optional Refresh Token)
```

授权码模式的授权流程如下：

(A) 用户访问客户端（Client），客户端将浏览器重定向到认证服务器的页面，重定向的 URL 会带上以下参数

- response_type：授权类型，必选项，在这个授权模式下固定值为”code“
- client_id：客户端 ID，必选项，用来标识是哪个客户端请求授权
- redirect_uri：重定向地址，可选项，用来让浏览器携带 code 重定向到客户端的接收地址，通常情况下都必须加上这个参数
- scope：授权的权限范围，可选项
- state：客户端当前状态，可选项，可以为任意值，授权服务器 code 的时候也会返回这个值，用来确认这个响应是客户端请求授权后授权服务器进行的响应，而不是其它人随便发过来的

(B) 用户选择是否给客户端进行授权，如果用户同意授权，那么进入 (C)
(C) 授权服务器将浏览器重定向到原本客户端指定的 redirect_uri（重定向地址），在地址上附带上授权码和 code（授权码）设定的 state
(D) 客户端服务器拿到 code，带上这个 code 和先前的 redirect_uri, 向认证服务器申请访问令牌
(E) 认证服务器核对 code 和 redirect_uri 通过后，将 access_token（访问令牌）响应给客户端，响应包含以下数据

- access_token：访问令牌，必选项
- token_type：令牌类型，必选项
- expires_in：令牌的过期时间，必选项
- refresh_token：更新令牌，可选项，用来获取下一次访问令牌
- scope：权限范围：如果和客户端一致可省略

### [隐式授权模式](#隐式授权模式)

```md
    Implicit Grant Flow (来自 RFC 6749)

    +----------+
    | Resource |
    |  Owner   |
    |          |
    +----------+
        ^
        |
        (B)
    +----|-----+          Client Identifier     +---------------+
    |         -+----(A)-- & Redirection URI --->|               |
    |  User-   |                                | Authorization |
    |  Agent  -|----(B)-- User authenticates -->|     Server    |
    |          |                                |               |
    |          |<---(C)--- Redirection URI ----<|               |
    |          |          with Access Token     +---------------+
    |          |            in Fragment
    |          |                                +---------------+
    |          |----(D)--- Redirection URI ---->|   Web-Hosted  |
    |          |          without Fragment      |     Client    |
    |          |                                |    Resource   |
    |     (F)  |<---(E)------- Script ---------<|               |
    |          |                                +---------------+
    +-|--------+
    |    |
    (A)  (G) Access Token
    |    |
    ^    v
    +---------+
    |         |
    |  Client |
    |         |
    +---------+
```

### [密码授权模式](#密码授权模式)

```md
    Resource Owner Password Credentials Flow (来自 RFC 6749)

    +----------+
    | Resource |
    |  Owner   |
    |          |
    +----------+
        v
        |    Resource Owner
        (A) Password Credentials
        |
        v
    +---------+                                  +---------------+
    |         |>--(B)---- Resource Owner ------->|               |
    |         |         Password Credentials     | Authorization |
    | Client  |                                  |     Server    |
    |         |<--(C)---- Access Token ---------<|               |
    |         |    (w/ Optional Refresh Token)   |               |
    +---------+                                  +---------------+
```

### [客户端凭证模式](#客户端凭证模式)

```md
    Client Credentials Flow (来自 RFC 6749)

    +---------+                                  +---------------+
    |         |                                  |               |
    |         |>--(A)- Client Authentication --->| Authorization |
    | Client  |                                  |     Server    |
    |         |<--(B)---- Access Token ---------<|               |
    |         |                                  |               |
    +---------+                                  +---------------+
```

## [参考资料](#参考资料)

> RFC 6749：https://tools.ietf.org/html/rfc6749
> 理解 OAuth 2.0 - 阮一峰的网络日志：https://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html

