# Sequelize ORM 数据库操作实战示例

## 简介
本项目是一个基于 Node.js 和 Sequelize ORM 的轻量级数据库操作演示，使用 PostgreSQL 作为后端数据库。通过创建用户模型和执行增删改查（CRUD）操作，帮助开发者快速掌握 Sequelize 的基本用法。

## 学习目标
- 理解 Sequelize ORM 的基本概念与优势
- 掌握如何定义数据模型
- 学会使用 Sequelize 进行 CRUD 操作
- 熟悉异步操作与错误处理

## 环境要求
- Node.js v16 或更高版本
- PostgreSQL 12+（本地或远程）
- npm 包管理器

> 注意：Python/Java 不需要用于此项目。

## 安装依赖的详细步骤

1. 克隆项目或创建新目录：
   ```bash
   mkdir sequelize-demo && cd sequelize-demo
   ```

2. 初始化 npm 项目：
   ```bash
   npm init -y
   ```

3. 安装 Sequelize 及 PostgreSQL 驱动：
   ```bash
   npm install sequelize pg pg-hstore
   ```

4. 将提供的代码文件保存到项目中：
   - `db.js`
   - `userModel.js`
   - `index.js`

5. 启动 PostgreSQL 服务并创建数据库（例如名为 `sequelize_demo`）

6. 修改 `db.js` 中的连接配置以匹配你的数据库设置

## 文件说明
- `db.js`: 数据库连接配置
- `userModel.js`: 用户模型定义
- `index.js`: 主程序，执行 CRUD 示例

## 逐步实操指南

### 第一步：启动数据库
确保 PostgreSQL 正在运行，并创建数据库：
```sql
CREATE DATABASE sequelize_demo;
```

### 第二步：运行程序
```bash
node index.js
```

### 预期输出：
```
✅ 数据库连接成功
✅ 用户已创建: { id: 1, name: 'Alice', email: 'alice@example.com', ... }
🔍 查询到的用户: Alice
✅ 用户邮箱已更新
✅ 用户已删除
✨ 所有操作完成
```

## 代码解析

### `db.js`
创建 Sequelize 实例并测试连接。关键点是使用 `async`/`await` 处理异步连接。

### `userModel.js`
使用 `sequelize.define` 定义 User 模型，字段包括 id、name、email 和时间戳。

### `index.js`
演示完整的 CRUD 流程：
- 创建用户 (`create`)
- 查询用户 (`findByPk`)
- 更新用户 (`update`)
- 删除用户 (`destroy`)

## 预期输出示例
```
✅ 数据库连接成功
✅ 用户已创建: {
  id: 1,
  name: 'Alice',
  email: 'alice@example.com',
  createdAt: 2025-04-05T10:00:00.000Z,
  updatedAt: 2025-04-05T10:00:00.000Z
}
🔍 查询到的用户: Alice
✅ 用户邮箱已更新
✅ 用户已删除
✨ 所有操作完成
```

## 常见问题解答

**Q: 报错 `FATAL: database \"sequelize_demo\" does not exist`？**
A: 请先在 PostgreSQL 中创建名为 `sequelize_demo` 的数据库。

**Q: 如何更换数据库？**
A: 修改 `db.js` 中的 `database`, `username`, `password`, `host` 即可。

**Q: 是否支持 MySQL？**
A: 支持，但需安装 `mysql2` 包并更改 dialect 为 'mysql'。

## 扩展学习建议
- 学习关联模型（如 User.hasMany(Post)）
- 使用迁移（migrations）管理表结构变更
- 添加数据验证规则（validations）
- 结合 Express 构建 REST API
- 使用 dotenv 管理环境变量