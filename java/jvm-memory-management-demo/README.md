<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# JVM内存管理演示

## 🎯 学习目标

通过本案例你将掌握JVM内存管理的核心知识：

- 理解JVM堆内存和栈内存的区别与用途
- 掌握Runtime API和MemoryMXBean的使用方法
- 学会监控和分析JVM内存池状态（Eden、Survivor、Old Gen）
- 能够估算Java对象的内存占用大小
- 掌握内存泄漏的检测、诊断和修复方法

## 🛠️ 环境准备

### 系统要求
- Java 11+ 运行环境
- Maven 3.6+
- 至少2GB可用内存

### 构建项目
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd java/jvm-memory-management-demo
mvn clean compile
```

### 运行测试
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn test
```

## 📁 项目结构

```
jvm-memory-management-demo/
├── pom.xml                          # Maven配置文件
├── README.md                        # 本文档
├── metadata.json                    # 元数据信息
└── src/
    ├── main/java/com/opendemo/java/jvm/memory/
    │   ├── MemoryDemo.java          # 主入口：堆栈对比、MemoryMXBean、Runtime
    │   ├── HeapDemo.java            # 堆内存演示：增长、区域划分、对象晋升
    │   ├── StackDemo.java           # 栈内存演示：栈帧结构、栈溢出
    │   ├── MemoryPoolDemo.java      # 内存池监控：Eden、Survivor、老年代
    │   ├── ObjectSizeDemo.java      # 对象大小估算：基本类型、对象、集合
    │   └── MemoryLeakDemo.java      # 内存泄漏演示：泄漏场景、检测方法
    └── test/java/com/opendemo/java/jvm/memory/
        └── MemoryDemoTest.java      # 单元测试
```

## 📚 核心知识点

### 1. JVM内存模型

JVM将内存划分为以下几个主要区域：

```
┌─────────────────────────────────────────────────┐
│                    JVM 内存                       │
├─────────────────────┬───────────────────────────┤
│     堆内存 (Heap)    │      非堆内存 (Non-Heap)   │
├─────────────────────┤───────────────────────────┤
│ ┌─────┐ ┌─────────┐ │  方法区 (Metaspace)        │
│ │Eden │ │Survivor │ │  代码缓存                   │
│ │     │ │ S0  S1  │ │  JIT编译器                  │
│ ├─────┴─┴─────────┤ │                            │
│ │   老年代 Old Gen  │ │                            │
│ └─────────────────┘ │                            │
├─────────────────────┴───────────────────────────┤
│              栈内存 (Stack, 每线程一个)             │
│  ┌──────┐ ┌──────┐ ┌──────┐                     │
│  │栈帧1 │ │栈帧2 │ │栈帧3 │  ...                 │
│  └──────┘ └──────┘ └──────┘                     │
├─────────────────────────────────────────────────┤
│           本地方法栈 (Native Method Stack)         │
├─────────────────────────────────────────────────┤
│           程序计数器 (PC Register)                 │
└─────────────────────────────────────────────────┘
```

### 2. Runtime API 内存监控

```java
Runtime runtime = Runtime.getRuntime();
long maxMemory = runtime.maxMemory();      // -Xmx 最大可用内存
long totalMemory = runtime.totalMemory();  // 当前已分配内存
long freeMemory = runtime.freeMemory();    // 当前空闲内存
long usedMemory = totalMemory - freeMemory; // 当前已使用内存
```

### 3. MemoryMXBean 高级监控

```java
MemoryMXBean mbean = ManagementFactory.getMemoryMXBean();
MemoryUsage heapUsage = mbean.getHeapMemoryUsage();

heapUsage.getInit();       // 初始内存
heapUsage.getUsed();       // 已使用内存
heapUsage.getCommitted();  // 已提交内存
heapUsage.getMax();        // 最大内存
```

### 4. 堆内存区域

| 区域 | 说明 | 大小比例 |
|------|------|---------|
| Eden区 | 新对象首先分配在此 | 新生代的80% |
| Survivor 0 | Minor GC后存活对象 | 新生代的10% |
| Survivor 1 | 与S0交替使用 | 新生代的10% |
| 老年代 | 长期存活对象 | 堆的2/3 |

**对象晋升流程：**
1. 新对象在Eden区分配
2. Eden区满时触发Minor GC
3. 存活对象复制到Survivor区
4. 对象年龄达到阈值（默认15）晋升到老年代
5. 老年代满时触发Major GC / Full GC

### 5. 栈内存结构

每个方法调用创建一个栈帧：

```
┌─────────────────────┐
│     栈帧 (Frame)     │
├─────────────────────┤
│ 局部变量表           │ - 方法参数和局部变量
│ 操作数栈             │ - 中间计算结果
│ 动态链接             │ - 指向运行时常量池
│ 方法返回地址         │ - 方法正常/异常退出后地址
└─────────────────────┘
```

**栈相关参数：**
- `-Xss256k` - 设置每个线程的栈大小为256KB
- `-Xss512k` - 默认值（64位JVM）
- `-Xss1m` - 设置为1MB

### 6. 内存池监控

通过MemoryPoolMXBean可以监控各个内存池的详细状态：

```java
List<MemoryPoolMXBean> pools = ManagementFactory.getMemoryPoolMXBeans();
for (MemoryPoolMXBean pool : pools) {
    System.out.println(pool.getName());          // 内存池名称
    System.out.println(pool.getType());          // HEAP或NON_HEAP
    System.out.println(pool.getUsage());         // 当前使用情况
    System.out.println(pool.getPeakUsage());     // 峰值使用情况
}
```

### 7. 对象大小估算

**对象内存布局：**
```
┌──────────────────────┐
│    对象头 (Header)     │  12-16 bytes (Mark Word + Klass Pointer)
├──────────────────────┤
│    实例数据 (Data)     │  各字段大小之和
├──────────────────────┤
│    对齐填充 (Padding)  │  补齐到8字节的倍数
└──────────────────────┘
```

**基本类型大小：**
| 类型 | 大小 | 类型 | 大小 |
|------|------|------|------|
| boolean | 1 byte | int | 4 bytes |
| byte | 1 byte | float | 4 bytes |
| short | 2 bytes | long | 8 bytes |
| char | 2 bytes | double | 8 bytes |
| 引用(压缩) | 4 bytes | 引用(无压缩) | 8 bytes |

### 8. 内存泄漏常见场景

#### 场景一：静态集合持有对象引用
```java
// 错误做法
public class Cache {
    private static final Map<String, Object> CACHE = new HashMap<>();
    public static void put(String key, Object value) {
        CACHE.put(key, value); // 永远不会被GC回收
    }
}

// 正确做法
public class Cache {
    private static final Map<String, Object> CACHE = new WeakHashMap<>();
    // 或使用带过期时间的缓存
}
```

#### 场景二：未关闭的资源
```java
// 错误做法
Connection conn = dataSource.getConnection();
// 忘记关闭，连接池被耗尽

// 正确做法
try (Connection conn = dataSource.getConnection()) {
    // 使用连接
} // 自动关闭
```

#### 场景三：覆盖equals但不覆盖hashCode
```java
// 错误：作为HashMap的key时可能导致泄漏
public class BadKey {
    private int value;
    // 只覆盖了equals，没覆盖hashCode
}

// 正确：同时覆盖equals和hashCode，使用不可变字段
```

#### 场景四：ThreadLocal未清理
```java
// 错误：线程池中ThreadLocal累积
threadLocal.set(largeObject);
// 忘记 remove()

// 正确
try {
    threadLocal.set(largeObject);
} finally {
    threadLocal.remove();
}
```

### 9. 内存泄漏检测工具

| 工具 | 用途 | 命令 |
|------|------|------|
| jmap | 查看对象直方图 | `jmap -histo <pid>` |
| jmap | 堆转储 | `jmap -dump:format=b,file=heap.bin <pid>` |
| jvisualvm | 可视化分析 | `jvisualvm` |
| MAT | 堆转储分析 | Eclipse Memory Analyzer |
| jcmd | 诊断命令 | `jcmd <pid> GC.heap_info` |

**自动堆转储配置：**
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dumps/
```

## 🚀 运行指南

### 运行MemoryDemo（主入口）
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.memory.MemoryDemo"
```

### 运行HeapDemo
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.memory.HeapDemo"
```

### 运行StackDemo
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用默认栈大小
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.memory.StackDemo"

# 指定栈大小
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.memory.StackDemo" \
    -Dexec.args="-Xss256k"
```

### 运行MemoryPoolDemo
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用G1垃圾收集器查看不同的内存池
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.memory.MemoryPoolDemo" \
    -Dexec.executable=java -Dexec.toolchain=jdk \
    -Dexec.args="-XX:+UseG1GC"
```

### 运行ObjectSizeDemo
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.memory.ObjectSizeDemo"
```

### 运行MemoryLeakDemo
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.memory.MemoryLeakDemo"
```

## ⚙️ JVM内存参数参考

### 堆内存参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `-Xms` | 初始堆大小 | `-Xms256m` |
| `-Xmx` | 最大堆大小 | `-Xmx1g` |
| `-Xmn` | 新生代大小 | `-Xmn256m` |
| `-XX:NewRatio` | 老年代/新生代比例 | `-XX:NewRatio=2` |
| `-XX:SurvivorRatio` | Eden/Survivor比例 | `-XX:SurvivorRatio=8` |

### 非堆内存参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `-XX:MetaspaceSize` | 元空间初始大小 | `-XX:MetaspaceSize=128m` |
| `-XX:MaxMetaspaceSize` | 元空间最大大小 | `-XX:MaxMetaspaceSize=256m` |
| `-Xss` | 每线程栈大小 | `-Xss512k` |

### 优化参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `-XX:+UseCompressedOops` | 压缩普通对象指针 | 64位默认开启 |
| `-XX:+UseCompressedClassPointers` | 压缩类指针 | 64位默认开启 |
| `-XX:MaxTenuringThreshold` | 对象晋升年龄阈值 | `-XX:MaxTenuringThreshold=15` |
| `-XX:PretenureSizeThreshold` | 大对象直接进入老年代 | `-XX:PretenureSizeThreshold=1m` |

## 📊 性能调优建议

### 1. 堆大小设置原则
- 初始堆和最大堆设为相同值，避免运行时扩容开销
- 一般设置为物理内存的50-80%
- 预留足够的内存给操作系统和其他进程

### 2. 新生代与老年代比例
- 默认比例 1:2（-XX:NewRatio=2）
- 短生命周期对象多的应用可增大新生代
- 长期存活对象多的应用可增大老年代

### 3. 监控指标
- 堆使用率应保持在70%以下
- GC停顿时间应小于200ms
- Full GC频率应小于每小时1次
- 元空间使用不应持续增长

## 🔗 相关资源

- [JVM内存管理官方文档](https://docs.oracle.com/en/java/javase/11/gctuning/)
- [相关Demo: garbage-collection-tuning-demo](../garbage-collection-tuning-demo/)
- [相关Demo: application-profiling-demo](../application-profiling-demo/)

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
