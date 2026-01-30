# Node.js HTTP模块实战演示

## 简介
本示例演示了如何使用Node.js内置的`http`模块创建Web服务器、处理请求与响应，以及发起HTTP客户端请求。包含三个典型场景：基础服务器、REST风格API响应、HTTP客户端请求。

## 学习目标
- 掌握Node.js中`http`模块的基本用法
- 学会创建HTTP服务器并处理不同路径请求
- 理解如何构建结构化响应（如JSON）
- 学会使用`http`模块作为客户端发起请求

## 环境要求
- Node.js 版本：v14.x 或更高（推荐v16+）
- 操作系统：Windows / Linux / macOS（跨平台兼容）
- 命令行工具（如终端、PowerShell、bash）

## 安装依赖
本项目仅使用Node.js内置模块，无需额外安装依赖。

## 文件说明
- `server.js`: 启动一个本地HTTP服务器，响应不同路由
- `client.js`: 使用http模块向本地服务器发起GET请求
- `api-server.js`: 模拟一个返回JSON数据的REST风格接口

## 逐步实操指南

### 步骤1：启动API服务器
运行以下命令启动返回JSON的服务器：
```bash
node api-server.js
```
**预期输出**：
```
API服务器运行在 http://localhost:3001
```

### 步骤2：启动主服务器
打开新终端窗口，运行：
```bash
node server.js
```
**预期输出**：
```
服务器运行在 http://localhost:3000
```

### 步骤3：运行客户端请求
在另一个终端中执行：
```bash
node client.js
```
**预期输出**：
```
状态码: 200
响应内容: {\"message\":\"Hello from API!\",\"timestamp\":...}
```

## 代码解析

### server.js
创建一个基础HTTP服务器，监听`/`和`/about`路径，返回HTML响应。展示了如何设置响应头、状态码和写入响应体。

### api-server.js
模拟一个简单的REST API端点，返回JSON格式数据，并正确设置`Content-Type`为`application/json`。

### client.js
使用`http.get()`方法作为客户端向`api-server.js`发起请求，通过流的方式接收数据并拼接输出。

## 预期输出示例
```
# node api-server.js
API服务器运行在 http://localhost:3001

# node server.js
服务器运行在 http://localhost:3000

# node client.js
状态码: 200
响应内容: {"message":"Hello from API!","timestamp":1712345678901}
```

## 常见问题解答

**Q: 运行时报错 'Address already in use'？**
A: 说明端口被占用。请检查是否有其他程序占用了3000或3001端口，或修改代码中的端口号。

**Q: 客户端收不到数据？**
A: 确保`api-server.js`已先启动。客户端请求的是本地3001端口，服务未启动则连接失败。

**Q: 如何支持POST请求？**
A: 可以监听`'data'`事件收集请求体，然后在`'end'`事件中处理。本示例聚焦GET，但原理类似。

## 扩展学习建议
- 尝试添加POST请求处理逻辑
- 使用`url`模块解析查询参数
- 进一步学习Express.js框架，它基于http模块提供了更高层的抽象
- 结合`fs`模块实现静态文件服务器