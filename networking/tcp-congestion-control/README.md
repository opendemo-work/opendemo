# TCP Congestion Control

TCP拥塞控制算法演示，展示现代Linux内核中的拥塞控制实现。

## 拥塞控制概述

拥塞控制是TCP防止网络过载的关键机制：

```
拥塞窗口(CWND)变化:
     CWND
      │
      │    ╱╲        拥塞避免
      │   ╱  ╲╱╲     (线性增长)
      │  ╱      ╲╱
      │ ╱  慢启动
      │╱  (指数增长)
      └────────────────▶ 时间
         │    │
        慢启动阈值
```

## 经典算法

### 1. Tahoe (1988)
- 慢启动 (Slow Start)
- 拥塞避免 (Congestion Avoidance)
- 快速重传 (Fast Retransmit)

### 2. Reno (1990)
在Tahoe基础上增加:
- 快速恢复 (Fast Recovery)

### 3. 现代算法
- **CUBIC**: Linux默认，适合高带宽延迟网络
- **BBR**: Google开发，基于带宽和RTT测量
- **Westwood**: 无线/移动网络优化

## 算法对比

```
不同算法的CWND行为:

CUBIC:              Reno:
     │                │
  16 ┤        ╭─     │      ╱╲
  12 ┤      ╭─╯      │     ╱  ╲
   8 ┤    ╭─╯        │    ╱    ╲
   4 ┤  ╭─╯          │   ╱      ╲
   0 ┼──┴─────▶      │  ╱        ╲
     └────────▶      └────────────▶

BBR:                Westwood:
     │                │
  16 ┤────────        │     ╱╲╱╲
  12 ┤                │    ╱    ╲
   8 ┤                │   ╱      ╲
   4 ┤                │  ╱        ╲
   0 ┤                │ ╱          ╲
     └────────▶       └──────────────▶
```

## Linux配置

### 查看当前算法
```bash
# 查看可用算法
cat /proc/sys/net/ipv4/tcp_available_congestion_control

# 查看当前算法
cat /proc/sys/net/ipv4/tcp_congestion_control

# 临时修改算法
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr

# 永久修改
echo "net.ipv4.tcp_congestion_control=bbr" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 内核参数调优
```bash
# 初始拥塞窗口
sudo sysctl -w net.ipv4.tcp_initial_cwnd=10

# 慢启动阈值
sudo sysctl -w net.ipv4.tcp_slow_start_after_idle=0

# 启用TCP快速打开
sudo sysctl -w net.ipv4.tcp_fastopen=3
```

## iperf3测试

### 测试不同算法
```bash
# 服务端
iperf3 -s

# 客户端 - CUBIC
iperf3 -c <server_ip> --cubic -t 30 -i 1

# 客户端 - BBR
iperf3 -c <server_ip> --bbr -t 30 -i 1
```

## 算法详解

### CUBIC算法
```
CUBIC窗口增长:
W_cubic(t) = C*(t-K)^3 + W_max

其中:
- C: CUBIC常数
- t: 上次丢包后的时间
- K: 窗口增长到W_max的时间
- W_max: 上次丢包时的窗口大小
```

### BBR算法
```
BBR基于两个测量值:
1. BtlBw (瓶颈带宽)
2. RTprop (传播时延)

发送速率 = BtlBw
Inflight = BtlBw × RTprop × 2
```

## 拥塞控制状态机

```
         ┌─────────────┐
         │   Open      │
         └──────┬──────┘
                │
        ┌───────┼───────┐
        ▼       ▼       ▼
   ┌────────┐ ┌────┐ ┌────────┐
   │ Disorder│ │CWR │ │Recovery│
   └────────┘ └────┘ └────────┘
        │       │       │
        └───────┼───────┘
                ▼
         ┌─────────────┐
         │    Loss     │
         └─────────────┘
```

## 实际应用

### 数据中心
- 使用DCTCP (Data Center TCP)
- 低延迟优先

### 移动网络
- 使用Westwood或Vegas
- 适应无线链路特性

### 卫星链路
- 使用Hybla
- 处理高RTT

## 学习要点

1. 拥塞控制原理和状态机
2. 不同算法的适用场景
3. Linux内核参数调优
4. 实际网络环境测试
