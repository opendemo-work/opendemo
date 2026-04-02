# IPv6 Fundamentals

IPv6基础与部署实践演示。

## IPv6 vs IPv4

| 特性 | IPv4 | IPv6 |
|------|------|------|
| 地址长度 | 32位 | 128位 |
| 地址数量 | 4.3×10⁹ | 3.4×10³⁸ |
| 表示方式 | 点分十进制 | 冒分十六进制 |
| 头部 | 可变长 | 固定40字节 |
| NAT | 广泛使用 | 不需要 |
| 安全性 | IPsec可选 | IPsec内置 |

## 地址格式

```
完整格式:
2001:0db8:85a3:0000:0000:8a2e:0370:7334

压缩格式:
2001:db8:85a3::8a2e:370:7334

特殊地址:
::1/128     - 环回地址
::/128      - 未指定地址
fe80::/10   - 链路本地地址
2000::/3    - 全球单播地址
ff00::/8    - 组播地址
```

## 地址配置

```bash
# 静态配置
ip -6 addr add 2001:db8::1/64 dev eth0

# SLAAC (无状态自动配置)
ip -6 addr show dev eth0

# 查看邻居表
ip -6 neigh show

# 路由配置
ip -6 route add default via 2001:db8::1
```

## 双栈部署

```bash
# Nginx双栈配置
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
}

# 测试连通性
ping6 google.com
curl -6 https://google.com
```
