---
title: ListView 优化与 RecyclerView 解析
date: 2020-01-01
category: 分类
hidden: true
---

基础使用

```Kotlin
class DemoAdapter(activity:Activity, val resourceId:Int, data:List<Demo>):
    ArrayAdapter<Demo>(activity, resourceId:Int, data) {
        override fun getView(position:Int, convertView:View?, parent:ViewGroup): View {
            val view = LayoutInflater.from(context).inflate(resourceId, parent, false)
            if(getItem(position) )
        }
}
```

```Kotlin
val listViewAdapter = DemoAdapter(this, R.layout.list_item, demoList)
listView.adapter = adapter
```

布局重用
```Kotlin

```
