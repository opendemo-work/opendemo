# GraphQL API 查询语言实战演示

## 简介
本项目是一个轻量级的Node.js应用，演示了如何使用GraphQL作为API查询语言来构建高效、灵活的数据查询接口。通过本Demo，你将学习到GraphQL的基本概念、Schema定义、解析器（Resolver）编写以及与Express集成的方法。

## 学习目标
- 理解GraphQL的核心概念（Schema、Type、Query、Resolver）
- 掌握使用`express-graphql`在Node.js中搭建GraphQL服务
- 学会定义类型和查询，并返回模拟数据
- 能够使用GraphQL进行字段选择查询

## 环境要求
- Node.js 16.x 或更高版本
- npm（随Node.js自动安装）
- 浏览器（用于访问GraphQL Playground）

## 安装依赖的详细步骤

1. 打开终端，进入项目根目录：
```bash
cd .
```

2. 初始化npm项目（如果尚未初始化）：
```bash
npm init -y
```

3. 安装所需依赖包：
```bash
npm install express graphql express-graphql
```

4. 安装完成后，启动服务器：
```bash
node server.js
```

## 文件说明
- `server.js`：主服务器文件，配置Express并挂载GraphQL中间件
- `schema.js`：定义GraphQL Schema和解析器逻辑
- `README.md`：本说明文档

## 逐步实操指南

### 第一步：启动服务
运行以下命令启动服务器：
```bash
node server.js
```

**预期输出**：
```bash
🚀 Server is running on http://localhost:4000/graphql
```

### 第二步：打开浏览器访问GraphQL Playground
在浏览器中访问：
```
http://localhost:4000/graphql
```

你会看到GraphQL Playground界面（由`express-graphql`提供）。

### 第三步：执行GraphQL查询
在左侧输入以下查询语句：
```graphql
{
  user(id: 1) {
    id
    name
    email
    posts {
      title
      published
    }
  }
}
```

点击“播放”按钮执行查询。

**预期输出**：
```json
{
  "data": {
    "user": {
      "id": "1",
      "name": "Alice",
      "email": "alice@example.com",
      "posts": [
        {"title": "我的第一篇博客", "published": true},
        {"title": "GraphQL入门", "published": false}
      ]
    }
  }
}
}
```

## 代码解析

### `schema.js` 关键代码段
```js
const typeDefs = `...`; // 使用SDL（Schema Definition Language）定义类型
```
- 定义了 `User` 和 `Post` 类型
- `Query` 类型包含 `user(id: Int): User` 查询入口

```js
const resolvers = { ... };
```
- `resolvers` 对象实现了解析逻辑
- `user` 解析器根据传入的 `id` 返回匹配的用户数据

### `server.js` 关键点
- 使用 Express 创建HTTP服务器
- 通过 `express-graphql` 中间件暴露 `/graphql` 端点
- 启用 `graphiql: true` 提供交互式开发界面

## 预期输出示例
成功运行后，在浏览器中执行查询将返回结构化JSON响应，仅包含请求的字段，体现GraphQL的“按需获取”特性。

## 常见问题解答

**Q: 访问 http://localhost:4000/graphql 显示空白？**
A: 确保已安装所有依赖且Node.js版本正确。尝试重新运行 `npm install` 并重启服务。

**Q: 如何添加新的查询？**
A: 在 `schema.js` 的 `typeDefs` 中添加新字段，在 `resolvers` 中实现对应逻辑即可。

**Q: 支持Mutation吗？**
A: 当前Demo仅演示Query，但可在Schema中扩展 `Mutation` 类型以支持写操作。

## 扩展学习建议
- 尝试添加 `Mutation` 实现用户创建功能
- 集成数据库（如MongoDB）替代模拟数据
- 使用Apollo Server替代`express-graphql`以获得更强大功能
- 学习GraphQL Fragment、Variables等高级特性