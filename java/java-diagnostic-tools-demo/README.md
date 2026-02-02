# Java诊断工具与Arthas实战演示

## 🎯 学习目标

通过本案例你将掌握Java应用诊断和性能分析的核心工具：

- Arthas在线诊断工具的使用和实践
- JVM性能监控和内存分析
- 线程状态分析和死锁检测
- GC日志分析和优化
- 应用性能瓶颈定位
- 生产环境问题快速排查

## 🛠️ 环境准备

### 系统要求
- Java 8+ 运行环境
- Linux/Unix系统（推荐）或Windows
- 至少2GB内存用于诊断工具运行
- 生产环境应用部署经验

### 依赖安装
```bash
# 安装Arthas
curl -O https://arthas.aliyun.com/arthas-boot.jar
# 或使用wget
wget https://arthas.aliyun.com/arthas-boot.jar

# 验证安装
java -jar arthas-boot.jar --version

# 其他Java诊断工具
# JVisualVM (JDK自带)
# JConsole (JDK自带)
# Eclipse MAT 内存分析工具
```

## 📁 项目结构

```
java-diagnostic-tools-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 诊断脚本
│   ├── arthas_launcher.sh             # Arthas启动脚本
│   ├── jvm_monitor.sh                 # JVM监控脚本
│   ├── thread_analyzer.sh             # 线程分析脚本
│   ├── gc_log_analyzer.sh             # GC日志分析脚本
│   └── memory_profiler.sh             # 内存分析脚本
├── configs/                           # 配置文件
│   ├── arthas_config.properties       # Arthas配置文件
│   ├── jvm_options.conf               # JVM参数配置
│   └── gc_logging.conf                # GC日志配置
├── examples/                          # 实际案例
│   ├── arthas_commands_demo.txt       # Arthas命令示例
│   ├── jstack_output_example.txt      # 线程堆栈示例
│   ├── gc_log_analysis.txt            # GC日志分析示例
│   └── memory_leak_case.txt           # 内存泄漏案例
└── docs/                              # 详细文档
    ├── arthas_user_guide.md           # Arthas使用指南
    ├── jvm_performance_tuning.md      # JVM性能调优
    ├── troubleshooting_manual.md      # 故障排查手册
    └── best_practices.md              # 最佳实践指南
```

## 🔧 核心诊断工具详解

### 1. Arthas在线诊断工具

```bash
# 启动Arthas
java -jar arthas-boot.jar

# 选择目标Java进程
# 输入对应的进程ID

# 常用Arthas命令
## 基础信息查看
dashboard                    # 仪表盘，显示系统概况
thread                       # 查看线程信息
jvm                          # 查看JVM信息
sysprop                      # 查看系统属性
sysenv                       # 查看环境变量

## 类和方法监控
sc *UserController          # 搜索类
sm com.example.UserController  # 查看类的方法
watch com.example.UserService getUser '{params, returnObj}' -x 2  # 监控方法执行
trace com.example.UserService saveUser  # 方法调用链路追踪
monitor -c 5 com.example.UserService saveUser  # 方法执行统计

## 内存和GC分析
heapdump /tmp/heap.hprof    # 生成堆转储文件
ognl '@com.example.Application@context'  # OGNL表达式访问对象
mbean java.lang:type=GarbageCollector,*  # 查看GC相关的MBean

## 线程分析
thread -n 5                 # 查看最忙的5个线程
thread -b                   # 查找阻塞的线程
thread [thread_id]          # 查看特定线程的堆栈

## 热更新
jad com.example.UserService  # 反编译类
mc /tmp/UserService.java    # 编译修改后的Java文件
redefine /tmp/UserService.class  # 热更新类定义
```

### 2. JVM内置诊断工具

```bash
# JPS - Java进程查看
jps -l                          # 显示Java进程和主类
jps -v                          # 显示Java进程和JVM参数

# JStack - 线程堆栈分析
jstack [pid] > thread_dump.txt  # 生成线程转储
jstack -l [pid]                 # 包含锁信息的线程转储

# JMap - 内存映像工具
jmap -heap [pid]                # 查看堆内存使用情况
jmap -histo [pid]               # 查看对象直方图
jmap -dump:format=b,file=heap.hprof [pid]  # 生成堆转储文件

# JStat - JVM统计监控
jstat -gc [pid] 1s 10           # 每秒输出GC统计信息，共10次
jstat -gccapacity [pid]         # 查看GC各区域容量
jstat -compiler [pid]           # 查看JIT编译统计

# JInfo - JVM配置信息
jinfo [pid]                     # 查看JVM参数
jinfo -flag PrintGC [pid]       # 查看特定参数值
jinfo -flag +PrintGC [pid]      # 开启特定参数
```

### 3. GC日志分析

```bash
# 启用GC日志
# JVM参数配置
-XX:+PrintGC                    # 打印GC基本信息
-XX:+PrintGCDetails             # 打印GC详细信息
-XX:+PrintGCTimeStamps          # 打印GC时间戳
-Xloggc:/tmp/gc.log             # 指定GC日志文件

# GC日志分析示例
# 使用gceasy.io在线分析工具
# 或使用GCViewer等离线工具

# 手动分析GC日志
grep "Full GC" gc.log | wc -l   # 统计Full GC次数
awk '/\[GC/ {print $NF}' gc.log | sort -n | tail -10  # 查看最长GC时间
```

### 4. 内存分析工具

```bash
# Eclipse MAT内存分析
# 下载MAT工具
wget http://www.eclipse.org/downloads/download.php?file=/mat/1.10.0/rcp/MemoryAnalyzer-1.10.0.20200916-linux.gtk.x86_64.zip

# 分析堆转储文件
# 在MAT中打开heap.hprof文件
# 使用以下功能：
# - Histogram: 对象直方图
# - Dominator Tree: 支配树分析
# - Leak Suspects: 内存泄漏嫌疑报告
# - Top Components: 顶级组件分析

# 命令行内存分析
jhat heap.hprof                 # 启动HTTP服务器分析堆转储
# 访问 http://localhost:7000 查看分析结果
```

## 🔍 实战诊断场景

### 场景1：CPU使用率过高问题排查

```bash
#!/bin/bash
# CPU高使用率诊断脚本

PID=$1
echo "诊断进程: $PID"

# 1. 查看进程CPU使用情况
top -p $PID -b -n 1

# 2. 获取最忙的线程
THREAD_INFO=$(top -H -p $PID -b -n 1 | head -20)
BUSY_THREAD_ID=$(echo "$THREAD_INFO" | awk 'NR>7 {print $1}' | head -1)
BUSY_THREAD_HEX=$(printf "%x\n" $BUSY_THREAD_ID)

echo "最忙线程ID: $BUSY_THREAD_ID (十六进制: $BUSY_THREAD_HEX)"

# 3. 获取线程堆栈
jstack $PID > /tmp/thread_dump_$PID.txt
grep -A 10 "nid=0x$BUSY_THREAD_HEX" /tmp/thread_dump_$PID.txt

# 4. 使用Arthas进一步分析
echo "建议使用Arthas命令:"
echo "thread -n 5"
echo "thread $BUSY_THREAD_ID"
```

### 场景2：内存泄漏检测

```bash
#!/bin/bash
# 内存泄漏检测脚本

PID=$1
APP_NAME=$2

echo "开始内存泄漏检测..."
echo "进程ID: $PID"
echo "应用名称: $APP_NAME"

# 1. 监控堆内存使用
echo "=== 堆内存使用监控 ==="
jstat -gc $PID 5s 10

# 2. 生成堆转储文件
echo "=== 生成堆转储文件 ==="
HEAP_DUMP_FILE="/tmp/${APP_NAME}_heap_$(date +%Y%m%d_%H%M%S).hprof"
jmap -dump:format=b,file=$HEAP_DUMP_FILE $PID
echo "堆转储文件: $HEAP_DUMP_FILE"

# 3. 分析对象直方图
echo "=== 对象直方图分析 ==="
jmap -histo $PID | head -20

# 4. 检查GC情况
echo "=== GC统计信息 ==="
jstat -gc $PID 1s 5

echo "诊断完成，请使用MAT工具分析堆转储文件"
```

### 场景3：死锁检测

```bash
# 使用jstack检测死锁
jstack [pid] | grep -A 10 "Found one Java-level deadlock"

# 使用Arthas检测死锁
# 在Arthas中执行:
thread -b                      # 查找阻塞的线程
thread                         # 查看所有线程状态

# 死锁分析脚本
#!/bin/bash
PID=$1

echo "=== 死锁检测 ==="
DEADLOCK_INFO=$(jstack $PID | grep -A 20 "Found one Java-level deadlock")

if [ -n "$DEADLOCK_INFO" ]; then
    echo "发现死锁:"
    echo "$DEADLOCK_INFO"
    
    # 生成详细线程转储
    jstack -l $PID > /tmp/deadlock_threads_$(date +%Y%m%d_%H%M%S).txt
    echo "详细线程信息已保存到文件"
else
    echo "未发现死锁"
fi
```

## 📊 性能监控最佳实践

### JVM参数优化配置
```bash
# 堆内存配置
-Xms2g -Xmx2g                   # 初始和最大堆大小
-XX:NewRatio=2                  # 老年代与新生代比例
-XX:SurvivorRatio=8             # Eden与Survivor比例

# GC配置
-XX:+UseG1GC                    # 使用G1垃圾收集器
-XX:MaxGCPauseMillis=200        # 最大GC暂停时间
-XX:G1HeapRegionSize=16m        # G1区域大小

# 监控配置
-XX:+PrintGC                    # 打印GC信息
-XX:+PrintGCDetails             # 打印GC详细信息
-XX:+PrintGCTimeStamps          # 打印GC时间戳
-Xloggc:/app/logs/gc.log        # GC日志文件
-XX:+HeapDumpOnOutOfMemoryError # OOM时生成堆转储
-XX:HeapDumpPath=/app/dumps/    # 堆转储文件路径
```

### 监控脚本示例
```bash
#!/bin/bash
# JVM健康检查脚本

APP_NAME="myapp"
PID=$(pgrep -f $APP_NAME)

if [ -z "$PID" ]; then
    echo "应用未运行"
    exit 1
fi

echo "=== JVM健康检查报告 ==="
echo "检查时间: $(date)"
echo "进程ID: $PID"

# 内存使用情况
echo "=== 内存使用情况 ==="
jstat -gc $PID | tail -1 | awk '{
    printf "年轻代使用: %.2f%%\n", ($3+$4)*100/($1+$2+$3+$4)
    printf "老年代使用: %.2f%%\n", $7*100/($5+$6+$7)
}'

# 线程情况
echo "=== 线程情况 ==="
THREAD_COUNT=$(jstack $PID | grep "java.lang.Thread.State" | wc -l)
RUNNABLE_THREADS=$(jstack $PID | grep "RUNNABLE" | wc -l)
BLOCKED_THREADS=$(jstack $PID | grep "BLOCKED" | wc -l)

echo "总线程数: $THREAD_COUNT"
echo "运行中线程: $RUNNABLE_THREADS"
echo "阻塞线程: $BLOCKED_THREADS"

# GC统计
echo "=== GC统计 ==="
jstat -gc $PID | tail -1 | awk '{
    printf "GC总次数: %d\n", $14+$15
    printf "Full GC次数: %d\n", $15
}'
```

## 🧪 验证测试

### 工具可用性测试
```bash
#!/bin/bash
# Java诊断工具验证脚本

echo "=== Java诊断工具验证 ==="

# 检查Arthas
if [ -f "arthas-boot.jar" ]; then
    java -jar arthas-boot.jar --version >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ Arthas工具可用"
    else
        echo "❌ Arthas工具异常"
    fi
else
    echo "⚠️  Arthas工具未安装"
fi

# 检查JVM工具
for tool in jps jstack jmap jstat jinfo; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool 工具可用"
    else
        echo "❌ $tool 工具不可用"
    fi
done

# 检查Java进程
JAVA_PROCESSES=$(jps -l | wc -l)
echo "当前Java进程数: $JAVA_PROCESSES"
```

## ❓ 常见问题处理

### Q1: Arthas无法附加到目标进程？
**解决方案**：
```bash
# 检查权限
sudo java -jar arthas-boot.jar

# 检查Java版本兼容性
java -version
# Arthas支持Java 8+

# 检查进程状态
jps -l
ps -ef | grep java
```

### Q2: 如何分析内存泄漏？
**分析步骤**：
1. 使用jmap生成堆转储文件
2. 使用MAT工具分析堆转储
3. 查看支配树找出内存占用大户
4. 分析对象引用链定位泄漏根源
5. 修复代码并重新验证

### Q3: GC频繁如何优化？
**优化建议**：
```bash
# 调整堆大小
-Xms4g -Xmx4g

# 选择合适的GC算法
-XX:+UseG1GC

# 调整GC参数
-XX:MaxGCPauseMillis=100
-XX:G1HeapRegionSize=32m

# 监控GC效果
jstat -gc [pid] 10s
```

## 📚 扩展学习

### 专业诊断工具
- **JProfiler**: 商业Java性能分析工具
- **YourKit**: 功能强大的Java Profiler
- **Pinpoint**: 分布式系统APM工具
- **SkyWalking**: 国产APM解决方案

### 学习进阶路径
1. 掌握JVM内存模型和GC机制
2. 学习各种GC算法的特点和适用场景
3. 理解Java并发编程和线程模型
4. 掌握分布式系统性能分析方法
5. 学习微服务架构下的诊断技术

### 认证考试推荐
- Oracle Certified Professional: Java Programmer
- JVM调优专家认证
- 性能工程专家认证

---
> **💡 提示**: 生产环境使用诊断工具时要注意性能影响，建议在低峰期进行深度分析，并做好数据备份。