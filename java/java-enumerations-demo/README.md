<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 🎨 Java枚举类型完整示例

## 🎯 案例概述

这是一个全面展示Java枚举（Enum）类型的完整示例，通过实际代码演示枚举基础定义、构造器和字段、方法实现、接口实现、switch语句使用等核心概念，帮助你掌握Java枚举的强大功能。

## 📚 学习目标

通过本示例你将掌握：
- 枚举类型的基本定义和使用
- 带构造器、字段和方法的枚举
- 枚举实现接口的方式
- 枚举中的抽象方法
- switch语句中使用枚举
- 枚举的实用工具方法（values, valueOf, ordinal）
- 枚举在实际项目中的应用模式

## 📁 项目结构

```
java-enumerations-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/
    ├── main/java/com/opendemo/java/enumerations/
    │   ├── Color.java          # 带字段和方法的枚举
    │   ├── Operation.java      # 运算接口
    │   ├── MathOperation.java  # 实现接口的枚举（含抽象方法）
    │   ├── HttpStatus.java     # HTTP状态码枚举
    │   └── EnumDemo.java       # 主程序入口
    └── test/java/com/opendemo/java/enumerations/
        └── EnumDemoTest.java   # 单元测试
```

## 🚀 快速开始

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.enumerations.EnumDemo"

# 运行测试
mvn test
```

## 📖 核心代码详解

### 1. 带字段和方法的枚举

枚举可以有构造器、字段和方法，使每个常量携带丰富的信息：

```java
public enum Color {
    RED("红色", "#FF0000"),
    GREEN("绿色", "#00FF00"),
    BLUE("蓝色", "#0000FF");

    private final String name;
    private final String hexCode;

    Color(String name, String hexCode) {
        this.name = name;
        this.hexCode = hexCode;
    }

    public String getName() { return name; }
    public String getHexCode() { return hexCode; }

    public boolean isPrimary() {
        return this == RED || this == GREEN || this == BLUE;
    }

    public static Color fromName(String name) {
        for (Color color : values()) {
            if (color.name.equals(name)) return color;
        }
        throw new IllegalArgumentException("未知颜色: " + name);
    }
}
```

### 2. 枚举实现接口

枚举可以实现接口，为每个常量提供不同的行为实现：

```java
public interface Operation {
    double apply(double a, double b);
}

public enum MathOperation implements Operation {
    ADD("+") {
        public double apply(double a, double b) { return a + b; }
    },
    SUBTRACT("-") {
        public double apply(double a, double b) { return a - b; }
    },
    MULTIPLY("*") {
        public double apply(double a, double b) { return a * b; }
    },
    DIVIDE("/") {
        public double apply(double a, double b) {
            if (b == 0) throw new ArithmeticException("除数不能为零");
            return a / b;
        }
    };

    private final String symbol;
    MathOperation(String symbol) { this.symbol = symbol; }
    public String getSymbol() { return symbol; }
}
```

### 3. 状态码枚举

枚举常用于表示状态码、类型码等固定集合：

```java
public enum HttpStatus {
    OK(200, "OK"),
    NOT_FOUND(404, "Not Found"),
    INTERNAL_SERVER_ERROR(500, "Internal Server Error");

    private final int code;
    private final String description;

    HttpStatus(int code, String description) {
        this.code = code;
        this.description = description;
    }

    public boolean isSuccess() { return code >= 200 && code < 300; }
    public boolean isClientError() { return code >= 400 && code < 500; }
    public boolean isServerError() { return code >= 500; }

    public static HttpStatus fromCode(int code) { ... }
}
```

### 4. Switch语句中使用枚举

```java
Color color = Color.GREEN;
switch (color) {
    case RED:
        result = "选择了红色";
        break;
    case GREEN:
        result = "选择了绿色";
        break;
    default:
        result = "选择了其他颜色";
        break;
}
```

## 🔍 枚举核心方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `values()` | 返回所有枚举常量 | `Color.values()` |
| `valueOf(String)` | 根据名称获取常量 | `Color.valueOf("RED")` |
| `name()` | 返回常量名称 | `Color.RED.name()` → "RED" |
| `ordinal()` | 返回常量序号（从0开始） | `Color.RED.ordinal()` → 0 |
| `toString()` | 可重写，返回自定义字符串 | `Color.RED.toString()` |

## ❓ 常见问题

### Q1: 枚举构造器为什么是private的？

枚举构造器默认且只能是private的。这是为了保证枚举常量的唯一性，外部无法通过new创建枚举实例。

### Q2: 枚举可以实现接口但不能继承类？

枚举隐式继承自 `java.lang.Enum`，Java不支持多重继承，因此枚举不能继承其他类。但可以实现任意数量的接口。

### Q3: 枚举和静态常量（int/String）相比有什么优势？

枚举提供类型安全、命名空间、可遍历、可携带数据和方法等优势。Effective Java推荐用枚举替代int常量。

### Q4: 枚举的ordinal()方法有什么问题？

ordinal()依赖于声明顺序，如果插入或重排常量会导致值变化。应该使用自定义字段而非ordinal()来存储有意义的值。

## 📈 扩展学习

- **EnumSet和EnumMap**：专为枚举设计的高效集合类
- **策略枚举模式**：用枚举实现策略模式
- **枚举单例**：利用枚举实现线程安全的单例模式
- **Effective Java枚举章节**：深入理解枚举的最佳实践

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
