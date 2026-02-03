# Go加密安全实践：Hash与JWT示例

## 简介
本项目演示了在Go语言中如何安全地使用加密哈希（如SHA-256）和JSON Web Token (JWT) 进行用户认证和数据完整性保护。包含三个独立但相关的场景：密码哈希存储、数据签名验证和JWT生成与解析。

## 学习目标
- 理解密码安全存储的最佳实践
- 掌握使用crypto/sha256进行数据哈希
- 学会使用JWT实现无状态身份验证
- 遵循Go语言工业级编码规范

## 环境要求
- Go 1.20 或更高版本
- 支持的操作系统：Windows、Linux、macOS

## 安装依赖步骤

```bash
# 初始化Go模块（如果尚未初始化）
go mod init jwt-demo

# 添加JWT库依赖
go get github.com/golang-jwt/jwt/v5@v5.0.0

# 下载所有依赖
go mod tidy
```

## 文件说明
- `main.go`：主程序，演示密码哈希和验证
- `jwt_utils.go`：JWT生成与解析工具函数
- `data_sign.go`：演示数据签名与验证

## 逐步实操指南

### 步骤1：创建项目目录并进入
```bash
mkdir go-security-demo && cd go-security-demo
```

### 步骤2：运行主程序
```bash
# 运行主程序
go run main.go
```

**预期输出**：
```
密码哈希成功: [哈希值]
密码验证通过: true

数据签名成功: [签名]
数据验证通过: true

JWT令牌生成: [token]
JWT解析成功: map[name:Alice]
```

### 步骤3：运行JWT工具测试
```bash
go run jwt_utils.go
```

> 注意：实际使用时应将所有代码整合运行。此处为教学拆分说明。

## 代码解析

### `main.go` - 密码哈希
使用 `crypto/sha256` 对密码加盐哈希，模拟安全存储流程。

### `data_sign.go` - 数据签名
利用HMAC-SHA256对数据进行签名，确保传输完整性。

### `jwt_utils.go` - JWT操作
使用第三方库生成和解析JWT令牌，包含过期时间、签发者等标准声明。

## 预期输出示例
```
密码哈希成功: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
密码验证通过: true

数据签名成功: 1a2b3c4d...
数据验证通过: true

JWT令牌生成: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
JWT解析成功: map[name:Alice]
```

## 常见问题解答

**Q: 为什么不用MD5或SHA-1？**
A: MD5和SHA-1已被证明存在碰撞漏洞，推荐使用SHA-256及以上强度算法。

**Q: JWT密钥应该如何管理？**
A: 使用环境变量或密钥管理系统（如Vault），避免硬编码在代码中。

**Q: 能否使用非对称加密JWT？**
A: 可以，本示例使用HS256对称算法；也可改用RS256配合私钥/公钥。

## 扩展学习建议
- 学习bcrypt/pbkdf2用于更安全的密码哈希
- 实现JWT刷新令牌机制
- 集成OAuth2.0或OpenID Connect
- 使用tls进行HTTPS通信加密