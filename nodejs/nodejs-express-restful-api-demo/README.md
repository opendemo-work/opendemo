# Express RESTful API 开发演示

## 简介
本项目是一个轻量级的 Node.js 应用，使用 Express 框架构建了一个简单的 RESTful API，用于管理用户数据（模拟 CRUD 操作）。适合学习 Express 路由、中间件、请求处理等核心概念。

## 学习目标
- 掌握 Express 框架的基本结构
- 理解 RESTful API 设计原则
- 学会使用 Express 处理 HTTP 请求（GET, POST, PUT, DELETE）
- 熟悉中间件和路由分离的最佳实践

## 环境要求
- Node.js 版本：v16.x 或更高（推荐 v18+）
- npm 包管理器（随 Node.js 自动安装）
- 终端工具（如：Windows Terminal、iTerm2、bash 等）

## 安装依赖步骤
1. 打开终端并进入项目目录
2. 运行以下命令安装依赖：
   ```bash
   npm install
   ```

## 文件说明
- `app.js`：主应用文件，配置 Express 实例和基本中间件
- `routes/users.js`：用户相关路由定义，实现 CRUD 接口
- `package.json`：项目依赖和脚本声明

## 逐步实操指南

### 步骤 1: 初始化项目（若未提供 package.json）
```bash
npm init -y
```

### 步骤 2: 安装 Express
```bash
npm install express
```

### 步骤 3: 启动应用
```bash
node app.js
```

预期输出：
```
✅ 服务器正在运行在 http://localhost:3000
```

### 步骤 4: 测试 API（使用 curl 或 Postman）

获取所有用户：
```bash
curl http://localhost:3000/users
```

创建新用户：
```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "email": "zhangsan@example.com"}'
```

更新用户（ID 为 1）：
```bash
curl -X PUT http://localhost:3000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "李四", "email": "lisi@example.com"}'
```

删除用户：
```bash
curl -X DELETE http://localhost:3000/users/1
```

## 代码解析

### `app.js`
- 使用 `express()` 创建应用实例
- 使用 `express.json()` 中间件解析 JSON 请求体
- 引入并挂载 `/users` 路由
- 监听 3000 端口

### `routes/users.js`
- 定义基于内存的用户数组模拟数据库
- 实现 GET /users 获取全部用户
- 实现 POST /users 创建用户（含基础验证）
- 实现 PUT /users/:id 更新指定用户
- 实现 DELETE /users/:id 删除用户

## 预期输出示例
启动服务后访问 `http://localhost:3000/users` 应返回：
```json
[
  {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com"
  }
]
```

## 常见问题解答

**Q: 启动时报错 'Cannot find module 'express''？**
A: 请确保已运行 `npm install` 安装依赖。

**Q: 如何更改端口？**
A: 修改 `app.js` 中 `app.listen(3000)` 的端口号即可。

**Q: 数据重启后丢失？**
A: 当前使用内存存储，仅用于演示。生产环境应使用数据库如 MongoDB 或 PostgreSQL。

## 扩展学习建议
- 集成 MongoDB 使用 Mongoose 进行持久化存储
- 添加输入验证（如使用 Joi）
- 实现错误处理中间件
- 使用 dotenv 管理环境变量
- 添加身份认证（如 JWT）
- 使用 Swagger 生成 API 文档