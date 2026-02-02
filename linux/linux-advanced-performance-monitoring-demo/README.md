# Linux高级性能监控与分析详解演示

## 🎯 学习目标

通过本案例你将掌握Linux系统高级性能监控和分析技能：

- 系统级性能瓶颈深度分析
- CPU、内存、IO子系统的精细化监控
- 进程和线程级别的性能诊断
- 存储系统性能优化和调优
- 网络性能深度分析和优化
- 资源隔离和限制管理(cgroups)

## 🛠️ 环境准备

### 系统要求
- Linux发行版（推荐CentOS 7+/Ubuntu 18.04+）
- root权限或sudo权限
- 性能监控和调优经验基础
- 内核调试能力

### 依赖安装
```bash
# 基础性能工具
sudo yum install -y perf sysstat numactl stress-ng
sudo apt-get install -y linux-perf sysstat numactl stress-ng

# 高级分析工具
sudo yum install -y blktrace iotop iftop nethogs
sudo apt-get install -y blktrace iotop iftop nethogs

# 开发工具（用于perf分析）
sudo yum groupinstall -y "Development Tools"
sudo apt-get install -y build-essential

# 验证安装
perf --version
blktrace --version
numactl --hardware
```

## 📁 项目结构

```
linux-advanced-performance-monitoring-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 高级分析脚本
│   ├── cpu_performance_analyzer.sh    # CPU性能分析脚本
│   ├── memory_profiler.sh             # 内存分析脚本
│   ├── io_bottleneck_detector.sh      # IO瓶颈检测脚本
│   ├── network_performance_analyzer.sh # 网络性能分析脚本
│   ├── thread_monitor.sh              # 线程监控脚本
│   └── resource_limiter.sh            # 资源限制脚本
├── configs/                           # 配置文件
│   ├── perf_config.conf               # perf配置文件
│   ├── cgroups_config.conf            # cgroups配置
│   └── tuning_parameters.conf         # 调优参数配置
├── examples/                          # 分析示例
│   ├── cpu_flame_graph.svg            # CPU火焰图示例
│   ├── memory_profile_output.txt      # 内存分析输出
│   ├── io_trace_analysis.txt          # IO追踪分析
│   └── network_bandwidth_report.txt   # 网络带宽报告
└── docs/                              # 详细文档
    ├── performance_troubleshooting.md # 性能故障排查指南
    ├── system_tuning_guide.md         # 系统调优指南
    ├── resource_isolation.md          # 资源隔离技术
    └── benchmark_best_practices.md    # 基准测试最佳实践
```

## 🚀 核心监控技术详解

### 1. CPU性能深度分析

```bash
# CPU使用率详细分析
mpstat -P ALL 1 5                           # 每个CPU核心使用情况
sar -u ALL 1 5                              # 系统CPU统计
vmstat 1 5                                  # 虚拟内存和CPU统计

# 进程级CPU分析
top -H -p $(pgrep nginx)                    # 查看进程的所有线程
ps -T -p $(pgrep nginx)                     # 显示线程信息
htop                                        # 交互式进程查看

# CPU调度分析
cat /proc/sched_debug | grep -A 10 nginx    # 进程调度信息
perf sched record -a sleep 10               # 记录调度事件
perf sched latency                          # 分析调度延迟

# CPU热点分析
perf record -g -p $(pgrep mysqld)           # 记录函数调用图
perf report                                 # 生成火焰图
perf top                                    # 实时热点分析
```

### 2. 内存性能分析

```bash
# 内存使用详细分析
free -w                                     # 详细内存使用情况
cat /proc/meminfo                           # 内存详细信息
vmstat 1 5                                  # 虚拟内存统计

# 内存分配分析
cat /proc/buddyinfo                         # 内存伙伴系统信息
cat /proc/zoneinfo                          # 内存区域信息
slabtop                                     # 内核slab分配器信息

# 内存压力测试
stress-ng --vm 4 --vm-bytes 1G --timeout 60s  # 内存压力测试
numastat                                    # NUMA内存统计

# 内存泄漏检测
valgrind --tool=memcheck ./application      # 内存泄漏检测
pmap -x $(pgrep application)                # 进程内存映射
```

### 3. IO性能深度监控

```bash
# 块设备IO分析
iostat -x 1 5                               # 详细IO统计
iotop                                       # 实时IO监控
blktrace -d /dev/sda -o trace.out           # 块层追踪
blkparse trace.out                          # 解析追踪数据

# 文件系统性能
df -i                                       # inode使用情况
du -sh /* 2>/dev/null | sort -hr | head -10 # 目录空间占用
lsof +L1                                    # 查找已删除但仍在使用的文件

# 存储性能测试
dd if=/dev/zero of=testfile bs=1M count=1000 # 磁盘写入测试
hdparm -Tt /dev/sda                         # 磁盘缓存和读取测试
fio --name=randread --ioengine=libaio --direct=1 --bs=4k --size=1g --readwrite=randread

# IO调度分析
cat /sys/block/sda/queue/scheduler          # 查看IO调度器
echo mq-deadline > /sys/block/sda/queue/scheduler  # 切换调度器
```

### 4. 网络性能深度分析

```bash
# 现代网络工具
ss -tulnp                                   # socket统计（netstat替代）
ip -s link show eth0                        # 网络接口统计
nethogs                                     # 按进程分组的网络流量
iftop -i eth0                               # 实时网络流量监控

# 网络性能测试
iperf3 -s                                   # 启动iperf服务端
iperf3 -c server_ip -t 30                   # 网络带宽测试
ping -c 10 google.com                       # 网络延迟测试
traceroute google.com                       # 路径追踪

# 网络连接分析
netstat -s                                  # 网络统计信息
cat /proc/net/dev                           # 网络设备统计
ss -i                                       # TCP连接信息

# 网络调优
sysctl net.core.rmem_max=16777216           # 调整接收缓冲区
sysctl net.core.wmem_max=16777216           # 调整发送缓冲区
ethtool -K eth0 gso off tso off             # 关闭网络卸载功能测试
```

### 5. 进程和线程监控

```bash
# 线程级监控
ps -T -p $(pgrep nginx)                     # 查看进程的所有线程
top -H                                      # 显示所有线程
htop -H                                     # 交互式线程查看

# 线程状态分析
cat /proc/$(pgrep nginx)/task/*/stat        # 线程状态信息
cat /proc/$(pgrep nginx)/task/*/sched       # 线程调度信息

# 线程性能分析
perf record -t $(pgrep -f "nginx: worker")  # 监控特定线程
strace -p $(pgrep nginx) -c                 # 系统调用统计

# 进程资源限制
ulimit -a                                   # 查看当前限制
cat /proc/$(pgrep nginx)/limits             # 进程资源限制
prlimit --pid=$(pgrep nginx)                # 查看/设置进程限制
```

### 6. 资源隔离和限制(cgroups)

```bash
# cgroups v1使用
sudo cgcreate -g cpu,memory:/mygroup        # 创建cgroup
sudo cgclassify -g cpu,memory:/mygroup $$   # 将当前进程加入cgroup
echo 50000 > /sys/fs/cgroup/cpu/mygroup/cpu.cfs_quota_us  # 限制CPU使用
echo 100M > /sys/fs/cgroup/memory/mygroup/memory.limit_in_bytes  # 限制内存

# cgroups v2使用
sudo mkdir /sys/fs/cgroup/mygroup
echo "+cpu +memory" > /sys/fs/cgroup/cgroup.subtree_control
echo $$ > /sys/fs/cgroup/mygroup/cgroup.procs

# 资源监控
cat /sys/fs/cgroup/mygroup/cpu.stat         # CPU使用统计
cat /sys/fs/cgroup/mygroup/memory.stat      # 内存使用统计

# systemd资源控制
systemctl set-property nginx.service CPUQuota=50%
systemctl set-property nginx.service MemoryMax=1G
systemctl show nginx.service | grep -i cpu
```

## 🔍 性能分析实战案例

### 案例1：CPU密集型应用性能优化
```bash
#!/bin/bash
# CPU性能瓶颈分析脚本

APP_PID=$(pgrep application)
echo "分析应用PID: $APP_PID"

# 收集基本信息
echo "=== CPU使用情况 ==="
top -b -n 1 -p $APP_PID | grep $APP_PID

echo "=== 进程线程信息 ==="
ps -T -p $APP_PID | head -10

echo "=== 性能剖析 ==="
perf record -g -p $APP_PID -o perf.data -- sleep 30
perf report -i perf.data --stdio

echo "=== 系统调用分析 ==="
strace -p $APP_PID -c -T 10
```

### 案例2：内存泄漏检测和分析
```bash
#!/bin/bash
# 内存泄漏分析脚本

APP_PID=$(pgrep application)
echo "监控应用PID: $APP_PID"

# 持续监控内存使用
while true; do
    RSS=$(ps -o pid,rss,vsz -p $APP_PID | awk 'NR==2 {print $2}')
    VSZ=$(ps -o pid,rss,vsz -p $APP_PID | awk 'NR==2 {print $3}')
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "$TIMESTAMP - RSS: ${RSS}KB, VSZ: ${VSZ}KB" >> memory_usage.log
    
    # 检查内存增长趋势
    if [ $((VSZ)) -gt 2000000 ]; then  # 超过2GB
        echo "警告: 内存使用过高 $VSZ KB"
        # 生成内存快照
        gcore $APP_PID
        break
    fi
    
    sleep 60
done
```

### 案例3：IO性能瓶颈定位
```bash
#!/bin/bash
# IO性能分析脚本

DEVICE=sda
echo "监控设备: $DEVICE"

# 实时IO监控
iostat -x 1 10 | tee io_stats.txt &

# 块层追踪
blktrace -d /dev/$DEVICE -o trace.out &
BLKTRACE_PID=$!

# 运行一段时间后停止
sleep 60
kill $BLKTRACE_PID

# 分析追踪结果
blkparse trace.out > parsed_trace.txt
echo "IO分析完成，结果保存在 parsed_trace.txt"
```

## 🧪 验证测试

### 性能基准测试套件
```bash
#!/bin/bash
# 系统性能基准测试

echo "=== 系统性能基准测试 ==="
echo "测试时间: $(date)"

# CPU基准测试
echo "1. CPU性能测试:"
sysbench --test=cpu --cpu-max-prime=20000 run

# 内存基准测试
echo "2. 内存性能测试:"
sysbench --test=memory --memory-block-size=1K --memory-total-size=100G run

# IO基准测试
echo "3. 磁盘IO测试:"
dd if=/dev/zero of=testfile bs=1M count=1000 oflag=direct
sync && echo 3 > /proc/sys/vm/drop_caches
hdparm -Tt /dev/sda

# 网络基准测试
echo "4. 网络性能测试:"
iperf3 -c localhost -t 30 -P 4

echo "基准测试完成"
```

## ❓ 常见问题处理

### Q1: perf工具权限不足怎么办？
**解决方案**：
```bash
# 临时解决
sudo sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'
sudo sh -c 'echo 0 >/proc/sys/kernel/kptr_restrict'

# 永久解决
echo 'kernel.perf_event_paranoid=1' >> /etc/sysctl.conf
echo 'kernel.kptr_restrict=0' >> /etc/sysctl.conf
sysctl -p
```

### Q2: 如何分析高负载但CPU使用率不高的情况？
**分析方法**：
```bash
# 检查不可中断睡眠进程
ps aux | awk '$8=="D" {print $0}'

# 检查IO等待时间
iostat -x 1 5

# 检查上下文切换
vmstat 1 5 | awk '{print $12,$13}'

# 检查锁竞争
perf record -e sched:sched_switch -a sleep 10
perf script | grep -v "sched_switch" | head -20
```

### Q3: 内存使用率高但应用响应慢怎么办？
**排查步骤**：
```bash
# 检查swap使用情况
free -h
swapon -s

# 检查页面错误
cat /proc/vmstat | grep pgfault

# 检查内存碎片
cat /proc/buddyinfo

# 检查SLAB使用
cat /proc/slabinfo | sort -k3 -nr | head -10
```

## 📚 扩展学习

### 高级性能工具
- **BPF/eBPF**: 现代内核追踪技术
- **bcc工具集**: BPF编译器集合工具
- **PCP**: Performance Co-Pilot系统
- **Prometheus**: 时间序列数据库监控

### 学习进阶路径
1. 掌握Linux内核性能调优原理
2. 学习系统级性能分析方法论
3. 理解硬件架构对性能的影响
4. 掌握大规模集群性能优化

### 企业级应用场景
- 数据库性能优化
- 高并发Web服务调优
- 容器化环境资源管理
- 云计算平台性能监控
- 微服务架构性能分析

---
> **💡 提示**: 高级性能分析需要深厚的系统知识基础，建议循序渐进学习，先掌握基础监控工具再深入学习高级分析技术。