---
title: Nginx 性能优化：worke 进程
date: 2020-2-8 3:30
categories: 学习笔记
tags:
    - Nginx
---

在 Nginx 中，是由 master 进程来管理 worker 进程的工作，由 worker 进程来处理 http 请求。
一个 worker 进程可以同时处理多个请求，其处理的请求数只受限于内存大小，并且不同的 worker 进程之间处理并发请求几乎没有同步锁的限制，worker 进程通常不会进入睡眠状态。

<!-- more -->

多个 worker 进程处理互联网请求既可以实现多核并发处理，也可以提高服务的健壮性，所以 worker 进程的数量将会直接影响性能。
在 master/worker 运行方式下，我们可以通过修改 worker_processes 配置项的值来配置 worker 的进程数

```Nginx
语法: worker_processes number;
默认: worker_processes 1;
```

**进程数量的设置和业务以及 CPU 内核数有关：**

worker 进程都是单线程进程，会调用各个模块来实现功能。
如果这些模块不会出现阻塞式的调用，通常有多少个 CPU 内核就配置多少个进程数量。
如果可能出现阻塞式调用，则需要配置稍多一些的 worker 进程。

**什么是阻塞式调用？**例如用户请求会读取本地磁盘的静态资源文件，且服务器内存小，大部分的请求访问静态资源文件时都必须读取磁盘，而不是内存中的磁盘缓存，那么磁盘 I/O 的调用可能会阻塞住 worker 进程少量时间，导致服务整体性能下降。

多 worker 进程可以充分利用多核系统架构，但 worker 进程的数量多于 CPU 内核数，将会增大进程间切换带来的消耗 (Linux 是抢占式内核）, 这也是为什么要配置和 CPU 内核数量一致的进程数的原因。

**配置与内核数量相等的 worker 进程时，要绑定 CPU 内核：**

假如每一个 worker 进程都非常繁忙，多个 worker 进程都在抢同一个 CUP 的话，会出现同步问题。反之，如果每一个 worker 进程都独享一个 CPU, 就在内核的调度策略上实现了完全的并发。

我们可以通过 worker_cpu_affinity 绑定 Nginx worker 进程到指定的 CPU 内存：

```Nginx
语法: worker_cpu_affinity cpumask [cpumask...]
默认: -
```

例如你有 4 个 CPU 内核，可在配置文件中进行如下配置，将进程数配置为 4, 绑定每个工作进程到单个 CPU 里：

```Nginx
worker_processes 4;
worker_cpu_affinity 1000 0100 0010 0001;
```

如果使用下面的配置的话，将会把第一个 worker 进程绑定到 CPU0/CPU2, 第二个进程绑定到 CPU1/CPU3:

```Nginx
worker_processes 2;
worker_cpu_affinity 0101 1010;
```

使用 auto 值可自动将 worker 进程绑定到可用 CPU:

```Nginx
worker_cpu_affinity auto;
```

worker_cpu_affinity 配置仅对 Linux 操作系统有效。
Linux 操作系统使用 sched_setaffinity() 系统调用实现这个功能。

**优先级设置：**

在 Linux 或者其它类 UNIX 操作系统中，当许多进程都处于可执行状态时，会按照所有进程的优先级来决定本次内核执行哪个进程，进程分配的 CPU 时间片大小也与进程优先级相关，优先级越高进程分配到的时间片越大。

我们可以通过 worker_priority 配置项来设置 worker 进程的 nice 优先级

```Nginx
语法: worker_priority nice;
默认: worker_priority 0;
```

nice 值是进程的静态优先级，他的取值范围是 -20 ~ +19, -20 是最高优先级，+19 是最低优先级；
优先级由静态优先级和内核根据进程执行情况所做的动态调整（目前只有±5 的调整）共同决定。
优先级高的进程会会占用更多的系统资源，如果希望 Nginx 占用更多的系统资源，可以把 nice 的值配置得小一点；
一般分配时不建议 nice 的值比内核进程的 nice 值（通常为 -5) 还要小。

**SSL 硬件加速：**

如果服务器上有 SSL 硬件加速设备，可以进行配置加快 SSL 协议的处理速度。

通过 OpenSSL 的命令查看是否有 SSL 硬件加速设备：`openssl engine -t`

Nginx 配置加速：

```Nginx
ssl_engine device;
```

>参考书籍《深入理解 Nginx 模块开发与架构解析 第 2 版》 陶辉 著 机械工业出版社
