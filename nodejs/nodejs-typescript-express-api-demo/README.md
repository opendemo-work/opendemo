# TypeScript Express API Demo

## 简介
本项目是一个使用TypeScript构建的简单Express REST API示例。它展示了如何在Node.js环境中使用TypeScript编写类型安全的Web服务，适合学习现代后端开发的最佳实践。

## 学习目标
- 掌握TypeScript与Express的集成方式
- 理解TS配置文件（tsconfig.json）的作用
- 学会编写类型安全的路由处理函数
- 熟悉项目结构组织和启动脚本

## 环境要求
- Node.js v16 或更高版本
- npm（随Node.js安装）
- TypeScript 和 ts-node 全局工具（可选）

## 安装依赖的详细步骤

1. 克隆或创建项目目录：
```bash
mkdir typescript-express-demo && cd typescript-express-demo
```

2. 初始化npm项目：
```bash
npm init -y
```

3. 安装生产依赖：
```bash
npm install express
npm install --save-dev typescript ts-node @types/express
```

4. 创建项目文件（见下文“文件说明”）

## 文件说明
- `src/app.ts`：主应用逻辑，包含Express服务器和路由
- `src/server.ts`：启动入口文件
- `tsconfig.json`：TypeScript编译配置
- `package.json`：已通过npm init生成并添加了脚本

## 逐步实操指南

### 步骤1：创建源码目录
```bash
mkdir src
```

### 步骤2：创建 app.ts
将代码写入 `src/app.ts`

### 步骤3：创建 server.ts
将代码写入 `src/server.ts`

### 步骤4：创建 tsconfig.json
运行以下命令生成默认配置：
```bash
npx tsc --init
```
然后根据示例替换内容。

### 步骤5：更新 package.json 添加启动脚本
在 `package.json` 中添加：
```json
"scripts": {
  "start": "ts-node src/server.ts"
}
```

### 步骤6：启动服务
```bash
npm start
```

**预期输出**：
```bash
Server is running on http://localhost:3000
```

访问 `http://localhost:3000/api/hello` 应返回 JSON 响应。

## 代码解析

### src/app.ts
- 使用 `import express from 'express'` 导入Express框架
- 定义接口 `RequestWithTime` 扩展原始请求对象，演示类型扩展能力
- 在中间件中注入 `requestTime` 字段，并确保类型系统识别该字段
- 路由 `/api/hello` 返回带有时间戳的JSON响应

### src/server.ts
- 实例化app并设置端口
- 使用 `app.listen()` 启动HTTP服务器
- 启动时打印清晰的日志信息

### tsconfig.json
- 设置输出目录为 `./dist`
- 启用严格类型检查
- 支持ES2020语法和模块解析

## 预期输出示例
启动服务后，浏览器访问 `http://localhost:3000/api/hello`：
```json
{
  "message": "Hello from TypeScript!",
  "timestamp": 1712345678901
}
```

终端日志：
```bash
GET /api/hello 200 3ms - 58
```

## 常见问题解答

**Q: 报错 `Cannot find module 'ts-node'`？**
A: 确保已安装开发依赖：`npm install --save-dev ts-node`

**Q: 修改代码后需要手动重启？**
A: 可安装 `nodemon` 实现热重载：
```bash
npm install --save-dev nodemon
```
然后修改 script 为：
```json
"start": "nodemon -L --exec ts-node src/server.ts"
```

**Q: 访问页面显示 Cannot GET / ?**
A: 检查是否访问的是 `/api/hello` 而非根路径 `/`

## 扩展学习建议
- 引入路由模块化（如 `routes/userRoutes.ts`）
- 添加环境变量管理（使用 `dotenv`）
- 集成数据库（MongoDB + Mongoose 或 PostgreSQL + TypeORM）
- 实现输入验证（使用 `zod` 或 `class-validator`）
- 添加全局错误处理中间件
- 使用 `swagger-jsdoc` 和 `swagger-ui-express` 生成API文档