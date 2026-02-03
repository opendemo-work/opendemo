# OpenTelemetry分布式追踪Go示例

## 简介
本项目是一个完整的Go语言示例，演示如何使用OpenTelemetry SDK实现本地和跨服务的分布式链路追踪。通过此Demo，开发者可以学习如何在微服务架构中集成追踪能力，并将数据导出到Jaeger或OTLP兼容的后端（如OpenTelemetry Collector）。

## 学习目标
- 理解OpenTelemetry的核心概念：Tracer、Span、Context传递
- 掌握在Go服务中初始化TracerProvider并配置导出器
- 实现同步与异步操作中的Span创建与上下文传播
- 将追踪数据发送至Jaeger进行可视化查看

## 环境要求
- Go 1.20 或更高版本
- Docker（用于运行Jaeger或OTel Collector）
- `go mod` 包管理工具

## 安装依赖
```bash
# 克隆项目（假设已下载代码）
go mod init otel-demo
go mod tidy
```

## 文件说明
- `main.go`：主程序，展示基本的Tracer初始化和Span创建
- `worker.go`：模拟后台任务，在独立goroutine中正确传递上下文
- `docker-compose.yml`（可选，未包含但推荐）：启动Jaeger UI

## 逐步实操指南

### 步骤1：启动Jaeger（使用Docker）
```bash
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest
```

> 预期输出：容器成功启动，可通过 http://localhost:16686 访问Jaeger UI

### 步骤2：运行Go程序
```bash
go run main.go
```

> 预期输出：
```
Worker task completed.
Press Enter to exit...
```

### 步骤3：查看追踪结果
打开浏览器访问 [http://localhost:16686](http://localhost:16686)，选择服务 `otel-demo`，点击“Find Traces”，应能看到生成的调用链。

## 代码解析

### main.go
- 初始化`TracerProvider`，配置OTLP导出器指向本地4317端口（Jaeger支持）
- 获取全局Tracer实例
- 创建父Span并在其Context下启动子任务

### worker.go
- 演示如何在Goroutine中安全传递`context.Context`以保持Span链路连续
- 使用`trace.SpanFromContext`恢复Span并记录事件

## 预期输出示例（控制台）
```
INFO: Initializing OpenTelemetry...
INFO: Starting parent span...
INFO: Launching background worker...
INFO: Worker processing work...
INFO: Worker task completed.
Press Enter to exit...
```

在Jaeger UI中，应看到至少两个Span：
- parent-span
  └── worker-span

## 常见问题解答

**Q: 追踪数据没有出现在Jaeger？**
A: 检查Jaeger是否监听4317（gRPC）或4318（HTTP），确保网络可达；确认Go程序使用的endpoint正确。

**Q: 如何改为使用HTTP协议导出？**
A: 修改`otlptracegrpc.New`为`otlptracehttp.New`，并将端口改为4318。

**Q: 跨服务如何传递上下文？**
A: 使用`propagation.TraceContext{} `注入到HTTP Header中，在接收端提取恢复Context。

## 扩展学习建议
- 添加Metrics和Logs集成，实现全栈可观测性
- 在gin或echo等Web框架中集成中间件自动追踪请求
- 使用OpenTelemetry Collector对数据做处理与路由
- 探索Baggage API传递业务上下文信息
