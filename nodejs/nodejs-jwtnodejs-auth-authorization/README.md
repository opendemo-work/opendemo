# JWT认证与授权Node.js演示

## 简介
本项目是一个完整的Node.js示例，演示如何使用`jsonwebtoken`库实现基于JWT（JSON Web Token）的用户认证与授权机制。包含令牌生成、验证和受保护路由的完整流程。

## 学习目标
- 理解JWT的基本结构和工作原理
- 掌握使用jsonwebtoken生成和验证令牌
- 实现基于中间件的路由保护
- 了解安全最佳实践（如密钥管理、过期设置）

## 环境要求
- Node.js 16.x 或更高版本
- npm 包管理器（随Node.js自动安装）

## 安装依赖
```bash
# 1. 确保已安装Node.js
node --version

# 2. 安装项目依赖
npm install
```

## 文件说明
- `auth-generator.js`: 演示JWT令牌生成
- `auth-validator.js`: 演示JWT令牌验证和受保护路由
- `package.json`: 项目依赖声明文件

## 逐步实操指南

### 步骤1: 初始化项目并安装依赖
```bash
# 创建项目目录（如果尚未克隆）
npm init -y
npm install jsonwebtoken express
```

### 步骤2: 运行令牌生成器
```bash
node auth-generator.js
```
**预期输出**: 
```
生成的JWT令牌:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEyMywibmFtZSI6IuW8oOS4iuaYr-WQjSIsImlhdCI6MTcyMDAwMDAwMCwiZXhwIjoxNzIwMDA0NjAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### 步骤3: 启动服务器并测试验证
```bash
node auth-validator.js
```

### 步骤4: 使用curl测试受保护的API
```bash
# 将下方TOKEN替换为上一步生成的实际令牌
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5c..." http://localhost:3000/protected
```

**预期输出**: 
```json
{
  "message": "访问成功",
  "user": {
    "userId": 123,
    "name": "张三"
  }
}
```

## 代码解析

### auth-generator.js 关键点
- 使用`jwt.sign()`生成令牌
- 设置`exp`（过期时间）为1小时后
- 使用HS256算法和密钥签名

### auth-validator.js 关键点
- 自定义中间件`authenticateToken`提取并验证JWT
- 使用`jwt.verify()`验证令牌有效性
- 失败时返回401状态码

## 预期输出示例
```
服务器运行在 http://localhost:3000
生成的JWT令牌:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEyMywibmFtZSI6IuW8oOS4iuaYr-WQjSIsImlhdCI6MTcyMDAwMDAwMCwiZXhwIjoxNzIwMDA0NjAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

验证成功: { userId: 123, name: '张三', iat: 1720000000, exp: 1720004600 }
```

## 常见问题解答

**Q: 为什么收到401 Unauthorized错误？**
A: 可能原因：令牌过期、格式错误（缺少'Bearer '前缀）、签名密钥不匹配。

**Q: 密钥应该怎样安全存储？**
A: 在生产环境中应使用环境变量（如`process.env.JWT_SECRET`），避免硬编码。

**Q: 如何刷新过期的令牌？**
A: 可实现refresh token机制，本示例未包含，建议扩展学习。

## 扩展学习建议
- 结合数据库实现用户登录验证
- 添加refresh token机制
- 使用Redis存储已注销的令牌（黑名单）
- 集成Passport.js进行更复杂的认证策略