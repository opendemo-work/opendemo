# async-await-nodejs-demo

## 简介
本项目是一个用于学习和理解 Node.js 中 `async` 和 `await` 语法的实践性演示。通过三个具体场景，展示如何使用现代异步编程模式处理异步操作，包括模拟 API 调用、顺序与并行执行、错误处理等。

## 学习目标
- 理解 `async/await` 的基本语法和工作原理
- 掌握如何用 `await` 等待 Promise 完成
- 学会处理异步函数中的错误（try/catch）
- 区分串行与并行异步操作

## 环境要求
- Node.js 版本：14.x 或更高（推荐 16+）
- 操作系统：Windows、macOS、Linux 均支持
- 包管理器：npm（随 Node.js 自动安装）

## 安装依赖的详细步骤
1. 确保已安装 Node.js 和 npm
   ```bash
   node --version
   npm --version
   ```
   预期输出类似：
   ```
   v16.14.0
   8.3.1
   ```

2. 初始化项目（如果尚未有 package.json）
   ```bash
   npm init -y
   ```

3. 本项目无外部依赖，无需额外安装包。

## 文件说明
- `example1.js`: 模拟用户数据获取，展示基础 async/await 用法
- `example2.js`: 展示多个异步任务的串行与并行执行差异
- `example3.js`: 演示 async 函数中的错误处理机制

## 逐步实操指南

### 步骤 1: 创建代码文件
创建以下三个文件并粘贴对应内容：

```bash
mkdir -p code
# 或在 Windows 上使用 mkdir code
```

### 步骤 2: 运行第一个示例
```bash
node code/example1.js
```
**预期输出**：
```text
正在获取用户信息...
用户姓名：Alice
```

### 步骤 3: 运行第二个示例
```bash
node code/example2.js
```
**预期输出**：
```text
【串行执行】
任务1完成
任务2完成
总耗时约2秒

【并行执行】
两个任务都已完成
总耗时约1秒
```

### 步骤 4: 运行第三个示例
```bash
node code/example3.js
```
**预期输出**：
```text
尝试获取受保护资源...
错误被捕获：访问被拒绝！
异步操作继续执行
```

## 代码解析

### example1.js
```js
async function fetchUser() {
  return new Promise(resolve => {
    setTimeout(() => resolve({ name: 'Alice' }), 1000);
  });
}
```
- 使用 `async` 定义异步函数，自动返回 Promise
- `await` 用于暂停函数执行直到 Promise 解析

### example2.js
- `await task1(); await task2();` 是串行：等待一个完成再开始下一个
- `await Promise.all([task1(), task2()])` 是并行：同时启动所有任务，等待全部完成

### example3.js
- 使用 try/catch 捕获 async 函数中抛出的错误
- 即使出错，程序也不会崩溃，可继续执行后续逻辑

## 预期输出示例
完整运行三个文件后，应看到如上所述的清晰输出，表明 async/await 正确工作。

## 常见问题解答

**Q: await 只能在 async 函数中使用吗？**
A: 是的，否则会报语法错误。

**Q: async 函数总是返回 Promise 吗？**
A: 是的，即使返回普通值，也会被包装成 Promise.resolve(value)。

**Q: 如何调试 async/await 代码？**
A: 可使用 `console.log` 或 VS Code 调试器设置断点，行为与同步代码类似。

## 扩展学习建议
- 阅读 MDN 文档：[Async/Await](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function)
- 学习 Promise.race() 和 Promise.any() 的使用
- 实践在 Express.js 中使用 async/await 处理路由