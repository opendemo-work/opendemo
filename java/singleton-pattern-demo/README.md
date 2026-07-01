<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 单例模式（Singleton Pattern）

## 1. 模式定义

单例模式（Singleton Pattern）是一种**创建型设计模式**，它确保一个类只有一个实例，并提供一个全局访问点来访问该实例。

**核心要点：**
- 构造函数私有化，防止外部通过 `new` 创建实例
- 类内部创建唯一实例
- 提供静态方法返回该唯一实例

## 2. UML 类图

```
┌──────────────────────────┐
│      Singleton           │
├──────────────────────────┤
│ - instance: Singleton    │
├──────────────────────────┤
│ - Singleton()            │
│ + getInstance(): Singleton│
│ + doSomething(): void    │
└──────────────────────────┘
```

## 3. 五种实现方式

### 3.1 饿汉式（Eager Initialization）

在类加载时就立即创建实例，线程安全，但不支持延迟加载。

```java
public class EagerSingleton {
    private static final EagerSingleton instance = new EagerSingleton();

    private EagerSingleton() {}

    public static EagerSingleton getInstance() {
        return instance;
    }
}
```

**优点：** 实现简单，线程安全（类加载时由 JVM 保证）
**缺点：** 无论是否使用都会创建实例，可能浪费资源

### 3.2 懒汉式（Lazy Initialization）

在第一次调用 `getInstance()` 时才创建实例，非线程安全。

```java
public class LazySingleton {
    private static LazySingleton instance;

    private LazySingleton() {}

    public static LazySingleton getInstance() {
        if (instance == null) {
            instance = new LazySingleton();
        }
        return instance;
    }
}
```

**优点：** 延迟加载，节省资源
**缺点：** 非线程安全，多线程环境下可能创建多个实例

### 3.3 双重检查锁定（Double-Checked Locking）

结合了懒汉式的延迟加载和线程安全，使用 `volatile` 关键字防止指令重排序。

```java
public class ThreadSafeSingleton {
    private static volatile ThreadSafeSingleton instance;

    private ThreadSafeSingleton() {}

    public static ThreadSafeSingleton getInstance() {
        if (instance == null) {
            synchronized (ThreadSafeSingleton.class) {
                if (instance == null) {
                    instance = new ThreadSafeSingleton();
                }
            }
        }
        return instance;
    }
}
```

**优点：** 延迟加载，线程安全，性能较好
**缺点：** 实现较复杂，需要理解 `volatile` 和指令重排序

### 3.4 枚举式（Enum Singleton）

利用 Java 枚举类型实现单例，Effective Book 推荐的最佳实践。

```java
public enum EnumSingleton {
    INSTANCE;

    public void doSomething() {
        System.out.println("Doing something...");
    }
}
```

**优点：** 线程安全，防止反序列化重新创建对象，防止反射攻击
**缺点：** 不能延迟加载，不能继承其他类

### 3.5 静态内部类式（Bill Pugh Singleton）

利用静态内部类的加载机制实现延迟加载和线程安全。

```java
public class InnerClassSingleton {
    private InnerClassSingleton() {}

    private static class SingletonHolder {
        private static final InnerClassSingleton INSTANCE = new InnerClassSingleton();
    }

    public static InnerClassSingleton getInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

**优点：** 延迟加载，线程安全，实现简洁
**缺点：** 无法防止反射攻击

## 4. 各实现方式对比

| 实现方式 | 延迟加载 | 线程安全 | 防反射 | 防序列化 | 推荐度 |
|---------|---------|---------|--------|---------|--------|
| 饿汉式 | ❌ | ✅ | ❌ | ❌ | ⭐⭐⭐ |
| 懒汉式 | ✅ | ❌ | ❌ | ❌ | ⭐ |
| 双重检查锁定 | ✅ | ✅ | ❌ | ❌ | ⭐⭐⭐⭐ |
| 枚举式 | ❌ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| 静态内部类 | ✅ | ✅ | ❌ | ❌ | ⭐⭐⭐⭐ |

## 5. 真实应用场景

### 5.1 Java 标准库中的单例

- `java.lang.Runtime` — 每个 Java 应用都有一个 Runtime 实例
- `java.awt.Desktop` — 桌面操作的单例
- `java.util.Currency` — 货币实例缓存

### 5.2 Spring 框架

- Spring Bean 默认作用域为 Singleton（虽然 Spring 的单例是容器级别的）
- `ApplicationContext` 通常为单例

### 5.3 其他常见场景

- **数据库连接池**：如 HikariCP 的连接池管理
- **日志管理器**：如 Log4j、SLF4J 的 Logger
- **配置管理器**：读取和管理应用配置
- **线程池**：如 `Executors` 创建的线程池
- **缓存**：如 Guava Cache 的实例管理

## 6. 代码说明

本 demo 包含以下文件：

| 文件 | 说明 |
|------|------|
| `SingletonDemo.java` | 主入口，演示所有单例实现 |
| `EagerSingleton.java` | 饿汉式单例 |
| `LazySingleton.java` | 懒汉式单例 |
| `ThreadSafeSingleton.java` | 双重检查锁定单例 |
| `EnumSingleton.java` | 枚举式单例 |
| `InnerClassSingleton.java` | 静态内部类单例 |
| `SingletonPatternTest.java` | 单元测试 |

## 7. 与其他模式的关系

### 7.1 与工厂方法模式
- 工厂方法经常使用单例来确保工厂实例的唯一性
- Abstract Factory 模式中的具体工厂通常是单例

### 7.2 与外观模式（Facade）
- Facade 对象通常是单例，因为只需要一个统一接口入口

### 7.3 与享元模式（Flyweight）
- 两者都用于共享对象，但单例保证唯一实例，享元共享多个可复用对象

### 7.4 与原型模式（Prototype）
- 单例模式与原型模式冲突 — 单例不应该实现 `Cloneable` 接口

## 8. 注意事项

### 8.1 反射攻击

通过反射可以调用私有构造函数破坏单例，防御方式：

```java
private Singleton() {
    if (SingletonHolder.INSTANCE != null) {
        throw new RuntimeException("Use getInstance() to get the singleton instance");
    }
}
```

### 8.2 序列化问题

反序列化时会创建新实例，需要实现 `readResolve()` 方法：

```java
protected Object readResolve() {
    return getInstance();
}
```

### 8.3 多线程环境

在多线程环境中，应选择线程安全的实现方式：枚举式、双重检查锁定或静态内部类。

## 9. 运行方式

```bash
# 编译
mvn clean compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.patterns.singleton.SingletonDemo"

# 运行测试
mvn test
```

## 10. 总结

单例模式是最简单也是最常被使用的设计模式之一。选择哪种实现方式取决于具体场景：

- **简单场景**：枚举式（最佳实践）
- **需要延迟加载**：静态内部类式
- **需要延迟加载且对性能敏感**：双重检查锁定
- **初始化开销小**：饿汉式

应避免使用非线程安全的懒汉式实现。

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

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
