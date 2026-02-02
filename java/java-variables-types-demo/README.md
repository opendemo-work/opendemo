# Java变量与数据类型演示

## 🎯 学习目标

通过本案例你将掌握：
- Java基本数据类型的使用
- 变量声明和初始化规则
- 类型转换和类型推断
- 常量和final关键字的使用
- 字符串和数组的基本操作

## 🛠️ 环境准备

### 系统要求
- JDK 11或更高版本
- 任意Java IDE（IntelliJ IDEA、Eclipse、VS Code推荐）
- 基本的命令行操作能力

### 环境验证
```bash
# 检查Java版本
java -version
javac -version

# 应该看到类似输出：
# openjdk version "11.0.18" 2023-01-17
# OpenJDK Runtime Environment (build 11.0.18+10-post-Ubuntu-0ubuntu122.04)
```

## 📁 项目结构

```
java-variables-types-demo/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   └── VariablesDemo.java
├── README.md
└── metadata.json
```

## 🚀 快速开始

### 步骤1：创建项目目录
```bash
mkdir java-variables-types-demo
cd java-variables-types-demo
mkdir -p src/main/java/com/example
```

### 步骤2：编写主程序
创建 `src/main/java/com/example/VariablesDemo.java` 文件：

```java
package com.example;

/**
 * Java变量与数据类型演示程序
 * 展示各种数据类型的声明、使用和转换
 */
public class VariablesDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Java变量与数据类型演示 ===\n");
        
        // 1. 整数类型演示
        demonstrateIntegerTypes();
        
        // 2. 浮点类型演示
        demonstrateFloatingPointTypes();
        
        // 3. 字符和布尔类型演示
        demonstrateCharBooleanTypes();
        
        // 4. 字符串类型演示
        demonstrateStringType();
        
        // 5. 数组类型演示
        demonstrateArrayTypes();
        
        // 6. 类型转换演示
        demonstrateTypeConversion();
        
        // 7. 常量演示
        demonstrateConstants();
    }
    
    /**
     * 演示整数类型
     */
    private static void demonstrateIntegerTypes() {
        System.out.println("1. 整数类型演示:");
        
        // byte类型 (-128 到 127)
        byte smallNumber = 100;
        System.out.println("byte: " + smallNumber);
        
        // short类型 (-32,768 到 32,767)
        short mediumNumber = 30000;
        System.out.println("short: " + mediumNumber);
        
        // int类型 (默认整数类型)
        int regularNumber = 2000000000;
        System.out.println("int: " + regularNumber);
        
        // long类型 (需要L后缀)
        long bigNumber = 9000000000L;
        System.out.println("long: " + bigNumber);
        
        System.out.println();
    }
    
    /**
     * 演示浮点类型
     */
    private static void demonstrateFloatingPointTypes() {
        System.out.println("2. 浮点类型演示:");
        
        // float类型 (需要F后缀)
        float price = 19.99F;
        System.out.println("float: " + price);
        
        // double类型 (默认小数类型)
        double preciseValue = 3.14159265359;
        System.out.println("double: " + preciseValue);
        
        System.out.println();
    }
    
    /**
     * 演示字符和布尔类型
     */
    private static void demonstrateCharBooleanTypes() {
        System.out.println("3. 字符和布尔类型演示:");
        
        // char类型 (单个字符，用单引号)
        char letter = 'A';
        char unicodeChar = '\u0041'; // Unicode表示
        System.out.println("char: " + letter + ", Unicode: " + unicodeChar);
        
        // boolean类型
        boolean isJavaFun = true;
        boolean isFinished = false;
        System.out.println("boolean true: " + isJavaFun);
        System.out.println("boolean false: " + isFinished);
        
        System.out.println();
    }
    
    /**
     * 演示字符串类型
     */
    private static void demonstrateStringType() {
        System.out.println("4. 字符串类型演示:");
        
        // String是引用类型，不是基本类型
        String greeting = "Hello";
        String name = "World";
        
        // 字符串连接
        String message = greeting + " " + name + "!";
        System.out.println("字符串连接: " + message);
        
        // 字符串长度
        System.out.println("字符串长度: " + message.length());
        
        // 字符串方法
        System.out.println("转大写: " + message.toUpperCase());
        System.out.println("包含'World': " + message.contains("World"));
        
        System.out.println();
    }
    
    /**
     * 演示数组类型
     */
    private static void demonstrateArrayTypes() {
        System.out.println("5. 数组类型演示:");
        
        // 整数数组
        int[] numbers = {1, 2, 3, 4, 5};
        System.out.println("整数数组长度: " + numbers.length);
        System.out.println("第一个元素: " + numbers[0]);
        
        // 字符串数组
        String[] fruits = {"苹果", "香蕉", "橙子"};
        System.out.println("水果数组:");
        for (String fruit : fruits) {
            System.out.println("  - " + fruit);
        }
        
        System.out.println();
    }
    
    /**
     * 演示类型转换
     */
    private static void demonstrateTypeConversion() {
        System.out.println("6. 类型转换演示:");
        
        // 自动类型转换 (隐式转换)
        int intValue = 100;
        long longValue = intValue; // int可以自动转换为long
        System.out.println("自动转换 int->long: " + longValue);
        
        // 强制类型转换 (显式转换)
        double doubleValue = 99.99;
        int convertedInt = (int) doubleValue; // 丢失小数部分
        System.out.println("强制转换 double->int: " + convertedInt);
        
        // 字符串与其他类型的转换
        String numberStr = "123";
        int parsedInt = Integer.parseInt(numberStr);
        System.out.println("字符串转整数: " + parsedInt);
        
        int age = 25;
        String ageStr = String.valueOf(age);
        System.out.println("整数转字符串: " + ageStr);
        
        System.out.println();
    }
    
    /**
     * 演示常量使用
     */
    private static void demonstrateConstants() {
        System.out.println("7. 常量演示:");
        
        // 使用final关键字声明常量
        final double PI = 3.14159;
        final String COMPANY_NAME = "OpenDemo";
        
        System.out.println("圆周率 PI = " + PI);
        System.out.println("公司名称 = " + COMPANY_NAME);
        
        // 常量一旦赋值就不能修改
        // PI = 3.14; // 这行会编译错误
        
        System.out.println();
    }
}
```

### 步骤3：编译和运行
```bash
# 编译Java文件
javac src/main/java/com/example/VariablesDemo.java

# 运行程序
java com.example.VariablesDemo
```

预期输出：
```
=== Java变量与数据类型演示 ===

1. 整数类型演示:
byte: 100
short: 30000
int: 2000000000
long: 9000000000

2. 浮点类型演示:
float: 19.99
double: 3.14159265359

3. 字符和布尔类型演示:
char: A, Unicode: A
boolean true: true
boolean false: false

4. 字符串类型演示:
字符串连接: Hello World!
字符串长度: 12
转大写: HELLO WORLD!
包含'World': true

5. 数组类型演示:
整数数组长度: 5
第一个元素: 1
水果数组:
  - 苹果
  - 香蕉
  - 橙子

6. 类型转换演示:
自动转换 int->long: 100
强制转换 double->int: 99
字符串转整数: 123
整数转字符串: 25

7. 常量演示:
圆周率 PI = 3.14159
公司名称 = OpenDemo
```

## 🔍 代码详解

### 1. 数据类型分类
Java的数据类型分为两大类：
- **基本数据类型**：byte, short, int, long, float, double, char, boolean
- **引用数据类型**：String, 数组, 类, 接口等

### 2. 变量命名规则
- 必须以字母、下划线(_)或美元符号($)开头
- 不能使用Java关键字
- 遵循驼峰命名法（camelCase）
- 建议使用有意义的变量名

### 3. 默认值
局部变量必须初始化后才能使用，成员变量有默认值：
- 数值类型：0
- boolean类型：false
- char类型：'\u0000'
- 引用类型：null

## 🧪 验证测试

### 编译测试
```bash
javac src/main/java/com/example/VariablesDemo.java
# 应该没有错误信息，生成.class文件
```

### 运行测试
```bash
java com.example.VariablesDemo
# 应该看到完整的演示输出
```

### 功能验证点
- [ ] 所有数据类型都能正确声明和使用
- [ ] 类型转换按预期工作
- [ ] 字符串操作正常执行
- [ ] 数组能够正确遍历
- [ ] 常量值保持不变

## ❓ 常见问题

### Q1: 为什么需要不同的整数类型？
**答**：不同类型占用不同大小的内存空间，选择合适的数据类型可以节省内存并提高性能。

### Q2: float和double有什么区别？
**答**：float是32位单精度浮点数，double是64位双精度浮点数。double精度更高但占用更多内存。

### Q3: 为什么要使用final关键字？
**答**：final关键字用于声明常量，防止意外修改，提高代码的安全性和可读性。

### Q4: String是基本数据类型吗？
**答**：不是，String是引用类型（类），但Java为了方便使用，提供了字符串字面量语法。

## 📚 扩展学习

### 相关技术
- [Java运算符](../java-operators-demo/)
- [Java控制流程](../java-control-flow-demo/)
- [Java数组操作](../java-arrays-demo/)

### 进阶主题
- 包装类（Wrapper Classes）
- 自动装箱和拆箱
- 枚举类型
- BigDecimal用于精确计算

### 企业级应用
- 在Spring Boot中使用配置属性
- 数据库字段类型映射
- REST API中的数据传输对象

---
> **💡 提示**: 掌握变量和数据类型是Java编程的基础，建议多练习不同类型的组合使用场景。