# NodeJS请求重试与指数退避机制实战Demo

## 简介
本项目演示了在Node.js环境中如何实现**请求重试（Retry）**与**指数退避（Exponential Backoff）**机制，用于增强网络请求的健壮性。当服务暂时不可用或出现网络抖动时，该机制能自动重试请求，避免程序因短暂故障而失败。

## 学习目标
- 理解指数退避的基本原理
- 掌握在Node.js中实现请求重试的多种方式
- 学会使用`axios`和原生`fetch`进行可重试的HTTP调用
- 提升异步编程和错误处理能力

## 环境要求
- Node.js 16.x 或更高版本
- npm 包管理器（随Node.js安装）

## 安装依赖步骤
1. 打开终端（Terminal）或命令提示符
2. 进入项目根目录：
   ```bash
   cd path/to/your/project
   ```
3. 安装所需依赖：
   ```bash
   npm install axios node-fetch
   ```

## 文件说明
- `retryWithAxios.js`：使用 Axios 实现带指数退避的请求重试
- `retryWithFetch.js`：使用 node-fetch + 自定义逻辑实现重试机制
- `package.json`：依赖声明文件（已包含在项目中）

## 逐步实操指南

### 步骤1：创建项目目录并初始化
```bash
mkdir retry-demo && cd retry-demo
npm init -y
```

### 步骤2：安装依赖
```bash
npm install axios node-fetch
```

### 步骤3：运行第一个示例（Axios）
```bash
node retryWithAxios.js
```

**预期输出**：
```
尝试第 1 次请求...
请求失败: Error: Request failed with status code 500, 2秒后重试
尝试第 2 次请求...
请求成功! 响应数据: {"message":"Success after retry"}
```

### 步骤4：运行第二个示例（Fetch）
```bash
node retryWithFetch.js
```

**预期输出**：
```
尝试第 1 次请求 (延迟 1000ms)...
请求失败: Server error, 重试中... 当前延迟: 2000ms
尝试第 2 次请求 (延迟 2000ms)...
请求成功: {"message":"OK"}
```

## 代码解析

### `retryWithAxios.js`
- 使用 `axios` 的拦截器和手动重试逻辑结合
- `exponentialBackoff` 函数根据尝试次数计算延迟时间：`delay = baseDelay * 2^(attempt - 1)`
- 最多重试3次，每次间隔呈指数增长（1s → 2s → 4s）
- 捕获 HTTP 5xx 错误并触发重试

### `retryWithFetch.js`
- 使用原生 `fetch` API（通过 node-fetch）
- 手动实现异步重试循环和延迟等待（`new Promise(resolve => setTimeout(resolve, delay))`）
- 支持自定义最大重试次数和基础延迟
- 更灵活地控制重试条件

## 预期输出示例
见“逐步实操指南”中的输出示例。

## 常见问题解答

**Q1: 为什么选择指数退避而不是固定间隔？**
A: 指数退避可以避免大量客户端同时重试造成“雪崩效应”，给服务器恢复留出时间。

**Q2: 如何限制最大重试延迟？**
A: 可以在计算延迟时加入上限，例如 `Math.min(delay, 10000)` 表示最大10秒。

**Q3: 能否取消重试？**
A: 可以引入 AbortController 实现超时或手动取消。

## 扩展学习建议
- 学习使用 `p-retry`、`async-retry` 等第三方库简化重试逻辑
- 结合 Circuit Breaker 模式提升系统弹性
- 在生产环境中集成日志记录和监控（如 Sentry、Prometheus）
- 探索 TypeScript 版本以增强类型安全