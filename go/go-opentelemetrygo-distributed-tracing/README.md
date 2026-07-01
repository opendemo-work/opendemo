<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

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

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```


---

## 📚 扩展阅读

### 相关概念

- 概念 1：补充说明
- 概念 2：补充说明
- 概念 3：补充说明

### 常见问题

#### Q1：本案例适用于哪些场景？

**A**：本案例适用于学习、实验和工程参考。

#### Q2：如何验证运行结果？

**A**：按照 README 中的命令执行，并观察输出是否符合预期。

#### Q3：遇到问题时如何排查？

**A**：检查环境依赖是否正确安装，查看命令输出和日志信息。

### 推荐资源

- [OpenDemo 官方文档](https://github.com/opendemo)
- [相关技术官方文档](https://example.com)

### 进阶主题

- [ ] 进阶主题 1
- [ ] 进阶主题 2
- [ ] 进阶主题 3

---

*本 README 为自动生成模板，请根据实际案例内容补充完善。*


---

## 📖 深入理解

### 工作原理

OpenTelemetry分布式追踪Go示例 的核心机制可以概括为以下几个步骤：

1. **初始化阶段**：准备运行环境，加载必要的配置和依赖。
2. **执行阶段**：按照预定的流程执行主要逻辑，处理输入并生成输出。
3. **验证阶段**：检查结果是否符合预期，记录关键指标和日志。
4. **清理阶段**：释放资源，确保环境可以重复运行。

### 关键设计决策

| 决策点 | 方案 | 理由 |
|--------|------|------|
| 部署方式 | 本地容器化 | 降低环境依赖，便于复现 |
| 配置管理 | 环境变量 + 配置文件 | 灵活且安全 |
| 可观测性 | 日志 + 指标 | 便于排查和优化 |
| 扩展性 | 模块化设计 | 方便后续添加新功能 |

### 性能考量

在实际生产环境中使用本案例时，建议关注以下性能指标：

- **响应时间**：确保核心操作在可接受范围内完成。
- **资源占用**：监控 CPU、内存、磁盘和网络使用情况。
- **吞吐量**：根据业务需求评估并发处理能力。
- **错误率**：建立告警机制，及时发现异常。

---

## 🛡️ 安全与最佳实践

### 安全建议

- 不要在生产环境中使用默认密码或密钥。
- 定期更新依赖组件到最新稳定版本。
- 对敏感配置使用密钥管理工具（如 Kubernetes Secrets、Vault）。
- 限制网络暴露面，使用防火墙或安全组控制访问。

### 最佳实践

- 在修改配置前备份现有环境。
- 使用版本控制管理所有配置文件和脚本。
- 编写自动化测试覆盖核心路径。
- 记录运行日志，便于审计和故障排查。

---

## 🧪 进阶实验

完成基础演示后，可以尝试以下进阶实验：

1. **参数调优**：修改关键配置参数，观察对结果的影响。
2. **故障注入**：故意制造错误，验证系统的容错能力。
3. **压力测试**：增加负载，评估系统瓶颈。
4. **集成测试**：将本案例与其他组件组合，构建完整链路。

---

## 📚 扩展资源

### 官方文档

- [相关技术官方文档](https://example.com)
- [OpenDemo 项目主页](https://github.com/opendemo)

### 推荐书籍

- 《相关技术权威指南》
- 《云原生架构实践》

### 社区与论坛

- Stack Overflow 相关标签
- GitHub Discussions
- 技术博客与公众号

---

## 🤝 贡献与反馈

如果你发现本案例有任何问题，或希望补充更多内容，欢迎提交 Issue 或 Pull Request。

---

*本 README 为 OpenDemo 五星案例标准模板，请根据实际案例内容持续完善。*
