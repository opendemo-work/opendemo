<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 🏗️ Java内部类应用完整示例

## 🎯 案例概述

这是一个全面展示Java内部类机制的完整示例，通过实际代码演示成员内部类、静态嵌套类、局部内部类和匿名内部类等核心概念，帮助你深入理解Java中类与类之间的嵌套关系。

## 📚 学习目标

通过本示例你将掌握：
- 成员内部类的定义和使用，以及访问外部类成员的机制
- 静态嵌套类的特点和使用场景
- 局部内部类的定义范围和生命周期
- 匿名内部类的创建和常见使用场景
- 不同类型内部类之间的区别和适用场景
- 内部类与外部类之间的访问规则

## 📁 项目结构

```
java-inner-classes-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/
    ├── main/java/com/opendemo/java/innerclasses/
    │   ├── OuterClass.java          # 外部类，包含所有内部类类型
    │   └── InnerClassesDemo.java    # 主程序入口
    └── test/java/com/opendemo/java/innerclasses/
        └── InnerClassesDemoTest.java # 单元测试
```

## 🚀 快速开始

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.innerclasses.InnerClassesDemo"

# 运行测试
mvn test
```

## 📖 核心代码详解

### 1. 成员内部类（Member Inner Class）

成员内部类定义在外部类的内部，没有`static`修饰符。它可以访问外部类的所有成员（包括私有成员）。

```java
public class OuterClass {
    private String outerField = "外部类字段";

    public class InnerClass {
        public void accessOuter() {
            // 可以直接访问外部类的私有字段
            System.out.println(outerField);
        }
    }
}

// 创建成员内部类实例需要先有外部类实例
OuterClass outer = new OuterClass();
OuterClass.InnerClass inner = outer.new InnerClass();
```

**关键点：**
- 成员内部类隐式持有外部类的引用
- 可以访问外部类的所有成员（包括private）
- 创建实例需要通过外部类实例

### 2. 静态嵌套类（Static Nested Class）

用`static`修饰的内部类，不持有外部类实例的引用。

```java
public class OuterClass {
    private static String staticField = "静态字段";

    public static class StaticNestedClass {
        public void display() {
            // 只能访问外部类的静态成员
            System.out.println(staticField);
        }
    }
}

// 创建静态嵌套类不需要外部类实例
OuterClass.StaticNestedClass nested = new OuterClass.StaticNestedClass();
```

**关键点：**
- 不持有外部类实例引用
- 只能访问外部类的静态成员
- 创建实例不需要外部类对象

### 3. 局部内部类（Local Class）

定义在方法内部的类，作用范围仅限于该方法。

```java
public String demonstrateLocalClass(String prefix) {
    class LocalClass {
        String process(String input) {
            return prefix + " - " + input;
        }
    }
    LocalClass local = new LocalClass();
    return local.process("处理结果");
}
```

**关键点：**
- 只在定义它的方法内可见
- 可以访问方法的局部变量（必须是effectively final）
- 不能使用public/private等访问修饰符

### 4. 匿名内部类（Anonymous Inner Class）

没有名字的内部类，通常用于实现接口或继承类的即时使用。

```java
Runnable runnable = new Runnable() {
    @Override
    public void run() {
        System.out.println("匿名内部类执行");
    }
};
runnable.run();
```

**关键点：**
- 没有类名，只能使用一次
- 通常用于实现函数式接口
- Java 8+ 可以用Lambda表达式替代部分匿名内部类

## 🔍 四种内部类对比

| 类型 | 修饰符 | 外部类引用 | 访问外部成员 | 使用场景 |
|------|--------|-----------|-------------|---------|
| 成员内部类 | 无static | 持有 | 所有成员 | 辅助类与外部类紧密关联 |
| 静态嵌套类 | static | 不持有 | 仅静态成员 | 辅助类不需要外部实例 |
| 局部内部类 | 无 | 持有 | 所有成员+final局部变量 | 复杂逻辑的局部封装 |
| 匿名内部类 | 无 | 持有 | 所有成员+final局部变量 | 一次性接口实现 |

## ❓ 常见问题

### Q1: 成员内部类和静态嵌套类有什么区别？

成员内部类持有外部类的引用，可以访问外部类的所有成员；静态嵌套类不持有外部类引用，只能访问外部类的静态成员。

### Q2: 为什么局部内部类访问的局部变量必须是effectively final？

因为局部变量的生命周期可能短于局部内部类对象。Java通过拷贝变量值来确保访问安全，因此要求变量不可变。

### Q3: 匿名内部类可以用Lambda替代吗？

当匿名内部类实现的接口只有一个抽象方法（函数式接口）时，可以用Lambda替代。如果接口有多个抽象方法则不能替代。

### Q4: 内部类有什么实际应用场景？

- Map的Entry是Map接口的内部接口
- Builder模式通常实现为静态嵌套类
- 事件监听器常用匿名内部类
- 迭代器模式中Iterator常作为内部类实现

## 📈 扩展学习

- **Java 8 Lambda表达式**：简化匿名内部类的写法
- **Java反射与内部类**：通过反射操作内部类
- **闭包概念**：理解内部类与闭包的关系
- **设计模式中的内部类**：Builder模式、迭代器模式

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
