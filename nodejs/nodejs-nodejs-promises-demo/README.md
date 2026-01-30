# Node.js Promises 实战演示

## 简介
本项目通过三个具体场景展示 JavaScript 中 `Promise` 的核心用法：基本使用、链式调用与错误处理、并发控制。帮助开发者深入理解异步编程的最佳实践。

## 学习目标
- 理解 Promise 的三种状态（pending, fulfilled, rejected）
- 掌握 Promise 链式调用和错误捕获
- 使用 Promise.all 控制并发请求
- 实践 async/await 语法糖的使用

## 环境要求
- Node.js 版本：v14.0 或更高（推荐 v16+）
- 操作系统：Windows、Linux、macOS 均支持
- 包管理器：npm（随 Node.js 自动安装）

## 安装依赖的详细步骤
1. 打开终端（命令行工具）
2. 进入项目根目录
3. 执行以下命令安装依赖（本项目无外部依赖，无需安装）

> 注意：本 demo 仅使用 Node.js 内置模块，无需额外依赖

## 文件说明
- `basic-promise.js`：演示 Promise 基本创建与使用
- `chained-handling.js`：展示链式调用与错误处理机制
- `concurrent-requests.js`：模拟并发 API 请求并使用 Promise.all 控制执行

## 逐步实操指南

### 步骤 1：检查 Node.js 版本
```bash
node --version
```
**预期输出**：
```bash
v16.14.0  # 或更高版本
```

### 步骤 2：运行第一个示例
```bash
node basic-promise.js
```
**预期输出**：
```bash
用户加载成功: Alice
```

### 步骤 3：运行第二个示例
```bash
node chained-handling.js
```
**预期输出**：
```bash
处理结果: 数据已验证并通过格式化
```

### 步骤 4：运行第三个示例
```bash
node concurrent-requests.js
```
**预期输出**：
```bash
所有请求完成: [ '结果1', '结果2', '结果3' ]
```

## 代码解析

### basic-promise.js
```js
const user = fetchUser(1); // 返回 Promise
user.then(...) // 注册成功回调
     .catch(...) // 注册失败回调
```
展示了如何创建和消费 Promise。

### chained-handling.js
```js
validateData(data)
  .then(formatData)
  .then(processData)
  .catch(err => console.error('流程失败:', err));
```
体现链式调用中每一步返回新 Promise，并统一错误处理。

### concurrent-requests.js
```js
Promise.all([fetchData(1), fetchData(2), fetchData(3)])
  .then(results => console.log('所有请求完成:', results));
```
利用 `Promise.all` 并发执行多个异步任务，提升性能。

## 预期输出示例
完整运行三段代码后应看到如下输出：
```
用户加载成功: Alice
处理结果: 数据已验证并通过格式化
所有请求完成: [ '结果1', '结果2', '结果3' ]
```

## 常见问题解答

**Q1: 为什么不用回调函数而用 Promise？**
A: Promise 解决了“回调地狱”问题，提供更好的可读性、错误处理和链式调用能力。

**Q2: Promise.all 失败时会发生什么？**
A: 只要其中一个 Promise 被 reject，整个 all 就会立即 reject，可使用 `.catch` 捕获。

**Q3: 如何在旧版浏览器运行？**
A: 本项目为 Node.js 环境设计，如需浏览器兼容，请使用 Babel 编译或 polyfill。

## 扩展学习建议
- 学习 `async/await` 语法（基于 Promise 的语法糖）
- 探索 `Promise.race`, `Promise.any`, `Promise.allSettled`
- 阅读 MDN 文档：[https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Using_promises](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Using_promises)
- 实践在 Express.js 中使用 Promise 处理路由异步逻辑