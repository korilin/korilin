---
title: 视图与索引 SQL 笔记
date: 2020-4-26
categories: 学习笔记
tags:
    - 数据库
    - SQL
---

视图是一个由查询定义内容的虚拟表，和基本表差不多，不过在数据库中并不上以数据值存储集形式存在的，除非是索引视图。
作用可以用来做筛选，而且定义视图可以来自多个表或者其它视图。

索引是一种加快检索的数据库结构，包含从表或视图的列生成的键和映射到指定数据存储位置的指针。
索引由 DBMS 自动管理和维护。

<!-- more -->

### 视图的操作

我觉得所有操作中，最麻烦的就是创建视图了，SQL 创建视图有可选参数

```SQL
create view view_name [ (column [ ,...n ]) ] -- 视图名和视图列名称
[ with <view_attribute> [ ,...n ] ] -- 定义视图时的参数
as select_statement -- 定义视图的select语句, 可以使用多个表或者其它视图
[ with check option ] [ ; ]
<view_attribute> ::= -- 参数包括以下
{
    [ encryption ] -- 加密后无法修改视图
    [ schemabinding ] -- 和底层应用的表进行定义绑定, 不难随便修改引用的表的架构
    [ view_metadata ] -- 返回视图自身列定义, 而不是底层表列的定义
}

-- 一个简单的创建例子

create view TCView(class, num)
as select class, count(*) from T group by class;
```

修改视图可以使用 SQL 的`ALTER VIEW`来修改

```SQL
alter view TCView(class, num)
as select class, count(*) from T group by class;
```

删除视图用`DROP VIEW`来删除

```SQL
drop view TCView;
```

查询视图和对基本表的查询操作一样

```SQL
select num from TCView where class=1;
```

因为视图是一张虚拟表，数据是对基本表的引用，所以对视图的数据进行更新会转换成对基本表的更新，包括增删改操作
视图增删改的 SQL 语法和基本表的一样，但是修改视图时有注意点：
1、插入时必须保证插入操作能在基本表里面插入数据，否则会插入失败，插入数据时
2、修改和删除数据时只能对一张表进行操作，无法同时操作多张表

```SQL
insert into view_name values (value1, value2, ...);
update view_name set field1=value2 where field2=value2;
delete from view_name where field1=value2;
```

### 索引

**索引基本类型：聚集索引和非聚集索引**
**索引其它类型：唯一索引、视图索引、全文索引、XML 索引**

创建索引

```SQL
create [ unique ] [ clustered ] [ nonclustered ] index index_name
on table_or_view_name ( column_name [ asc | desc ] [ ,...n ] )
[ with <index_option> [ ,...n ] ]
[ on { filegroup_name | "default" } ]
```

unique 表示创建唯一索引，clustered 表示创建聚集索引，nonclustered 表示创建非聚集索引

```SQL
-- 为表SC在SNo和CNo上创建唯一索引
create unique index SCI on SC(SNo,CNo);
```

修改索引

```SQL
alter index { index_name | all }
on table_or_view_name
{
    rebuild
        [
            [partition = ALL]
            [
                with ( <rebuild_index_option> [ ,...n ] )
            ] | [
                partition = pratition_number
                [ with ( <single_partition_rebuild_index_option> [ ,...n ] ) ]
            ]
        ]
    | disable
    | reorganize
        [
            [ partition = pratition_number ]
            [ with ( lob_compaction = { ON | OFF } ) ]
        ]
    | set ( <set_index_option> [ ,...n ] )
}
```

首先我没看懂这东西，好像也不经常用的亚子，就先在这放着吧

删除索引

```SQL
drop index <table or view name>.<index name>;
drop index <index name> on <table or view name>;
```

查看索引

```SQL
exec Sp_heplindex [@objname =] 'name';
```

更改索引名

```SQL
exec Sp_rename 'table_name.old_index_name', 'new_index_name';
```

*说实话看了这么久我还是不明白索引怎么用？*

>参考自：《数据库原理及应用 第四版|微课版》 人民邮电出版社
