# Node.js Buffer 操作实战演示

## 简介
本示例演示了在 Node.js 中如何使用 `Buffer` 处理二进制数据。Buffer 是 Node.js 的核心模块之一，用于在没有 DOM ArrayBuffer 的环境中操作原始二进制数据。本 demo 展示了三种典型场景：字符串与 Buffer 的转换、Buffer 与文件流的结合使用、以及多个 Buffer 的拼接。

## 学习目标
- 理解 Buffer 的作用及其在 Node.js 中的重要性
- 掌握字符串与 Buffer 之间的编码/解码方法
- 学会处理流式二进制数据
- 掌握多个 Buffer 的安全拼接方式

## 环境要求
- Node.js 版本：v14.x 或更高（推荐 v16+）
- 操作系统：Windows、macOS、Linux 均支持
- 包管理器：npm（随 Node.js 自动安装）

## 安装依赖的详细步骤
1. 确保已安装 Node.js 和 npm
   ```bash
   node --version
   npm --version
   ```
   预期输出示例：
   ```
   v16.15.0
   8.10.0
   ```
2. 克隆项目或创建目录并进入
   ```bash
   mkdir buffer-demo && cd buffer-demo
   ```
3. 初始化 npm 项目（可选，仅用于结构化）
   ```bash
   npm init -y
   ```
4. 将以下三个文件按路径创建：
   - `buffer-string.js`
   - `buffer-stream.js`
   - `buffer-concat.js`

## 文件说明
- `buffer-string.js`：演示字符串与 Buffer 的相互转换，包括 UTF-8 和 Base64 编码
- `buffer-stream.js`：使用 Buffer 创建可读流，并模拟网络传输场景
- `buffer-concat.js`：展示如何安全地合并多个 Buffer 实例

## 逐步实操指南

### 步骤 1：运行字符串与 Buffer 转换示例
```bash
node buffer-string.js
```
**预期输出**：
```text
原始字符串: Hello, Buffer!
UTF-8 Buffer: <Buffer 48 65 6c 6c 6f 2c 20 42 75 66 66 65 72 21>
从 Buffer 解码: Hello, Buffer!
Base64 编码: SGVsbG8sIEJ1ZmZlciE=
从 Base64 解码: Hello, Buffer!
```

### 步骤 2：运行流式 Buffer 示例
```bash
node buffer-stream.js
```
**预期输出**：
```text
正在通过流发送数据块...
数据块接收: H
数据块接收: e
数据块接收: l
...
流结束，传输完成。
```

### 步骤 3：运行 Buffer 拼接示例
```bash
node buffer-concat.js
```
**预期输出**：
```text
分段 Buffer: <Buffer 48 65 6c 6c 6f>, <Buffer 20>, <Buffer 57 6f 72 6c 64>
合并后的 Buffer: <Buffer 48 65 6c 6c 6f 20 57 6f 72 6c 64>
最终字符串: Hello World
```

## 代码解析

### buffer-string.js
```js
// 使用 Buffer.from() 将字符串转为 Buffer，默认 UTF-8
const buf = Buffer.from(str);
// 使用 toString() 将 Buffer 解码回字符串
buf.toString(); // 默认 'utf8'
// 支持 Base64 编码
Buffer.from(str).toString('base64');
```

### buffer-stream.js
```js
const { Readable } = require('stream');
// 创建一个可读流，每次 push 一个字节的 Buffer
_readableState.push(chunk);
_readableState.push(null); // 结束信号
```
该模式常用于处理大文件或网络数据流，避免内存溢出。

### buffer-concat.js
```js
// 使用 Buffer.concat() 安全合并多个 Buffer
const merged = Buffer.concat([buf1, buf2, buf3]);
```
这是官方推荐的合并方式，性能优于字符串拼接或循环写入。

## 预期输出示例（综合）
所有脚本运行成功后，应分别输出上述各段所示内容，无错误信息。

## 常见问题解答

**Q: 为什么不能直接用字符串处理二进制数据？**
A: JavaScript 字符串是 Unicode 编码的，无法准确表示原始字节（如图片、音频），而 Buffer 可以精确控制每个字节。

**Q: Buffer 是不是已经废弃了？**
A: 否。尽管现代 JS 有 ArrayBuffer，但 Buffer 仍是 Node.js 中处理 I/O 的标准方式，且被广泛支持。

**Q: 如何避免 Buffer 内存泄漏？**
A: 避免创建超大 Buffer；使用流处理大数据；及时释放引用。

## 扩展学习建议
- 学习 Node.js Stream API（Readable/Writable/Duplex）
- 阅读官方文档：https://nodejs.org/api/buffer.html
- 实践：用 Buffer 读取并分析 PNG 文件头
- 探索 TypedArray 与 Buffer 的互操作性