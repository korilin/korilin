---
title: Android 数据本地存储方案
date: 2021-7-19
category: Android
---

Android 开发中有 3 种持久化数据存储方案：**文件存储**、**SharePreferences**、**SQLite 数据库**。

这里做个笔记记录一下这 3 种方案的使用方式。

## 文件存储

文件存储就是将数据存储到文件中，使用 Context 提供的 API 来完成。

Android 系统中应用的文件默认存储在 `/data/data/<package name>/files/` 目录下，文件写入有两种操作模式可以选择：

- `MODE_PRIVATE` 写入的内容会覆盖原文件的内容
- `MODE_APPEND` 文件存在时往文件追加内容

无论哪种操作模式，指定的文件如果不存在时都会创建新的文件。

另外还有 `MODE_WORLD_READABLE` 和 `MODE_WORLD_WRITEABLE` 这两种模式允许其它应用对本应用的文件进行读写，但因为安全问题在 Android 4.2 中被废弃了。

文件存储的读写方式如下：

```Kotlin
try {
    // write data
    val output = openFileOutput("file_name", Context.MODE_PRIVATE)
    val writer = BufferedWriter(OutputStreamWriter(output))
    writer.use {
        it.write("some data")
    }

    // read data
    val input = openFileInput("file_name")
    val reader = BufferedReader(InputStreamReader(input))
    reader.use {
        it.forEachLine {
            line -> TODO("do something")
        }
    }
} catch (e: IOException) {
    // catch io exception
}
```

## SharedPreferences

SharedPreferences 是使用 XML 文件来存储数据，文件默认存储在 `/data/data/<package name>/shared_prefs/`，我们可以使用键值对来存储数据，并且可以支持多种基本数据类型。

使用 SharedPreferences 存储需要获取 SharedPreferences 对象，然后获取对象的 Editor 来进行操作。获取 SharedPreferences 对象有两种方式：

- Context 类的 `getSharedPreferences()` ：接收**文件名**和**操作模式**两个参数，目前可选操作模式只有 `MODE_PRIVATE` 一种，该模式的实际值是 `0`，其它的操作模式都被废弃了
- Activity 类中的 `getPreferences()` ：只接收**操作模式**一个参数，该方法默认将当前 Activity 的类名作为 SharedPreferences 的文件名

SharedPreferences 写入数据的方式如下：

```Kotlin
// val sp = getPreferences(Context.MODE_PRIVATE)
val sp = getSharedPreferences("file_name", 0)

val editor = sp.edit()

editor.putString("key1", "string")
editor.putInt("key2", 1)
editor.putBoolean("key3", true)

// editor.commit()
editor.apply()
```

SharedPreferences 修改数据时，是通过将数据先放到 Editor 里，再提交这些操作，提交方式有两种，这两种方式都是全量写入：

- `commit()` 是**同步**提交的方式，它会把 Editor 的操作直接写入到文件中，并且会阻塞当前线程，直到修改完成，并返回一个 Boolean 值来代表修改是否成功
- `apply()` 是**异步**提交的方式，它会将修改数据的原子操作提交到内存，再从内存异步提交到磁盘中的文件，因为提交到内存后文件操作结果是未知的，因此该方法没有返回值

SharedPreferences 存储数据的 XML 文件中，可能没有我们想要读取的 key，因此我们在读取数据的时候可以指定默认值，作为找不到对应值时返回的默认值，读取数据的方式如下：

```Kotlin
val sp = getSharedPreferences("file_name", 0)
val v1 = sp.getString("key1", "")
val v2 = sp.getInt("key1", 0)
val v3 = sp.getBoolean("key1", false)
```

## SQLite 数据库

在 Android 开发中使用 SQLite 数据库可以使用 SQLiteOpenHelper 来进行管理，它有两个方法可以获取 SQLiteDatabase 对象进行数据库操作，如果数据库不存在则创建新的数据库，存在则直接打开数据库：

- `getWritableDatabase()` 可读写方式，当磁盘空间已满，数据库不可写入时，会出现异常
- `getReadableDatabase()` 只读方式，不可写入这是一个抽象类，我们需要自己实现其抽象的方法。

SQLiteOpenHelper 是一个抽象类，需要我们去实现它的两个抽象方法：

- `onCreate()` 当找不到对应数据库时，会调用这个方法来执行我们创建数据库的操作
- `onUpgrade()` SQLiteOpenHelper 构造方法的第四个参数是版本号，如果当前的版本号大于原本数据库的版本号，会调用这个方法来执行我们更新数据库的操作

```Kotlin
const val databaseName = "ExampleDatabase.Name"
const val databaseVersion = 20210720

class ExampleDatabaseHelper(val context: Context) :
    SQLiteOpenHelper(context, databaseName, null, databaseVersion) {

    private val createSQL = """
        data table creation sql statement
    """

    private val upgradeSQL = """
        data table upgrade sql statement
    """

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(createSQL)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        db.execSQL(upgradeSQL)
    }
}
```

### 使用 SQLiteDatabase API 进行 CRUD

SQLiteDatabase 提供了一系列 API 来让我们不用写 SQL 语句也可以进行 CRUD 操作。

添加数据可以使用 `insert()` 方法，该方法有 3 个参数：
1. 数据表名
2. 指定一个可 NULL 的列，当第三个参数为 null 时或没有 put 数据时，将插入一个全为 NULL 的行，不需要该参数时可以指定为 null
3. ContentValues 对象，使用一系列 `put()` 方法来为每个列设置数据

```Kotlin
val tableName = "table name"

writableDatabase.insert(tableName, null, ContentValues().apply {
    put("column1", value1)
    put("column2", value2)
})
```

更新数据的话可以使用 `update()` 方法，它接收 4 个参数：
1. 数据表名
2. ContentValues 对象，指定修改的字段和新数据
3. 约束条件，不指定的话将会更新所有行
4. 传入一个数组，指定约束条件占位符的值

```Kotlin
writableDatabase.insert(tableName, ContentValues().apply {
    put("column2", newValue2)
}, "column1 = ?", arrayOf(value1))
```

删除操作使用 `delete`，第一个参数指定表名，第二和第三个参数指定约束条件

```Kotlin
writableDatabase.delete(tableName, "column2 > ?", arrayOf(100))
```

查询数据可以使用 `query()`，它最少需要指定 7 个参数。

| 参数 | 参数类型 | 对应 SQL | 描述 |
| -- | -- | -- | -- |
| table | String | from table_name | 查询的表名 |
| columns | String[] | select column1, column2 | 查询的列名 |
| selection | String | where column = ? | where 查询约束条件 |
| selectionArgs | string[] | - | 约束条件占位符的具体值 |
| groupBy | String | group by column | 指定分组的列 |
| having | String | having column = value | 分组后的约束条件 |
| orderBy | String | order by column1, column2 | 查询结果的排序方式 |

这些参数最终会被 `buildQueryString()` 方法拼接成查询 SQL 语句，不需要的参数可以指定为 null，具体使用方法如下：

```Kotlin
val cursor = writableDatabase.query(
    tableName, null, "column1 = ?", arrayOf(value1), null, null, null
)

if (cursor.moveToFirst()) {
    do {
        val value1 = cursor.getString(cursor.getColumnIndex("column1")),
        val value2 = cursor.getInt(cursor.getColumnIndex("column2"))
    } while (cursor.moveToNext())
}

cursor.close()
```

### 使用 SQL 语句进行 CRUD

使用 SQL 语句进行增删改都是使用 SQLiteDatabase 的 `execSQL()` 方法来执行 SQL 语句进行操作，而查询数据则是使用 `rawQuery()` 来执行查询获得 Cursor 数据游标。

```Kotlin
val db = writableDatabase

db.execSQL("insert into $tableName (column1, column2) values (?, ?)", arrayOf(value1, value2))
db.execSQL("update $tableName set column2 = ? where column1 = ?", arrayOf(value1, value2))
db.execSQL("delete from $tableName where column2 > ?", arrayOf(value2))

val cursor = db.rawQuery("select * from $tableName", null)
```

## 参考

> 《第一行代码 Android 第三版》 - 郭霖
> 
> SQLiteDatabase 部分源码和注释
> 
> SharedPreferences 源码注释
