# Axios拦截器实战演示

## 简介
本演示项目展示了如何使用Axios HTTP客户端的请求和响应拦截器来统一处理API调用中的认证、错误处理和日志记录。通过三个具体场景，帮助开发者掌握拦截器的核心用法。

## 学习目标
- 理解Axios拦截器的工作原理
- 掌握请求拦截器的典型应用场景（如添加认证头）
- 掌握响应拦截器的错误统一处理方式
- 学会移除拦截器以避免内存泄漏

## 环境要求
- Node.js 14.x 或更高版本
- npm（随Node.js自动安装）

## 安装依赖的详细步骤

1. 打开终端或命令行工具
2. 进入项目目录：`cd axios-interceptor-demo`
3. 安装依赖包：
   ```bash
   npm install
   ```

## 文件说明
- `request-interceptor.js`: 演示请求拦截器——自动添加认证头和请求日志
- `response-interceptor.js`: 演示响应拦截器——统一错误处理和成功响应日志
- `combined-interceptor.js`: 综合使用请求与响应拦截器，并展示如何清除拦截器
- `package.json`: 项目依赖声明文件

## 逐步实操指南

### 步骤1: 创建项目目录并初始化
```bash
mkdir axios-interceptor-demo && cd axios-interceptor-demo
npm init -y
```

### 步骤2: 安装Axios
```bash
npm install axios
```

### 步骤3: 运行示例

运行请求拦截器示例：
```bash
node request-interceptor.js
```
**预期输出**：
```
[请求拦截] 即将发送请求: https://jsonplaceholder.typicode.com/posts/1
{
  "userId": 1,
  "id": 1,
  "title": "...",
  "body": "..."
}
```

运行响应拦截器示例：
```bash
node response-interceptor.js
```
**预期输出**：
```
[响应拦截] 请求成功: 200 OK
{ "userId": 1, "id": 1, ... }
```

运行综合拦截器示例：
```bash
node combined-interceptor.js
```

## 代码解析

### 请求拦截器关键代码
```js
axiosInstance.interceptors.request.use(
  config => {
    console.log(`[请求拦截] 即将发送请求: ${config.url}`);
    config.headers['Authorization'] = 'Bearer fake-token';
    return config;
  },
  error => Promise.reject(error)
);
```
> 作用：在每个请求发出前自动注入认证令牌并打印日志。

### 响应拦截器关键代码
```js
axiosInstance.interceptors.response.use(
  response => {
    console.log(`[响应拦截] 请求成功: ${response.status} ${response.statusText}`);
    return response;
  },
  error => {
    console.error(`[响应拦截] 请求失败: ${error.message}`);
    return Promise.reject(error);
  }
);
```
> 作用：统一捕获网络错误或HTTP异常状态码，并集中处理。

## 预期输出示例
```bash
[请求拦截] 即将发送请求: https://jsonplaceholder.typicode.com/posts/1
[响应拦截] 请求成功: 200 OK
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit..."
}
```

## 常见问题解答

**Q: 拦截器是否会影响性能？**
A: 不会显著影响。拦截器只是同步函数，除非执行复杂逻辑，否则开销极小。

**Q: 可以添加多个拦截器吗？**
A: 可以。Axios支持多个请求和响应拦截器，按添加顺序执行。

**Q: 如何移除拦截器？**
A: 使用 `axiosInstance.interceptors.request.eject(id)` 方法移除指定拦截器，防止内存泄漏。

## 扩展学习建议
- 尝试在请求拦截器中实现自动刷新JWT令牌
- 在响应拦截器中集成重试机制（如请求失败时自动重试3次）
- 结合环境变量管理不同环境下的Base URL和认证配置