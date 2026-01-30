# PM2多进程部署Node.js示例

## 简介
本示例演示如何使用PM2在生产环境中部署Node.js应用，支持单实例、集群模式（多进程）和配置文件管理。通过本Demo，您将掌握PM2的核心功能和最佳实践。

## 学习目标
- 理解PM2的作用与优势
- 掌握PM2的基本命令
- 使用PM2启动单进程和多进程Node.js应用
- 使用ecosystem.config.js配置文件管理应用

## 环境要求
- Node.js 16.x 或更高版本
- npm 8.x 或更高版本
- 操作系统：Windows、Linux、macOS（跨平台兼容）

## 安装依赖的详细步骤
1. 确保已安装Node.js和npm
   ```bash
   node -v
   npm -v
   ```
2. 全局安装PM2
   ```bash
   npm install -g pm2
   ```
3. 进入项目目录并安装本地依赖
   ```bash
   npm install
   ```

## 文件说明
- `app.js`：基础Express服务器，用于模拟Web应用
- `cluster-app.js`：使用内置集群模式启动多个实例
- `ecosystem.config.js`：PM2配置文件，定义多进程部署策略

## 逐步实操指南

### 步骤1：启动单个实例
```bash
pm2 start app.js --name="single-api" --watch
```
**预期输出**：
> [PM2] Process successfully started
> ┌────┬────────────────────┬─────────────┬─────────┐
> │ id │ name               │ mode        │ status  │
> ├────┼────────────────────┼─────────────┼─────────┤
> │ 0  │ single-api         │ fork        │ online  │
> └────┴────────────────────┴─────────────┴─────────┘

### 步骤2：查看进程状态
```bash
pm2 list
```

### 步骤3：使用配置文件启动多进程集群模式
```bash
pm2 start ecosystem.config.js
```
**预期输出**：
> [PM2] Process successfully started
> 可见多个实例（如4个）运行在cluster模式下

### 步骤4：查看实时监控
```bash
pm2 monit
```
可观察CPU、内存使用情况

### 步骤5：停止所有进程
```bash
pm2 delete all
```

## 代码解析

### `app.js`
```js
const express = require('express');
const app = express();
// 基础路由返回进程ID和PID
app.get('/', (req, res) => {
  res.json({
    message: 'Hello from PM2 demo',
    processId: process.env.pm_id || 'N/A', // PM2分配的进程ID
    pid: process.pid // 系统PID
  });
});
```

### `ecosystem.config.js`
```js
module.exports = {
  apps: [
    {
      name: 'api-cluster',
      script: './cluster-app.js',
      instances: 'max', // 使用CPU核心数的最大实例
      exec_mode: 'cluster', // 启用集群模式
      watch: true,
      env: {
        NODE_ENV: 'development'
      },
      env_production: {
        NODE_ENV: 'production'
      }
    }
  ]
};
```

## 预期输出示例
访问 `http://localhost:3000` 返回：
```json
{
  "message": "Hello from PM2 demo",
  "processId": 0,
  "pid": 12345
}
```
在集群模式下，多次刷新会看到不同的`pid`，表明请求被不同进程处理。

## 常见问题解答

**Q: PM2是什么？**
A: PM2是Node.js的进程管理器，提供后台运行、自动重启、负载均衡、监控等功能。

**Q: cluster模式和fork模式有什么区别？**
A: fork是单实例；cluster利用Node.js的cluster模块启用多进程，共享端口，提高性能和容错。

**Q: 如何开机自启？**
A: 使用 `pm2 startup` 和 `pm2 save` 自动生成启动脚本。

**Q: 如何查看日志？**
A: 使用 `pm2 logs` 查看所有日志，或 `pm2 logs api-cluster` 查看指定应用。

## 扩展学习建议
- 阅读PM2官方文档：https://pm2.keymetrics.io/
- 学习使用Keymetrics监控PM2应用
- 尝试结合Docker + PM2部署
- 探索PM2的API和事件系统