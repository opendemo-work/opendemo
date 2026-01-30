# Node.js + MongoDB + Mongoose 示例项目

## 简介
本项目演示了如何在 Node.js 中使用 Mongoose ODM 连接 MongoDB 数据库，执行基本的增删改查（CRUD）操作。包含连接管理、Schema 定义和模型操作的最佳实践。

## 学习目标
- 掌握 Mongoose 的基本安装与配置
- 学会定义 Schema 和 Model
- 实现 MongoDB 的连接与断开
- 执行基本的数据操作（创建、读取、更新、删除）
- 遵循 Node.js 异步编程最佳实践

## 环境要求
- Node.js v16 或更高版本
- npm（随 Node.js 自动安装）
- MongoDB（本地或云端，如 MongoDB Atlas）

## 安装依赖步骤
1. 确保已安装 Node.js：
   ```bash
   node -v
   # 输出示例: v18.17.0
   ```

2. 初始化项目（如果尚未初始化）：
   ```bash
   npm init -y
   ```

3. 安装依赖：
   ```bash
   npm install mongoose express
   ```

## 文件说明
- `server.js`：启动 Express 服务器并连接 MongoDB
- `models/User.js`：定义用户数据模型
- `demo.js`：执行 CRUD 操作的独立脚本

## 逐步实操指南

### 步骤 1：启动 MongoDB 服务（若使用本地）
```bash
# 在终端运行 MongoDB（确保已安装 MongoDB Server）
mongod --dbpath ./data
```

### 步骤 2：运行 demo 脚本
```bash
node demo.js
```

**预期输出**：
```
✅ 已成功连接到 MongoDB
📝 新用户已创建： { name: 'Alice', age: 25, _id: ..., __v: 0 }
🔍 查询到的用户： { name: 'Alice', age: 25, _id: ..., __v: 0 }
✏️ 用户已更新： { name: 'Alice', age: 26, _id: ..., __v: 0 }
🗑️ 用户已删除
🔌 已断开数据库连接
```

## 代码解析

### `models/User.js`
- 定义了一个用户 Schema，包含 `name`（字符串）和 `age`（数字）字段
- 使用 `mongoose.model` 创建可复用的模型

### `demo.js`
- 使用 `mongoose.connect()` 建立连接（推荐使用异步/await）
- 使用 `try/catch` 处理数据库异常
- 演示了 `create()`, `find()`, `findOneAndUpdate()`, `deleteOne()` 方法

## 预期输出示例
见“逐步实操指南”部分。

## 常见问题解答

**Q: 连接 MongoDB 时报错 ECONNREFUSED？**
A: 确保 MongoDB 服务正在运行。如果是远程数据库，请检查连接字符串和网络权限。

**Q: 如何使用 MongoDB Atlas？**
A: 将连接字符串替换为 Atlas 提供的 URI，格式如下：
```javascript
mongodb+srv://<username>:<password>@cluster.mongodb.net/mydb
```

**Q: Mongoose 和原生 MongoDB 驱动有什么区别？**
A: Mongoose 是 ODM（对象数据建模）工具，提供 Schema 验证、中间件、类型转换等高级功能，适合结构化数据管理。

## 扩展学习建议
- 学习 Mongoose 中间件（pre/post hooks）
- 实现 RESTful API 使用 Express + Mongoose
- 添加 Joi 或 Yup 进行请求数据验证
- 使用 dotenv 管理环境变量（如数据库密码）
- 探索聚合管道（Aggregation Pipeline）进行复杂查询