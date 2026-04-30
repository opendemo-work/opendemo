# λ Java Lambda表达式完整示例

## 🎯 案例概述

这是一个全面展示Java Lambda表达式和函数式编程的完整示例，通过实际代码演示Lambda语法、函数式接口、方法引用、Stream API等核心概念，帮助你掌握Java 8+函数式编程范式。

## 📚 学习目标

通过本示例你将掌握：
- Lambda表达式的基本语法和多种写法
- 自定义函数式接口的定义和使用
- Java内置函数式接口（Predicate, Consumer, Function, Supplier）
- 方法引用的四种形式
- Stream API的核心操作（filter, map, reduce, sorted等）
- 函数式编程的思维方式

## 📁 项目结构

```
java-lambda-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/
    ├── main/java/com/opendemo/java/lambda/
    │   ├── StringProcessor.java        # 自定义函数式接口
    │   ├── LambdaDemo.java             # 主程序入口
    │   ├── FunctionalInterfaceDemo.java # 函数式接口示例
    │   └── StreamApiDemo.java          # Stream API示例
    └── test/java/com/opendemo/java/lambda/
        └── LambdaDemoTest.java         # 单元测试
```

## 🚀 快速开始

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.lambda.LambdaDemo"

# 运行测试
mvn test
```

## 📖 核心代码详解

### 1. Lambda表达式基础

Lambda表达式是匿名函数的简洁表示，用于实现函数式接口：

```java
// 无参数
() -> System.out.println("Hello")

// 单参数（可省略括号）
s -> s.length()

// 多参数
(a, b) -> a + b

// 多行代码块
(x, y) -> {
    int sum = x + y;
    return sum;
}

// 显式声明类型
(String s) -> s.toUpperCase()
```

**语法规则：**
- `(参数列表) -> {方法体}`
- 单参数可省略括号：`x -> x * 2`
- 单行表达式可省略大括号和return：`x -> x * 2`
- 类型可以自动推断，也可以显式声明

### 2. 自定义函数式接口

函数式接口是只包含一个抽象方法的接口：

```java
@FunctionalInterface
public interface StringProcessor {
    String process(String input);

    // 可以有default方法
    default String processWithDefault(String input) {
        if (input == null) return "null";
        return process(input);
    }
}

// 使用Lambda实现
StringProcessor toUpper = s -> s.toUpperCase();
StringProcessor reverse = s -> new StringBuilder(s).reverse().toString();
```

### 3. Java内置函数式接口

Java 8在 `java.util.function` 包中提供了大量内置函数式接口：

```java
// Predicate<T> - 判断型，返回boolean
Predicate<String> isLong = s -> s.length() > 5;
Predicate<String> isEmpty = s -> s == null || s.isEmpty();
Predicate<String> complex = isEmpty.negate().and(isLong);

// Consumer<T> - 消费型，无返回值
Consumer<String> print = s -> System.out.println(s);
Consumer<String> printLength = s -> System.out.println(s.length());
print.andThen(printLength).accept("Hello");

// Function<T, R> - 转换型，T -> R
Function<String, Integer> length = String::length;
Function<Integer, String> toString = Object::toString;
length.andThen(toString).apply("Hello");  // "5"

// Supplier<T> - 供给型，无参有返回
Supplier<String> greeting = () -> "Hello";
Supplier<Double> random = Math::random;
```

### 4. 方法引用

方法引用是Lambda表达式的简写形式，共有四种类型：

```java
// 1. 静态方法引用：类名::静态方法
Function<String, Integer> parse = Integer::parseInt;

// 2. 实例方法引用：对象::方法
Function<String, String> upper = String::toUpperCase;

// 3. 特定类型的实例方法引用：类名::方法
BiPredicate<String, String> equals = String::equals;

// 4. 构造方法引用：类名::new
Supplier<List<String>> listSupplier = ArrayList::new;
```

### 5. Stream API核心操作

Stream API将函数式编程风格引入集合操作：

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

// filter - 过滤
List<String> filtered = names.stream()
    .filter(name -> name.length() > 3)
    .collect(Collectors.toList());

// map - 映射
List<String> upper = names.stream()
    .map(String::toUpperCase)
    .collect(Collectors.toList());

// reduce - 归约
String result = names.stream()
    .reduce("", (a, b) -> a + b);

// sorted - 排序
List<String> sorted = names.stream()
    .sorted(Comparator.comparingInt(String::length))
    .collect(Collectors.toList());

// 统计
long count = numbers.stream().filter(n -> n % 2 == 0).count();
int sum = numbers.stream().mapToInt(Integer::intValue).sum();

// 匹配
boolean allMatch = numbers.stream().allMatch(n -> n > 0);
boolean anyMatch = numbers.stream().anyMatch(n -> n > 5);

// flatMap - 展平嵌套结构
List<Integer> flat = nested.stream()
    .flatMap(List::stream)
    .collect(Collectors.toList());
```

## 🔍 内置函数式接口一览

| 接口 | 参数 | 返回 | 用途 | 示例 |
|------|------|------|------|------|
| `Predicate<T>` | T | boolean | 判断 | `s -> s.isEmpty()` |
| `Consumer<T>` | T | void | 消费 | `s -> log(s)` |
| `Function<T,R>` | T | R | 转换 | `s -> s.length()` |
| `Supplier<T>` | 无 | T | 供给 | `() -> new Object()` |
| `BiFunction<T,U,R>` | T, U | R | 双参数转换 | `(a,b) -> a+b` |
| `UnaryOperator<T>` | T | T | 一元操作 | `x -> -x` |
| `BinaryOperator<T>` | T, T | T | 二元操作 | `(a,b) -> a*b` |

## ❓ 常见问题

### Q1: Lambda表达式和匿名内部类有什么区别？

Lambda只能用于函数式接口，匿名内部类可用于任何接口/抽象类。Lambda不引入新的作用域（this指向外部类），匿名内部类有自己的this。

### Q2: 什么是effectively final？

Lambda表达式中使用的局部变量不需要声明为final，但不能被修改（effectively final）。这是为了确保Lambda捕获的值不会改变。

### Q3: Stream和Collection有什么区别？

Stream不是数据结构，不存储数据，是计算的管道。Stream是惰性求值的（中间操作不立即执行），且只能消费一次。

### Q4: 什么时候用方法引用代替Lambda？

当Lambda表达式只是调用一个已存在的方法时，优先使用方法引用，代码更简洁易读。

## 📈 扩展学习

- **Optional类**：结合Lambda处理空值
- **CompletableFuture**：Lambda与异步编程
- **Collectors工具类**：Stream的终端操作工具
- **并行流（Parallel Stream）**：利用多核处理器的并行计算
