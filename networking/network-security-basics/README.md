# Network Security Basics

网络安全基础与防护策略演示。

## 安全层次

```
网络安全层次:
┌─────────────────────────────────────────────────────────┐
│  应用层: HTTPS, TLS, 认证授权                            │
├─────────────────────────────────────────────────────────┤
│  传输层: TCP/UDP安全, VPN加密                            │
├─────────────────────────────────────────────────────────┤
│  网络层: 防火墙, ACL, IDS/IPS                            │
├─────────────────────────────────────────────────────────┤
│  链路层: MAC过滤, VLAN隔离                               │
├─────────────────────────────────────────────────────────┤
│  物理层: 门禁, 监控, 防雷                                │
└─────────────────────────────────────────────────────────┘
```

## 防火墙配置

```bash
# iptables基础
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -P INPUT DROP

# 保存规则
sudo iptables-save > /etc/iptables/rules.v4
```

## 入侵检测

```bash
# Snort安装配置
sudo apt install snort
sudo snort -T -c /etc/snort/snort.conf
sudo snort -A console -i eth0
```

## 学习要点

1. 防火墙策略设计
2. 入侵检测规则
3. VPN安全配置
4. DDoS防护策略
