


而 LinkedList 直接 extends `AbstractSequentialList<E>` abstract 类，间接 extends `AbstractList<E>`，由于实现了 `Deque<E>`，它同时是 List 接口和 Queue 接口的实现类。

```Java
public class LinkedList<E> extends AbstractSequentialList<E>
    implements List<E>, Deque<E>, Cloneable, java.io.Serializable
```

![LinkedList](./LinkedList.png)