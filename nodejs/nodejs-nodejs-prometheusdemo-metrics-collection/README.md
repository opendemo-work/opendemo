# Node.js Prometheus监控指标采集Demo

## 简介
本示例演示如何在Node.js应用中集成Prometheus指标采集功能，通过HTTP端点暴露系统和自定义业务指标，供Prometheus服务器抓取。

## 学习目标
- 理解Prometheus监控的基本原理
- 掌握在Node.js中使用`prom-client`库暴露指标
- 学会创建自定义计数器、直方图等指标类型
- 能够配置Express应用以提供/metrics端点

## 环境要求
- Node.js 16.x 或更高版本
- npm（随Node.js自动安装）
- 命令行工具（支持Windows PowerShell、Linux/macOS Terminal）

## 安装依赖的详细步骤

1. 打开终端，进入项目目录：
```bash
npm init -y
```

2. 安装所需依赖：
```bash
npm install express prom-client
```

## 文件说明
- `server.js`: 主服务文件，启动Express服务器并注册指标
- `metrics.js`: 定义和收集自定义监控指标
- `README.md`: 本说明文档

## 逐步实操指南

### 步骤1: 启动服务
运行以下命令启动Node.js应用：
```bash
node server.js
```

**预期输出**：
```
Server is running on http://localhost:3000
访问 http://localhost:3000/metrics 查看Prometheus指标
```

### 步骤2: 访问指标端点
打开浏览器或使用curl访问：
```bash
curl http://localhost:3000/metrics
```

**预期输出**：
返回格式为Prometheus文本格式的指标数据，包含HTTP请求数、响应时间、自定义事件计数等。

### 步骤3: 观察指标变化
刷新页面几次，再次请求 `/metrics`，观察计数器数值是否增长。

## 代码解析

### server.js 关键部分
```js
// 创建Express应用并暴露/metrics端点
app.get('/metrics', async (req, res) => {
  const metrics = await client.register.metrics();
  res.set('Content-Type', client.register.contentType);
  res.end(metrics);
});
```
此路由将收集所有已注册的指标，并以Prometheus兼容格式返回。

### metrics.js 中的自定义指标
```js
// 创建请求计数器
const httpRequestCounter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests made',
  labelNames: ['method', 'route', 'status_code']
});
```
该计数器按HTTP方法、路径和状态码维度统计请求数量，便于后续分析。

## 预期输出示例
```
# HELP http_requests_total Total number of HTTP requests made
# TYPE http_requests_total counter
http_requests_total{method="GET",route="/",status_code="200"} 5
http_requests_total{method="GET",route="/metrics",status_code="200"} 3

# HELP api_response_time_milliseconds API请求响应时间（毫秒）
# TYPE api_response_time_milliseconds histogram
...更多指标...
```

## 常见问题解答

**Q: /metrics 返回404？**
A: 检查是否正确注册了`/metrics`路由，并确认Express服务器已启动。

**Q: 指标没有更新？**
A: 确保在处理请求时调用了`.inc()`或`.observe()`方法来记录数据。

**Q: 如何让Prometheus抓取这些指标？**
A: 在Prometheus配置文件中添加job指向 `localhost:3000` 和路径 `/metrics`。

## 扩展学习建议
- 将指标推送至Pushgateway（适用于批处理任务）
- 集成Grafana可视化指标
- 添加系统级指标（内存、CPU）
- 使用Kubernetes部署并配置ServiceMonitor