<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 🏷️ Java注解机制完整示例

## 🎯 案例概述

这是一个全面展示Java注解（Annotation）机制的完整示例，通过实际代码演示内置注解的使用、自定义注解的定义、以及通过反射处理注解等核心概念，帮助你掌握Java元编程技术。

## 📚 学习目标

通过本示例你将掌握：
- Java内置注解（@Override, @Deprecated, @SuppressWarnings）的使用
- 自定义注解的定义方法
- 元注解（@Retention, @Target, @Inherited, @Documented）的作用
- 通过反射在运行时读取和处理注解
- 注解在代码文档化和配置中的作用

## 📁 项目结构

```
java-annotations-demo/
├── pom.xml
├── README.md
├── metadata.json
└── src/
    ├── main/java/com/opendemo/java/annotations/
    │   ├── Author.java              # @Author自定义注解
    │   ├── Version.java             # @Version自定义注解
    │   ├── Todo.java                # @Todo自定义注解
    │   ├── TodoPriority.java        # 优先级枚举
    │   ├── MyAnnotation.java        # 通用自定义注解
    │   ├── CustomAnnotations.java   # 使用注解的示例类
    │   ├── AnnotationProcessor.java # 注解处理器
    │   └── AnnotationsDemo.java     # 主程序入口
    └── test/java/com/opendemo/java/annotations/
        └── AnnotationsDemoTest.java # 单元测试
```

## 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.annotations.AnnotationsDemo"

# 运行测试
mvn test
```

## 📖 核心代码详解

### 1. 内置注解

Java语言自带的标准注解：

```java
@Override       // 标记方法重写父类方法，编译器检查是否正确重写
@Deprecated     // 标记过时的元素，编译器会产生警告
@SuppressWarnings("unchecked")  // 抑制编译器警告
@FunctionalInterface  // 标记函数式接口，确保只有一个抽象方法
```

### 2. 自定义注解

使用元注解来定义自定义注解：

```java
@Retention(RetentionPolicy.RUNTIME)    // 保留策略：运行时可见
@Target({ElementType.TYPE, ElementType.METHOD})  // 使用目标：类和方法
public @interface Author {
    String name() default "Unknown";
    String email() default "";
}

@Target(ElementType.TYPE)
public @interface Version {
    int major() default 1;
    int minor() default 0;
    String date() default "";
}

@Target({ElementType.METHOD, ElementType.CONSTRUCTOR})
public @interface Todo {
    String value();                          // 默认属性
    String assignee() default "";
    TodoPriority priority() default TodoPriority.MEDIUM;
}
```

### 3. 元注解说明

| 元注解 | 作用 | 说明 |
|--------|------|------|
| `@Retention` | 保留策略 | SOURCE（源码）、CLASS（字节码）、RUNTIME（运行时） |
| `@Target` | 使用目标 | TYPE、METHOD、FIELD、CONSTRUCTOR等 |
| `@Inherited` | 继承性 | 子类是否自动继承父类的注解 |
| `@Documented` | 文档化 | 注解是否出现在JavaDoc中 |

### 4. 使用自定义注解

```java
@Author(name = "OpenDemo", email = "team@opendemo.com")
@Version(major = 1, minor = 0, date = "2024-01-15")
public class CustomAnnotations {

    @MyAnnotation(value = "示例方法", count = 3)
    public String annotatedMethod(String input) {
        return input.toUpperCase();
    }

    @Todo(value = "需要优化性能", assignee = "developer", priority = TodoPriority.HIGH)
    public void pendingMethod() { }
}
```

### 5. 通过反射处理注解

```java
AnnotationProcessor processor = new AnnotationProcessor();
Class<?> clazz = CustomAnnotations.class;

// 读取类上的注解
String author = processor.getAuthorInfo(clazz);  // "OpenDemo <team@opendemo.com>"
String version = processor.getVersionInfo(clazz); // "1.0 (2024-01-15)"

// 读取方法上的注解
List<String> todos = processor.getTodos(clazz);
// ["pendingMethod: 需要优化性能 [HIGH]", "legacyMethod: 即将移除 [LOW]"]

// 检查注解是否存在
boolean hasAuthor = processor.hasAnnotation(clazz, Author.class);  // true
```

## 🔍 注解保留策略对比

| 策略 | 源码阶段 | 编译阶段 | 运行阶段 | 典型应用 |
|------|---------|---------|---------|---------|
| SOURCE | 可见 | 不可见 | 不可见 | @Override, @SuppressWarnings |
| CLASS | 可见 | 可见 | 不可见 | 字节码工具使用 |
| RUNTIME | 可见 | 可见 | 可见 | 反射处理、框架配置 |

## ❓ 常见问题

### Q1: 注解和接口有什么区别？

注解使用 `@interface` 定义，编译器会自动继承 `java.lang.annotation.Annotation` 接口。注解只能定义属性（无参方法），不能有逻辑实现。

### Q2: @Retention(RUNTIME) 什么时候需要？

只有当你需要在运行时通过反射读取注解信息时才需要RUNTIME策略。像@Override这样的注解只需要SOURCE策略。

### Q3: 注解的value属性有什么特殊之处？

value是注解的默认属性。当只给value赋值时可以省略属性名：`@Todo("待办事项")` 等价于 `@Todo(value = "待办事项")`。

### Q4: 注解可以继承吗？

注解本身不能继承（不能extends另一个注解）。但使用 `@Inherited` 元注解可以让类上的注解被子类继承（仅对类声明有效，对方法无效）。

## 📈 扩展学习

- **Spring注解驱动开发**：@Component, @Autowired, @RequestMapping等
- **注解处理器（APT）**：编译时处理注解生成代码
- **Lombok原理**：通过注解处理器自动生成getter/setter等代码
- **Hibernate/JPA注解**：使用注解进行ORM映射配置

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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
