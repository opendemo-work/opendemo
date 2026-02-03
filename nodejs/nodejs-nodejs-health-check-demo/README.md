# Node.js 健康检查示例

## 简介
本示例演示如何在Node.js应用中实现标准的 **Liveness（存活）** 和 **Readiness（就绪）** 健康检查端点，常用于Kubernetes等容器编排平台中的服务监控。

## 学习目标
- 理解 liveness 与 readiness 的区别
- 实现 RESTful 健康检查接口
- 遵循行业最佳实践构建可靠服务
- 学会使用 Express 构建轻量级服务

## 环境要求
- Node.js 版本：16.x 或更高（推荐 18.x）
- npm 包管理器（随 Node.js 自动安装）
- 操作系统：Windows、Linux 或 macOS

## 安装依赖步骤
1. 打开终端（命令行工具）
2. 进入项目目录：`cd node-health-check-demo`
3. 安装依赖包：
   ```bash
   npm install
   ```

## 文件说明
- `server.js`：主服务文件，包含健康检查路由
- `config.js`：配置管理模块
- `.env`：环境变量文件
- `package.json`：依赖声明和脚本入口

## 逐步实操指南

### 第一步：初始化项目（如未提供 package.json）
```bash
npm init -y
```

### 第二步：安装依赖
```bash
npm install express dotenv
```

### 第三步：启动服务器
```bash
node server.js
```

预期输出：
```bash
✅ 应用正在监听端口 3000...
➡️  Liveness: http://localhost:3000/health/liveness
➡️  Readiness: http://localhost:3000/health/readiness
```

### 第四步：测试健康检查端点
打开新终端窗口或浏览器标签页执行：

检查存活状态：
```bash
curl http://localhost:3000/health/liveness
```
预期输出：`{"status":"up"}`

检查就绪状态：
```bash
curl http://localhost:3000/health/readiness
```
预期输出：`{"status":"ready"}`

模拟服务未就绪（关闭数据库连接等）：
```bash
curl -X POST http://localhost:3000/debug/fail-readiness
```
再次请求 readiness 将返回 503。

## 代码解析

### `server.js` 关键逻辑
- `/health/liveness`：始终返回 200，表示进程运行中
- `/health/readiness`：可检测内部依赖（如数据库），失败时返回 503
- 使用 `app.use(express.json())` 解析 JSON 请求体

### `config.js` 设计意图
通过环境变量控制服务行为，便于多环境部署。

## 预期输出示例
启动日志：
```
✅ 应用正在监听端口 3000...
➡️  Liveness: http://localhost:3000/health/liveness
➡️  Readiness: http://localhost:3000/health/readiness
```

健康检查响应：
```json
{"status":"up"}
```

## 常见问题解答

**Q: 为什么需要两个健康检查？**
A: Liveness 判断是否重启容器；Readiness 判断是否接收流量。两者职责分离更安全。

**Q: 如何集成数据库检查？**
A: 在 readiness 中添加数据库 ping 检查逻辑，超时则返回失败。

**Q: 跨平台兼容性如何？**
A: 使用标准 Node.js API 和 Express，支持所有主流操作系统。

## 扩展学习建议
- 将此模式集成到 Kubernetes 的 probe 配置中
- 添加 Prometheus 指标暴露 `/metrics` 端点
- 使用 TypeScript 提升类型安全性
- 引入 Winston 日志库进行结构化日志记录