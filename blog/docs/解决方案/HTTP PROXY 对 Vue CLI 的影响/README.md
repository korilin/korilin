---
title: HTTP PROXY 对 Vue CLI 的影响
date: 2020-11-6 13:00
categories: 解决方案
tags:
    - Vue.js
---

当计算机拥有代理服务时，通常命令行并不会走这个代理，如果我们希望命令行也走代理服务的话，需要在环境变量配置`HTTP_PROXY`和`HTTPS_PROXY`，将其指向对应的代理端口，这样就可以实现命令行也走网络代理了。

然而在实际的使用，并不是所有命令行的网络命令都需要使用代理，有一些在代理模式下某些模块也可能会出现错误，例如`@vue/cli`。

<!-- more -->

在我再次开发 Vue 项目的前一段时间，在环境变量配置了相对于 PROXY，让命令行也走代理，以便提高命令行下 npm 的下载国外包的速度。
然而这一次配置却让我本次使用 Vue CLI 的过程中花费了很长时间来研究请求失败这个问题。

当我使用`vue ui`来打开项目的时候，出现了如下`ERROR Failed to get response`这一问题。

```Powershell
@korilin ➜  ~  vue ui
🚀  Starting GUI...
🌠  Ready on http://localhost:8000
 ERROR  Failed to get response from https://registry.npm.taobao.org/vue-cli-version-marker
 ERROR  Failed to get response from https://registry.npm.taobao.org/core-js
 ERROR  Failed to get response from https://registry.npm.taobao.org/core-js
 ERROR  Failed to get response from https://registry.npm.taobao.org/vue
 ERROR  Failed to get response from https://registry.npm.taobao.org/vue
 ERROR  Failed to get response from https://registry.npm.taobao.org/vue-template-compiler
 ERROR  Failed to get response from https://registry.npm.taobao.org/vue-template-compiler
 ERROR  Failed to get response from https://registry.npm.taobao.org/eslint-plugin-vue
 ERROR  Failed to get response from https://registry.npm.taobao.org/eslint-plugin-vue
 ERROR  Failed to get response from https://registry.npm.taobao.org/babel-eslint
 ERROR  Failed to get response from https://registry.npm.taobao.org/babel-eslint
 ERROR  Failed to get response from https://registry.npm.taobao.org/eslint
 ERROR  Failed to get response from https://registry.npm.taobao.org/eslint
```

起初我以为是版本问题，官方有提到建议 Node 的最低版本，于是我依次将`@vue/cli`、`Node`、`npm`都升级到最新的稳定版本，然而这个操作并不起作用。

```Powershell
@korilin ➜  ~  node -v
v12.13.1
@korilin ➜  ~  npm -v
6.14.8
@korilin ➜  ~  vue -V
@vue/cli 4.5.8
```

于是我在 vue-cli 的 GitHUb 寻找相关的 Issues，希望可以得到有效的解决方案，在我发现报错信息里 npm 的镜像源是使用 taobao 镜像，于是我采用了尤雨溪在 Issues 中的一个提议。

修改用户目录下的`.vuerc`文件，将`useTaobaoRegistry`改为`false`，关闭 Vue CLI 使用淘宝镜像，但随机带来的依旧是这一个问题，只不过用另外一种方式呈现了。

报错信息还是那样，只不过这一次不是使用 taobao 镜像，而是 npm 原有的镜像。

```Powershell
 ERROR  Failed to get response from https://registry.npmjs.org/vue-cli-version-marker
 ERROR  Failed to get response from https://registry.npmjs.org/@vue/cli-plugin-babel
 ERROR  Failed to get response from https://registry.npmjs.org/@vue/cli-plugin-babel
 ERROR  Failed to get response from https://registry.npmjs.org/@vue/cli-service
 ERROR  Failed to get response from https://registry.npmjs.org/@vue/cli-plugin-eslint
 ERROR  Failed to get response from https://registry.npmjs.org/@vue/cli-service
 ERROR  Failed to get response from https://registry.npmjs.org/@vue/cli-plugin-eslint
```

即便我清除 npm 的缓存，或是将包管理器切换为`yarn`，结果也是一样请求失败。于是我将`@vue/cli`重装了一次，在此过程中继续在 Issues 寻找相关的解决方案。

虽然重装完依旧没能解决这个问题，但在 Issues 中有一个词引起了我的注意，那就是`proxy`，我发现在 vue-cli 和 npm 的 GitHub 中有一部分 Issues 提及到了 proxy，在一个中文 Issues 的回答中提及到这明显是网络问题，于是我将矛头指向了网络代理。此时我希望的是当我关闭代理时`@vue/cli`可以正常工作，但很遗憾在无代理、PAC、全局这 3 中配置下依旧没办法正常工作。

于是我查看了 windows 的环境变量配置，发现了之前配置的 HTTP_PROXY 和 HTTPS_PROXY，这两个配置导致无论本地开不开启网络代理服务，命令行都会走这个代理，直接在命令行使用`npm`命令将可以正常运行，但不知道什么原因导致在代理环境下内部请求无法使用网络，因此`@vue/cli`中的包管理器无法正常工作，此外`yrm`和`cgr`这一类工具的`test`命令也无法正常获得网络。

```Powershell
@korilin ➜  ~  cgr test

N npm ---- Fetch Error
  cnpm --- Fetch Error
Y taobao - Fetch Error
  yarn --- Fetch Error

@korilin ➜  ~  yrm test

* npm ---- Fetch Error
  cnpm --- Fetch Error
  taobao - Fetch Error
  nj ----- Fetch Error
  rednpm - Fetch Error
  npmMirror  Fetch Error
  edunpm - Fetch Error
  yarn --- Fetch Error
```

于是我修改了 HTTP_PROXY 和 HTTPS_PROXY 这两个配置，将命令行的代理关闭，此时`@vue/cli`和`yrm`、`cgr`的`test`命令就可以正常使用了，而内部具体原因还没探究清楚，时间原因就先放置着，有空再进行研究。

```Powershell
@korilin ➜  ~  yrm test

* npm ---- 1424ms
  cnpm --- 1456ms
  taobao - 1082ms
  nj ----- Fetch Error
  rednpm - Fetch Error
  npmMirror  3033ms
  edunpm - Fetch Error
  yarn --- Fetch Error

@korilin ➜  ~  cgr test

N npm ---- 908ms
  cnpm --- 1133ms
Y taobao - 1015ms
  yarn --- 1630ms
```
