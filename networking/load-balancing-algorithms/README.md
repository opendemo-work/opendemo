# Load Balancing Algorithms

负载均衡算法原理与实现演示。

## 算法对比

| 算法 | 特点 | 适用场景 |
|------|------|----------|
| Round Robin | 轮询分发 | 服务器性能均衡 |
| Least Connections | 最少连接 | 长连接应用 |
| IP Hash | IP哈希 | 会话保持 |
| Weighted | 加权分发 | 服务器性能差异 |
| Consistent Hash | 一致性哈希 | 缓存场景 |

## Nginx配置

```nginx
upstream backend {
    least_conn;
    server 10.0.0.1:8080 weight=5;
    server 10.0.0.2:8080 weight=5;
    server 10.0.0.3:8080 backup;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

## 一致性哈希

```
一致性哈希环:
     0
     │
2┌───┴───┐3
 │  ●────┼────●  
 │  │Node1    │Node2
 │  │         │
1└──┼─────────┘4
    ●
   Key
```

## 学习要点

1. 负载均衡算法选择
2. 健康检查机制
3. 会话保持策略
4. 动态权重调整
