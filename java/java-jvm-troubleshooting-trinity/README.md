# JVM性能分析三剑客实战演示

## 🎯 学习目标

通过本案例你将掌握Java应用性能分析的三大核心工具：

- **JVM三剑客**: jps、jstack、jmap的深度使用技巧
- **线程状态分析**: 线程堆栈解读和问题定位
- **内存分析技术**: 堆内存使用分析和内存泄漏检测
- **GC性能调优**: 垃圾回收监控和优化策略
- **生产环境快速排查**: 问题诊断的标准流程和最佳实践

## 🛠️ 环境准备

### 系统要求
- Java 8+ 运行环境
- Linux/Unix系统（推荐RHEL/CentOS/Ubuntu）
- 至少4GB内存用于性能分析
- 生产环境应用部署和运维经验

### 依赖安装
```bash
# 验证JVM工具可用性
java -version
jps -V

# 安装额外分析工具（可选）
# Eclipse MAT内存分析工具
wget http://www.eclipse.org/downloads/download.php?file=/mat/1.10.0/rcp/MemoryAnalyzer-1.10.0.20200916-linux.gtk.x86_64.zip

# VisualVM图形化分析工具（JDK自带）
which jvisualvm

# GC日志分析工具
pip install gceasy  # Python GC日志分析库
```

## 📁 项目结构

```
java-jvm-troubleshooting-trinity/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 三剑客分析脚本
│   ├── jvm_trinity_analyzer.sh        # 三剑客综合分析脚本
│   ├── thread_dump_analyzer.sh        # 线程转储分析脚本
│   ├── memory_leak_detector.sh        # 内存泄漏检测脚本
│   ├── gc_performance_monitor.sh      # GC性能监控脚本
│   └── quick_diagnosis.sh             # 快速诊断脚本
├── configs/                           # 配置文件
│   ├── jvm_monitoring.conf            # JVM监控配置
│   ├── gc_logging.conf                # GC日志配置模板
│   └── analysis_rules.conf            # 分析规则配置
├── examples/                          # 实际案例
│   ├── thread_dump_samples.txt        # 线程转储样本
│   ├── memory_analysis_report.txt     # 内存分析报告示例
│   ├── gc_log_analysis.txt            # GC日志分析示例
│   └── troubleshooting_cases.txt      # 故障排查案例集
└── docs/                              # 详细文档
    ├── jvm_trinity_guide.md           # 三剑客使用指南
    ├── thread_analysis_manual.md      # 线程分析手册
    ├── memory_profiling_guide.md      # 内存分析指南
    └── gc_optimization_strategies.md  # GC优化策略
```

## 🔧 JVM三剑客详解

### 1. JPS - Java进程扫描器

```bash
# 基础用法
jps                        # 显示本地Java进程PID和主类名
jps -l                     # 显示完整包名
jps -v                     # 显示JVM启动参数
jps -m                     # 显示传递给main方法的参数

# 高级用法
jps -V                     # 显示版本信息
jps -J-version             # 显示JVM版本
jps -mlvV                  # 组合显示所有信息

# 远程主机监控
jps hostname:port          # 监控远程主机Java进程
jps -J-Djava.rmi.server.hostname=hostname  # 指定RMI主机名

# 实用脚本示例
#!/bin/bash
# Java进程健康检查脚本
echo "=== Java进程状态检查 ==="
echo "检查时间: $(date)"
echo ""

jps -lv | while read line; do
    PID=$(echo $line | awk '{print $1}')
    CLASS=$(echo $line | awk '{print $2}')
    ARGS=$(echo $line | cut -d' ' -f3-)
    
    echo "PID: $PID"
    echo "类名: $CLASS"
    echo "参数: $ARGS"
    
    # 检查进程是否响应
    kill -0 $PID 2>/dev/null && echo "状态: 运行中" || echo "状态: 无响应"
    echo "---"
done
```

### 2. JSTACK - 线程堆栈分析器

```bash
# 基础线程分析
jstack [pid] > thread_dump.txt     # 生成线程转储文件
jstack -l [pid]                    # 包含锁信息的详细转储
jstack -F [pid]                    # 强制生成转储（当进程无响应时）

# 线程状态过滤
# 查找阻塞线程
grep -A 10 "BLOCKED" thread_dump.txt

# 查找等待线程
grep -A 10 "WAITING" thread_dump.txt

# 查找运行中线程
grep -A 10 "RUNNABLE" thread_dump.txt

# 死锁检测
jstack [pid] | grep -A 20 "Found one Java-level deadlock"

# 线程CPU使用率分析脚本
#!/bin/bash
PID=$1

# 获取最忙的线程
TOP_THREADS=$(top -H -p $PID -b -n 1 | head -20 | tail -15)
echo "最忙的线程:"
echo "$TOP_THREADS"

# 转换线程ID为十六进制
BUSY_THREAD_ID=$(echo "$TOP_THREADS" | head -1 | awk '{print $1}')
BUSY_THREAD_HEX=$(printf "%x\n" $BUSY_THREAD_ID)
echo "线程ID: $BUSY_THREAD_ID (十六进制: $BUSY_THREAD_HEX)"

# 在线程转储中查找对应线程
jstack $PID | grep -A 15 "nid=0x$BUSY_THREAD_HEX"
```

### 3. JMAP - 内存映像工具

```bash
# 堆内存概览
jmap -heap [pid]              # 显示堆内存使用情况
jmap -histo [pid]             # 显示对象直方图
jmap -histo:live [pid]        # 仅显示存活对象（会触发Full GC）

# 堆转储生成
jmap -dump:format=b,file=heap.hprof [pid]  # 生成二进制堆转储文件
jmap -dump:format=b,live,file=heap_live.hprof [pid]  # 仅转储存活对象

# PermGen/Metaspace分析（Java 8+）
jmap -permstat [pid]          # 显示永久代统计信息

# 内存泄漏检测脚本
#!/bin/bash
PID=$1
APP_NAME=$2

echo "=== 内存泄漏检测开始 ==="
echo "进程ID: $PID"
echo "应用名称: $APP_NAME"

# 1. 对象直方图分析
echo "=== 对象直方图分析 ==="
OBJECT_HISTO=$(jmap -histo:live $PID | head -20)
echo "$OBJECT_HISTO"

# 2. 检查大对象
echo "=== 大对象检测 ==="
jmap -histo:live $PID | awk '$3 > 1000000 {print $0}'  # 大于1MB的对象

# 3. 生成堆转储
HEAP_FILE="/tmp/${APP_NAME}_heap_$(date +%Y%m%d_%H%M%S).hprof"
echo "生成堆转储文件: $HEAP_FILE"
jmap -dump:format=b,live,file=$HEAP_FILE $PID

echo "=== 内存分析完成 ==="
echo "请使用MAT工具分析: $HEAP_FILE"
```

## 🔍 综合诊断实战

### 场景1：CPU使用率过高问题

```bash
#!/bin/bash
# CPU高使用率三剑客诊断脚本

PID=$1
echo "=== CPU高使用率诊断 ==="
echo "目标进程: $PID"

# 1. 使用JPS确认进程状态
echo "1. 进程确认:"
jps | grep $PID

# 2. 使用TOP找到最忙线程
echo "2. 最忙线程识别:"
BUSY_THREAD_ID=$(top -H -p $PID -b -n 1 | head -8 | tail -1 | awk '{print $1}')
BUSY_THREAD_HEX=$(printf "%x\n" $BUSY_THREAD_ID)
echo "最忙线程ID: $BUSY_THREAD_ID (十六进制: $BUSY_THREAD_HEX)"

# 3. 使用JSTACK分析线程堆栈
echo "3. 线程堆栈分析:"
jstack $PID | grep -A 15 "nid=0x$BUSY_THREAD_HEX"

# 4. 生成线程转储供进一步分析
jstack $PID > /tmp/thread_dump_${PID}_$(date +%Y%m%d_%H%M%S).txt
echo "线程转储已保存"

# 5. 检查内存使用情况
echo "4. 内存使用情况:"
jmap -heap $PID
```

### 场景2：内存不足和OOM问题

```bash
#!/bin/bash
# 内存问题三剑客诊断脚本

PID=$1
APP_NAME=$2

echo "=== 内存问题诊断 ==="

# 1. 堆内存使用情况
echo "1. 堆内存分析:"
jmap -heap $PID

# 2. 对象直方图
echo "2. 对象分布:"
jmap -histo:live $PID | head -20

# 3. 检查是否有内存泄漏迹象
echo "3. 潜在内存泄漏对象:"
jmap -histo:live $PID | awk '$3 > 10000000 {print $0}'  # 超过10MB的对象

# 4. 生成堆转储文件
HEAP_FILE="/tmp/${APP_NAME}_oom_analysis_$(date +%Y%m%d_%H%M%S).hprof"
echo "4. 生成堆转储: $HEAP_FILE"
jmap -dump:format=b,live,file=$HEAP_FILE $PID

# 5. 检查GC统计
echo "5. GC统计信息:"
jstat -gc $PID 1s 5

echo "诊断完成，请使用MAT分析堆转储文件"
```

### 场景3：死锁和线程阻塞问题

```bash
#!/bin/bash
# 死锁检测三剑客脚本

PID=$1

echo "=== 死锁和线程阻塞检测 ==="

# 1. 死锁检测
echo "1. 死锁检查:"
DEADLOCK_INFO=$(jstack $PID | grep -A 20 "Found one Java-level deadlock")
if [ -n "$DEADLOCK_INFO" ]; then
    echo "发现死锁:"
    echo "$DEADLOCK_INFO"
else
    echo "未发现死锁"
fi

# 2. 阻塞线程分析
echo "2. 阻塞线程分析:"
BLOCKED_THREADS=$(jstack $PID | grep -c "BLOCKED")
echo "阻塞线程数: $BLOCKED_THREADS"

if [ $BLOCKED_THREADS -gt 0 ]; then
    echo "阻塞线程详情:"
    jstack $PID | grep -A 10 "BLOCKED"
fi

# 3. 等待线程分析
echo "3. 等待线程分析:"
WAITING_THREADS=$(jstack $PID | grep -c "WAITING")
echo "等待线程数: $WAITING_THREADS"

# 4. 生成完整线程转储
THREAD_DUMP_FILE="/tmp/thread_analysis_$(date +%Y%m%d_%H%M%S).txt"
jstack -l $PID > $THREAD_DUMP_FILE
echo "完整线程转储已保存: $THREAD_DUMP_FILE"
```

## 📊 性能监控最佳实践

### JVM监控配置模板
```bash
# 生产环境JVM参数配置
JAVA_OPTS="
-server
-Xms4g -Xmx4g                   # 堆内存大小
-XX:NewRatio=2                  # 老年代与新生代比例
-XX:SurvivorRatio=8             # Eden与Survivor比例

# GC配置
-XX:+UseG1GC                    # 使用G1垃圾收集器
-XX:MaxGCPauseMillis=200        # 最大GC暂停时间
-XX:G1HeapRegionSize=16m        # G1区域大小

# 监控和诊断配置
-XX:+PrintGC                    # 打印GC信息
-XX:+PrintGCDetails             # 打印GC详细信息
-XX:+PrintGCTimeStamps          # 打印GC时间戳
-Xloggc:/app/logs/gc.log        # GC日志文件
-XX:+HeapDumpOnOutOfMemoryError # OOM时生成堆转储
-XX:HeapDumpPath=/app/dumps/    # 堆转储文件路径
-XX:+PrintClassHistogram        # Ctrl+Break时打印类直方图
"

# 应用健康检查脚本
#!/bin/bash
APP_NAME="myapp"
PID=$(pgrep -f $APP_NAME)

if [ -z "$PID" ]; then
    echo "应用未运行"
    exit 1
fi

echo "=== 应用健康检查报告 ==="
echo "检查时间: $(date)"
echo "进程ID: $PID"

# 内存使用情况
echo "=== 内存使用情况 ==="
jmap -heap $PID 2>/dev/null || echo "无法获取堆信息"

# 线程情况
echo "=== 线程统计 ==="
TOTAL_THREADS=$(jstack $PID 2>/dev/null | grep "java.lang.Thread.State" | wc -l)
RUNNABLE_THREADS=$(jstack $PID 2>/dev/null | grep "RUNNABLE" | wc -l)
BLOCKED_THREADS=$(jstack $PID 2>/dev/null | grep "BLOCKED" | wc -l)

echo "总线程数: $TOTAL_THREADS"
echo "运行中线程: $RUNNABLE_THREADS"
echo "阻塞线程: $BLOCKED_THREADS"

# GC统计
echo "=== GC统计 ==="
jstat -gc $PID 1s 1 2>/dev/null || echo "无法获取GC统计"
```

## 🧪 验证测试

### 工具可用性验证
```bash
#!/bin/bash
# JVM三剑客工具验证脚本

echo "=== JVM三剑客工具验证 ==="

# 检查Java环境
java -version >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Java环境正常"
    JAVA_VERSION=$(java -version 2>&1 | head -1)
    echo "Java版本: $JAVA_VERSION"
else
    echo "❌ Java环境异常"
    exit 1
fi

# 检查三剑客工具
TOOLS=("jps" "jstack" "jmap" "jstat" "jinfo")
for tool in "${TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool 工具可用"
        VERSION=$($tool -version 2>&1 | head -1)
        echo "   版本信息: $VERSION"
    else
        echo "❌ $tool 工具不可用"
    fi
done

# 检查当前Java进程
echo "=== 当前Java进程 ==="
jps -l
CURRENT_JAVA_PROCESSES=$(jps | wc -l)
echo "当前Java进程数: $CURRENT_JAVA_PROCESSES"

if [ $CURRENT_JAVA_PROCESSES -gt 1 ]; then
    echo "✅ 可进行三剑客测试"
else
    echo "⚠️  无Java进程可供测试"
fi
```

## ❓ 常见问题处理

### Q1: jstack无法连接到目标进程？
**解决方案**：
```bash
# 检查权限
sudo jstack [pid]

# 检查进程状态
kill -0 [pid]  # 验证进程是否存在

# 使用强制模式
jstack -F [pid]

# 检查JVM版本兼容性
java -version
jstack -version
```

### Q2: jmap生成堆转储很慢怎么办？
**优化建议**：
```bash
# 只转储存活对象
jmap -dump:format=b,live,file=heap.hprof [pid]

# 在低峰期执行
# 或使用采样方式
jmap -histo:live [pid]  # 先查看对象分布

# 增加堆大小临时缓解
export JAVA_OPTS="-Xmx8g"  # 临时增加内存
```

### Q3: 如何分析线程转储中的死锁？
**分析步骤**：
1. 使用`jstack -l [pid]`生成带锁信息的线程转储
2. 查找"Found one Java-level deadlock"关键字
3. 分析涉及的线程和锁资源
4. 检查代码中的同步块和锁使用
5. 设计避免死锁的解决方案

## 📚 扩展学习

### 专业分析工具
- **Eclipse MAT**: 内存分析和泄漏检测
- **JProfiler**: 商业级性能分析工具
- **YourKit**: 功能全面的Java Profiler
- **VisualVM**: JDK自带的图形化分析工具

### 学习进阶路径
1. 深入理解JVM内存模型和GC机制
2. 掌握各种垃圾收集器的特点和调优
3. 学习分布式系统性能分析方法
4. 掌握微服务架构下的诊断技术
5. 学习APM工具和全链路追踪

### 认证考试推荐
- Oracle Certified Professional: Java Programmer
- JVM性能调优专家认证
- 企业级应用架构师认证

---
> **💡 提示**: 使用三剑客进行生产环境诊断时，建议在业务低峰期操作，避免对线上服务造成影响。同时要做好数据备份和回滚准备。