# DNS Configuration

DNS配置与服务搭建演示，涵盖BIND、CoreDNS、DNS记录类型等。

## DNS基础架构

```
DNS解析流程:
User → Local DNS → Root DNS → TLD DNS → Authoritative DNS
     │              │            │              │
     ▼              ▼            ▼              ▼
  8.8.8.8      198.41.0.4   a.gtld-servers.net  ns1.example.com
  (Google)     (根服务器)    (顶级域)            (权威DNS)
```

## 安装BIND

```bash
# Ubuntu/Debian
sudo apt install bind9 bind9utils bind9-doc

# CentOS/RHEL
sudo yum install bind bind-utils

# 启动服务
sudo systemctl start named
sudo systemctl enable named
```

## 配置区域文件

```bash
# /etc/bind/named.conf.local
zone "example.com" {
    type master;
    file "/etc/bind/db.example.com";
};

zone "1.168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/db.192.168.1";
};
```

## 常用记录类型

| 类型 | 用途 | 示例 |
|------|------|------|
| A | IPv4地址 | example.com. IN A 192.168.1.100 |
| AAAA | IPv6地址 | example.com. IN AAAA 2001:db8::1 |
| CNAME | 别名 | www IN CNAME example.com. |
| MX | 邮件交换 | IN MX 10 mail.example.com. |
| NS | 名称服务器 | IN NS ns1.example.com. |
| TXT | 文本记录 | IN TXT "v=spf1 include:_spf.google.com ~all" |
| SOA | 权威记录 | 区域授权起始 |

## 测试DNS

```bash
# dig命令
dig @localhost example.com A
dig @localhost example.com MX
dig @localhost -x 192.168.1.100

# nslookup
nslookup example.com 127.0.0.1

# 检查配置
named-checkconf
named-checkzone example.com /etc/bind/db.example.com
```
