# Linux iproute2网络工具详解演示

## 🎯 学习目标

通过本案例你将掌握：
- ip命令的基础语法和常用选项
- 现代Linux网络配置和管理技巧
- 网络接口、路由、隧道等高级配置方法
- 生产环境网络管理最佳实践

## 🛠️ 环境准备

### 系统要求
- Linux发行版（Ubuntu/CentOS/RHEL等）
- root权限或sudo权限
- 基本的网络配置知识

### 依赖检查
```bash
# 检查iproute2是否安装
which ip || echo "iproute2未安装"

# 安装iproute2工具
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install iproute2

# CentOS/RHEL:
sudo yum install iproute
```

## 📁 项目结构

```
linux-iproute2-network-tool-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── network_manager.sh             # 网络管理脚本
│   ├── route_configurator.sh          # 路由配置脚本
│   └── tunnel_setup.sh                # 隧道设置脚本
├── examples/                          # 示例输出
│   ├── ip_basic.txt                   # 基础命令输出示例
│   ├── ip_advanced.txt                # 高级命令输出示例
│   └── troubleshooting_examples.txt   # 故障排查示例
└── docs/                              # 详细文档
    ├── ip_commands_guide.md           # ip命令详解
    ├── network_namespace_guide.md     # 网络命名空间指南
    └── advanced_networking_guide.md   # 高级网络配置指南
```

## 🚀 快速开始

### 步骤1：基础命令练习

```bash
# 显示所有网络接口
ip addr show
# 或简写
ip a

# 显示特定网络接口
ip addr show eth0
# 或简写
ip a s eth0

# 显示路由表
ip route show
# 或简写
ip r

# 显示ARP表
ip neigh show
# 或简写
ip n

# 显示网络接口状态
ip link show
# 或简写
ip l
```

### 步骤2：实用技巧

```bash
# 启用/禁用网络接口
sudo ip link set eth0 up
sudo ip link set eth0 down

# 配置IP地址
sudo ip addr add 192.168.1.100/24 dev eth0

# 删除IP地址
sudo ip addr del 192.168.1.100/24 dev eth0

# 添加默认路由
sudo ip route add default via 192.168.1.1

# 删除路由
sudo ip route del default via 192.168.1.1

# 添加静态路由
sudo ip route add 10.0.0.0/8 via 192.168.1.1
```

### 步骤3：高级用法

```bash
# 网络命名空间操作
# 创建网络命名空间
sudo ip netns add testns

# 列出所有命名空间
sudo ip netns list

# 在命名空间中执行命令
sudo ip netns exec testns ip addr show

# 删除命名空间
sudo ip netns delete testns

# 创建虚拟以太网对（veth pair）
sudo ip link add veth0 type veth peer name veth1

# 将一端移到命名空间
sudo ip link set veth1 netns testns

# 配置网络接口和命名空间
sudo ip addr add 10.0.0.1/24 dev veth0
sudo ip link set veth0 up
sudo ip netns exec testns ip addr add 10.0.0.2/24 dev veth1
sudo ip netns exec testns ip link set veth1 up
sudo ip netns exec testns ip link set lo up
```

## 🔍 代码详解

### 核心概念解析

#### 1. ip命令子命令详解
```bash
# ip addr (a): 管理IP地址
# ip link (l): 管理网络接口
# ip route (r): 管理路由表
# ip neigh (n): 管理邻居表（类似ARP）
# ip netns: 管理网络命名空间
# ip tunnel: 管理隧道接口
# ip maddr: 管理多播地址
```

#### 2. 实际应用示例

##### 场景1：网络故障排查
```bash
# 检查网络接口状态
ip -s link show eth0  # 显示统计信息

# 检查IP地址配置
ip addr show | grep -A 5 "inet "

# 检查路由表
ip route show
ip route get 8.8.8.8  # 查看到达特定地址的路由

# 检查ARP表
ip neigh show
```

##### 场景2：动态网络配置
```bash
# 动态获取IP地址（DHCP）
sudo dhclient eth0
# 或使用ip命令配合dhclient
sudo ip addr flush dev eth0  # 清除IP地址
sudo dhclient eth0  # 获取新IP

# 配置多个IP地址
sudo ip addr add 192.168.1.100/24 dev eth0
sudo ip addr add 192.168.1.101/24 dev eth0  # 添加第二个IP
```

##### 场景3：高级网络配置
```bash
# 创建网桥
sudo ip link add br0 type bridge
sudo ip link set br0 up
sudo ip link set eth0 master br0

# 创建VLAN接口
sudo ip link add link eth0 name eth0.100 type vlan id 100
sudo ip addr add 192.168.100.1/24 dev eth0.100
sudo ip link set eth0.100 up

# 配置隧道
sudo ip tunnel add tun0 mode gre remote 10.0.0.2 local 10.0.0.1
sudo ip addr add 172.16.0.1/30 dev tun0
sudo ip link set tun0 up
```

## 🧪 验证测试

### 测试1：基础功能验证
```bash
#!/bin/bash
echo "=== Iproute2基础功能测试 ==="

# 测试ip命令存在性
echo "1. 测试ip命令存在性..."
if ! command -v ip &> /dev/null; then
    echo "❌ ip命令未找到，请安装iproute2包"
    exit 1
fi
echo "✅ ip命令可用"

# 测试显示接口功能
echo "2. 测试显示接口功能..."
result=$(ip addr show 2>/dev/null | head -10)
if [[ -n "$result" ]]; then
    echo "✅ 显示接口功能正常"
    echo "示例输出:"
    echo "$result"
else
    echo "❌ 显示接口功能异常"
fi
```

### 测试2：网络配置验证
```bash
#!/bin/bash
echo "=== 网络配置验证测试 ==="

# 获取网络接口信息
echo "当前网络接口信息:"
ip -br addr show

# 检查默认路由
echo -e "\n默认路由:"
ip route show default

# 检查到外部网络的可达性
echo -e "\n到外部网络的路由:"
ip route get 8.8.8.8
```

## ❓ 常见问题

### Q1: ip命令找不到怎么办？
**解决方案**：
```bash
# Ubuntu/Debian系统
sudo apt-get update && sudo apt-get install iproute2

# CentOS/RHEL系统
sudo yum install iproute

# 检查可用的网络工具
which ip || which ifconfig || echo "需要安装网络工具包"
```

### Q2: 如何进行网络命名空间的高级操作？
**解决方案**：
```bash
#!/bin/bash
# 高级网络命名空间操作脚本
ADVANCED_NETNS_SETUP() {
    local ns_name=$1
    local veth_outer=$2
    local veth_inner=$3
    local outer_ip=$4
    local inner_ip=$5
    
    echo "创建高级网络命名空间配置..."
    
    # 创建命名空间
    sudo ip netns add $ns_name
    
    # 创建虚拟以太网对
    sudo ip link add $veth_outer type veth peer name $veth_inner
    
    # 将内侧接口移到命名空间
    sudo ip link set $veth_inner netns $ns_name
    
    # 配置外侧接口
    sudo ip addr add $outer_ip dev $veth_outer
    sudo ip link set $veth_outer up
    
    # 配置命名空间内接口
    sudo ip netns exec $ns_name ip addr add $inner_ip dev $veth_inner
    sudo ip netns exec $ns_name ip link set $veth_inner up
    sudo ip netns exec $ns_name ip link set lo up
    
    # 设置默认路由
    sudo ip netns exec $ns_name ip route add default via ${outer_ip%/*} dev $veth_inner
    
    echo "网络命名空间 $ns_name 已创建并配置完成"
}

# 使用示例
# ADVANCED_NETNS_SETUP "container1" "veth0" "eth0" "10.0.0.1/24" "10.0.0.2/24"
```

### Q3: 如何进行网络性能监控？
**解决方案**：
```bash
#!/bin/bash
# 网络性能监控脚本
NETWORK_PERFORMANCE_MONITOR() {
    local interface=${1:-"eth0"}
    
    echo "=== 网络接口 $interface 性能监控 ==="
    
    # 显示接口统计信息
    echo "接口统计信息:"
    ip -s link show $interface
    
    # 监控实时流量（需要安装iftop或nethogs）
    if command -v nethogs &> /dev/null; then
        echo "运行 nethogs 进行进程级流量监控..."
        sudo nethogs $interface
    elif command -v iftop &> /dev/null; then
        echo "运行 iftop 进行流量监控..."
        sudo iftop -i $interface
    else
        echo "安装 nethogs 或 iftop 以获得更详细的流量信息"
        echo "sudo apt-get install nethogs iftop"
    fi
}

# 运行监控
# NETWORK_PERFORMANCE_MONITOR "eth0"
```

## 📚 扩展学习

### 相关命令
- `ss` - 套接字统计
- `tc` - 流量控制
- `nftables/iptables` - 防火墙配置
- `bridge` - 网桥管理
- `iw` - 无线网络管理

### 进阶学习路径
1. 掌握网络命名空间和容器网络
2. 学习流量控制和QoS配置
3. 理解VPN和隧道技术
4. 掌握SDN和网络虚拟化

### 企业级应用场景
- 容器网络配置（Docker/Kubernetes）
- 网络虚拟化和隔离
- 高级路由和策略路由
- 网络性能调优和监控
- 网络安全和访问控制

---
> **💡 提示**: iproute2是现代Linux系统的标准网络配置工具集，相比传统的net-tools（ifconfig等），它提供了更强大和灵活的功能，是每个Linux系统管理员必须掌握的工具。