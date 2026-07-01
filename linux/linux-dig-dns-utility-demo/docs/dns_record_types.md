# DNS 记录类型速查

## 常见记录类型

| 记录类型 | 用途 | 示例 |
|----------|------|------|
| A | 将域名解析为 IPv4 地址 | `example.com. 300 IN A 93.184.216.34` |
| AAAA | 将域名解析为 IPv6 地址 | `example.com. 300 IN AAAA 2606:2800:220:1::` |
| CNAME | 别名记录 | `www.example.com. 300 IN CNAME example.com.` |
| MX | 邮件交换记录 | `example.com. 300 IN MX 10 mail.example.com.` |
| NS | 权威名称服务器 | `example.com. 300 IN NS a.iana-servers.net.` |
| TXT | 文本记录，常用于 SPF、DKIM、DMARC | `example.com. 300 IN TXT "v=spf1 -all"` |
| SOA | 起始授权记录 | 包含主 DNS 服务器、管理员邮箱、序列号等 |
| PTR | 反向解析记录 | `34.216.184.93.in-addr.arpa. PTR example.com.` |
| SRV | 服务定位记录 | `_sip._tcp.example.com. SRV 10 5 5060 sip.example.com.` |
| CAA | 证书颁发机构授权 | 指定哪些 CA 可以为域名签发证书 |
| DNSKEY | DNSSEC 公钥 | 用于验证 DNS 响应签名 |
| DS | 委托签名者 | 父区域用于验证子区域 DNSKEY |

## 查询命令对照

```bash
# A 记录
dig example.com A +short

# MX 记录
dig example.com MX +short

# TXT 记录
dig example.com TXT +short

# 全部信息
dig example.com ANY
```
