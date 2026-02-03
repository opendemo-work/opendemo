# Linux常用系统监控命令综合演示

## 🎯 学习目标

通过本案例你将掌握Linux系统中最常用的监控和管理命令：
- ps命令：进程状态查看和管理
- df命令：磁盘空间使用情况监控
- du命令：目录和文件空间使用分析
- iostat命令：IO性能统计和分析
- sar命令：系统活动报告和历史数据分析

## 🛠️ 环境准备

### 系统要求
- Linux发行版（主流发行版均可）
- 基本的系统管理权限
- 系统监控基础知识

### 依赖安装
```bash
# Ubuntu/Debian系统
sudo apt-get update
sudo apt-get install -y sysstat procps

# CentOS/RHEL系统
sudo yum install -y sysstat procps-ng

# 验证安装
which ps df du iostat sar
```

## 📁 项目结构

```
linux-common-monitoring-commands-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── system_health_check.sh         # 系统健康检查脚本
│   ├── disk_space_monitor.sh          # 磁盘空间监控脚本
│   ├── process_analyzer.sh            # 进程分析脚本
│   └── io_performance_monitor.sh      # IO性能监控脚本
├── examples/                          # 示例输出
│   ├── ps_examples.txt                # ps命令示例
│   ├── df_examples.txt                # df命令示例
│   ├── du_examples.txt                # du命令示例
│   ├── iostat_examples.txt            # iostat命令示例
│   └── sar_examples.txt               # sar命令示例
└── docs/                              # 详细文档
    ├── ps_command_guide.md            # ps命令详解
    ├── df_du_guide.md                 # 磁盘空间管理指南
    ├── iostat_analysis.md             # IO性能分析
    └── sar_historical_analysis.md     # 历史数据分析指南
```

## 🚀 快速开始

### 1. ps命令 - 进程状态查看

```bash
# 查看所有进程
ps aux

# 查看特定用户的进程
ps -u username

# 查看进程树结构
ps -ef --forest

# 实时监控进程（类似top）
watch -n 1 'ps aux --sort=-%cpu | head -20'

# 查找特定进程
ps aux | grep nginx

# 显示进程的完整命令行
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -10
```

### 2. df命令 - 磁盘空间监控

```bash
# 查看所有文件系统使用情况
df -h

# 查看inode使用情况
df -i

# 查看特定文件系统类型
df -t ext4

# 以兆字节显示
df -m

# 显示文件系统统计信息
df -h --total
```

### 3. du命令 - 目录空间分析

```bash
# 查看当前目录各子目录大小
du -h --max-depth=1

# 查找占用空间最大的文件
du -ah | sort -rh | head -20

# 查看特定目录大小
du -sh /var/log/

# 排除特定文件类型
du -h --exclude="*.log" /home/user/

# 显示修改时间
du -h --time /etc/
```

### 4. iostat命令 - IO性能监控

```bash
# 基本IO统计
iostat

# 按设备显示详细信息
iostat -x

# 实时监控（每2秒刷新）
iostat -x 2

# 显示特定设备
iostat -p sda

# 历史数据查看
iostat -h
```

### 5. sar命令 - 系统活动报告

```bash
# CPU使用率历史数据
sar -u

# 内存使用情况
sar -r

# 网络统计
sar -n DEV

# IO统计
sar -b

# 指定时间范围
sar -u -s 09:00:00 -e 18:00:00
```

## 🔍 代码详解

### 核心命令组合应用

#### 场景1：系统资源综合分析
```bash
#!/bin/bash
# 系统资源一键分析脚本

echo "=== 系统资源综合分析报告 ==="
echo "生成时间: $(date)"
echo ""

echo "1. CPU使用情况:"
top -b -n 1 | head -5
echo ""

echo "2. 内存使用情况:"
free -h
echo ""

echo "3. 磁盘空间使用:"
df -h | head -10
echo ""

echo "4. IO性能统计:"
iostat -x 1 1
echo ""

echo "5. 高CPU消耗进程:"
ps aux --sort=-%cpu | head -10
echo ""

echo "6. 高内存消耗进程:"
ps aux --sort=-%mem | head -10
```

#### 场景2：磁盘空间预警监控
```bash
#!/bin/bash
# 磁盘空间监控和预警脚本

THRESHOLD=80  # 空间使用率阈值

# 检查各分区使用情况
df -h | awk -v threshold="$THRESHOLD" '
NR>1 {
    usage = substr($5, 1, length($5)-1)
    if (usage > threshold) {
        print "警告: " $6 " 分区使用率达到 " usage "%"
        print "可用空间: " $4
        print "---"
    }
}'

# 检查inode使用情况
df -i | awk -v threshold="$THRESHOLD" '
NR>1 {
    usage = substr($5, 1, length($5)-1)
    if (usage > threshold) {
        print "警告: " $6 " inode使用率达到 " usage "%"
    }
}'
```

#### 场景3：进程性能分析
```bash
#!/bin/bash
# 进程性能深度分析脚本

echo "=== 进程性能分析 ==="

# 查找僵尸进程
ZOMBIE_COUNT=$(ps aux | awk '$8=="Z" {count++} END {print count+0}')
echo "僵尸进程数: $ZOMBIE_COUNT"

# 查找不可中断睡眠进程
UNINTERRUPTIBLE_COUNT=$(ps aux | awk '$8=="D" {count++} END {print count+0}')
echo "不可中断睡眠进程数: $UNINTERRUPTIBLE_COUNT"

# 显示进程状态统计
echo ""
echo "进程状态分布:"
ps aux | awk 'NR>1 {states[$8]++} END {for(state in states) print state ": " states[state]}'

# 显示父进程关系
echo ""
echo "顶级进程树:"
ps -eo pid,ppid,cmd --no-headers | awk '$2==1 {print $1 " " $3}' | head -10
```

## 🧪 验证测试

### 测试1：命令功能验证
```bash
#!/bin/bash
echo "=== 常用监控命令功能测试 ==="

# 测试ps命令
echo "1. 测试ps命令..."
ps aux >/dev/null && echo "✅ ps命令正常" || echo "❌ ps命令异常"

# 测试df命令
echo "2. 测试df命令..."
df -h >/dev/null && echo "✅ df命令正常" || echo "❌ df命令异常"

# 测试du命令
echo "3. 测试du命令..."
du -sh /tmp/ >/dev/null && echo "✅ du命令正常" || echo "❌ du命令异常"

# 测试iostat命令
echo "4. 测试iostat命令..."
if command -v iostat &> /dev/null; then
    iostat >/dev/null && echo "✅ iostat命令正常" || echo "❌ iostat命令异常"
else
    echo "⚠️  iostat命令未安装"
fi

# 测试sar命令
echo "5. 测试sar命令..."
if command -v sar &> /dev/null; then
    sar -u 1 1 >/dev/null && echo "✅ sar命令正常" || echo "❌ sar命令异常"
else
    echo "⚠️  sar命令未安装"
fi
```

### 测试2：性能基准测试
```bash
#!/bin/bash
echo "=== 系统性能基准测试 ==="

# CPU性能测试
echo "CPU性能测试:"
time echo "scale=2000; 4*a(1)" | bc -l >/dev/null

# 内存测试
echo "内存访问测试:"
dd if=/dev/zero of=/tmp/test bs=1M count=100 conv=fdatasync

# 磁盘IO测试
echo "磁盘IO测试:"
hdparm -Tt /dev/sda 2>/dev/null || echo "无法测试磁盘性能"

# 网络测试
echo "网络连通性测试:"
ping -c 3 127.0.0.1 >/dev/null && echo "本地网络正常" || echo "本地网络异常"
```

## ❓ 常见问题

### Q1: df显示的空间和du统计不一致怎么办？
**原因分析**：
- 已删除但仍在使用的文件
- 挂载点覆盖了原有目录
- 不同的文件系统类型

**解决方案**：
```bash
# 查找已删除但仍被占用的文件
lsof +L1

# 重启相关服务释放文件句柄
sudo systemctl restart service_name
```

### Q2: iostat显示await时间很高怎么办？
**优化建议**：
```bash
# 检查IO调度器
cat /sys/block/sda/queue/scheduler

# 调整读取提前量
echo 4096 > /sys/block/sda/queue/read_ahead_kb

# 优化文件系统参数
tune2fs -o journal_data_writeback /dev/sda1
```

### Q3: sar历史数据不完整怎么办？
**配置方法**：
```bash
# 编辑sysstat配置文件
sudo vim /etc/default/sysstat

# 确保启用数据收集
ENABLED="true"
SA1_OPTIONS="-S DISK"

# 重启sysstat服务
sudo systemctl restart sysstat
```

## 📚 扩展学习

### 相关工具链
- `htop` - 增强版进程查看器
- `iotop` - 实时IO监控工具
- `nmon` - 系统性能监控工具
- `glances` - 现代化系统监控
- `atop` - 高级系统监控工具

### 学习进阶路径
1. 掌握系统调用和进程间通信
2. 学习Linux内核性能优化
3. 理解存储系统和文件系统原理
4. 掌握网络协议栈和性能调优
5. 学习容器化环境下的监控策略

### 企业应用场景
- 服务器日常巡检和维护
- 性能瓶颈分析和优化
- 容量规划和资源分配
- 故障排查和应急响应
- 自动化运维平台集成

---
> **💡 提示**: 建议将这些监控命令集成到自动化运维脚本中，建立完善的系统监控体系，及时发现和处理系统异常。