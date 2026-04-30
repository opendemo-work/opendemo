# Java并发编程演示

## 🎯 学习目标

通过本案例你将掌握Java并发编程的核心技术：

- 掌握Thread、Runnable、Callable三种线程创建方式
- 理解synchronized和ReentrantLock的使用与区别
- 掌握ConcurrentHashMap等并发集合的使用和原理
- 学会使用线程池和CompletableFuture进行异步编程
- 理解原子变量和CAS无锁机制
- 掌握生产者消费者模式的多种实现

## 🛠️ 环境准备

### 系统要求
- Java 11+ 运行环境
- Maven 3.6+

### 构建项目
```bash
cd java/concurrent-programming-demo
mvn clean compile
```

### 运行测试
```bash
mvn test
```

## 📁 项目结构

```
concurrent-programming-demo/
├── pom.xml                          # Maven配置文件
├── README.md                        # 本文档
├── metadata.json                    # 元数据信息
└── src/
    ├── main/java/com/opendemo/java/concurrent/
    │   ├── ConcurrentDemo.java          # 主入口
    │   ├── ThreadCreationDemo.java      # 线程创建方式演示
    │   ├── SynchronizedDemo.java        # 同步机制演示
    │   ├── ConcurrentCollectionsDemo.java # 并发集合演示
    │   ├── ExecutorServiceDemo.java     # 线程池和异步编程演示
    │   ├── AtomicVariableDemo.java      # 原子变量演示
    │   └── ProducerConsumerDemo.java    # 生产者消费者模式演示
    └── test/java/com/opendemo/java/concurrent/
        └── ConcurrentDemoTest.java      # 单元测试
```

## 📚 核心知识点

### 1. 线程创建方式

#### 方式一：继承Thread类
```java
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("线程运行: " + getName());
    }
}
new MyThread().start();
```

**优点**: 简单直接
**缺点**: Java单继承，无法继承其他类

#### 方式二：实现Runnable接口
```java
Runnable task = () -> System.out.println("Runnable任务");
new Thread(task).start();
```

**优点**: 可继承其他类，支持Lambda
**缺点**: 无返回值

#### 方式三：实现Callable接口
```java
Callable<Integer> task = () -> {
    return 1 + 2 + 3;
};
FutureTask<Integer> future = new FutureTask<>(task);
new Thread(future).start();
Integer result = future.get(); // 阻塞获取结果
```

**优点**: 有返回值，可抛受检异常
**缺点**: 需要配合FutureTask使用

#### 线程生命周期
```
NEW → start() → RUNNABLE ⇄ BLOCKED/WAITING/TIMED_WAITING → TERMINATED
```

### 2. 同步机制

#### synchronized
```java
// 同步方法
public synchronized void increment() { counter++; }

// 同步块
synchronized (lock) { counter++; }

// 静态同步方法（类锁）
public static synchronized void staticMethod() { }
```

**特点**: JVM内置，自动释放锁，不可中断

#### ReentrantLock
```java
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    // 临界区
} finally {
    lock.unlock(); // 必须手动释放
}
```

**特点**: API层面，支持中断、超时、公平锁、条件变量

#### 对比表
| 特性 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 实现 | JVM内置 | API层面 |
| 锁释放 | 自动 | 手动unlock |
| 可中断 | 否 | lockInterruptibly() |
| 超时 | 不支持 | tryLock(timeout) |
| 公平性 | 非公平 | 可选 |
| 条件变量 | wait/notify | Condition |

#### 读写锁
```java
ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
rwLock.readLock().lock();   // 多个读者可同时持有
rwLock.writeLock().lock();  // 写者独占
```

### 3. 并发集合

#### ConcurrentHashMap
- 分段锁（Java 7）或CAS+synchronized（Java 8+）
- 高并发读写，线程安全
- 提供原子操作: compute(), merge(), putIfAbsent()

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.compute("key", (k, v) -> v == null ? 1 : v + 1);
map.merge("key", 1, Integer::sum);
```

#### CopyOnWriteArrayList
- 写时复制策略，读无锁
- 适合读多写少场景
- 写操作开销大（需要复制整个数组）

#### 集合对比
| 集合 | 线程安全 | 读性能 | 写性能 |
|------|---------|--------|--------|
| HashMap | 否 | 高 | 高 |
| ConcurrentHashMap | 是 | 高 | 中高 |
| ArrayList | 否 | 高 | 高 |
| CopyOnWriteArrayList | 是 | 高 | 低 |
| synchronizedList | 是 | 中 | 中 |

### 4. 线程池

#### 线程池类型
```java
// 固定大小线程池
ExecutorService fixed = Executors.newFixedThreadPool(n);

// 缓存线程池（按需创建）
ExecutorService cached = Executors.newCachedThreadPool();

// 定时线程池
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(n);

// 单线程池
ExecutorService single = Executors.newSingleThreadExecutor();
```

#### 推荐方式：ThreadPoolExecutor
```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    4,                      // 核心线程数
    8,                      // 最大线程数
    60L, TimeUnit.SECONDS,  // 空闲线程存活时间
    new ArrayBlockingQueue<>(100),  // 工作队列
    new ThreadPoolExecutor.CallerRunsPolicy()  // 拒绝策略
);
```

#### 线程数计算
```
CPU密集型: 线程数 = CPU核心数 + 1
IO密集型:  线程数 = CPU核心数 * 2
混合型:    根据任务比例调整
```

#### CompletableFuture异步编排
```java
CompletableFuture
    .supplyAsync(() -> fetchData())
    .thenApply(data -> processData(data))
    .thenCompose(result -> saveAsync(result))
    .thenAccept(saved -> notify(saved))
    .exceptionally(ex -> { log.error(ex); return null; });
```

### 5. 原子变量与CAS

#### 原子操作类
```java
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();       // ++i
counter.getAndIncrement();       // i++
counter.addAndGet(10);           // += 10
counter.compareAndSet(5, 10);    // CAS
```

#### CAS机制
```
Compare-And-Swap: 读取→比较→交换（原子操作）
V = 当前值, E = 期望值, N = 新值
if (V == E) { V = N; return true; }
else { return false; } // 重试
```

#### 原子类选择
| 原子类 | 用途 |
|--------|------|
| AtomicInteger | 整型计数器 |
| AtomicLong | 长整型计数器 |
| AtomicBoolean | 布尔标志 |
| AtomicReference | 引用类型原子更新 |
| LongAdder | 高并发累加（优于AtomicLong） |

### 6. 生产者消费者模式

#### BlockingQueue实现
```java
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);

// 生产者
queue.put(item);  // 队列满时阻塞

// 消费者
String item = queue.take();  // 队列空时阻塞
```

#### wait/notify实现
```java
// 生产者
synchronized (buffer) {
    while (buffer.isFull()) buffer.wait();
    buffer.add(item);
    buffer.notifyAll();
}

// 消费者
synchronized (buffer) {
    while (buffer.isEmpty()) buffer.wait();
    String item = buffer.remove();
    buffer.notifyAll();
}
```

#### 阻塞队列对比
| 队列 | 有界 | 特点 |
|------|------|------|
| ArrayBlockingQueue | 固定 | 有界，公平可选 |
| LinkedBlockingQueue | 可选 | 高吞吐 |
| PriorityBlockingQueue | 否 | 优先级排序 |
| SynchronousQueue | 容量0 | 直接传递 |
| DelayQueue | 否 | 延迟取出 |

## 🚀 运行指南

### 运行完整演示
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.concurrent.ConcurrentDemo"
```

### 运行单个模块
```bash
# 线程创建
mvn exec:java -Dexec.mainClass="com.opendemo.java.concurrent.ThreadCreationDemo"

# 同步机制
mvn exec:java -Dexec.mainClass="com.opendemo.java.concurrent.SynchronizedDemo"

# 并发集合
mvn exec:java -Dexec.mainClass="com.opendemo.java.concurrent.ConcurrentCollectionsDemo"

# 线程池
mvn exec:java -Dexec.mainClass="com.opendemo.java.concurrent.ExecutorServiceDemo"

# 原子变量
mvn exec:java -Dexec.mainClass="com.opendemo.java.concurrent.AtomicVariableDemo"

# 生产者消费者
mvn exec:java -Dexec.mainClass="com.opendemo.java.concurrent.ProducerConsumerDemo"
```

## ⚠️ 并发编程注意事项

### 常见陷阱
1. **竞态条件**: 多线程同时修改共享变量 → 使用同步或原子类
2. **死锁**: 互相等待对方持有的锁 → 按固定顺序获取锁
3. **内存可见性**: 线程间变量不可见 → 使用volatile或synchronized
4. **虚假唤醒**: wait被意外唤醒 → 使用while循环检查条件

### 最佳实践
1. 优先使用并发集合而非synchronized包装
2. 使用线程池而非直接创建线程
3. 优先使用原子类而非加锁
4. 使用CompletableFuture进行异步编排
5. 始终在finally块中释放锁
6. 避免在持有锁时调用外部方法

## 🔗 相关资源

- [Java并发编程官方教程](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [java.util.concurrent API文档](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/concurrent/package-summary.html)
- [相关Demo: jvm-memory-management-demo](../jvm-memory-management-demo/)
- [相关Demo: application-profiling-demo](../application-profiling-demo/)
