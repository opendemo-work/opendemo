# Node.js文件系统操作演示

## 简介
本项目是一个简单的Node.js演示程序，展示了如何使用内置的`fs`（文件系统）模块进行常见的文件操作，包括文件读取、写入、追加和目录管理。所有代码均遵循最佳实践，并支持跨平台运行（Windows/Linux/Mac）。

## 学习目标
- 掌握Node.js中fs模块的基本用法
- 理解同步与异步文件操作的区别
- 学会处理文件路径和错误捕获
- 实践Node.js的错误优先回调模式

## 环境要求
- Node.js 14.x 或更高版本
- npm（随Node.js自动安装）

## 安装依赖的详细步骤
此项目仅使用Node.js内置模块，无需额外安装依赖。

1. 确保已安装Node.js：
   ```bash
   node --version
   ```
   预期输出：`v14.0.0` 或更高版本

2. 克隆或创建项目目录并进入：
   ```bash
   mkdir fs-demo && cd fs-demo
   ```

3. 将以下文件保存到项目根目录：
   - `file-write.js`
   - `file-read.js`
   - `dir-create.js`

## 文件说明
- `file-write.js`: 演示如何异步写入文件
- `file-read.js`: 演示如何安全地读取文件内容
- `dir-create.js`: 创建目录并写入测试文件

## 逐步实操指南

### 步骤1：运行文件写入示例
```bash
node file-write.js
```
**预期输出**：
```
文件已成功写入: hello.txt
```

### 步骤2：运行文件读取示例
```bash
node file-read.js
```
**预期输出**：
```
文件内容: Hello, this is a test file created with Node.js fs module.
```

### 步骤3：运行目录创建示例
```bash
node dir-create.js
```
**预期输出**：
```
目录 'logs' 已创建或已存在
日志文件已写入: logs/app.log
```

## 代码解析

### `file-write.js`
```js
const fs = require('fs');
```
引入Node.js内置的fs模块。

```js
fs.writeFile('hello.txt', 'Hello, this is a test file created with Node.js fs module.', 'utf8', (err) => {
```
使用异步方式写入文件，避免阻塞主线程。指定编码为UTF-8以确保文本正确存储。

### `file-read.js`
```js
fs.readFile('hello.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('读取文件时出错:', err.message);
    return;
  }
  console.log('文件内容:', data);
});
```
采用错误优先回调模式，先检查错误再处理数据，这是Node.js的标准做法。

### `dir-create.js`
```js
fs.mkdir('logs', { recursive: true }, (err) => {
```
使用 `{ recursive: true }` 可安全创建嵌套目录而不会报错。

## 预期输出示例
完整流程输出如下：
```
$ node file-write.js
文件已成功写入: hello.txt
$ node file-read.js
文件内容: Hello, this is a test file created with Node.js fs module.
$ node dir-create.js
目录 'logs' 已创建或已存在
日志文件已写入: logs/app.log
```

## 常见问题解答

**Q: 运行时报错 `Error: EACCES`？**
A: 当前用户没有权限访问该目录，请尝试在有写权限的位置运行，如用户主目录。

**Q: 中文乱码怎么办？**
A: 确保所有文件操作都显式指定 `'utf8'` 编码，Node.js默认使用UTF-8，但明确声明更安全。

**Q: 是否可以使用Promise风格？**
A: 可以！从Node.js v8起支持 `fs.promises`，例如 `fs.promises.writeFile()`，适合配合async/await使用。

## 扩展学习建议
- 学习使用 `fs.promises` API 和 async/await 语法提升代码可读性
- 探索 `path` 模块来安全拼接文件路径
- 尝试监听文件变化：`fs.watch()`
- 了解流式文件处理：`fs.createReadStream()` / `fs.createWriteStream()`