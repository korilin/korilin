---
title: 数据表 SQL 笔记
date: 2020-9-11
categories: 学习笔记
tags:
    - 数据库
---

### 数据完整性

数据完整性是指保护数据库中数据的正确性、有效性和相容性，防止错误的数据进入数据库造成无效操作。
SQL Server 提供的数据完整性机制包括：约束（Constraint）、默认（Default）、规则（Rule）、触发器（Trigger）、存储过程（Stored Procedure）等

<!-- more -->

### 约束定义

1. NULL/NOT NULL 约束
    - 语法格式：`[CONSTRAINT <约束名>] [NULL|NOT NULL]`
2. UNIQUE 约束（唯一约束）
    - 语法格式：`[CONSTRAINT <约束名>] UNIQUE`
3. PRIMARY KEY 约束（主键约束）
    - 列约束语法格式：`CONSTRAINT <约束名> PRIMARY KEY`
    - 表约束语法格式：`[CONSTRAINT <约束名>] PRIMARY KEY (<列名>[,{列名}])`
4. FOREIGN KEY 约束（外键约束）
    - 语法格式：`[CONSTRAINT <约束名>] FOREIGN KEY REFERENCES <主表名> (<列名>[,{列名}])`
5. CHECK 约束
    - 语法格式：`[CONSTRAINT <约束名>] CHECK (<条件>)`

```SQL
create table <表名> (
    <列名> <数据类型> [DEFAULT] [{列约束}],
    SNo VARCHAR(6) PRIMARY KEY, // 列主键约束
    SN VARCHAR(10) UNIQUE, // 唯一约束
    Sex CHAR(1) NOT NULL, // 非空约束
    Age INT CHECK (Age>=18 AND Age<=25), // CHECK 约束
    CNo VARCHAR(20) FOREIGN KEY REFERENCES C(CNo), // 外键约束
    CONSTRAINT SC_Prim PRIMARY KEY(SNo,CNo) //表主键约束
)
```

### 修改表

**新增列和完整性约束**

```SQL
ALTER TABLE <表名> ADD <列定义> | <完整性约束>
// 此方式增加的新列自动填充 NULL 指，不能为增加的新列指定 NOT NULL 约束

ALTER TABLE S ADD
Class_No VARCHAR(6), // 添加列
CONSTRAINT Score_Chk CHECK(Score BETWEEN 0 AND 100) //添加约束
```

**修改表中的列**

```SQL
ALTER TABLE <表名> ALTER COLUMN <列名> <数据类型> [NULL|NOT NULL]

ALTER TABLE S ALTER COLUMN
SN NVARCHAR(20) // 增加列长度
CNo VARCHAR(20) NULL // 修改NULL/NOT NULL约束
```

- 不能改变列名
- 不能将有空值得列的定义修改为 NOT NULL 约束
- 列中已有数据不能减少该列的宽度，也不能改变其数据类型
- 只能修改 NULL/NOT NULL 约束，其它类型的约束在修改前必须先将约束删除，重新添加修改过的约束定义

**删除完整性约束定义**

```SQL
ALTER TABLE <表名> DROP CONSTRAINT <约束名>
// 该方法只用于删除完整性约束定义

ALTER TABLE S DROP CONSTRAINT S_Prim
```

### 参考自

>《数据库原理及应用 第四版|微课版》 人民邮电出版社
