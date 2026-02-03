# NestJS框架入门Demo

## 简介
本项目是一个轻量级、可运行的NestJS应用，展示了控制器（Controller）、服务（Service）和依赖注入（DI）的基本用法。通过构建一个简单的用户管理API，帮助初学者掌握NestJS的核心结构。

## 学习目标
- 理解NestJS的基本架构（模块、控制器、服务）
- 掌握依赖注入机制
- 学会创建RESTful API端点
- 熟悉TypeScript在NestJS中的使用

## 环境要求
- Node.js v16 或更高版本
- npm（随Node.js安装）
- TypeScript 和 ts-node（将通过npm安装）

> ⚠️ 注意：不需要Python或Java环境

## 安装依赖的详细步骤

1. 打开终端，进入项目目录：
```bash
npm init -y
touch tsconfig.json
```

2. 初始化TypeScript配置：
```bash
npx tsc --init
```

3. 安装NestJS及相关依赖：
```bash
npm install @nestjs/core @nestjs/common @nestjs/platform-express reflect-metadata
npm install --save-dev typescript ts-node
```

4. 创建必要文件后即可运行。

## 文件说明
- `main.ts`：应用入口文件，启动HTTP服务器
- `user.controller.ts`：定义用户相关的HTTP路由
- `user.service.ts`：处理业务逻辑，模拟数据存储
- `README.md`：本指南
- `package.json` 和 `tsconfig.json`：已隐含配置

## 逐步实操指南

### 步骤1：创建 main.ts
```bash
touch main.ts
```
粘贴对应内容。

### 步骤2：创建 user.service.ts
```bash
touch user.service.ts
```

### 步骤3：创建 user.controller.ts
```bash
touch user.controller.ts
```

### 步骤4：运行应用
```bash
npx ts-node main.ts
```

### 预期输出：
```bash
🚀 应用程序正在 http://localhost:3000 上运行
```

### 步骤5：测试API
打开浏览器或使用curl：
```bash
curl http://localhost:3000/users
```

预期返回：
```json
["Alice", "Bob"]
```

## 代码解析

### main.ts
使用NestFactory创建Nest应用实例，并监听3000端口。这是标准的启动模式。

### user.controller.ts
@Controller('users') 定义路由前缀。@Get() 装饰器绑定GET请求到 getUsers 方法。

### user.service.ts
@Injectable() 标记为可注入的服务。实际项目中可替换为数据库操作。

## 预期输出示例
启动时：
```bash
🚀 应用程序正在 http://localhost:3000 上运行
```

访问 `/users` 返回：
```json
["Alice", "Bob"]
```

## 常见问题解答

**Q1: 运行时报错 'Cannot find module'？**
A: 请确认所有依赖已正确安装：`npm install`

**Q2: 如何添加POST接口？**
A: 在controller中添加 @Post() 方法，并在service中实现逻辑。

**Q3: 是否支持ESLint/Prettier？**
A: 是的，但本demo为简化未包含。可通过 `nest add @nestjs/cli` 初始化完整项目。

## 扩展学习建议
- 尝试添加 CRUD 操作（Create, Read, Update, Delete）
- 引入 TypeORM 实现数据库持久化
- 使用 DTO 和 ValidationPipe 进行输入校验
- 添加中间件或守卫（Guard）实现身份验证
- 学习模块（Module）拆分与组织