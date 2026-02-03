# Node.js负载均衡HTTP代理Demo

## 简介
本项目演示如何使用Node.js构建一个简单的负载均衡HTTP代理服务器。它将请求分发到多个后端服务实例，提升系统的可用性和伸缩性。

## 学习目标
- 理解负载均衡的基本概念
- 掌握使用`http-proxy`实现反向代理
- 学会用轮询算法分配请求
- 构建高可用的代理网关

## 环境要求
- Node.js 16.x 或更高版本
- npm 8.x 或更高版本

## 安装依赖
```bash
npm install
```

## 文件说明
- `server.js`: 主代理服务器，实现负载均衡逻辑
- `backend.js`: 模拟多个后端服务实例
- `package.json`: 项目依赖声明

## 逐步实操指南

### 第一步：启动两个后端服务实例
```bash
node backend.js 3001
```
预期输出：
> 后端服务器运行在端口 3001

打开新终端：
```bash
node backend.js 3002
```
预期输出：
> 后端服务器运行在端口 3002

### 第二步：启动负载均衡代理
```bash
node server.js
```
预期输出：
> 负载均衡代理运行在端口 8000
> 将请求轮询转发到 [ 'http://localhost:3001', 'http://localhost:3002' ]

### 第三步：发送测试请求
```bash
curl http://localhost:8000
```
预期输出（交替出现）：
> 响应来自后端端口 3001
> 响应来自后端端口 3002

## 代码解析

### server.js 关键逻辑
```js
const proxy = httpProxy.createProxyServer();
// 创建代理实例，用于转发请求

// 轮询选择后端服务器
let currentIndex = 0;
function getNextBackend() {
  currentIndex = (currentIndex + 1) % backends.length;
  return backends[currentIndex];
}
```
- 使用轮询算法均匀分配请求
- `http-proxy`负责透明转发HTTP请求

### backend.js 功能
- 模拟多个后端服务，返回自身端口号
- 便于观察负载均衡效果

## 预期输出示例
```bash
$ curl http://localhost:8000
响应来自后端端口 3001
$ curl http://localhost:8000
响应来自后端端口 3002
$ curl http://localhost:8000
响应来自后端端口 3001
```

## 常见问题解答

**Q: 为什么请求没有轮流转发？**
A: 确保两个backend服务都已正确启动，并监听3001和3002端口。

**Q: 如何添加更多后端？**
A: 在 `server.js` 中修改 `backends` 数组即可。

**Q: 是否支持HTTPS？**
A: 当前示例为HTTP，可通过配置`http-proxy`支持HTTPS。

## 扩展学习建议
- 实现加权轮询或最少连接算法
- 添加健康检查机制
- 使用Redis共享会话状态
- 集成日志和监控（如Prometheus）
- 结合Docker部署多实例