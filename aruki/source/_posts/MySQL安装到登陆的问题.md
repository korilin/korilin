---
title: MySQL安装到登陆的问题
date: 2019-4-8
tags: 
    - MySQL
    - windows命令
categories: 数据库
top: 20190408
---
{% note warning %} 
**经过一晚上的折腾，我终于登陆进数据库了！！这期间遇到了不少问题，虽然网上有很多解决方案，但要找到适用的真的不容易，每个问题都花了很长时间去尝试那些指令，绕了很多弯路才解决。**
{% endnote %}

### 端口冲突
**安装完遇到的第一个问题就是，没办法打开mysql服务，删了安装目录下的date文件夹重新用`mysqld --initialize`初始化，重新配置my.ini文件都没用。**
**之后用`mysqld --console`查了错误信息发现了端口被占用了：**
>**[ERROR] Can't start server: Bind on TCP/IP port: Address already in use**
>**[ERROR] Do you already have another mysqld server running on port: 3306 ?**

**因为我这边的命令行无法识别`netstat -nltp|grep mysql`，到后面才用`netstat  -aon|findstr 3306`查到了占用3306端口的进程，记住了进程后面的PID号，用`taskkil /f /pid 对应的PID号`把进程给杀了才解决问题**

### 无法登陆
**耗了一些时间后，我用`net start mysql`开启了数据库后，用`mysql -uroot -密码`尝试登陆，结果又报了一个这样的错误**
>**mysql: [ERROR] mysql: unknown option '-R'.**

**于是用`mysql -uroot -p`后再输入密码,才知道原先输入密码前也要加个p，也就是`mysql -uroot -p密码`。**
**但是接下来又报了一个错误**
>**mysql: [Warning] Using a password on the command line interface can be insecure.**
>**ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)**

**查了一下发现是密码错误，因为我输入的是安装时的密码，但是初始化的时候密码重置了，所以密码错了，所以我又绕了一次弯路，把date删了重新初始化了一遍，把初始化输出的临时密码记了下来**
>**[Note] A temporary password is generated for root@localhost: TKk51x#bOi0S**
**之后就可以成功登陆了**

### 修改密码
**登陆后没办法使用其他语句，说是必须修改一下密码，而且自动生成的密码太难记了，我想改回自己的密码，但是在网上查了很多指令都用不成功，错误提示的ALTER USER语句也不知道怎么用，所以又上网馊了一下，还看了一下官方文档，总结就是看不懂【**
**查到最后终于发现了一个可以用的语句**
>`alter user 'root'@'localhost' identified by 'password';`

**这下问题终于解决了，可以开始进一步学习了。**

{% note info %} 
**虽然遇到了很多问题，但是也知道了很多MySQL和命令行的语句，有些没派上用场就是了，至少折腾了一夜一些有用的语句都变熟悉了。**
{% endnote %}