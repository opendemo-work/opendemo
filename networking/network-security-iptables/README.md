# Network Security with iptables

iptables防火墙配置与安全策略演示。

## iptables基础

```
iptables规则链:
┌─────────┐    ┌─────────┐    ┌─────────┐
│  PREROUTING │───▶│  FORWARD  │───▶│ POSTROUTING│
└─────────┘    └─────────┘    └─────────┘
      │              │
      ▼              ▼
┌─────────┐    ┌─────────┐
│  INPUT    │    │  OUTPUT   │
└─────────┘    └─────────┘
```

## 基本命令

```bash
# 查看规则
sudo iptables -L -v -n

# 查看特定表
sudo iptables -t nat -L -v -n

# 清除规则
sudo iptables -F
sudo iptables -X

# 保存规则
sudo iptables-save > /etc/iptables/rules.v4

# 恢复规则
sudo iptables-restore < /etc/iptables/rules.v4
```

## 常用规则示例

```bash
# 允许SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 允许HTTP/HTTPS
sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# 允许本地回环
sudo iptables -A INPUT -i lo -j ACCEPT

# 允许已建立的连接
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 默认拒绝
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
```

## NAT配置

```bash
# 源地址转换 (SNAT)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# 目的地址转换 (DNAT/端口转发)
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.100:80

# 启用IP转发
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

## 防DDoS规则

```bash
# 限制连接速率
sudo iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT

# 阻止SYN flood
sudo iptables -A INPUT -p tcp --syn -m limit --limit 1/second --limit-burst 3 -j ACCEPT

# 阻止ping flood
sudo iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/second -j ACCEPT
```
