# Java 并发编程 - 线程池、锁与原子类

> 系统学习 Java 并发编程核心机制，包括线程池、synchronized、ReentrantLock、Atomic 原子类和并发集合。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 Java 线程生命周期和并发基础
- ✅ 使用 Executors 创建和管理线程池
- ✅ 使用 synchronized 和 ReentrantLock 实现同步
- ✅ 使用 Atomic 类和并发集合避免数据竞争
- ✅ 理解线程安全性和内存可见性

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Java 并发编程组件                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   任务 ──▶ ThreadPoolExecutor ──▶ Worker Thread 1..N           │
│                                                                 │
│   共享资源 ──┬──▶ synchronized / ReentrantLock                  │
│             ├──▶ AtomicInteger / AtomicLong                     │
│             ├──▶ volatile / CAS                                 │
│             └──▶ ConcurrentHashMap / BlockingQueue              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| JDK | >= 17 | 编译运行 Java |
| Maven | >= 3.8 | 构建项目 |

### 编译运行

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd java/concurrent-programming-demo
mvn clean package
java -jar target/concurrent-programming-demo-1.0.jar
```

---

## 📖 核心概念

### 1. 线程池

线程池可以复用线程，减少创建和销毁线程的开销：

```java
ExecutorService executor = Executors.newFixedThreadPool(4);
executor.submit(() -> System.out.println("Task"));
executor.shutdown();
```

### 2. synchronized

Java 内置锁，用于方法或代码块同步：

```java
public synchronized void increment() {
    count++;
}
```

### 3. ReentrantLock

显式锁，提供更灵活的锁定机制：

```java
Lock lock = new ReentrantLock();
lock.lock();
try {
    count++;
} finally {
    lock.unlock();
}
```

### 4. Atomic 类

基于 CAS 实现无锁并发：

```java
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();
```

---

## 💻 代码示例

### 线程池示例

```java
ExecutorService executor = Executors.newFixedThreadPool(4);
for (int i = 0; i < 10; i++) {
    final int taskId = i;
    executor.submit(() -> {
        System.out.println("Task " + taskId + " running in " + Thread.currentThread().getName());
    });
}
executor.shutdown();
```

### 计数器同步

```java
public class SafeCounter {
    private final AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();
    }

    public int get() {
        return count.get();
    }
}
```

### 生产者消费者

```java
BlockingQueue<String> queue = new LinkedBlockingQueue<>(10);

// Producer
new Thread(() -> {
    try {
        queue.put("message");
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
}).start();

// Consumer
new Thread(() -> {
    try {
        String msg = queue.take();
        System.out.println(msg);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
}).start();
```

---

## 🔧 配置说明

| 文件 | 作用 |
|------|------|
| `pom.xml` | Maven 构建配置 |
| `src/main/java/` | Java 示例代码 |
| `src/test/java/` | 测试代码 |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn test
```

---

## 📊 运行结果

```
Task 0 running in pool-1-thread-1
Task 1 running in pool-1-thread-2
...
Counter final value: 10000
```

---

## 🐛 常见问题

### Q1：线程池未关闭导致内存泄漏？

**A**：确保调用 `shutdown()` 或 `shutdownNow()`，或使用 try-with-resources。

### Q2：死锁怎么排查？

**A**：使用 `jstack` 导出线程快照，查找 BLOCKED 状态和循环等待。

### Q3：Atomic 类一定比 synchronized 快？

**A**：不一定，高竞争下 CAS 自旋可能更耗 CPU，需要根据实际情况选择。

---

## 📚 扩展学习

- [Java 异步编程](../async-demo/)
- [Spring Boot Actuator](../actuator-demo/)
- [Java Concurrency in Practice](https://jcip.net/)

---

*最后更新：2026-06-27*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
