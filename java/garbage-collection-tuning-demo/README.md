<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# 垃圾回收调优演示

## 🎯 学习目标

通过本案例你将掌握JVM垃圾回收调优的核心技能：

- 理解Serial、Parallel、G1三种GC算法的工作原理和区别
- 掌握GC日志的启用参数和分析方法
- 学会WeakReference、SoftReference、PhantomReference的使用场景
- 能够根据应用特征选择合适的GC策略并调优
- 掌握GC性能基准测试方法

## 🛠️ 环境准备

### 系统要求
- Java 11+ 运行环境
- Maven 3.6+
- 至少4GB可用内存（用于GC对比测试）

### 构建项目
```bash
cd java/garbage-collection-tuning-demo
mvn clean compile
```

### 运行测试
```bash
mvn test
```

## 📁 项目结构

```
garbage-collection-tuning-demo/
├── pom.xml                          # Maven配置文件
├── README.md                        # 本文档
├── metadata.json                    # 元数据信息
└── src/
    ├── main/java/com/opendemo/java/jvm/gc/
    │   ├── GCDemo.java              # 主入口：System.gc()、finalize、GC MXBean
    │   ├── GCLogDemo.java           # GC日志参数和分析方法
    │   ├── SerialGCExample.java     # Serial GC算法演示
    │   ├── ParallelGCExample.java   # Parallel GC算法演示
    │   ├── G1GCExample.java         # G1 GC算法演示
    │   ├── GCTuningDemo.java        # GC调优策略和基准测试
    │   └── WeakReferenceDemo.java   # 引用类型演示
    └── test/java/com/opendemo/java/jvm/gc/
        └── GCDemoTest.java          # 单元测试
```

## 📚 核心知识点

### 1. 垃圾回收基础

**什么是垃圾回收（GC）？**
GC是JVM自动回收不再被引用的对象所占内存的机制。开发者无需手动释放内存，但需要理解GC的工作方式以进行性能调优。

**GC的基本流程：**
```
1. 标记（Mark）    - 找出所有存活对象
2. 删除（Sweep）   - 回收未被标记的对象
3. 压缩（Compact） - 整理内存碎片（部分GC算法）
```

### 2. GC算法对比

#### Serial GC（串行收集器）
```
特点: 单线程执行GC
算法: 标记-复制（新生代）+ 标记-压缩（老年代）
参数: -XX:+UseSerialGC
适用: 客户端应用、小堆(<200MB)
```

#### Parallel GC（并行收集器）
```
特点: 多线程并行执行GC，吞吐量优先
算法: 标记-复制（新生代）+ 标记-压缩（老年代）
参数: -XX:+UseParallelGC
适用: 批处理应用、Java 8默认GC
```

#### G1 GC（Garbage First）
```
特点: 分Region管理，停顿时间可预测
算法: 分区收集 + 混合GC
参数: -XX:+UseG1GC
适用: 大堆(>4GB)、低延迟服务、Java 9+默认GC
```

#### GC对比表
| 特性 | Serial | Parallel | G1 | ZGC |
|------|--------|----------|-----|-----|
| 线程数 | 1 | 多 | 多 | 多 |
| 停顿时间 | 长 | 中 | 短可控 | 极短 |
| 吞吐量 | 低 | 高 | 中高 | 高 |
| 堆大小 | <200MB | 任意 | >4GB | >4GB |
| 内存开销 | 低 | 低 | 中 | 中 |
| Java版本 | 所有 | 8默认 | 9+默认 | 15+ |

### 3. GC日志

#### Java 8 GC日志参数
```bash
-XX:+PrintGC                          # 基本GC日志
-XX:+PrintGCDetails                   # 详细GC日志
-XX:+PrintGCTimeStamps                # 时间戳
-XX:+PrintGCDateStamps                # 日期时间戳
-XX:+PrintGCApplicationStoppedTime    # STW时间
-XX:+PrintHeapAtGC                    # GC时打印堆信息
-Xloggc:/path/to/gc.log               # 输出到文件
-XX:+UseGCLogFileRotation             # 日志轮转
-XX:NumberOfGCLogFiles=10             # 保留10个日志文件
-XX:GCLogFileSize=10M                 # 每个文件最大10MB
```

#### Java 9+ 统一日志参数
```bash
-Xlog:gc                              # 基本GC日志
-Xlog:gc*                             # 所有GC相关日志
-Xlog:gc*=info                        # info级别
-Xlog:gc*:file=gc.log:time,uptime     # 输出到文件，带时间
-Xlog:gc+heap=debug                   # 堆详情
-Xlog:gc+phases=debug                 # GC阶段
-Xlog:gc+alloc                        # 分配信息
```

#### GC日志关键指标
- **Pause Time**: GC停顿时间，越短越好
- **GC Frequency**: GC频率，过于频繁需调优
- **Heap Before/After**: GC前后堆大小变化
- **GC Cause**: GC触发原因（Allocation Failure, System.gc(), Metadata GC Threshold等）

### 4. 引用类型详解

```
强引用 (Strong Reference)
├── Object obj = new Object()
├── 永远不会被GC回收（除非超出作用域）
└── 最常用的引用类型

软引用 (Soft Reference)
├── SoftReference<byte[]> ref = new SoftReference<>(data)
├── 内存不足时才被GC回收
├── 适合实现内存敏感的缓存
└── 可配合ReferenceQueue使用

弱引用 (Weak Reference)
├── WeakReference<Object> ref = new WeakReference<>(obj)
├── 下次GC时必然被回收
├── 适合临时缓存、监听器列表
└── WeakHashMap使用弱引用作为key

虚引用 (Phantom Reference)
├── PhantomReference<Object> ref = new PhantomReference<>(obj, queue)
├── get()始终返回null
├── 对象被回收后加入ReferenceQueue
└── 用于替代finalize()进行资源清理
```

### 5. G1 GC深入理解

#### Region分区
G1将堆划分为大小相等的Region（1-32MB）：
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ E   │ E   │ S   │ O   │ O   │ H   │ E   │Free │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
E=Eden  S=Survivor  O=Old  H=Humongous  Free=空闲
```

#### GC阶段
1. **Young GC**: 回收所有Eden和Survivor Region
2. **并发标记**: 标记老年代中的存活对象
3. **Mixed GC**: 回收新生代 + 部分老年代Region
4. **Full GC**: 回收整个堆（应避免）

#### G1关键参数
| 参数 | 说明 | 推荐值 |
|------|------|--------|
| -XX:MaxGCPauseMillis | 目标最大停顿时间 | 200 |
| -XX:G1HeapRegionSize | Region大小 | 根据堆自动计算 |
| -XX:InitiatingHeapOccupancyPercent | 触发并发标记的堆占用率 | 45 |
| -XX:G1MixedGCCountTarget | Mixed GC次数目标 | 8 |
| -XX:G1MixedGCLiveThresholdPercent | Region回收阈值 | 85 |

### 6. GC调优实战

#### 吞吐量优先调优
```bash
java -XX:+UseParallelGC \
     -XX:ParallelGCThreads=4 \
     -XX:GCTimeRatio=99 \
     -XX:MaxGCPauseMillis=200 \
     -Xms2g -Xmx2g \
     -jar app.jar
```

#### 延迟优先调优
```bash
java -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=50 \
     -XX:G1HeapRegionSize=4m \
     -XX:InitiatingHeapOccupancyPercent=45 \
     -Xms4g -Xmx4g \
     -jar app.jar
```

#### 超低延迟调优
```bash
java -XX:+UseZGC \
     -Xms4g -Xmx4g \
     -Xlog:gc*:file=gc.log \
     -jar app.jar
```

### 7. 常见GC问题诊断

#### 频繁Full GC
```
原因:
  1. 内存泄漏导致老年代持续增长
  2. 大对象直接进入老年代
  3. Metaspace不足
  4. System.gc()被频繁调用
解决:
  1. 分析堆转储找出泄漏对象
  2. 调整-XX:PretenureSizeThreshold
  3. 增大Metaspace
  4. 添加-XX:+DisableExplicitGC
```

#### GC停顿时间过长
```
原因:
  1. 堆过大导致标记/复制时间长
  2. 对象存活率高
  3. 使用了不合适的GC算法
解决:
  1. 考虑使用G1/ZGC
  2. 优化对象生命周期
  3. 减少不必要的对象分配
```

## 🚀 运行指南

### 运行GCDemo（主入口）
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.gc.GCDemo"
```

### 使用不同GC运行对比
```bash
# Serial GC
java -XX:+UseSerialGC -Xms64m -Xmx128m -Xlog:gc* -cp target/classes com.opendemo.java.jvm.gc.GCDemo

# Parallel GC
java -XX:+UseParallelGC -Xms256m -Xmx512m -Xlog:gc* -cp target/classes com.opendemo.java.jvm.gc.GCDemo

# G1 GC
java -XX:+UseG1GC -Xms256m -Xmx512m -Xlog:gc* -cp target/classes com.opendemo.java.jvm.gc.GCDemo
```

### 运行GC基准测试
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.gc.GCTuningDemo"
```

### 运行引用类型演示
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jvm.gc.WeakReferenceDemo"
```

## 📊 性能对比参考

### 不同GC算法的典型表现
| 指标 | Serial | Parallel | G1 |
|------|--------|----------|-----|
| Young GC停顿 | 10-50ms | 5-20ms | 5-30ms |
| Full GC停顿 | 100ms-1s | 50ms-500ms | 尽量避免 |
| 吞吐量影响 | 5-10% | 1-5% | 2-8% |
| 适合堆大小 | <200MB | 任意 | >4GB |

## ⚙️ GC调优检查清单

- [ ] 确定应用类型（吞吐量 vs 延迟）
- [ ] 设置-Xms = -Xmx避免堆扩容
- [ ] 选择合适的GC算法
- [ ] 开启GC日志
- [ ] 监控GC停顿时间和频率
- [ ] 检查Full GC频率
- [ ] 验证GC占比 < 5%
- [ ] 进行压力测试验证

## 🔗 相关资源

- [Java GC调优官方指南](https://docs.oracle.com/en/java/javase/11/gctuning/)
- [GCEasy在线分析](https://gceasy.io)
- [相关Demo: jvm-memory-management-demo](../jvm-memory-management-demo/)
- [相关Demo: application-profiling-demo](../application-profiling-demo/)

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
