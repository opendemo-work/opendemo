# Linux进程线程深度排查与OOM分析实战演示

## 🎯 学习目标

通过本案例你将掌握Linux系统进程和线程的深度排查技能：

- 进程状态分析和资源监控
- 线程级性能分析和死锁检测
- OOM Killer机制理解和预防
- 内存泄漏检测和分析
- 系统级性能瓶颈定位
- 生产环境进程管理最佳实践

## 🛠️ 环境准备

### 系统要求
- Linux发行版（推荐CentOS 7+/Ubuntu 18.04+）
- root权限或sudo权限
- 系统管理员经验
- 进程管理基础知识

### 依赖安装
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装系统监控工具
sudo yum install -y sysstat procps-ng htop strace lsof
sudo apt-get install -y sysstat procps htop strace lsof

# 安装高级分析工具
sudo yum install -y perf valgrind systemtap
sudo apt-get install -y linux-perf valgrind systemtap

# 验证工具安装
which ps top htop strace lsof perf valgrind
```

## 📁 项目结构

```
linux-process-thread-debugging-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 排查脚本
│   ├── process_analyzer.sh            # 进程分析脚本
│   ├── thread_inspector.sh            # 线程检查脚本
│   ├── oom_predictor.sh               # OOM预测脚本
│   ├── memory_leak_detector.sh        # 内存泄漏检测脚本
│   ├── deadlock_finder.sh             # 死锁检测脚本
│   └── system_health_monitor.sh       # 系统健康监控脚本
├── configs/                           # 配置文件
│   ├── oom_killer_config.conf         # OOM Killer配置
│   ├── process_limits.conf            # 进程限制配置
│   └── monitoring_thresholds.conf     # 监控阈值配置
├── examples/                          # 实际案例
│   ├── process_state_samples/         # 进程状态样本
│   ├── thread_analysis_reports/       # 线程分析报告
│   ├── oom_incidents/                 # OOM事件记录
│   └── troubleshooting_playbooks/     # 故障排查手册
└── docs/                              # 详细文档
    ├── process_debugging_guide.md     # 进程调试指南
    ├── thread_analysis_manual.md      # 线程分析手册
    ├── oom_handling_strategies.md     # OOM处理策略
    └── system_performance_tuning.md   # 系统性能调优
```

## 🔧 核心排查技术详解

### 1. 进程状态深度分析

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 进程状态详解
ps aux --sort=-%cpu | head -20    # 按CPU使用率排序
ps aux --sort=-%mem | head -20    # 按内存使用率排序
ps -eo pid,ppid,cmd,%cpu,%mem,stime,etime,args  # 详细进程信息

# 进程树分析
pstree -p                     # 显示进程树和PID
pstree -a                     # 显示命令行参数
pstree -u                     # 显示用户信息

# 实时进程监控
watch -n 1 'ps aux --sort=-%cpu | head -15'

# 进程详细信息查看
cat /proc/[PID]/status        # 进程状态信息
cat /proc/[PID]/stat          # 进程统计信息
cat /proc/[PID]/sched         # 调度信息
ls -la /proc/[PID]/fd/        # 文件描述符列表
```

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 进程深度分析脚本

PID=$1

if [ -z "$PID" ]; then
    echo "用法: $0 <PID>"
    exit 1
fi

echo "=== 进程 $PID 详细分析 ==="
echo "分析时间: $(date)"
echo ""

# 1. 基本进程信息
echo "1. 基本信息:"
ps -p $PID -o pid,ppid,user,%cpu,%mem,vsz,rss,etime,nice,stat,wchan,comm

# 2. 详细状态信息
echo -e "\n2. 详细状态:"
if [ -f "/proc/$PID/status" ]; then
    cat /proc/$PID/status | grep -E "Name|State|Vm|Threads|Sig"
fi

# 3. 内存映射
echo -e "\n3. 内存映射:"
if [ -f "/proc/$PID/smaps" ]; then
    echo "内存区域统计:"
    awk '/^Size:/ {size+=$2} /^Rss:/ {rss+=$2} /^Pss:/ {pss+=$2} END {printf "Total Size: %d KB\nRSS: %d KB\nPSS: %d KB\n", size, rss, pss}' /proc/$PID/smaps
    
    echo -e "\n主要内存区域:"
    grep -A 5 -B 1 "Size:" /proc/$PID/smaps | head -20
fi

# 4. 文件描述符
echo -e "\n4. 文件描述符:"
FD_COUNT=$(ls /proc/$PID/fd/ 2>/dev/null | wc -l)
echo "文件描述符数量: $FD_COUNT"

if [ $FD_COUNT -gt 0 ]; then
    echo "文件描述符详情:"
    ls -la /proc/$PID/fd/ | head -10
fi

# 5. 网络连接
echo -e "\n5. 网络连接:"
netstat -tulnp | grep $PID 2>/dev/null || ss -tulnp | grep $PID 2>/dev/null

# 6. 线程信息
echo -e "\n6. 线程信息:"
ps -T -p $PID -o pid,tid,ppid,time,%cpu,stat,comm

# 7. 调度信息
echo -e "\n7. 调度信息:"
if [ -f "/proc/$PID/sched" ]; then
    cat /proc/$PID/sched | head -10
fi

# 8. 环境变量
echo -e "\n8. 环境变量:"
if [ -f "/proc/$PID/environ" ]; then
    tr '\0' '\n' < /proc/$PID/environ | head -10
fi
```

### 2. 线程级分析和死锁检测

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 线程查看和分析
ps -T -p [PID]                # 查看进程的所有线程
ps -eLf                       # 查看所有线程的详细信息
top -H -p [PID]               # 以线程模式查看特定进程

# 线程堆栈分析
# 使用gdb附加到进程
gdb -p [PID] -batch -ex "thread apply all bt" -ex "quit"

# 使用strace跟踪系统调用
strace -p [PID] -T -tt -f    # 跟踪所有线程的系统调用

# 线程状态分析
cat /proc/[PID]/task/*/stat  # 查看所有线程状态
```

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 线程死锁检测脚本

PID=$1
THRESHOLD=${2:-300}  # 线程阻塞时间阈值(秒)

echo "=== 线程死锁检测 ==="
echo "进程ID: $PID"
echo "阻塞阈值: ${THRESHOLD}秒"

# 1. 获取所有线程信息
echo "1. 线程状态概览:"
ps -T -p $PID -o pid,tid,time,%cpu,stat,wchan,comm --no-headers

# 2. 分析线程等待状态
echo -e "\n2. 等待状态分析:"
BLOCKED_THREADS=$(ps -T -p $PID -o stat= | grep -c "D\|S\+")
TOTAL_THREADS=$(ps -T -p $PID -o tid= | wc -l)
echo "阻塞线程数: $BLOCKED_THREADS/$TOTAL_THREADS"

# 3. 检查系统调用阻塞
echo -e "\n3. 系统调用分析:"
timeout 10 strace -p $PID -c 2>&1 | tail -10

# 4. 详细线程堆栈分析
echo -e "\n4. 线程堆栈分析:"
if command -v gdb &> /dev/null; then
    gdb -p $PID -batch \
        -ex "set pagination off" \
        -ex "info threads" \
        -ex "thread apply all bt" \
        -ex "quit" 2>/dev/null | head -50
fi

# 5. 检查常见的死锁模式
echo -e "\n5. 死锁模式检查:"

# 检查是否在等待锁
LOCK_WAITING=$(ps -T -p $PID -o wchan= | grep -c "futex_wait")
if [ $LOCK_WAITING -gt 0 ]; then
    echo "⚠️  发现线程在等待futex锁"
fi

# 检查是否在I/O等待
IO_WAITING=$(ps -T -p $PID -o stat= | grep -c "D")
if [ $IO_WAITING -gt 0 ]; then
    echo "⚠️  发现线程在不可中断睡眠(D状态)"
fi

# 6. 生成分析报告
REPORT_FILE="/tmp/thread_analysis_$(date +%Y%m%d_%H%M%S).txt"
cat > $REPORT_FILE << EOF
线程分析报告
============
进程ID: $PID
分析时间: $(date)
总线程数: $TOTAL_THREADS
阻塞线程数: $BLOCKED_THREADS

详细分析请查看上面的输出。
EOF

echo "分析报告已保存: $REPORT_FILE"
```

### 3. OOM Killer机制和预防

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# OOM相关信息查看
cat /proc/meminfo              # 内存信息
cat /proc/sys/vm/oom_kill_allocating_task  # OOM killer配置
cat /proc/sys/vm/overcommit_memory         # 内存超分配置

# 查看OOM killer日志
dmesg | grep -i "killed process" | tail -10
journalctl | grep -i "oom\|killed" | tail -10

# 进程OOM评分查看
for pid in $(pgrep -f .); do
    if [ -f "/proc/$pid/oom_score" ]; then
        score=$(cat /proc/$pid/oom_score)
        name=$(cat /proc/$pid/comm)
        echo "PID: $pid, Score: $score, Name: $name"
    fi
done | sort -rnk 3 | head -10
```

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# OOM预测和预防脚本

echo "=== OOM风险评估 ==="
echo "检查时间: $(date)"
echo ""

# 1. 系统内存使用情况
echo "1. 内存使用概览:"
free -h
echo ""

# 2. 详细内存统计
echo "2. 详细内存统计:"
awk '/^MemTotal:|^MemFree:|^MemAvailable:|^Buffers:|^Cached:/ {printf "%-15s %10.2f GB\n", $1, $2/1024/1024}' /proc/meminfo
echo ""

# 3. 计算内存使用率
MEM_TOTAL=$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)
MEM_AVAILABLE=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
MEM_USAGE_PERCENT=$(awk "BEGIN {printf \"%.2f\", (1-$MEM_AVAILABLE/$MEM_TOTAL)*100}")

echo "内存使用率: ${MEM_USAGE_PERCENT}%"

# 4. OOM风险评估
if (( $(echo "$MEM_USAGE_PERCENT > 90" | bc -l) )); then
    echo "⚠️  高风险: 内存使用率超过90%"
    RISK_LEVEL="HIGH"
elif (( $(echo "$MEM_USAGE_PERCENT > 80" | bc -l) )); then
    echo "⚠️  中等风险: 内存使用率超过80%"
    RISK_LEVEL="MEDIUM"
else
    echo "✅ 内存使用正常"
    RISK_LEVEL="LOW"
fi
echo ""

# 5. 查看高内存使用进程
echo "5. 高内存使用进程:"
ps aux --sort=-%mem | head -10 | awk 'NR==1 || $4>1.0'
echo ""

# 6. 检查内存泄漏迹象
echo "6. 内存泄漏检查:"
# 检查是否有进程内存持续增长
for pid in $(pgrep -f . | head -5); do
    if [ -d "/proc/$pid" ]; then
        rss=$(awk '/VmRSS:/ {print $2}' /proc/$pid/status 2>/dev/null)
        name=$(cat /proc/$pid/comm 2>/dev/null)
        if [ -n "$rss" ] && [ -n "$name" ]; then
            echo "PID: $pid, 进程: $name, RSS: ${rss}KB"
        fi
    fi
done
echo ""

# 7. Swap使用情况
echo "7. Swap使用情况:"
SWAP_TOTAL=$(awk '/^SwapTotal:/ {print $2}' /proc/meminfo)
SWAP_FREE=$(awk '/^SwapFree:/ {print $2}' /proc/meminfo)

if [ "$SWAP_TOTAL" != "0" ]; then
    SWAP_USAGE=$(awk "BEGIN {printf \"%.2f\", (1-$SWAP_FREE/$SWAP_TOTAL)*100}")
    echo "Swap使用率: ${SWAP_USAGE}%"
    
    if (( $(echo "$SWAP_USAGE > 50" | bc -l) )); then
        echo "⚠️  Swap使用率较高，可能影响性能"
    fi
else
    echo "未配置Swap空间"
fi
echo ""

# 8. OOM Killer配置检查
echo "8. OOM Killer配置:"
echo "OOM kill allocating task: $(cat /proc/sys/vm/oom_kill_allocating_task)"
echo "Overcommit memory: $(cat /proc/sys/vm/overcommit_memory)"
echo "Overcommit ratio: $(cat /proc/sys/vm/overcommit_ratio)"
echo ""

# 9. 生成预防建议
echo "9. 预防建议:"
case $RISK_LEVEL in
    "HIGH")
        echo "- 立即清理不必要的进程"
        echo "- 考虑增加物理内存"
        echo "- 调整进程内存限制"
        echo "- 启用内存监控告警"
        ;;
    "MEDIUM")
        echo "- 监控内存使用趋势"
        echo "- 优化应用程序内存使用"
        echo "- 考虑调整OOM优先级"
        ;;
    "LOW")
        echo "- 继续监控内存使用"
        echo "- 定期检查内存泄漏"
        ;;
esac

# 10. 保存报告
REPORT_FILE="/tmp/oom_assessment_$(date +%Y%m%d_%H%M%S).txt"
cat > $REPORT_FILE << EOF
OOM风险评估报告
===============
检查时间: $(date)
内存使用率: ${MEM_USAGE_PERCENT}%
风险等级: $RISK_LEVEL

详细信息请查看上述输出。

建议措施:
$(case $RISK_LEVEL in
    "HIGH") echo "- 立即清理不必要的进程"
            echo "- 考虑增加物理内存"
            echo "- 调整进程内存限制"
            echo "- 启用内存监控告警" ;;
    "MEDIUM") echo "- 监控内存使用趋势"
              echo "- 优化应用程序内存使用"
              echo "- 考虑调整OOM优先级" ;;
    "LOW") echo "- 继续监控内存使用"
           echo "- 定期检查内存泄漏" ;;
esac)
EOF

echo ""
echo "完整报告已保存: $REPORT_FILE"
```

### 4. 内存泄漏检测技术

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 使用valgrind检测内存泄漏
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all ./your_program

# 使用pmap分析进程内存映射
pmap -x [PID]                 # 详细内存映射
pmap -d [PID]                 # 设备映射信息

# 实时内存监控
watch -n 1 'cat /proc/[PID]/status | grep Vm'

# 内存增长趋势分析
for i in {1..10}; do
    timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    rss=$(awk '/VmRSS:/ {print $2}' /proc/[PID]/status)
    echo "$timestamp RSS: ${rss}KB"
    sleep 5
done
```

## 🔍 综合诊断实战

### 场景1：进程CPU使用异常

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# CPU异常进程诊断脚本

THRESHOLD=${1:-80}  # CPU使用率阈值

echo "=== CPU异常进程诊断 ==="
echo "阈值: ${THRESHOLD}%"
echo "检查时间: $(date)"
echo ""

# 1. 查找高CPU使用进程
echo "1. 高CPU使用进程:"
HIGH_CPU_PROCESSES=$(ps aux --sort=-%cpu | awk -v threshold="$THRESHOLD" '$3 > threshold {print $0}')
echo "$HIGH_CPU_PROCESSES"
echo ""

# 2. 分析每个高CPU进程
echo "2. 详细进程分析:"
echo "$HIGH_CPU_PROCESSES" | while read line; do
    PID=$(echo $line | awk '{print $2}')
    CPU=$(echo $line | awk '{print $3}')
    COMMAND=$(echo $line | awk '{for(i=11;i<=NF;i++) printf "%s ", $i; print ""}')
    
    echo "--- 进程 PID: $PID (CPU: ${CPU}%) ---"
    echo "命令: $COMMAND"
    
    # 进程详细信息
    if [ -d "/proc/$PID" ]; then
        # 线程分析
        THREAD_COUNT=$(ps -T -p $PID --no-headers | wc -l)
        echo "线程数: $THREAD_COUNT"
        
        # 内存使用
        MEM_RSS=$(awk '/VmRSS:/ {print $2}' /proc/$PID/status 2>/dev/null)
        echo "内存使用: ${MEM_RSS}KB"
        
        # 打开文件数
        FD_COUNT=$(ls /proc/$PID/fd/ 2>/dev/null | wc -l)
        echo "文件描述符: $FD_COUNT"
        
        # 系统调用跟踪（简短）
        echo "最近系统调用:"
        timeout 2 strace -p $PID -c 2>&1 | tail -5
    fi
    echo ""
done

# 3. 系统级CPU分析
echo "3. 系统CPU使用:"
top -b -n 1 | head -5

# 4. CPU负载分析
echo "4. CPU负载信息:"
uptime
cat /proc/loadavg

# 5. 生成告警
HIGH_COUNT=$(echo "$HIGH_CPU_PROCESSES" | wc -l)
if [ $HIGH_COUNT -gt 0 ]; then
    echo "⚠️  发现 $HIGH_COUNT 个高CPU使用进程"
    
    # 发送告警（示例）
    # echo "High CPU usage detected: $HIGH_COUNT processes above ${THRESHOLD}%" | mail -s "CPU Alert" admin@example.com
else
    echo "✅ CPU使用正常"
fi
```

### 场景2：内存泄漏深入分析

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 内存泄漏深度分析脚本

PID=$1
DURATION=${2:-300}  # 监控持续时间(秒)
INTERVAL=${3:-30}   # 检查间隔(秒)

echo "=== 内存泄漏深度分析 ==="
echo "进程ID: $PID"
echo "监控时长: ${DURATION}秒"
echo "检查间隔: ${INTERVAL}秒"
echo ""

if [ ! -d "/proc/$PID" ]; then
    echo "❌ 进程 $PID 不存在"
    exit 1
fi

PROCESS_NAME=$(cat /proc/$PID/comm)
echo "进程名称: $PROCESS_NAME"
echo ""

# 1. 基准内存使用
BASELINE_RSS=$(awk '/VmRSS:/ {print $2}' /proc/$PID/status)
BASELINE_VSZ=$(awk '/VmSize:/ {print $2}' /proc/$PID/status)
echo "基准内存使用:"
echo "  RSS: ${BASELINE_RSS}KB ($(echo "scale=2; $BASELINE_RSS/1024" | bc)MB)"
echo "  VSZ: ${BASELINE_VSZ}KB ($(echo "scale=2; $BASELINE_VSZ/1024" | bc)MB)"
echo ""

# 2. 持续监控内存增长
echo "开始监控内存变化..."
CHECKS=$((DURATION/INTERVAL))
LEAK_DETECTED=false

for i in $(seq 1 $CHECKS); do
    if [ ! -d "/proc/$PID" ]; then
        echo "⚠️  进程已终止"
        break
    fi
    
    CURRENT_RSS=$(awk '/VmRSS:/ {print $2}' /proc/$PID/status)
    CURRENT_VSZ=$(awk '/VmSize:/ {print $2}' /proc/$PID/status)
    
    RSS_GROWTH=$((CURRENT_RSS - BASELINE_RSS))
    VSZ_GROWTH=$((CURRENT_VSZ - BASELINE_VSZ))
    
    TIMESTAMP=$(date "+%H:%M:%S")
    echo "${TIMESTAMP} - RSS: ${CURRENT_RSS}KB (+${RSS_GROWTH}KB), VSZ: ${CURRENT_VSZ}KB (+${VSZ_GROWTH}KB)"
    
    # 判断是否内存泄漏
    if [ $RSS_GROWTH -gt 102400 ]; then  # 增长超过100MB
        echo "⚠️  可能存在内存泄漏 (RSS增长: $((RSS_GROWTH/1024))MB)"
        LEAK_DETECTED=true
        
        # 详细分析
        echo "执行详细内存分析..."
        
        # 内存映射分析
        echo "内存映射变化:"
        pmap -x $PID | tail -10
        
        # 进程状态分析
        echo "进程状态:"
        cat /proc/$PID/status | grep -E "Vm|Threads|Rss"
        
        break
    fi
    
    sleep $INTERVAL
done

# 3. 最终分析
echo ""
echo "=== 最终分析结果 ==="
FINAL_RSS=$(awk '/VmRSS:/ {print $2}' /proc/$PID/status 2>/dev/null)
if [ -n "$FINAL_RSS" ]; then
    FINAL_GROWTH=$((FINAL_RSS - BASELINE_RSS))
    echo "总内存增长: $((FINAL_GROWTH/1024))MB"
    
    if [ "$LEAK_DETECTED" = true ] || [ $FINAL_GROWTH -gt 51200 ]; then
        echo "⚠️  存在内存泄漏风险"
        
        # 生成内存分析报告
        REPORT_FILE="/tmp/memory_leak_analysis_$(date +%Y%m%d_%H%M%S).txt"
        cat > $REPORT_FILE << EOF
内存泄漏分析报告
================
进程ID: $PID
进程名称: $PROCESS_NAME
分析时间: $(date)
基准RSS: ${BASELINE_RSS}KB
最终RSS: ${FINAL_RSS}KB
总增长: $((FINAL_GROWTH/1024))MB

详细内存映射:
$(pmap -x $PID 2>/dev/null | tail -15)

建议措施:
1. 使用valgrind进行详细内存检查
2. 检查程序中的内存分配和释放
3. 考虑重启进程释放内存
EOF
        echo "详细报告已生成: $REPORT_FILE"
    else
        echo "✅ 内存使用相对稳定"
    fi
else
    echo "❌ 无法获取进程信息（可能已终止）"
fi
```

### 场景3：系统级性能瓶颈分析

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 系统级性能瓶颈分析脚本

echo "=== 系统级性能瓶颈分析 ==="
echo "分析时间: $(date)"
echo ""

# 1. CPU瓶颈分析
echo "1. CPU瓶颈分析:"
echo "CPU使用率:"
top -b -n 1 | grep "Cpu(s)" | head -1

echo "CPU负载:"
uptime
cat /proc/loadavg

echo "进程CPU使用排行:"
ps aux --sort=-%cpu | head -10 | awk 'NR==1 || $3>1.0'

# 2. 内存瓶颈分析
echo -e "\n2. 内存瓶颈分析:"
echo "内存使用情况:"
free -h

echo "内存使用排行:"
ps aux --sort=-%mem | head -10 | awk 'NR==1 || $4>1.0'

echo "Swap使用情况:"
swapon --show

# 3. I/O瓶颈分析
echo -e "\n3. I/O瓶颈分析:"
echo "磁盘使用情况:"
df -h | head -10

echo "I/O统计:"
iostat -x 1 3 | grep -A 10 "^Device"

echo "高I/O进程:"
iotop -b -n 1 2>/dev/null | head -10 || echo "iotop未安装"

# 4. 网络瓶颈分析
echo -e "\n4. 网络瓶颈分析:"
echo "网络连接统计:"
ss -s

echo "网络接口状态:"
ip -s link show | grep -A 5 "RX\|TX"

echo "高网络使用进程:"
netstat -tulnp | head -10

# 5. 进程和线程瓶颈
echo -e "\n5. 进程和线程瓶颈:"
echo "总进程数: $(ps aux | wc -l)"
echo "总线程数: $(ps -eLf | wc -l)"

echo "僵尸进程:"
ps aux | awk '$8=="Z" {print $0}' | wc -l

echo "不可中断睡眠进程:"
ps aux | awk '$8=="D" {print $0}' | wc -l

# 6. 系统资源限制
echo -e "\n6. 系统资源限制:"
echo "文件描述符限制:"
ulimit -n

echo "进程数限制:"
ulimit -u

echo "内存锁定限制:"
ulimit -l

# 7. 内核参数检查
echo -e "\n7. 关键内核参数:"
echo "OOM Killer开关:"
cat /proc/sys/vm/oom-kill

echo "内存超分设置:"
cat /proc/sys/vm/overcommit_memory

echo "脏页刷新设置:"
cat /proc/sys/vm/dirty_ratio

# 8. 生成综合报告
REPORT_FILE="/tmp/system_bottleneck_analysis_$(date +%Y%m%d_%H%M%S).txt"
cat > $REPORT_FILE << EOF
系统性能瓶颈分析报告
=====================
分析时间: $(date)

主要发现:
$(echo "CPU负载: $(uptime | awk -F'load average:' '{print $2}')")
$(echo "内存使用: $(free -h | awk 'NR==2{printf "%.1f%%", $3*100/$2}')")
$(echo "Swap使用: $(free -h | awk 'NR==3{if($2>0) printf "%.1f%%", $3*100/$2; else print "N/A"}')")

建议优化方向:
1. 根据CPU使用情况调整进程调度
2. 优化内存使用，减少Swap依赖
3. 检查I/O密集型操作
4. 监控网络流量和连接数
5. 调整系统资源限制参数
EOF

echo -e "\n完整分析报告已保存: $REPORT_FILE"
echo "✅ 系统性能分析完成"
```

## 📊 监控和告警配置

### 自动化监控脚本
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# 系统健康监控守护脚本

CONFIG_FILE="/etc/system_monitor.conf"
LOG_FILE="/var/log/system_monitor.log"

# 默认配置
CPU_THRESHOLD=80
MEM_THRESHOLD=85
DISK_THRESHOLD=90
CHECK_INTERVAL=60

# 加载配置文件
if [ -f "$CONFIG_FILE" ]; then
    source $CONFIG_FILE
fi

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

check_cpu() {
    CPU_USAGE=$(top -b -n 1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 | cut -d'.' -f1)
    if [ $CPU_USAGE -gt $CPU_THRESHOLD ]; then
        log "WARN: CPU使用率过高 ${CPU_USAGE}%"
        # 发送告警
        echo "High CPU usage: ${CPU_USAGE}%" | mail -s "CPU Alert" admin@example.com
    fi
}

check_memory() {
    MEM_USAGE=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [ $MEM_USAGE -gt $MEM_THRESHOLD ]; then
        log "WARN: 内存使用率过高 ${MEM_USAGE}%"
        # 检查是否有进程接近OOM
        ps aux --sort=-%mem | head -5 >> $LOG_FILE
    fi
}

check_disk() {
    DISK_USAGE=$(df -h | awk '$5 > 90 {print $5}' | head -1 | tr -d '%')
    if [ -n "$DISK_USAGE" ] && [ $DISK_USAGE -gt $DISK_THRESHOLD ]; then
        log "WARN: 磁盘使用率过高 ${DISK_USAGE}%"
    fi
}

# 主监控循环
while true; do
    check_cpu
    check_memory
    check_disk
    sleep $CHECK_INTERVAL
done
```

## 🧪 验证测试

### 工具可用性验证
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
#!/bin/bash
# Linux排查工具验证脚本

echo "=== Linux排查工具验证 ==="

# 检查基本工具
BASIC_TOOLS=("ps" "top" "htop" "free" "df" "iostat" "vmstat")
for tool in "${BASIC_TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool 可用"
    else
        echo "❌ $tool 不可用"
    fi
done

# 检查高级工具
ADVANCED_TOOLS=("strace" "lsof" "perf" "valgrind")
for tool in "${ADVANCED_TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool 可用"
        $tool --version 2>/dev/null | head -1
    else
        echo "⚠️  $tool 未安装"
    fi
done

# 检查系统信息访问权限
echo "=== 权限检查 ==="
if [ -r "/proc/meminfo" ]; then
    echo "✅ /proc/meminfo 可读"
else
    echo "❌ /proc/meminfo 无法访问"
fi

if [ -r "/proc/sys/vm" ]; then
    echo "✅ /proc/sys/vm 可读"
else
    echo "❌ /proc/sys/vm 无法访问"
fi

# 测试进程分析
echo "=== 测试进程分析 ==="
TEST_PID=$$
echo "测试进程PID: $TEST_PID"

# 基本信息
echo "进程基本信息:"
ps -p $TEST_PID -o pid,ppid,cmd,%cpu,%mem,stime,etime

# 详细状态
if [ -f "/proc/$TEST_PID/status" ]; then
    echo "进程状态信息:"
    cat /proc/$TEST_PID/status | head -10
fi

echo "✅ 工具验证完成"
```

## ❓ 常见问题处理

### Q1: 无法访问/proc目录下的文件？
**解决方案**：
🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 检查权限
ls -la /proc/
sudo chmod +r /proc/[PID]/*

# 检查SELinux/AppArmor
getenforce  # 检查SELinux状态
aa-status   # 检查AppArmor状态

# 临时禁用SELinux测试
sudo setenforce 0
```

### Q2: strace跟踪进程影响性能？
**解决方案**：
🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 使用采样方式
timeout 10 strace -p [PID] -c  # 只统计，不输出详细信息

# 降低跟踪频率
strace -p [PID] -T -tt -e trace=!poll,select,epoll_wait

# 使用perf替代部分功能
perf record -g -p [PID]
perf report
```

### Q3: OOM Killer频繁杀进程？
**解决方案**：
🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 调整OOM优先级
echo -1000 > /proc/[PID]/oom_score_adj  # 降低被杀概率

# 增加交换空间
sudo fallocate -l 2G /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 调整内核参数
echo 1 > /proc/sys/vm/overcommit_memory  # 允许内存超分
```

## 📚 扩展学习

### 专业工具推荐
- **SystemTap**: 系统级动态插桩工具
- **eBPF/bpftrace**: 现代内核跟踪工具
- **sysdig**: 系统调用级别的监控工具
- **PCP**: Performance Co-Pilot性能监控套件

### 学习进阶路径
1. 深入理解Linux进程调度机制
2. 掌握内存管理和虚拟内存原理
3. 学习系统调用和内核调试技术
4. 掌握性能调优方法论
5. 学习容器化环境下的资源管理

---
> **💡 提示**: Linux系统排查需要结合多种工具和方法，建议建立完整的监控体系，及时发现问题并预防严重故障。
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

### 环境要求

- Linux 或 macOS 系统
- 已安装相关命令工具

## 📖 核心概念

### 1. 基本概念

本节介绍该工具的基本工作原理与关键术语。

### 2. 常用场景

- 场景 1：日常监控与诊断
- 场景 2：故障排查
- 场景 3：性能分析

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际工具替换
command --help
```

### 实际场景

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际工具替换
command -a -b target
```
