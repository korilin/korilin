---
title: ThreadLocal 使用与原理分析
date: 2021-08-17
category: Oh! Java
---

破坏同一资源要素


```Java
public T get() {
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    if (map != null) {
        ThreadLocalMap.Entry e = map.getEntry(this);
        if (e != null) {
            @SuppressWarnings("unchecked")
            T result = (T)e.value;
            return result;
        }
    }
    return setInitialValue();
}
```

```Java
private T setInitialValue() {
    T value = initialValue();
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    if (map != null)
        map.set(this, value);
    else
        createMap(t, value);
    return value;
}

// 初始化值
protected T initialValue() {
    return null;
}
```

```Java
public void set(T value) {
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    if (map != null)
        map.set(this, value);
    else
        createMap(t, value);
}
```

```Java
void createMap(Thread t, T firstValue) {
    t.threadLocals = new ThreadLocalMap(this, firstValue);
}

ThreadLocalMap(ThreadLocal<?> firstKey, Object firstValue) {
    table = new Entry[INITIAL_CAPACITY];
    int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);
    table[i] = new Entry(firstKey, firstValue);
    size = 1;
    setThreshold(INITIAL_CAPACITY);
}
```

## 内存溢出问题

```Java
static class Entry extends WeakReference<ThreadLocal<?>> {
    /** The value associated with this ThreadLocal. */
    Object value;

    Entry(ThreadLocal<?> k, Object v) {
        super(k);
        value = v;
    }
}
```

ThreadLocal 对象并不会发生内存泄露，当我们将 ThreadLocal 引用置为 null 时，由于在 Thread 中的 ThreadLocalMap 中，对 ThreadLocal 是一个弱引用，因此发生 GC 时就会被回收。

所以在 ThreadLocalMap 中将存在 key 为 null 的 Entry，从这个方面讲，由于这个 Entry 的 value 是一个强引用，因此对应的 Object 不会被回收，这才发生了内存泄露

```Java
public void remove() {
    ThreadLocalMap m = getMap(Thread.currentThread());
    if (m != null)
        m.remove(this);
}

private void remove(ThreadLocal<?> key) {
    Entry[] tab = table;
    int len = tab.length;
    int i = key.threadLocalHashCode & (len-1);
    for (Entry e = tab[i];
            e != null;
            e = tab[i = nextIndex(i, len)]) {
        if (e.get() == key) {
            e.clear();
            expungeStaleEntry(i);
            return;
        }
    }
}

// WeakReference --> Reference
public void clear() {
    this.referent = null;
}
```

在 ThreadLocal 使用完后，置 null 前，应当调用 remove 移除对应的 Entry，让 Entry 和 value 的对象能够被回收。


## 参考

https://www.cnblogs.com/tkzL/p/12926797.html
