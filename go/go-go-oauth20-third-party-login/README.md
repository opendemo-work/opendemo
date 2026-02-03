# Go OAuth2.0 第三方登录示例

## 简介
本项目演示了如何使用 Go 语言通过 OAuth2.0 协议实现第三方登录（以 GitHub 登录为例）。代码包含完整的 Web 服务端处理流程：重定向到授权页、接收回调、获取访问令牌并拉取用户信息。

## 学习目标
- 理解 OAuth2.0 授权码模式的工作流程
- 掌握在 Go 中集成第三方 OAuth2.0 登录的方法
- 学会使用 `golang.org/x/oauth2` 库进行安全的身份验证

## 环境要求
- Go 1.19 或更高版本
- 支持 Git 的终端环境
- 有效的 GitHub 账户用于测试

## 安装依赖的详细步骤

1. 克隆或创建项目目录：
   ```bash
   mkdir oauth2-demo && cd oauth2-demo
   go mod init oauth2-demo
   ```

2. 添加所需依赖：
   ```bash
   go get github.com/gorilla/mux
   go get golang.org/x/oauth2
   go get golang.org/x/oauth2/github
   ```

3. 将代码文件保存到对应路径：
   - `main.go`
   - `handlers.go`

## 文件说明
- `main.go`: 启动 HTTP 服务器并设置路由
- `handlers.go`: 实现 OAuth2.0 登录逻辑和回调处理

## 逐步实操指南

### 步骤 1: 创建 GitHub OAuth App
1. 登录 [GitHub Developer Settings](https://github.com/settings/developers)
2. 点击 "New OAuth App"
3. 填写应用信息：
   - Application name: `Go OAuth Demo`
   - Homepage URL: `http://localhost:8080`
   - Authorization callback URL: `http://localhost:8080/callback`
4. 记下生成的 `Client ID` 和 `Client Secret`

### 步骤 2: 设置环境变量
```bash
export GITHUB_CLIENT_ID="your_client_id"
export GITHUB_CLIENT_SECRET="your_client_secret"
```

### 步骤 3: 运行程序
```bash
go run *.go
```

预期输出：
```text
服务器启动在 :8080...
访问 http://localhost:8080/login 使用 GitHub 登录
```

### 步骤 4: 测试登录
1. 打开浏览器访问 `http://localhost:8080/login`
2. 点击链接跳转至 GitHub 授权页面
3. 授权后将重定向回 `/callback` 并显示用户信息

## 代码解析

### main.go
初始化路由器，注册 `/login` 和 `/callback` 路由，并启动 Web 服务。

### handlers.go
- `loginHandler`: 将用户重定向到 GitHub 的 OAuth 授权 URL
- `callbackHandler`: 处理回调请求，交换授权码为访问令牌，并获取用户信息
- 使用 `oauth2.Config` 配置 GitHub OAuth 参数，确保安全性

## 预期输出示例
成功登录后，浏览器应显示：
```text
欢迎你，[你的用户名]！
邮箱: user@example.com
头像: https://avatars.githubusercontent.com/u/123456?v=4
```

## 常见问题解答

**Q: 出现 `invalid client_id` 错误？**
A: 检查 `GITHUB_CLIENT_ID` 是否正确设置，且未包含引号。

**Q: 回调地址不匹配？**
A: 确保 GitHub OAuth App 中配置的回调 URL 是 `http://localhost:8080/callback`。

**Q: 如何支持其他平台如 Google 或微信？**
A: 替换 `golang.org/x/oauth2/github` 为对应平台的配置，调整 `oauth2.Config` 中的 endpoints 即可。

## 扩展学习建议
- 将用户信息存储到数据库（如 SQLite 或 PostgreSQL）
- 添加 session 管理以维持登录状态
- 实现多个第三方登录选项（Google、Facebook 等）
- 使用 HTTPS 部署到公网服务器
- 集成 JWT 进行无状态认证