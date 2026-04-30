# 🪞 Java反射API完整示例

## 🎯 案例概述

这是一个全面展示Java反射（Reflection）API的完整示例，通过实际代码演示Class对象获取、字段访问、方法调用、构造器操作等核心概念，帮助你理解Java运行时类型信息和动态编程能力。

## 📚 学习目标

通过本示例你将掌握：
- 获取Class对象的三种方式及其适用场景
- 通过反射访问和修改字段（包括私有字段）
- 通过反射调用方法（包括私有方法和静态方法）
- 通过反射创建对象（包括调用私有构造器）
- 反射工具类的封装和设计
- 反射在实际框架中的应用原理

## 📁 项目结构

```
java-reflection-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/
    ├── main/java/com/opendemo/java/reflection/
    │   ├── SampleClass.java        # 反射目标类
    │   ├── ReflectionUtils.java    # 反射工具类
    │   └── ReflectionDemo.java     # 主程序入口
    └── test/java/com/opendemo/java/reflection/
        └── ReflectionDemoTest.java # 单元测试
```

## 🚀 快速开始

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.reflection.ReflectionDemo"

# 运行测试
mvn test
```

## 📖 核心代码详解

### 1. 获取Class对象

反射的入口是Class对象，有三种获取方式：

```java
// 方式1：通过类名.class（编译时已知类型）
Class<?> clazz1 = SampleClass.class;

// 方式2：通过对象的getClass()方法
SampleClass sample = new SampleClass();
Class<?> clazz2 = sample.getClass();

// 方式3：通过Class.forName()（运行时动态加载）
Class<?> clazz3 = Class.forName("com.opendemo.java.reflection.SampleClass");
```

### 2. 获取类信息

```java
// 获取类的基本信息
List<String> info = ReflectionUtils.getClassInfo(SampleClass.class);
// 类名, 简单类名, 包名, 修饰符, 父类, 实现的接口

// 获取所有声明的字段
List<String> fields = ReflectionUtils.getFields(SampleClass.class);
// private String name
// public int age
// protected String email

// 获取所有声明的方法
List<String> methods = ReflectionUtils.getMethods(SampleClass.class);
// public String getName()
// public void setName(String)
// public String greet(String)

// 获取所有构造器
List<String> constructors = ReflectionUtils.getConstructors(SampleClass.class);
// public SampleClass()
// public SampleClass(String, int)
// private SampleClass(String)
```

### 3. 字段访问

通过反射可以访问和修改任意字段，包括私有字段：

```java
SampleClass sample = new SampleClass("张三", 25);

// 读取私有字段
String name = (String) ReflectionUtils.getFieldValue(sample, "name");
// "张三"

// 修改私有字段
ReflectionUtils.setFieldValue(sample, "name", "李四");
ReflectionUtils.setFieldValue(sample, "age", 30);
```

**关键点：** 访问私有成员需要先调用 `field.setAccessible(true)` 解除访问限制。

### 4. 方法调用

```java
SampleClass sample = new SampleClass("王五", 28);

// 调用公共方法
String result = (String) ReflectionUtils.invokeMethod(
    sample, "greet", new Class[]{String.class}, new Object[]{"你好"});
// "你好, I am 王五"

// 调用私有方法
String privateResult = (String) ReflectionUtils.invokeMethod(
    sample, "privateMethod", new Class[]{String.class}, new Object[]{"test"});
// "processed: test"

// 调用静态方法（对象传null）
String staticResult = (String) ReflectionUtils.invokeMethod(
    null, "staticMethod", new Class[]{}, new Object[]{});
// "static result"
```

### 5. 构造器操作

通过反射可以调用任意构造器，包括私有构造器：

```java
// 无参构造
Object instance1 = ReflectionUtils.createInstance(
    SampleClass.class, new Class[]{}, new Object[]{});

// 有参构造
Object instance2 = ReflectionUtils.createInstance(
    SampleClass.class,
    new Class[]{String.class, int.class},
    new Object[]{"赵六", 35});

// 私有构造器
Object instance3 = ReflectionUtils.createInstance(
    SampleClass.class,
    new Class[]{String.class},
    new Object[]{"私有构造"});
```

## 🔍 反射API核心类

| 类 | 用途 |
|----|------|
| `Class` | 表示类的运行时类型信息 |
| `Field` | 表示类的字段（属性） |
| `Method` | 表示类的方法 |
| `Constructor` | 表示类的构造器 |
| `Modifier` | 解析访问修饰符 |
| `Array` | 动态创建和操作数组 |

## ❓ 常见问题

### Q1: 反射的性能如何？

反射比直接调用慢20-100倍，因为需要在运行时查找方法、检查权限等。在性能敏感场景应避免使用反射，或缓存反射结果。

### Q2: setAccessible(true)是否破坏了封装性？

是的，setAccessible(true)可以绕过Java的访问控制。这主要用于框架和工具类（如序列化、依赖注入），应用代码通常不应这样做。

### Q3: 反射能操作注解吗？

可以。通过 `getAnnotation()`, `getAnnotations()` 等方法可以读取RUNTIME保留策略的注解。这是Spring等框架的基础。

### Q4: 什么时候应该使用反射？

- 框架开发（Spring、Hibernate等）
- ORM映射
- 依赖注入
- 单元测试（访问私有方法）
- 序列化/反序列化

## 📈 扩展学习

- **动态代理**：`java.lang.reflect.Proxy` 实现AOP
- **Spring IoC容器**：基于反射实现依赖注入
- **JavaBeans规范**：反射操作属性的标准模式
- **MethodHandle**：Java 7+ 提供的更高效的动态调用机制
