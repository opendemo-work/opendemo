# Wireshark Packet Analysis

Wireshark网络抓包与协议分析演示。

## Wireshark基础

```
Wireshark界面:
┌─────────────────────────────────────────────────────────┐
│  Filter: tcp.port == 80                                 │
├─────────────────────────────────────────────────────────┤
│  No.  Time    Source    Destination  Protocol  Info     │
│  1    0.00   10.0.0.1   10.0.0.2     TCP      SYN      │
│  2    0.01   10.0.0.2   10.0.0.1     TCP      SYN,ACK  │
│  3    0.02   10.0.0.1   10.0.0.2     TCP      ACK      │
├─────────────────────────────────────────────────────────┤
│  Frame 1: 74 bytes                                      │
│  Ethernet II, Src: ...                                  │
│  Internet Protocol Version 4                            │
│  Transmission Control Protocol                          │
└─────────────────────────────────────────────────────────┘
```

## 常用过滤器

```
# 显示过滤器
ip.addr == 192.168.1.1
tcp.port == 443
http.request.method == "GET"
dns.qry.name contains "google"

# 捕获过滤器
tcp port 80
host 192.168.1.1
net 192.168.0.0/24
```

## TCP流分析

```
三次握手:
Client                Server
   │      SYN(seq=x)    │
   │───────────────────▶│
   │                    │
   │  SYN,ACK(seq=y,ack=x+1)│
   │◀───────────────────│
   │                    │
   │   ACK(ack=y+1)     │
   │───────────────────▶│
```

## 学习要点

1. 捕获过滤与显示过滤
2. 协议解码分析
3. TCP流重组
4. 性能问题诊断
5. 安全事件分析
