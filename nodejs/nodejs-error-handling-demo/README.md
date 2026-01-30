# NodeJS错误处理实战演示

## 简介
本演示项目展示了在Node.js环境中如何正确处理同步、异步以及基于Promise的代码中的错误。通过三个独立示例，帮助开发者掌握现代JavaScript中健壮的错误处理技术。

## 学习目标
- 理解同步与异步错误的区别
- 掌握 try-catch 在同步和异步函数中的使用
- 学会处理 Promise 链中的拒绝（rejection）
- 遵循行业最佳实践进行错误日志记录和传递

## 环境要求
- Node.js >= 14.0.0
- 操作系统：Windows / Linux / macOS（跨平台兼容）

## 安装依赖的详细步骤
1. 确保已安装Node.js：打开终端运行 `node --version`
2. 若未安装，请访问 https://nodejs.org 下载并安装LTS版本
3. 克隆或创建项目目录，并进入该目录
4. 无需第三方包，仅使用Node.js内置功能

## 文件说明
- `sync-error.js`：演示同步操作中的错误捕获
- `async-error.js`：演示 async/await 中的错误处理
- `promise-chain.js`：演示 Promise 链中的 .catch() 使用
- `package.json`：基础项目配置文件

## 逐步实操指南

### 步骤 1: 创建项目结构
```bash
mkdir error-demo
cd error-demo
npm init -y
```

### 步骤 2: 运行同步错误示例
```bash
node sync-error.js
```
**预期输出**：
```
[SYNC] 开始执行可能出错的操作...
[SYNC] 错误被捕获: 发生了一个同步错误！
[SYNC] 程序继续运行，未崩溃。
```

### 步骤 3: 运行异步错误示例
```bash
node async-error.js
```
**预期输出**：
```
[ASYNC] 异步操作开始...
[ASYNC] 错误被捕获: 异步任务失败：网络请求超时
[ASYNC] 错误已妥善处理，程序正常退出。
```

### 步骤 4: 运行 Promise 链示例
```bash
node promise-chain.js
```
**预期输出**：
```
[PROMISE] 开始一连串异步操作...
[PROMISE] 第一步完成：数据已加载
[PROMISE] 第二步完成：数据已处理
[PROMISE] 错误被捕获: 第三步模拟失败
[PROMISE] 整个流程结束，错误被集中处理。
```

## 代码解析

### sync-error.js
使用标准 `try...catch` 捕获同步抛出的错误。关键点是 `throw new Error()` 能被立即捕获。

### async-error.js
`async/await` 必须配合 `try/catch` 使用。`await` 会等待Promise拒绝，并将其转为可捕获的异常。

### promise-chain.js
`.then()` 链中任意环节出错都会跳转到最终的 `.catch()`，实现集中错误处理，适合复杂流程。

## 预期输出示例（汇总）
所有脚本应输出清晰的错误信息而不导致进程非正常终止。控制台不应出现未捕获的异常堆栈。

## 常见问题解答

**Q: 为什么 async 函数内的错误需要用 try/catch？**
A: 因为即使函数是异步的，`await` 会让错误表现得像同步一样，必须显式捕获。

**Q: 如果不写 catch 会发生什么？**
A: Node.js 会抛出 UnhandledPromiseRejectionWarning，未来版本将直接终止程序。

**Q: 如何全局监听未捕获的异常？**
A: 可监听 `process.on('unhandledRejection')` 和 `process.on('uncaughtException')`，但应尽量避免依赖它。

## 扩展学习建议
- 学习使用 Winston 或 Pino 进行结构化错误日志记录
- 了解 Express 中间件中的错误处理机制
- 阅读 MDN 文档关于 Error 对象和自定义错误类型