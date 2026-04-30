# 📦 Java泛型编程完整示例

## 🎯 案例概述

这是一个全面展示Java泛型机制的完整示例，通过实际代码演示泛型类、泛型方法、有界类型参数、通配符等核心概念，帮助你编写类型安全且可复用的Java代码。

## 📚 学习目标

通过本示例你将掌握：
- 泛型类的定义和使用方法
- 泛型方法的声明和调用
- 有界类型参数（Bounded Type Parameters）的使用
- 通配符（Wildcards）的三种形式及应用场景
- 类型安全的集合操作
- 泛型在方法重载和继承中的行为

## 📁 项目结构

```
java-generics-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/
    ├── main/java/com/opendemo/java/generics/
    │   ├── GenericBox.java         # 泛型类示例
    │   ├── GenericMethodDemo.java  # 泛型方法示例
    │   ├── BoundedTypeDemo.java    # 有界类型参数示例
    │   ├── WildcardDemo.java       # 通配符示例
    │   └── GenericsDemo.java       # 主程序入口
    └── test/java/com/opendemo/java/generics/
        └── GenericsDemoTest.java   # 单元测试
```

## 🚀 快速开始

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.generics.GenericsDemo"

# 运行测试
mvn test
```

## 📖 核心代码详解

### 1. 泛型类（Generic Class）

泛型类使用类型参数来定义可以操作多种类型的类。

```java
public class GenericBox<T> {
    private T content;

    public void set(T content) {
        this.content = content;
    }

    public T get() {
        return content;
    }
}

// 使用时指定具体类型
GenericBox<String> stringBox = new GenericBox<>("Hello");
GenericBox<Integer> intBox = new GenericBox<>(42);
```

**关键点：**
- 类型参数通常使用单个大写字母：`T`（Type）、`E`（Element）、`K`（Key）、`V`（Value）
- 编译器进行类型检查，消除运行时ClassCastException
- 不能使用基本类型，必须使用包装类

### 2. 泛型方法（Generic Method）

泛型方法在自己的方法签名中声明类型参数。

```java
public static <T> T getMiddle(T[] array) {
    return array[array.length / 2];
}

public static <T extends Comparable<T>> T findMax(T[] array) {
    T max = array[0];
    for (T item : array) {
        if (item.compareTo(max) > 0) max = item;
    }
    return max;
}

// 调用
Integer middle = getMiddle(new Integer[]{1, 2, 3});
Integer max = findMax(new Integer[]{3, 7, 1, 9});
```

**关键点：**
- 类型参数声明在返回值之前
- 可以有多个类型参数 `<T, U>`
- 支持有界约束 `<T extends Comparable<T>>`

### 3. 有界类型参数（Bounded Type Parameters）

限制类型参数的范围。

```java
// 上界约束：T必须是Number或其子类
public class NumberBox<T extends Number> {
    private T value;
    public double doubleValue() {
        return value.doubleValue();
    }
}

NumberBox<Integer> intBox = new NumberBox<>(10);     // OK
NumberBox<Double> doubleBox = new NumberBox<>(3.14);  // OK
// NumberBox<String> strBox = new NumberBox<>("hi");  // 编译错误
```

### 4. 通配符（Wildcards）

通配符提供了泛型类型的灵活性。

```java
// 无界通配符 ?
public static void printList(List<?> list) { ... }

// 上界通配符 ? extends T
public static double sumList(List<? extends Number> list) {
    double sum = 0.0;
    for (Number n : list) sum += n.doubleValue();
    return sum;
}

// 下界通配符 ? super T
public static void addIntegers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
}
```

**PECS原则（Producer Extends, Consumer Super）：**
- 如果需要从集合读取（生产者），使用 `? extends T`
- 如果需要向集合写入（消费者），使用 `? super T`
- 如果两者都需要，不要使用通配符

## 🔍 通配符对比

| 通配符 | 含义 | 可读 | 可写 | 示例 |
|--------|------|------|------|------|
| `?` | 任意类型 | 仅Object | 不可 | `List<?>` |
| `? extends T` | T或T的子类 | 可以 | 不可 | `List<? extends Number>` |
| `? super T` | T或T的父类 | 仅Object | 可以 | `List<? super Integer>` |

## ❓ 常见问题

### Q1: 什么是类型擦除？

Java泛型在编译时进行类型检查，编译后会擦除泛型信息。`GenericBox<String>` 和 `GenericBox<Integer>` 在运行时都是同一个类 `GenericBox`。

### Q2: 为什么不能创建泛型数组？

由于类型擦除，运行时无法保证数组元素的类型安全。可以使用 `List<T>` 或反射 (`Array.newInstance()`) 替代。

### Q3: 泛型方法和泛型类中的类型参数有什么区别？

泛型类的类型参数在整个类中有效，泛型方法的类型参数只在方法内有效。静态方法不能使用类的类型参数，需要单独声明。

### Q4: `<T extends Class>` 和 `<T extends Interface>` 有区别吗？

没有区别。Java中 `extends` 同时用于类和接口。多重约束使用 `<T extends ClassA & InterfaceB & InterfaceC>` 语法。

## 📈 扩展学习

- **Java集合框架**：大量使用泛型的实战案例
- **Java Stream API**：泛型与函数式编程结合
- **类型令牌模式（Type Token）**：通过 `Class<T>` 在运行时保留类型信息
- **Java泛型限制**：理解桥方法、类型擦除的影响
