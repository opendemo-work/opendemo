# NodeJS加密安全示例：Crypto Hash与Bcrypt实战

本项目演示了在Node.js中如何正确使用`crypto`模块和`bcrypt`库对敏感数据（如密码）进行安全哈希处理，适用于用户认证等场景。

## 学习目标
- 理解密码哈希的基本原理
- 掌握Node.js内置`crypto`模块的SHA-256哈希用法
- 学会使用`bcrypt`进行自适应哈希（推荐用于密码存储）
- 区分固定哈希与加盐哈希的安全性差异

## 环境要求
- Node.js 版本：14.x 或更高（推荐 16+）
- npm 包管理器（随Node.js自动安装）
- 操作系统：Windows、Linux、macOS 均支持

## 安装依赖的详细步骤

1. 打开终端（命令行工具）
2. 进入项目根目录
3. 执行以下命令安装依赖：

```bash
npm install
```

## 文件说明
- `hash-crypto.js`：使用Node.js内置crypto模块进行SHA-256哈希
- `hash-bcrypt.js`：使用bcrypt库进行安全加盐哈希和验证
- `package.json`：项目依赖声明文件

## 逐步实操指南

### 步骤1：初始化项目（如未提供package.json）

```bash
npm init -y
```

### 步骤2：安装bcrypt依赖

```bash
npm install bcrypt
```

### 步骤3：运行crypto哈希示例

```bash
node hash-crypto.js
```

**预期输出**：
```
原始密码: mySecurePassword123
SHA-256哈希值: fba0f8... (一长串十六进制字符)
SHA-256哈希值: 7c9e8b... (再次运行可能相同，无随机盐)
```

> 注意：相同输入总是生成相同输出，易受彩虹表攻击，不推荐直接用于生产环境密码存储。

### 步骤4：运行bcrypt哈希示例

```bash
node hash-bcrypt.js
```

**预期输出**：
```
原始密码: mySecurePassword123
Bcrypt哈希结果: $2b$10$abc123... (每次不同)
验证密码: true
验证错误密码: false
```

> 每次哈希结果都不同，因为bcrypt自动添加随机盐，安全性高。

## 代码解析

### hash-crypto.js 关键代码段
```js
const crypto = require('crypto');
// 使用createHash创建SHA-256哈希实例
const hash = crypto.createHash('sha256').update(password).digest('hex');
```
- `sha256` 是加密哈希算法
- `update()` 输入要哈希的数据
- `digest('hex')` 输出十六进制字符串

### hash-bcrypt.js 关键代码段
```js
const saltRounds = 10;
const hashedPassword = await bcrypt.hash(password, saltRounds);
const match = await bcrypt.compare(inputPassword, hashedPassword);
```
- `saltRounds` 控制哈希强度（越高越慢越安全）
- `bcrypt.hash()` 自动生成盐并哈希
- `bcrypt.compare()` 安全比较明文与哈希值

## 预期输出示例
见上述“预期输出”部分。

## 常见问题解答

**Q1: 为什么不能直接存储明文密码？**
A: 明文存储一旦数据库泄露，所有用户密码立即暴露。必须使用单向哈希。

**Q2: 为什么SHA-256不适合直接用于密码？**
A: SHA-256太快且无盐，攻击者可用彩虹表或暴力破解。应使用bcrypt、scrypt或Argon2。

**Q3: bcrypt的saltRounds设置多少合适？**
A: 推荐10-12。太高影响性能，太低降低安全性。根据服务器能力调整。

**Q4: 如何在Express中集成bcrypt？**
A: 在用户注册时`hash`密码，登录时`compare`输入密码与数据库中哈希值。

## 扩展学习建议
- 学习使用`argon2`（比bcrypt更现代）
- 实践JWT令牌与bcrypt结合的认证流程
- 了解HMAC用于消息认证
- 阅读OWASP密码存储指南