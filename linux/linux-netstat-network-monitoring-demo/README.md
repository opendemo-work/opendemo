# Linux netstat网络监控命令详解演示

## 🎯 学习目标

通过本案例你将掌握：
- netstat命令的基础语法和常用选项
- 网络连接状态的识别和分析
- 端口监听和服务监控技巧
- 网络故障排查的基本方法
- 网络性能监控的实际应用

## 🛠️ 环境准备

### 系统要求
- Linux发行版（Ubuntu/CentOS/RHEL等）
- root权限或sudo权限
- 基本的网络知识

### 依赖检查
```bash
# 检查netstat是否安装
which netstat || echo "netstat未安装"

# 在现代系统中，可能需要安装net-tools包
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install net-tools

# CentOS/RHEL:
sudo yum install net-tools
```

## 📁 项目结构

```
linux-netstat-network-monitoring-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── network_monitor.sh             # 网络监控脚本
│   ├── connection_analyzer.sh         # 连接分析脚本
│   └── port_scanner.sh                # 端口扫描脚本
├── examples/                          # 示例输出
│   ├── netstat_basic.txt              # 基础命令输出示例
│   ├── netstat_advanced.txt           # 高级命令输出示例
│   └── troubleshooting_examples.txt   # 故障排查示例
└── docs/                              # 详细文档
    ├── netstat_options_guide.md       # 选项详解
    ├── network_troubleshooting.md     # 网络故障排查指南
    └── security_monitoring.md         # 安全监控指南
```

## 🚀 快速开始

### 步骤1：基础命令练习

```bash
# 查看所有网络连接
netstat -a

# 查看TCP连接
netstat -t

# 查看UDP连接
netstat -u

# 显示进程ID和程序名称
netstat -p

# 显示数字形式的地址和端口
netstat -n

# 组合使用常用选项
netstat -tulnp
```

### 步骤2：实时监控

```bash
# 每2秒刷新一次显示
netstat -tulnp -c 2

# 或使用watch命令
watch -n 2 'netstat -tulnp'
```

### 步骤3：连接统计分析

```bash
# 统计各状态的连接数
netstat -an | awk '/^tcp/ {print $6}' | sort | uniq -c | sort -nr

# 查看特定端口的连接
netstat -an | grep :80 | wc -l

# 查看连接最多的IP地址
netstat -an | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head
```

## 🔍 代码详解

### 核心概念解析

#### 1. 连接状态含义
```
LISTEN     - 服务正在监听端口等待连接
ESTABLISHED - 连接已建立
SYN_SENT   - 正在尝试建立连接
SYN_RECV   - 已收到连接请求
FIN_WAIT1  - 正在关闭连接
FIN_WAIT2  - 等待远程关闭
TIME_WAIT  - 连接已关闭，等待资源释放
CLOSE      - 连接正在关闭
CLOSE_WAIT - 等待本地应用程序关闭
LAST_ACK   - 等待所有分组死掉
```

#### 2. 常用选项组合详解
```bash
# -t: TCP协议
# -u: UDP协议  
# -l: 仅显示监听端口
# -n: 数字形式显示地址和端口
# -p: 显示进程ID和程序名
# -a: 显示所有连接和监听端口
# -c: 持续显示，指定间隔秒数
```

### 实际应用示例

#### 场景1：Web服务器监控
```bash
# 监控HTTP/HTTPS连接
netstat -tlnp | grep -E ':(80|443)'
netstat -an | grep :80 | grep ESTABLISHED | wc -l
```

#### 场景2：数据库连接监控
```bash
# MySQL连接监控
netstat -an | grep :3306 | grep ESTABLISHED
netstat -tlnp | grep :3306

# PostgreSQL连接监控
netstat -an | grep :5432 | grep ESTABLISHED
```

#### 场景3：安全审计
```bash
# 查找异常连接
netstat -tulnp | grep -v '127.0.0.1'

# 查找未知进程的网络连接
netstat -tulnp | grep -E '(unknown|rpc)' 

# 监控外部连接
netstat -an | grep ESTABLISHED | grep -v '127.0.0.1' | grep -v '::1'
```

## 🧪 验证测试

### 测试1：基础功能验证
```bash
#!/bin/bash
echo "=== Netstat基础功能测试 ==="

# 测试基本命令
echo "1. 测试netstat命令存在性..."
if ! command -v netstat &> /dev/null; then
    echo "❌ netstat命令未找到，请安装net-tools包"
    exit 1
fi
echo "✅ netstat命令可用"

# 测试常用选项
echo "2. 测试常用选项..."
netstat -tulnp &>/dev/null && echo "✅ 基本选项正常" || echo "❌ 基本选项异常"
```

### 测试2：连接状态分析
```bash
#!/bin/bash
echo "=== 连接状态分析测试 ==="

# 获取TCP连接状态统计
echo "当前TCP连接状态统计："
netstat -an | awk '/^tcp/ {print $6}' | sort | uniq -c | sort -nr

# 检查是否有大量TIME_WAIT连接
time_wait_count=$(netstat -an | grep TIME_WAIT | wc -l)
echo "TIME_WAIT连接数: $time_wait_count"

if [ $time_wait_count -gt 1000 ]; then
    echo "⚠️  警告：TIME_WAIT连接过多，可能需要调整内核参数"
fi
```

## ❓ 常见问题

### Q1: netstat命令找不到怎么办？
**解决方案**：
```bash
# Ubuntu/Debian系统
sudo apt-get update && sudo apt-get install net-tools

# CentOS/RHEL系统
sudo yum install net-tools

# 或使用现代替代命令ss
ss -tulnp
```

### Q2: 如何区分正常和异常连接？
**判断标准**：
- 正常：本地服务监听常见端口（22,80,443,3306等）
- 异常：监听不常见端口、大量外部连接、未知进程

### Q3: TIME_WAIT连接过多如何处理？
**优化建议**：
```bash
# 查看当前设置
sysctl net.ipv4.tcp_fin_timeout
sysctl net.ipv4.tcp_tw_reuse

# 临时调整
echo 30 > /proc/sys/net/ipv4/tcp_fin_timeout
echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse

# 永久设置（添加到/etc/sysctl.conf）
echo "net.ipv4.tcp_fin_timeout = 30" >> /etc/sysctl.conf
echo "net.ipv4.tcp_tw_reuse = 1" >> /etc/sysctl.conf
sysctl -p
```

## 📚 扩展学习

### 相关命令
- `ss` - 现代网络工具，功能更强大
- `lsof` - 列出打开的文件和网络连接
- `iftop` - 实时网络流量监控
- `nethogs` - 按进程分组的网络带宽监控

### 进阶学习路径
1. 掌握ss命令作为netstat的现代化替代
2. 学习iptables防火墙规则配合网络监控
3. 理解TCP/IP协议栈和连接状态机
4. 掌握网络性能调优和故障排查技巧

### 企业级应用场景
- 服务器安全监控和入侵检测
- 负载均衡器健康检查
- 数据库连接池监控
- 微服务间通信监控
- CDN边缘节点网络状态监控

---
> **💡 提示**: 在生产环境中使用netstat时，注意性能影响，对于高并发场景建议使用ss命令替代。