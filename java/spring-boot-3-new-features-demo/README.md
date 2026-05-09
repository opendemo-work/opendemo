# Spring Boot 3.x 新特性演示

## 学习目标

1. 掌握 Spring Boot 3.x 核心新特性
2. 理解 Virtual Threads (协程线程) 的使用场景
3. 学会使用 Spring Boot 3.x 的record作为 DTO
4. 了解 Jakarta EE 10 的变化

## 环境要求

- JDK 21+ (必须)
- Maven 3.9+ 或 Gradle 8+
- IntelliJ IDEA 2024.1+ (推荐)

## 项目结构

```
spring-boot-3-new-features-demo/
├── code/
│   ├── main/
│   │   └── java/com/opendemo/springboot3/
│   │       ├── SpringBoot3Application.java
│   │       ├── VirtualThreadsDemo.java
│   │       ├── RecordDtoDemo.java
│   │       ├── JakartaEE10Demo.java
│   │       └── config/
│   │           └── AppConfig.java
│   └── test/
│       └── java/com/opendemo/springboot3/
│           └── FeaturesTest.java
├── pom.xml
└── README.md
```

## 快速开始

### 1. 环境检查

```bash
# 检查 Java 版本 (必须 21+)
java -version

# 预期输出:
# java version "21.0.1" 2024-01-16
# Java(TM) SE Runtime Environment (build 21.0.1+12)
```

### 2. 编译项目

```bash
cd spring-boot-3-new-features-demo
mvn clean compile
```

### 3. 运行演示

```bash
# 运行 Virtual Threads 演示
mvn exec:java -Dexec.mainClass="com.opendemo.springboot3.VirtualThreadsDemo"

# 运行 Record DTO 演示
mvn exec:java -Dexec.mainClass="com.opendemo.springboot3.RecordDtoDemo"
```

## 核心特性详解

### 1. Virtual Threads (虚拟线程)

Spring Boot 3.x 基于 Jakarta EE 10，默认支持 Virtual Threads。

**传统线程 vs 虚拟线程对比：**

```java
// 传统线程模型 (消耗资源)
ExecutorService executor = Executors.newFixedThreadPool(100);

// 虚拟线程模型 (轻量级)
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
```

**适用场景：**
- 高并发 HTTP 请求 (每个请求一个虚拟线程)
- 异步 I/O 操作 (数据库查询、API 调用)
- 长时间保持连接的场景 (WebSocket)

**不适用场景：**
- CPU 密集型计算 (应使用传统线程池)
- 需要精确控制线程数量的场景

### 2. Record DTO

Spring Boot 3.x 全面支持 Java Record 作为 DTO。

**传统 DTO vs Record 对比：**

```java
// 传统 DTO (繁琐)
public class UserDto {
    private final String name;
    private final int age;

    public UserDto(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
}

// Record DTO (简洁)
public record UserDto(String name, int age) {}
```

**Record 特性：**
- 自动生成 `equals()`, `hashCode()`, `toString()`
- 自动生成 `getter` 方法 (name, age 而非 getName)
- 不可变对象
- 适合作为 DTO 和不可变数据对象

### 3. Jakarta EE 10

Spring Boot 3.x 升级到 Jakarta EE 10 API。

**主要变化：**
| 旧 API (EE 8/9) | 新 API (EE 10) |
|-----------------|----------------|
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.transaction.*` | `jakarta.transaction.*` |

**迁移检查清单：**
```bash
# 检查是否使用旧 API
grep -r "javax\." src/ || echo "无旧 API 依赖"
```

## 代码解析

### VirtualThreadsDemo.java

```java
package com.opendemo.springboot3;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class VirtualThreadsDemo {

    public static void main(String[] args) throws InterruptedException {
        // 使用虚拟线程执行器
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {

            // 提交 1000 个任务
            for (int i = 0; i < 1000; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    // 模拟 I/O 操作
                    System.out.println("Task " + taskId + " running in virtual thread");
                    Thread.sleep(Duration.ofMillis(100));
                });
            }
        }

        System.out.println("所有任务完成");
    }
}
```

### RecordDtoDemo.java

```java
package com.opendemo.springboot3;

import java.time.LocalDate;

// Record 作为 DTO
public record UserRegistrationRequest(
    String username,
    String email,
    LocalDate birthDate,
    int age
) {
    // Record 自动生成:
    // - 构造方法
    // - equals(), hashCode()
    // - toString()
    // - getter: username(), email(), birthDate(), age()

    // 可以添加约束校验
    public UserRegistrationRequest {
        if (username == null || username.isBlank()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("年龄不合法");
        }
    }
}

public class RecordDtoDemo {
    public static void main(String[] args) {
        // 创建 Record 实例
        var request = new UserRegistrationRequest(
            "张三",
            "zhangsan@example.com",
            LocalDate.of(1990, 5, 15),
            34
        );

        // 访问字段 (使用方法而非 getter)
        System.out.println("用户名: " + request.username());
        System.out.println("邮箱: " + request.email());
        System.out.println("年龄: " + request.age());

        // 自动生成的 toString()
        System.out.println(request);
    }
}
```

## 扩展学习

1. [Spring Boot 3.0 官方发布说明](https://spring.io/blog/2022/11/24/spring-boot-3-0-is-now-ga)
2. [Virtual Threads 深度解析](https://openjdk.org/jeps/444)
3. [Jakarta EE 10 变化](https://jakarta.ee/specifications/platform/10/)

## 常见问题

### Q1: 虚拟线程与传统线程池如何选择？

**选择虚拟线程的场景：**
- 高并发 (1000+) 短时任务
- I/O 密集型应用
- 需要处理大量并发请求的 HTTP 服务

**选择传统线程池的场景：**
- CPU 密集型任务
- 需要精确控制线程数量的场景
- 需要线程局部变量

### Q2: 如何升级现有 Spring Boot 2.x 项目？

```bash
# 1. 升级 Java 版本到 21
# 2. 升级 Spring Boot 版本到 3.x
# 3. 修改 javax.* 为 jakarta.*
# 4. 更新依赖库版本
# 5. 运行全面测试
```

---

**技术栈**: Java 21 | Spring Boot 3.2 | Jakarta EE 10

**维护者**: OpenDemo Team

**版本**: 1.0.0