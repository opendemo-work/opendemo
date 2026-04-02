# Networking 命名规范

## 网络设备命名

### 网卡命名
```
eth0, eth1          # 物理网卡 (传统命名)
enp0s3, enp0s8      # 可预测命名 (systemd)
ens33, ens34        # VMware虚拟网卡
```

### 接口命名规范
```
eth0        - 第一块以太网卡
lo          - 本地回环接口
tun0, tap0  - VPN隧道接口
br0         - 网桥接口
veth0       - 虚拟以太网接口 (容器)
```

## 配置文件命名

### 网络配置
```
/etc/sysconfig/network-scripts/ifcfg-eth0   # RHEL/CentOS
/etc/netplan/00-installer-config.yaml       # Ubuntu
/etc/network/interfaces                     # Debian传统
```

## 防火墙规则命名

### iptables链命名
```
INPUT       - 入站流量
OUTPUT      - 出站流量
FORWARD     - 转发流量
PREROUTING  - 路由前处理
POSTROUTING - 路由后处理
```

## 文档命名

### 案例目录命名
```
tcp-ip-fundamentals         # TCP/IP基础
socket-programming          # Socket编程
network-protocols-analysis  # 协议分析
load-balancing-algorithms   # 负载均衡算法
network-security-basics     # 网络安全基础
wireshark-packet-analysis   # Wireshark抓包分析
```
