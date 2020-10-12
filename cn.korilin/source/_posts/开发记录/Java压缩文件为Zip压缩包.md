---
title: Java 压缩文件为 Zip 压缩包
date: 2020-3-14
categories: 开发记录
tags:
    - Java
---

这是目前我尝试过的 Java 压缩文件最快的方法，使用 Channel 来将文件压缩成压缩包

压缩方法是建立一个压缩包文件对象，然后用 Zip 压缩流来输出压缩包，用输入流来写入压缩包，通过使用 Channel 建立两个流的通道，利用通道进行数据传输。

<!--more-->

## [压缩流](#压缩流)

```Java
File zipFile = new File("测试.zip");
ZipOutputStream zipOutputStream = new ZipOutputStream(new FileOutputStream(zipFile));
//file为文件位置
File toCompress = new File(file);
FileInputStream fileInputStream = new FileInputStream(toCompress);
```

每个压缩包可能会有多个文件，每个文件用 ZipEntry 对象来表示，所以将文件压缩到压缩包时要用`putNextEntry`来设置一个 ZipEntry 对象

```Java
zipOutputStream.putNextEntry(new ZipEntry(toCompress.getName()));
```

## [使用Channel](#使用Channel)

接下来我们可以使用字节写入的方式来将文件写入压缩包，但是一个字节一个字节写入会导致压缩速度非常慢，如果为写入字节设置缓冲区大小的话，又会导致写入内容多出一些无关内容

所以我们可以使用 Channel 的方式来写入文件

建立压缩包和文件的通道

```Java
WritableByteChannel writableByteChannel = Channels.newChannel(zipOutputStream);
FileChannel fileChannel = new FileInputStream(toCompress).getChannel();
```

然后通过使用`transferTo`直连两个通道传输数据来将文件写入压缩包，`transferTo`可以设置文件中的传输起点和传输的最大字节数，这样就不会造成写入的文件多出不可用的空白内容

```Java
// public abstract long transferTo(long position, long count, WritableByteChannel target) throws IOException;
// position代表传输起点, count代表传输最大字节数, target代表要连接的通道
fileChannel.transferTo(0, toCompress.length(), writableByteChannel);
```

最后将通道以及流关闭就完成了压缩，完整的压缩流程如下

```Java
// 压缩包输出流与压缩包写入通道
File zipFile = new File("测试.zip");
ZipOutputStream zipOutputStream = new ZipOutputStream(new FileOutputStream(zipFile));
WritableByteChannel writableByteChannel = Channels.newChannel(zipOutputStream);

// 文件输入通道
File toCompress = new File(file);
FileChannel fileChannel = new FileInputStream(toCompress).getChannel();

// 在压缩包内新建压缩文件空间与连接通道传输数据
zipOutputStream.putNextEntry(new ZipEntry(toCompress.getName()));
fileChannel.transferTo(0, toCompress.length(), writableByteChannel);

// 结束压缩
fileChannel.close();
writableByteChannel.close();
zipOutputStream.close();
```

## [文件夹压缩](#文件夹压缩)

当我们有多个文件需要压缩时，可以建立通过遍历或者递归的方式来将文件一个个压缩进入压缩包，这也是压缩文件夹的一个思路

**示例代码：**

```Java
public void CompressZip(ArrayList<String> files, String zipName) throws IOException{
    File zipFile = new File(zipName);
    ZipOutputStream zipOutputStream = new ZipOutputStream(new FileOutputStream(zipFile));
    WritableByteChannel writableByteChannel = Channels.newChannel(zipOutputStream);
    for(String file : files){
        File toCompress = new File(file);
        FileChannel fileChannel = new FileInputStream(toCompress).getChannel();
        zipOutputStream.putNextEntry(new ZipEntry(toCompress.getName()));
        fileChannel.transferTo(0, toCompress.length(),writableByteChannel);
        fileChannel.close();
    }
    writableByteChannel.close();
    zipOutputStream.close();
}
```

## [参考资料](#参考资料)

**压缩 20M 文件从 30 秒到 1 秒的优化过程：<https://juejin.im/post/5d5626cdf265da03a65312be>**
**FileChannal 文档：<https://docs.oracle.com/javase/7/docs/api/java/nio/channels/FileChannel.html>**
