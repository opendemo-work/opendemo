# HTTP Protocol Deep Dive

HTTP协议深度解析演示。

## HTTP/2特性

```
HTTP/2多路复用:
Stream 1: ──[HEADERS]─[DATA]─────────────────────▶
Stream 3: ────────[HEADERS]─[DATA]─[DATA]────────▶
Stream 5: ───────────────[HEADERS]─[DATA]────────▶
                  ↓
           单个TCP连接
```

## HTTP/3与QUIC

```
QUIC优势:
- 0-RTT连接建立
- 无队头阻塞
- 内置加密
- 连接迁移
```

## 性能优化

```bash
# 启用HTTP/2
curl --http2 -I https://example.com

# 检查TLS版本
openssl s_client -connect example.com:443 -tls1_3
```

## 学习要点

1. HTTP版本演进
2. 二进制分帧
3. 首部压缩
4. 性能调优
