---
title: MySQL增删改查
date: 2019-4-9
tags: 
    - MySQL
    - 编程学习
categories: 数据库
---
{% note primary %} 
**建数据库      `create database database_name;`**
**查看数据库    `show databases;`**
**选择数据库    `use database_name;`**
**删除数据库    `drop database database_name;`**
{% endnote %}

{% note info %} 
**创建建数据表  `create table table_name(column_name column_type);`**
**查看表创建语句 `show create table table_name`**
**查看数据表    `show tables;`**
**删除数据表    `drop table table_name;`**
{% endnote %}

{% note success %} 
**查看表结构    `describe table_name;`**
**查看表数据    `select * from table_name;`**
**添加表数据    `insert into table_name (column_name) value (value_name);`**
**修改表数据    `update table_name set 修改内容 where 条件`**
**删除表数据    `delete from table_name where 条件;`**
{% endnote %}

{% note default %} 
**键类型：      primary unique**
**增加属性      `alter table table_name add 属性;`**
**查看属性      `show variables like '属性%';`**
**修改属性      `alter table table_name modify 属性;`**
**删除属性      `alter table table_name drop 属性;`**
**修改自增长值  `alter table table_name auto_increment=value;`  修改自增长值时不能比当前值小**
**清除自增长    `alter table table_name modify column_name cloumn_type;` 修改字段时如果没有添加自增长，就可以把自增长清除了**
**删除唯一键    `alter table table_name drop index unique_name;`**
{% endnote %}

### 注意点
>**主键只能创建一个：一个主键可以选择多个字段，但是不可以创建多个主键**
>**自动增长只能用于数值，一张表只能拥有一个自增长**
>**无法修改唯一键，只能通过先删除后增加的方式**

### 内容更新中......
