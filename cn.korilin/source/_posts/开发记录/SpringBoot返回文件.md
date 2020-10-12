---
title: SpringBoot 返回文件
date: 2020-3-14
categories: 开发记录
tags:
    - Spring Boot
    - Java
---

项目开发需求，要在用户发送请求后把对应的数据打包成压缩包，再放回给浏览器，这种情况下无法使用`<a>`标签来进行跳转下载，所以我们可以通过返回文件的方式来，在压缩包打包后让浏览器下载

使用 ResponseEntity 配置 Http 的响应，在使用文件系统资源类 FileSystemResource 来把文件放入响应的数据中

<!--more-->

首先需要配置响应头和创建文件资源对象

```Java
// 创建文件资源对象, fileName为文件名
FileSystemResource file = new FileSystemResource(fileName);
// 响应头配置
HttpHeaders headers = new HttpHeaders();
headers.add("Cache-Control", "no-cache, no-store, must-revalidate");
// zipName为传输时文件的名称, 也就是下载后的文件名
headers.add("Content-Disposition", "attachment; filename=" + new String(zipName.getBytes(StandardCharsets.UTF_8), StandardCharsets.ISO_8859_1));
headers.add("Pragma", "no-cache");
headers.add("Expires", "0");
headers.add("Last-Modified", new Date().toString());
headers.add("ETag", String.valueOf(System.currentTimeMillis()));
```

这里的响应头有一个行是配置可以配置下载的文件的名称，由`Content-Disposition`的`filename`可来决定文件的名称，并且需要将字符串转为 UTF—8 的格式，这样才能支持中文。
由于消息头有特定的格式，所以要注意传入的文件名不能有双引号，否则会导致消息头格式错误返回无效的响应

接着返回带有文件的响应信息

```Java
return ResponseEntity
        .ok()
        .headers(headers)   // 传入响应头
        .contentLength(file.contentLength())    // 内容大小
        .contentType(MediaType.parseMediaType("application/octet-stream"))  // 传输类型
        .body(file);    // 传入文件到响应消息体
```

这样就可以把文件放回出去了

在我的项目里，完整代码是这样

```Java
@GetMapping("/downZip/{activity}/{collegename}")
    public ResponseEntity<FileSystemResource> downZip(@PathVariable String activity, @PathVariable String collegename) throws IOException {

        // 压缩文件
        operator = new Operator();
        operator.saveZip(fileInfoMapper.findFilenames(activity, collegename), activity, collegename);
        // 打开文件对象
        FileSystemResource file = new FileSystemResource("/www/website/contribute/static/" + activity + "/" + collegename + ".zip");
        // 传输的压缩包名称
        String zipName = collegename + ".zip";
        // 消息头
        HttpHeaders headers = new HttpHeaders();
        headers.add("Cache-Control", "no-cache, no-store, must-revalidate");
        headers.add("Content-Disposition", "attachment; filename=" + new String(zipName.getBytes(StandardCharsets.UTF_8), StandardCharsets.ISO_8859_1));
        headers.add("Pragma", "no-cache");
        headers.add("Expires", "0");
        headers.add("Last-Modified", new Date().toString());
        headers.add("ETag", String.valueOf(System.currentTimeMillis()));
        // 放回响应
        return ResponseEntity
                .ok()
                .headers(headers)
                .contentLength(file.contentLength())
                .contentType(MediaType.parseMediaType("application/octet-stream"))
                .body(file);
    }
```
