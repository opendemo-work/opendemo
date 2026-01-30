# Node.js Streams 实战演示

## 简介
本项目通过两个实用场景演示 Node.js 中 `stream` 模块的强大功能：大文件复制与实时数据处理。流（Streams）是处理大量数据时避免内存溢出的核心机制，广泛应用于文件操作、网络请求和数据管道。

## 学习目标
- 理解可读流、可写流和双工流的基本概念
- 掌握使用 `pipe()` 方法构建数据管道
- 学会通过 Transform 流进行实时数据转换
- 了解流在处理大文件时的内存优势

## 环境要求
- Node.js >= 14.0.0（推荐使用 LTS 版本）
- npm（随 Node.js 自动安装）
- 操作系统：Windows / Linux / macOS 均支持

## 安装依赖的详细步骤
1. 确保已安装 Node.js：
   ```bash
   node --version
   ```
   预期输出：`v14.0.0` 或更高版本

2. 初始化项目并生成 package.json（如果尚未存在）：
   ```bash
   npm init -y
   ```

3. 无需额外第三方依赖，仅使用内置模块

## 文件说明
- `copy-stream.js`：使用流实现大文件安全复制
- `transform-stream.js`：使用 Transform 流实时处理数据（转为大写）
- `input.txt`：输入测试文件
- `output.txt`：复制或处理后的输出文件

## 逐步实操指南

### 步骤 1：创建测试输入文件
```bash
echo "Hello, this is a test file for Node.js streams." > input.txt
```

### 步骤 2：运行文件复制示例
```bash
node copy-stream.js
```
**预期输出**：
```
文件复制完成：input.txt → output.txt
```

### 步骤 3：运行数据转换示例
```bash
node transform-stream.js
```
**预期输出**：
```
数据处理完成，结果已写入 output.txt
```

然后查看 output.txt 内容：
```bash
cat output.txt
```
应看到全部为大写字符：
```
HELLO, THIS IS A TEST FILE FOR NODE.JS STREAMS.
```

## 代码解析

### `copy-stream.js`
- 使用 `fs.createReadStream()` 创建可读流
- 使用 `fs.createWriteStream()` 创建可写流
- 利用 `.pipe()` 自动处理背压（backpressure），无需手动管理内存
- 监听 `finish` 事件确保写入完成

### `transform-stream.js`
- 使用 `Transform` 类创建自定义转换流
- 重写 `_transform` 方法实现逐块数据处理
- 将每块数据转为大写后推送至下游
- 展示如何构建高效的数据处理管道

## 预期输出示例
```bash
$ node copy-stream.js
文件复制完成：input.txt → output.txt

$ node transform-stream.js
数据处理完成，结果已写入 output.txt

$ cat output.txt
HELLO, THIS IS A TEST FILE FOR NODE.JS STREAMS.
```

## 常见问题解答

**Q: 为什么不用 fs.readFile()？**
A: `readFile` 会将整个文件加载到内存，大文件可能导致内存溢出；而流以小块方式处理，更安全高效。

**Q: pipe 会自动处理错误吗？**
A: 不会！生产环境中应监听 `error` 事件或使用 `pipeline()` 工具函数进行更好的错误处理。

**Q: 如何提升性能？**
A: 可调整 `highWaterMark` 参数控制每次读取的字节数，根据硬件和用途优化吞吐量。

## 扩展学习建议
- 阅读官方文档 [Node.js Stream API](https://nodejs.org/api/stream.html)
- 学习 `pipeline()` 和 `promisify` 结合使用 async/await
- 探索 `Duplex` 和 `PassThrough` 流的实际应用场景
- 在 Express/Koa 中使用流传输文件响应