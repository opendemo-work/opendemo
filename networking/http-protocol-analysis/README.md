# HTTP Protocol Analysis

HTTP协议深度分析，展示HTTP/1.1、HTTP/2、HTTP/3的演进和差异。

## HTTP演进历程

```
HTTP发展时间线:
1991  HTTP/0.9    单行协议
1996  HTTP/1.0     headers引入
1997  HTTP/1.1    持久连接、管道化
2015  HTTP/2      多路复用、二进制分帧
2022  HTTP/3      基于QUIC，无队头阻塞
```

## HTTP/1.1 特性

### 持久连接
```
HTTP/1.0:              HTTP/1.1:
┌───┐  Req  ┌───┐      ┌───┐  Req  ┌───┐
│ C │◄─────►│ S │      │ C │◄─────►│ S │
└───┘  Resp └───┘      └───┘  Resp └───┘
   ╲  Req  ╱              ╲  Req2 ╱
    ╲◄────►/               ╲◄────►/  (复用连接)
     └──┘                     └──┘
   每次请求新连接              Keep-Alive
```

### 管道化限制
```
队头阻塞 (Head-of-Line Blocking):
请求1 ───────────────────────────────▶ 响应1 (慢)
请求2 ───────▶ 响应2 (快，但必须等1完成)
请求3 ───────▶ 响应3 (快，但必须等1完成)
```

## HTTP/2 核心特性

### 二进制分帧层
```
HTTP/1.1 (文本):           HTTP/2 (二进制帧):
GET / HTTP/1.1            ┌────────┬────────┬───────┐
Host: example.com         │Length  │Type    │Flags  │
                          │(24 bit)│(8 bit) │(8 bit)│
                          ├────────┼────────┼───────┤
                          │R       │Stream Identifier(31 bit)│
                          │(1 bit) │                           │
                          ├────────┴────────┴───────┤
                          │      Payload (...)
                          └─────────────────────────┘
```

### 多路复用
```
HTTP/2 多路复用:
Stream 1: ──[HEADERS]─[DATA]─────────────────────▶
Stream 3: ────────[HEADERS]─[DATA]─[DATA]────────▶
Stream 5: ───────────────[HEADERS]─[DATA]────────▶
Stream 7: ───────────────────[HEADERS]─[DATA]────▶
                  ↓
           单个TCP连接
           (无队头阻塞)
```

### 首部压缩 (HPACK)
```
静态表:                    动态表:
Index  Header              Index  Header
  1    :authority             62   :method: GET
  2    :method: GET           63   :scheme: https
  3    :method: POST          64   :path: /
  4    :path: /
  ...                        (由连接上下文构建)

编码前: 500+ bytes
编码后: ~50 bytes (使用索引)
```

### 服务器推送
```
客户端请求:                服务器推送:
GET /index.html            PUSH_PROMISE /style.css
      │                          │
      ▼                          ▼
<index.html>              <style.css> (缓存)
      │                          │
      └──────────────────────────┘
              减少往返次数
```

## HTTP/3 与 QUIC

### QUIC协议栈
```
传统:                      QUIC:
┌────────────┐            ┌────────────┐
│   HTTP/2   │            │   HTTP/3   │
├────────────┤            ├────────────┤
│    TLS     │            │   QUIC     │ ← 加密+传输
├────────────┤            ├────────────┤
│    TCP     │            │    UDP     │
├────────────┤            ├────────────┤
│    IP      │            │    IP      │
└────────────┘            └────────────┘
```

### 无队头阻塞
```
TCP丢包影响所有流:          QUIC流独立:
Stream 1 ───X──▶ (丢包)     Stream 1 ───X──▶ (仅影响1)
Stream 2 ──────▶ (阻塞!)    Stream 2 ──────▶ (正常)
Stream 3 ──────▶ (阻塞!)    Stream 3 ──────▶ (正常)

TCP: 单队列                QUIC: 多队列
```

## 性能对比

### 加载时间对比
```
场景: 100个小资源 + 10个大资源

HTTP/1.1:                    HTTP/2:
[==========] Resource 1      [==] R1  [==] R11 [==] R21
[==========] Resource 2      [==] R2  [==] R12 [==] R22
[==========] Resource 3      [==] R3  [==] R13 [==] R23
    ...                        (并发交错)
[==========] Resource 10
(6连接并行，队头阻塞)

HTTP/3 (QUIC):
[==] R1  [==] R11 [==] R21  [==] R31
[==] R2  [==] R12 [==] R22  [==] R32
    (更快连接建立，无队头阻塞)
```

### 关键指标
| 特性 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|--------|--------|
| 并发 | 6-8连接 | 单连接多流 | 单连接多流 |
| 头部压缩 | 无 | HPACK | QPACK |
| 队头阻塞 | TCP层 | TCP层 | 无 |
| 连接建立 | 2-3 RTT | 2-3 RTT | 0-1 RTT |
| 安全性 | 可选 | 强制TLS | 强制TLS |

## 实践操作

### 检查HTTP版本
```bash
# 使用curl
curl -I --http2 https://example.com
curl -I --http3 https://example.com

# 使用Chrome DevTools
# Network面板 - Protocol列显示h2, h3

# 使用npx http2-test
npx http2-test https://example.com
```

### 启用HTTP/2 (Nginx)
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # HTTP/2推送示例
    location = / {
        http2_push /style.css;
        http2_push /script.js;
    }
}
```

### 启用HTTP/3 (Nginx + quiche)
```nginx
server {
    listen 443 quic reuseport;
    listen 443 ssl;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # 启用0-RTT
    ssl_early_data on;
    
    # 告知客户端支持HTTP/3
    add_header Alt-Svc 'h3=":443"; ma=86400';
}
```

## Wireshark分析

### 过滤HTTP/2帧
```
# 过滤HTTP/2流量
http2

# 过滤特定流
http2.streamid == 1

# 过滤特定帧类型
http2.type == 0  # DATA帧
http2.type == 1  # HEADERS帧
http2.type == 2  # PRIORITY帧
```

### 分析QUIC
```
# 解密QUIC (需要密钥)
# 设置SSLKEYLOGFILE环境变量
export SSLKEYLOGFILE=/tmp/ssl-keys.log

# Wireshark中配置
# Preferences → Protocols → TLS → (Pre)-Master-Secret log filename
```

## 学习要点

1. HTTP版本演进和设计动机
2. 二进制分帧和多路复用原理
3. HPACK/QPACK压缩算法
4. QUIC协议优势
5. 实际部署和调优
