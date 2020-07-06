---
title: Nginx请求处理配置
date: 2020-3-18 16:20
categories: 技术笔记
tags:
    - Nginx
---

Nginx可以用来做Web服务器或者反向代理，当Nginx作为反向代理软件时，每个网络请求都会先由Nginx接收，Nginx会根据配置文件里的配置对请求进行过滤处理，等请求完全接收完再发送给上游服务器一次性处理，从而可以提高上游服务器的工作性能。
<!--more-->
以下是Nginx常用的一些http请求连接的配置。

## [Http请求配置项](#Http请求配置项)

### [Http包头读取超时时间](#Http头部读取超时时间)

```config
语法: client_header_timeout time(默认单位: 秒);
默认: client_header_timeout 60;
配置块: http、server、location
```

### [Http包体读取超时时间](#Http头部读取超时时间)

```config
语法: client_body_timeout time(默认单位: 秒);
默认: client_body_timeout 60;
配置块: http、server、location
```

### [Http包体最大值](#Http消息体最大值)

该配置影响请求消息体的最大值，Http包头会有一个Content-Length的字段，代表Http包体的大小，如果这个值超过了client_max_body_size的值，将会中断连接返回413("Request Entity Too Large")响应给客户端

```config
语法: client_max_body_size size;
默认: client_max_body_size 1m;
配置块: http、server、location
```

### [请求的限速](#请求的限速)

限制客户端每秒传输的字节数，0代表不限速

```config
语法: limit_rate speed;
默认: limit_rate 0;
配置块: http、server、location、if
```

### [响应发送超时时间](#响应发送超时时间)

```config
语法: send_timeout time;
默认: send_timeout 60;
配置块: http、server、location
```

## [长连接配置项](#长连接配置项)

### [禁用某些浏览器使用keepalive](#禁用某些浏览器使用keepalive)

keepalive可以让多个请求服用一个HTTP长连接来提高服务器性能，但是IE6及其早期版本、Safari浏览器对使用keepalive功能的POST请求处理有问题，所以Nginx默认禁用了keepalive功能

```config
语法: keepalive_disable [ msie6 | safari | none ]...;
默认: keepalive_disable msie6 safari;
配置块: http、server、location
```

### [keepalive超时时间](#keepalive超时时间)

当一个keepalive连接闲置超过一段时间后(默认75秒)，服务器和浏览器会关闭这个连接，keepalive_timeout配置项用来约束Nginx服务器，Nginx会按照规范把这个时间传给浏览器

```config
语法: keepalive_timeout time(默认单位: 秒);
默认: keepalive_timeout 75;
配置块: http、server、location
```

### [一个keepalive长连接允许承载的请求最大数](#一个keepalive长连接允许承载的请求最大数)

```config
语法: keepalive_requests n;
默认: keepalive_requests 100;
配置块: http、server、location
```

## [连接关闭配置项](#连接关闭配置项)

### [关闭用户连接的方式](#关闭用户连接的方式)

always: 关闭连接前必须处理连接上所有用户的数据
on: 关闭连接前会处理连接上的用户数据，除了一些情况下业务上认定关闭连接后是不必要的数据
off: 不管是否已经有准备就绪的用户数据都关闭连接

```config
语法: lingering_close off|on|always;
默认: lingering_close on;
配置块: http、server、location
```

### [连接关闭时间](#连接关闭时间)

在返回响应后经过lingering_time设置的时间，Nginx将不管用户是否仍在上传，都会关闭连接

```config
语法: lingering_time time;
默认: lingering_time 30s;
配置块: http、server、location
```

### [连接关闭延迟](#连接关闭延迟)

在关闭连接前，如果超过lingering_timeout时间后没有数据可读，直接关闭连接；否则，读取完连接缓冲区上的数据并丢弃后才会关闭连接

```config
语法: lingering_timeout time;
默认: lingering_timeout 5s;
配置块: http、server、location
```
