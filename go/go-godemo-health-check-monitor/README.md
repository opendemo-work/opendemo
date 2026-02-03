# Go健康检查服务监控Demo

## 简介
本项目演示如何使用Go语言构建一个简单但功能完整的健康检查（Health Check）服务监控系统。该系统可以用于微服务架构中，对外暴露`/health`端点供负载均衡器或Kubernetes探针调用，同时支持自定义组件状态检测（如数据库、缓存等）。

## 学习目标
- 掌握Go中构建HTTP健康检查端点的方法
- 理解服务健康状态的设计模式
- 学会如何扩展健康检查以包含外部依赖项
- 实践Go语言的最佳实践：结构化日志、错误处理、HTTP路由

## 环境要求
- Go 1.20 或更高版本
- 操作系统：Windows / Linux / macOS（跨平台兼容）
- 命令行工具（终端）

## 安装依赖的详细步骤
1. 确保已安装Go环境：
   ```bash
   go version
   # 预期输出：go version go1.20.x linux/amd64（或其他平台）
   ```

2. 初始化Go模块（如果尚未初始化）：
   ```bash
   go mod init healthcheck-demo
   ```

3. 本项目无外部第三方依赖，仅使用标准库，无需额外安装。

## 文件说明
- `main.go`：主HTTP服务器，提供`/health`健康检查接口
- `health_checker.go`：健康检查逻辑封装，支持多组件状态聚合
- `README.md`：本说明文档

## 逐步实操指南

### 步骤1：创建项目目录并进入
```bash
mkdir healthcheck-demo && cd healthcheck-demo
```

### 步骤2：复制代码文件
将以下两个文件内容保存到对应路径：

创建 `main.go`：
```bash
touch main.go
```

将 `main.go` 的代码粘贴进去。

创建 `health_checker.go`：
```bash
touch health_checker.go
```

将 `health_checker.go` 的代码粘贴进去。

### 步骤3：运行程序
```bash
go run main.go
```

**预期输出**：
```bash
服务启动在 :8080...
```

### 步骤4：访问健康检查接口
打开新终端或浏览器，执行：
```bash
curl -s http://localhost:8080/health | python -m json.tool
```

**预期输出**：
```json
{
  "status": "healthy",
  "timestamp": "2025-04-05T12:00:00Z",
  "details": {
    "database": "ok",
    "cache": "ok"
  }
}
```

### 步骤5：模拟服务异常（可选）
修改 `health_checker.go` 中 `Check` 方法，将某个组件设为故障，重新运行并观察返回状态变为 `degraded` 或 `unhealthy`。

## 代码解析

### `health_checker.go`
- `HealthStatus` 结构体：定义健康检查的响应格式，包含总体状态、时间戳和各组件详情。
- `HealthChecker` 接口：支持未来扩展更多检查器（如数据库连接、外部API等）。
- `CompositeHealthChecker`：组合多个健康检查，统一返回聚合状态。

### `main.go`
- 使用标准库 `net/http` 启动HTTP服务。
- 注册 `/health` 路由，调用健康检查逻辑并返回JSON。
- 使用 `log` 输出启动信息，便于调试。

## 预期输出示例
```json
{
  "status": "healthy",
  "timestamp": "2025-04-05T12:00:00Z",
  "details": {
    "database": "ok",
    "cache": "ok"
  }
}
```

若某组件失败（如数据库不可用），则返回：
```json
{
  "status": "degraded",
  "timestamp": "2025-04-05T12:01:00Z",
  "details": {
    "database": "failed: connection timeout",
    "cache": "ok"
  }
}
```

## 常见问题解答

**Q1：为什么没有使用第三方库？**
A：本Demo专注于Go标准库能力展示，避免依赖复杂化，适合学习核心概念。

**Q2：如何集成数据库健康检查？**
A：可在 `CompositeHealthChecker` 中添加 `*sql.DB.Ping()` 检查，并捕获错误。

**Q3：能否用于Kubernetes liveness/readiness探针？**
A：完全可以！`/health` 返回200表示健康，非200可用于标记不健康实例。

**Q4：如何让服务在健康检查失败时返回503？**
A：修改 `main.go` 中根据 `status` 判断，若为 `unhealthy` 则设置 `w.WriteHeader(503)`。

## 扩展学习建议
- 将健康检查与 Prometheus 监控集成，暴露指标
- 添加 readiness 与 liveness 分开的端点
- 使用 context 控制检查超时
- 引入配置文件动态控制检查项
- 使用 Zap 日志库替代标准 log 以获得更好性能