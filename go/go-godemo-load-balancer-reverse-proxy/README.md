# Go负载均衡与反向代理Demo

## 简介
本项目是一个使用Go语言实现的轻量级反向代理和负载均衡器，支持轮询策略分发请求到多个后端服务。适用于理解微服务架构中的网关核心机制。

## 学习目标
- 掌握Go中`net/http/httputil`构建反向代理
- 实现简单的轮询负载均衡算法
- 理解反向代理在分布式系统中的作用
- 学会并发安全地管理共享状态（后端健康状态）

## 环境要求
- Go 1.20 或更高版本
- 支持Windows、Linux、macOS

## 安装依赖步骤
无需外部依赖，仅使用标准库。

```bash
# 检查Go版本
go version
# 输出应类似：go version go1.21.0 darwin/amd64
```

## 文件说明
- `main.go`: 主程序，启动反向代理服务器
- `backend.go`: 模拟两个后端HTTP服务

## 逐步实操指南

### 第一步：创建项目目录并进入
```bash
mkdir lb-proxy-demo && cd lb-proxy-demo
```

### 第二步：保存以下代码文件
将 `main.go` 和 `backend.go` 内容分别复制保存到对应文件中。

### 第三步：运行后端服务（在不同终端）
```bash
# 终端1：启动后端1
go run backend.go :8081 "Hello from Backend 1"

# 终端2：启动后端2
go run backend.go :8082 "Hello from Backend 2"
```

预期输出：
```text
Backend server starting on :8081 with message: Hello from Backend 1
```

### 第四步：启动反向代理
新开终端运行：
```bash
go run main.go
```

预期输出：
```text
Reverse proxy server starting on :8000
Load balancing requests between :8081 and :8082
```

### 第五步：发送请求测试负载均衡
```bash
curl http://localhost:8000
# 第一次可能返回：Hello from Backend 1
# 第二次可能返回：Hello from Backend 2
```

重复执行多次，观察轮询效果。

## 代码解析

### `main.go` 关键点
- 使用 `httputil.NewSingleHostReverseProxy` 创建代理对象
- 自定义 `RoundTripper` 实现轮询选择后端
- 使用 `sync.Mutex` 保证索引访问的线程安全
- 动态更新代理目标URL

### `backend.go` 说明
提供最简HTTP服务，返回指定消息，用于模拟真实后端节点。

## 预期输出示例
```text
Reverse proxy server starting on :8000
Load balancing requests between :8081 and :8082
Serving request via backend: http://localhost:8081
Serving request via backend: http://localhost:8082
```

## 常见问题解答

**Q: 请求总是打到同一个后端？**
A: 检查是否两个后端都已正确启动，并确认代理服务重启过（避免连接复用缓存）。

**Q: 出现连接拒绝错误？**
A: 确保后端服务先于代理启动，并监听正确的地址和端口。

**Q: 如何扩展为更多后端？**
A: 修改 `backends` 切片添加新URL即可。

## 扩展学习建议
- 添加健康检查机制自动剔除不可用节点
- 实现加权轮询或最少连接算法
- 引入TLS支持HTTPS代理
- 使用etcd/zookeeper做后端服务发现
- 集成Prometheus进行流量监控