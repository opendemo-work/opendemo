<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 应用性能分析演示

## 🎯 学习目标

通过本案例你将掌握Java应用性能分析的核心方法：

- 掌握JMX Bean进行运行时应用监控的方法
- 学会使用ThreadMXBean进行CPU时间和线程分析
- 掌握内存使用监控和分析技术
- 能够构建简单的性能基准测试框架
- 理解JIT编译器和热点代码优化机制

## 🛠️ 环境准备

### 系统要求
- Java 11+ 运行环境
- Maven 3.6+
- JVisualVM或JConsole（可选）

### 构建项目
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd java/application-profiling-demo
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
application-profiling-demo/
├── pom.xml                          # Maven配置文件
├── README.md                        # 本文档
├── metadata.json                    # 元数据信息
└── src/
    ├── main/java/com/opendemo/java/profiling/
    │   ├── ProfilingDemo.java           # 主入口
    │   ├── JmxProfilingDemo.java        # JMX监控演示
    │   ├── CpuProfilingDemo.java        # CPU分析演示
    │   ├── MemoryProfilingDemo.java     # 内存分析演示
    │   ├── PerformanceBenchmark.java    # 基准测试框架
    │   └── HotspotDemo.java             # JIT编译和热点优化
    └── test/java/com/opendemo/java/profiling/
        └── ProfilingDemoTest.java       # 单元测试
```

## 📚 核心知识点

### 1. JMX监控体系

JMX (Java Management Extensions) 提供了管理和监控应用的标准化方式。

#### RuntimeMXBean
```java
RuntimeMXBean bean = ManagementFactory.getRuntimeMXBean();
bean.getVmName();           // JVM名称
bean.getVmVersion();        // JVM版本
bean.getUptime();           // 运行时间
bean.getInputArguments();   // JVM启动参数
bean.getName();             // 进程ID@主机名
```

#### OperatingSystemMXBean
```java
OperatingSystemMXBean bean = ManagementFactory.getOperatingSystemMXBean();
bean.getAvailableProcessors();   // CPU核心数
bean.getSystemLoadAverage();     // 系统负载

// com.sun.management 扩展
((com.sun.management.OperatingSystemMXBean) bean).getProcessCpuLoad(); // 进程CPU
((com.sun.management.OperatingSystemMXBean) bean).getSystemCpuLoad();  // 系统CPU
((com.sun.management.OperatingSystemMXBean) bean).getTotalPhysicalMemorySize();
```

#### CompilationMXBean
```java
CompilationMXBean bean = ManagementFactory.getCompilationMXBean();
bean.getName();                   // JIT编译器名称 (HotSpot 64-Bit Tiered Compilers)
bean.getTotalCompilationTime();   // JIT编译总耗时
```

#### ThreadMXBean
```java
ThreadMXBean bean = ManagementFactory.getThreadMXBean();
bean.getThreadCount();              // 当前线程数
bean.getPeakThreadCount();          // 峰值线程数
bean.getAllThreadIds();             // 所有线程ID
bean.getThreadInfo(id);             // 线程信息
bean.findDeadlockedThreads();       // 死锁检测
bean.getCurrentThreadCpuTime();     // 当前线程CPU时间
```

### 2. CPU分析

#### CPU时间测量
```java
ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
threadBean.setThreadCpuTimeEnabled(true);

long cpuTimeBefore = threadBean.getCurrentThreadCpuTime();
long userTimeBefore = threadBean.getCurrentThreadUserTime();

// 执行被测代码
executeCode();

long cpuTimeAfter = threadBean.getCurrentThreadCpuTime();
long userTimeAfter = threadBean.getCurrentThreadUserTime();

// CPU时间 = 用户时间 + 系统时间
long systemTime = (cpuTimeAfter - cpuTimeBefore) - (userTimeAfter - userTimeBefore);
```

#### 死锁检测
```java
ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
long[] deadlocked = threadBean.findDeadlockedThreads();
if (deadlocked != null) {
    ThreadInfo[] infos = threadBean.getThreadInfo(deadlocked);
    // 分析死锁线程的栈帧和锁信息
}
```

#### CPU分析工具
| 工具 | 类型 | 特点 |
|------|------|------|
| jstack | 命令行 | 线程栈转储 |
| jvisualvm | 可视化 | CPU采样和 profiling |
| JProfiler | 商业 | 方法级CPU分析 |
| YourKit | 商业 | 深度CPU分析 |
| async-profiler | 开源 | 低开销，火焰图 |

### 3. 内存分析

#### 堆内存监控
```java
MemoryMXBean memBean = ManagementFactory.getMemoryMXBean();
MemoryUsage heapUsage = memBean.getHeapMemoryUsage();

heapUsage.getInit();       // 初始化内存
heapUsage.getUsed();       // 已使用内存
heapUsage.getCommitted();  // 已提交内存
heapUsage.getMax();        // 最大可用内存

double usagePercent = (double) heapUsage.getUsed() / heapUsage.getMax() * 100;
```

#### 内存分配速率测量
```java
long usedBefore = runtime.totalMemory() - runtime.freeMemory();
long startTime = System.nanoTime();

// 执行内存分配代码
allocateObjects();

long duration = System.nanoTime() - startTime;
long usedAfter = runtime.totalMemory() - runtime.freeMemory();
long allocatedBytes = usedAfter - usedBefore;
double allocRateMBps = (allocatedBytes / (1024.0 * 1024.0)) / (duration / 1e9);
```

#### 内存优化对比
```
100,000个Integer (ArrayList): ~2,400 KB
100,000个int (原始数组):     ~400 KB
装箱开销: ~6x

结论: 使用原始类型数组比包装类型集合节省大量内存
```

### 4. 基准测试框架

#### 基本原则
```
1. 预热 (Warmup): 让JIT编译热点代码
2. 多次测量: 取统计值（平均、最小、最大、标准差）
3. 避免死代码消除: 确保计算结果被使用
4. 控制变量: 对比测试保持其他条件相同
5. 使用专业工具: JMH (Java Microbenchmark Harness)
```

#### 自定义基准测试框架
```java
public static <T> BenchmarkResult benchmark(String name, Supplier<T> task, int iterations) {
    // 1. 预热
    for (int i = 0; i < 3; i++) task.get();
    
    // 2. 正式测量
    List<Long> durations = new ArrayList<>();
    for (int i = 0; i < iterations; i++) {
        long start = System.nanoTime();
        task.get();
        durations.add(System.nanoTime() - start);
    }
    
    // 3. 统计
    long min = durations.stream().mapToLong(Long::longValue).min().orElse(0);
    long max = durations.stream().mapToLong(Long::longValue).max().orElse(0);
    double avg = durations.stream().mapToLong(Long::longValue).average().orElse(0);
    
    return new BenchmarkResult(name, iterations, min, max, avg);
}
```

#### JMH示例（推荐）
```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Thread)
public class MyBenchmark {
    
    @Benchmark
    public long testMethod() {
        long sum = 0;
        for (long i = 0; i < 1_000_000; i++) sum += i;
        return sum;
    }
}
```

### 5. JIT编译与热点优化

#### JIT编译过程
```
Java源码 → 字节码 → 解释执行
                     ↓ (热点方法被多次调用)
              JIT编译 (C1/C2编译器)
                     ↓
              本地机器码 (直接执行)
```

#### 分层编译
```
Level 0: 解释执行         → 启动快，执行慢
Level 1: C1简单编译       → 快速编译，基本优化
Level 2: C1有限编译       → 部分性能分析
Level 3: C1完全编译       → 完全性能分析
Level 4: C2深度优化编译   → 最优性能，编译慢
```

#### JIT优化技术

**方法内联 (Method Inlining)**
```
优化前:
  int result = add(a, b);  // 方法调用开销

优化后 (内联):
  int result = a + b;      // 直接计算

条件: 方法体足够小 (<325字节)
```

**分支预测 (Branch Prediction)**
```
已排序数据: 分支模式稳定，CPU预测准确 → 快
未排序数据: 分支模式随机，CPU预测失败 → 慢

优化: 对频繁条件判断的数据预先排序
```

**循环优化**
- 循环展开 (Loop Unrolling): 减少循环控制开销
- 循环不变量外提 (LICM): 将循环内不变计算移出
- 数组边界检查消除: 消除不必要的边界检查

#### JIT编译参数
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
-XX:+PrintCompilation           # 打印编译信息
-XX:+PrintInlining              # 打印内联信息
-XX:CompileThreshold=10000      # 编译阈值
-XX:+TieredCompilation          # 分层编译(默认开启)
-XX:MaxInlineSize=35            # 最大内联方法大小
-XX:FreqInlineSize=325          # 热点方法内联大小
```

## 🚀 运行指南

### 运行完整演示
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.profiling.ProfilingDemo"
```

### 运行单个模块
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# JMX监控
mvn exec:java -Dexec.mainClass="com.opendemo.java.profiling.JmxProfilingDemo"

# CPU分析
mvn exec:java -Dexec.mainClass="com.opendemo.java.profiling.CpuProfilingDemo"

# 内存分析
mvn exec:java -Dexec.mainClass="com.opendemo.java.profiling.MemoryProfilingDemo"

# 基准测试
mvn exec:java -Dexec.mainClass="com.opendemo.java.profiling.PerformanceBenchmark"

# JIT编译
mvn exec:java -Dexec.mainClass="com.opendemo.java.profiling.HotspotDemo"
```

### 使用JVisualVM监控
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 启动应用并开启JMX远程连接
mvn exec:java -Dexec.mainClass="com.opendemo.java.profiling.ProfilingDemo" \
    -Dexec.args="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9010 \
    -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false"

# 启动JVisualVM
jvisualvm
```

### 使用JConsole监控
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
jconsole
# 连接到本地进程或远程 9010 端口
```

## 📊 性能分析检查清单

### 分析前
- [ ] 明确性能目标和指标
- [ ] 准备可重现的测试场景
- [ ] 使用生产环境相似的配置

### CPU分析
- [ ] 识别CPU热点方法
- [ ] 检查线程数是否合理
- [ ] 排查死锁和线程阻塞
- [ ] 检查GC对CPU的影响

### 内存分析
- [ ] 监控堆内存使用趋势
- [ ] 分析对象创建和回收速率
- [ ] 检查内存泄漏
- [ ] 优化数据结构选择

### JIT分析
- [ ] 确认热点方法被JIT编译
- [ ] 检查是否有大方法阻止内联
- [ ] 验证预热后的性能稳定

## 🔗 相关资源

- [JMX官方教程](https://docs.oracle.com/javase/tutorial/jmx/)
- [JMH基准测试框架](https://openjdk.org/projects/code-tools/jmh/)
- [async-profiler](https://github.com/async-profiler/async-profiler)
- [相关Demo: jvm-memory-management-demo](../jvm-memory-management-demo/)
- [相关Demo: garbage-collection-tuning-demo](../garbage-collection-tuning-demo/)

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
