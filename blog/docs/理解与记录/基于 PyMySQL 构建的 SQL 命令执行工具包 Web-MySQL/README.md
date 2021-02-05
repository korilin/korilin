---
title: 基于 PyMySQL 构建的 SQL 命令执行工具包 Web-MySQL
date: 2020-1-30 1:49
categories: 理解与记录
tags:
    - Python
    - MySQL
---

### [简介](#简介)

Web-MySQL 是一个是基于 PyMySQL 构建出来的一个简单的 SQL 命令执行工具包，用于后端使用 Python 连接数据库的包。

目前为个人为方便进行数据库 CRUD 操作在 PyMySQL 的基础上进行封装，已发布到 PyPi，可以使用 pip 命令进行安装。

主要使用 Connector 类的 executor、fetchone 和 fetchall 这 3 个功能，调用了 PyMySQL 的功能进行自动连接数据库和断开连接。

使用 Web-MySQL 的时候，需要导入 Web-MySQL 的 Connector 类，创建一个对象并初始化数据库配置，就可以调用函数对相应的 MySQL 数据库执行 SQL 命令。

GitHub仓库地址：[https://github.com/korilin/Web-MySQL](https://github.com/korilin/Web-MySQL)

<!-- more -->

### [使用](#使用)

首先它开发时是采用 Python 3，所以确保你的环境是 Python 3。

可以使用 pip 安装来 Web-MySQL：`pip install Web-MySQL`

使用时推荐将操作这个数据库的函数写在一个单独 Python 文件里，方便函数的管理和引入使用，创建一个全局的 Connector 实例，并修改实例中连接数据库的相应信息变量

调用相应函数传入 SQL 命令和 values 就可以执行数据库操作，当 SQL 命令中没有需要传入的变量时，可不传入 values, 默认 values 为 None。

### [示例](#示例)

```Python
from web_mysql import Connector

connector = Connector()
connector.host = "localhost"
connector.user = "root"
connector.password = "123456"
connector.database = "test"

def insert_user():
  sql = "insert into users (name,id) values (%s,%s);"
  values = ["name", 10001]
  connector.executor(sql, values)

def get_user(name, id):
  sql = "select * from users where name=%s and id=%s;"
  values = [name, id]
  user = connector.fetchone(sql, values)

def get_users():
  sql = "select * from users;"
  all_user = connector.fetchall(sql)
```

### [建议](#建议)

对不同数据库进行操作是应当在不同文件下创建另外一个 connector 实例，这也是为什么要将该数据库的操作函数写在同一个单独的 Python 文件里，这样有利于代码的维护。

当然也可以使用类来代替文件，此时应有多个 Python 类来创建不同的实例去操作不同的数据库

### [相关](#相关)

**PyMySQL：<https://github.com/PyMySQL/PyMySQL>**
