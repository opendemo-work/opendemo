# TCP/IP Fundamentals Demo

TCP/IP协议基础演示项目，深入理解网络通信的核心协议。

## 技术栈

- TCP/IP协议栈
- Socket编程
- Wireshark抓包分析

## 核心概念

### TCP/IP四层模型

```
应用层    - HTTP, FTP, DNS, SSH
传输层    - TCP, UDP
网络层    - IP, ICMP, ARP
链路层    - Ethernet, Wi-Fi
```

### TCP三次握手

```
客户端                    服务器
   |     SYN(seq=x)       |
   |--------------------->|
   |   SYN(seq=y,ACK=x+1) |
   |<---------------------|
   |     ACK(y+1)         |
   |--------------------->|
   |                      |
   |==== 连接建立完成 =====|
```

## 快速开始

### 1. 查看网络配置

```bash
# Linux
ifconfig
ip addr

# 查看路由表
route -n
ip route

# 查看DNS配置
cat /etc/resolv.conf
```

### 2. TCP连接测试

```bash
# 使用nc测试端口连通性
nc -vz google.com 443

# 使用telnet
telnet google.com 80

# TCPDUMP抓包
sudo tcpdump -i eth0 port 80
```

## 学习要点

1. OSI七层模型与TCP/IP四层模型对比
2. TCP三次握手与四次挥手
3. IP地址分类与子网划分
4. ARP协议工作原理
5. ICMP与Ping实现

## 参考

- [RFC 791 - IP](https://tools.ietf.org/html/rfc791)
- [RFC 793 - TCP](https://tools.ietf.org/html/rfc793)
