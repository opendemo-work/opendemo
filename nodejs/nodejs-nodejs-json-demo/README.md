# Node.js JSON处理实战演示

## 简介
本示例展示了在Node.js中如何安全高效地处理JSON数据，包括字符串解析、对象序列化以及JSON文件的读写操作。适用于初学者学习Node.js核心模块fs和JSON API的使用。

## 学习目标
- 掌握JSON.parse() 和 JSON.stringify() 的正确用法
- 学会使用fs模块同步/异步读写JSON文件
- 理解错误处理在JSON操作中的重要性
- 遵循Node.js编码最佳实践

## 环境要求
- Node.js 版本：14.x 或更高（推荐使用 LTS 版本）
- 操作系统：Windows / macOS / Linux（跨平台兼容）
- 包管理器：npm（随Node.js自动安装）

## 安装依赖的详细步骤
此项目不依赖第三方库，仅使用Node.js内置模块，无需额外安装依赖。

## 文件说明
- `json-parser.js`：演示JSON字符串的解析与安全处理
- `json-file-io.js`：演示JSON文件的读取与写入

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir json-demo
cd json-demo
```

### 步骤2：创建代码文件
将以下两个文件内容分别保存到对应路径：
- 创建 `json-parser.js`
- 创建 `json-file-io.js`

### 步骤3：运行第一个示例
```bash
node json-parser.js
```

**预期输出**：
```
✅ 解析成功：{ name: 'Alice', age: 30, city: 'Beijing' }
🔄 序列化回字符串：{"name":"Alice","age":30,"city":"Beijing"}
⚠️ 错误输入处理完成：无效的JSON字符串
```

### 步骤4：运行第二个示例
```bash
node json-file-io.js
```

**预期输出**：
```
📄 数据已写入 data.json
💾 正在读取 data.json...
🔍 读取并解析成功：{ id: 1, message: 'Hello from JSON file!' }
```

## 代码解析

### json-parser.js 关键点
- 使用 `JSON.parse()` 将JSON字符串转为JavaScript对象
- 使用 `try/catch` 捕获非法JSON格式异常
- 使用 `JSON.stringify()` 将对象转换为标准JSON字符串

### json-file-io.js 关键点
- 使用 `fs.writeFileSync` 同步写入格式化JSON文件
- 使用 `fs.readFileSync` 读取文件内容并解析JSON
- 设置 `'utf8'` 编码确保文本正确读取
- 添加 `
` 换行符提升文件可读性

## 预期输出示例
见“逐步实操指南”中的输出部分。

## 常见问题解答

**Q1：为什么需要 try-catch 包裹 JSON.parse？**
A：因为用户输入或网络响应可能包含非法JSON，直接解析会抛出 SyntaxError 导致程序崩溃。

**Q2：可以使用异步方法替代同步读写吗？**
A：可以！生产环境建议使用 `fs.readFile` 和 `fs.writeFile` 配合 Promise 或 async/await 提升性能。

**Q3：如何美化输出的JSON文件？**
A：使用 `JSON.stringify(obj, null, 2)` 第三个参数指定缩进空格数即可。

## 扩展学习建议
- 学习使用 `fs/promises` API 实现异步非阻塞IO
- 尝试构建一个简单的REST API来接收和返回JSON数据（使用Express）
- 学习使用Joi或zod进行JSON数据验证
- 探索大型JSON文件的流式处理（stream）方式