# Network Troubleshooting

网络故障排查技巧与工具演示。

## 排查流程

```
网络故障排查金字塔:
      ┌─────────┐
      │ 应用层   │  dig, curl
      ├─────────┤
      │ 传输层   │  netstat, ss
      ├─────────┤
      │ 网络层   │  ping, traceroute
      ├─────────┤
      │ 链路层   │  arp, ip link
      ├─────────┤
      │ 物理层   │  ethtool, dmesg
      └─────────┘
```

## 常用工具

```bash
# 连通性测试
ping -c 4 google.com

# 路由追踪
traceroute google.com
mtr google.com

# DNS检查
dig google.com
nslookup google.com

# 连接检查
netstat -tulpn
ss -tulpn
lsof -i :80

# 抓包分析
tcpdump -i eth0 port 80
wireshark &

# 带宽测试
iperf3 -c server_ip
```

## 常见问题排查

### DNS问题
```bash
# 检查DNS配置
cat /etc/resolv.conf

# 测试DNS服务器
dig @8.8.8.8 google.com

# 清除缓存
sudo systemd-resolve --flush-caches
```

### 路由问题
```bash
# 查看路由表
ip route show

# 追踪路由
ip route get 8.8.8.8

# 检查策略路由
ip rule show
```
