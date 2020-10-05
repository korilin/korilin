---
title: SQL查询笔记
date: 2020-4-24
categories: 技术笔记
tags:
    - 数据库
---

这段时间终于是教SQL了, 还是习惯小写的SQL语句, 大写后总觉得有点不习惯。
上课基本都是在教查询就是了, 毕竟查询是用的最多的。
查询分单表查询和多表查询, 单表查询并不难, 主要难点都是在多表查询。

<!--more-->

## 单表查询

**记录一下之前没用过的和容易忘记的知识点:**

**通过`IN`操作查询属性值属于指定集合的元组, 也可以用or来替代, 不过值多了的话in看起来会简洁一点, 还可以用not in来查询指定集合外的元组, 也可以用在后面的多表查询。**

```SQL
select * from table where field in (value1,value2,...);
select * from table where field=value1 or field=value2 or ...;
select * from table where field not in (value1,value2,...);
```

**使用`LIKE`进行部分匹配查询(模糊查询), 似乎只能用在数据类型是字符的属性, 和正则表达式差不多。**

| 通配符 | 说明 |
| :--: | :--: |
| % | 代表0个或者多个字符 |
| _ | 代表一个字符 |
| [] | 表示某一范围的字符 |
| [^] | 表示不在某一范围的字符 |

```SQL
select * from table where field like 'name%';
select * from table where field like '_name%';
select * from table where field like 'name[0-9]';
select * from table where field like 'name[^0-9]';
```

好像老版本的SQL的中文字符要用两个下划线来匹配, 现在一个下划线也可以匹配一个中文了。

**要使用`IS NULL`来进行空值查询, 不能使用field==NULL。**

```SQL
select * from table where field is null;
```

**使用`HAVING`来对分组后的数据进行筛选。**

直接筛选表中的数据可以使用`WHERE`来做条件查询, 但是要给分组后的数据加上条件进行筛选就得使用`HAVING`了

```SQL
select field from table group by field having (count(*)>=2);
```

关于分组后的数据, 根据某个属性的值进行分组, 就只能直接查询该属性或者使用函数查询操作后的数据, 因为进行分组后得到的不是一个普通的二维表。

**查询结果排序可以使用`ORDER BY field DESC/ASC`, DESC为降序, ASC为升序。**

## 多表查询

### 连接查询

**连接方式:**

1、使用`FROM`子句指明连接的表, `WHERE`子句指明连接的列名和条件；
2、使用`[INNER|LEFT|RIGHT|FULL] JOIN table ON`进行连接。

**内连接查询:**

```SQL
select * from table1,table2 where table1.field=table2.field;
select * from table1 inner join table2 on table1.field=table2.field;
```

**外连接查询:**

```SQL
select * from table1 [left|rgiht|full] join table2 on table1.field=table2.field;
```

**交叉查询:**

```SQL
select * from table1 cross join table2;
```

查询结果的集合的行数是两个表行数的乘积, 列数是两个表列数的和。

**自连接查询:**

一个表与自身进行连接操作, 称为表的自身连接。

```SQL
select t1.field as tf1, t2.field as tf2
from table as t1, table as t2
where t1.field>t2.field;

select t1.field as tf1, t2.field as tf2
from table as t1 inner join table as t2
on t1.field>t2.field;
```

两个以上的表进行连接称为多表连接。

### 子查询

**普通子查询的执行顺序是由里到外处理, 将子查询的结果作为父查询的查询条件值。**

**返回一组值的普通子查询:**

`ANY`任意一个, 可用`IN`来代替`=ANY`
`ALL`代表全部

```SQL
select * from table where field = any(select field from table where 条件);
select * from table where field in (select field from table where 条件);
select * from table where field > all(select field from table where 条件);
```

按照逻辑来讲, ANY前面不应该使用不等于, 而ALL前面不应该使用等于。

**相关子查询:**

先在获取父查询的一条记录, 然后子查询根据这条记录相关的内容进行条件查询, 根据子程序的结果判断这一条记录是否满足查询条件。

```SQL
select * from table1 where field1 <> (select field2 from table2 where table1.tno!=table2.tno);
```

`EXISTS`表示存在的量词, 不返回任何实际数据, 只判断子程序返回的结果集合是否为空, `NOT EXISTES`

```SQL
select * from table1 where exists (select * from table2 where table1.tno=table2.tno);
-- 这句相当于 select * from table1,table2 where table1.tno=table2.tno;
```

**集合运算查询:**

`UNION`可以把不同查询的数据组合起来, 去除重复的数据, 形成一个合并的查询结果。
参加合并查询的各个子查询的结果的表结构必须相同。

```SQL
select field1,field2
from table where field3=value1
union
select field1,field2
from table where field3=value2;
```

**存储查询结果:**

可以使用`INTO`语句把查询结果存到一个新数据表或临时表中

```SQL
select field1,field2 into new_table from table;
-- into new_table 改成 into #new_table 就是存入临时表
```

既然能存入表, 按理也可以存入文件, 在MySQL中存到文件是用`INTO OUTFILE`。

参考自:
>《数据库原理及应用 第四版|微课版》 人民邮电出版社
