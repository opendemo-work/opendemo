# OAuth2.0授权 Passport 集成 Node.js Demo

## 简介
本项目是一个完整的、可执行的Node.js演示应用，展示了如何使用Passport.js库实现基于OAuth2.0协议的第三方身份验证（以Google登录为例）。通过此Demo，开发者可以快速理解OAuth2.0流程和Passport中间件的实际用法。

## 学习目标
- 理解OAuth2.0授权码模式的基本流程
- 掌握Passport.js在Express应用中的集成方式
- 学会配置Google OAuth2.0客户端ID与密钥
- 实现安全的用户认证回调处理

## 环境要求
- Node.js 16 或更高版本
- npm 包管理器
- 浏览器用于测试登录流程

> ⚠️ 注意：本Demo不依赖Python/Java，仅需Node.js环境

## 安装依赖步骤

1. 克隆或创建项目目录并进入：
```bash
mkdir oauth-demo && cd oauth-demo
```

2. 初始化npm项目（按提示回车即可）：
```bash
npm init -y
```

3. 安装所需依赖包：
```bash
npm install express passport passport-google-oauth20 dotenv
```

4. 创建 `.env` 文件并添加你的Google OAuth凭据（见扩展建议获取方法）：
```env
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
PORT=3000
```

## 文件说明
- `app.js`: 主服务入口，配置Express和Passport策略
- `README.md`: 当前文档，指导运行和学习
- `.env`: 环境变量存储（已.gitignore）

## 逐步实操指南

### 第一步：启动服务器
```bash
node app.js
```

**预期输出**：
```
✅ 服务器运行在 http://localhost:3000
👉 请访问 http://localhost:3000/auth/google 开始Google登录
```

### 第二步：打开浏览器访问
访问以下地址：
```
http://localhost:3000/auth/google
```

你将被重定向到Google登录页面。选择账户后，授权应用访问基本信息。

### 第三步：查看登录成功响应
授权成功后，你会看到类似如下信息：
```
🎉 欢迎，张三！
📧 邮箱：zhangsan@gmail.com
🔐 原始用户对象已记录在控制台
```
同时终端会打印出用户详细信息。

## 代码解析

### Passport策略初始化
```js
passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: "/auth/google/callback"
}, (accessToken, refreshToken, profile, done) => {
  return done(null, profile);
}));
```
- 使用Google OAuth20策略，传入客户端ID/密钥
- `callbackURL` 是授权完成后跳转的本地路由
- 回调函数中接收profile（用户公开信息），传递给`done()`保存到session

### 序列化用户
```js
passport.serializeUser((user, done) => {
  done(null, user.id);
});
```
- 将用户唯一标识存入session，避免每次请求都传完整对象

### 反序列化用户
```js
passport.deserializeUser((id, done) => {
  done(null, user);
});
```
- 根据session中的id恢复用户对象（实际项目应查数据库）

## 预期输出示例（控制台）
```
✅ 服务器运行在 http://localhost:3000
👉 请访问 http://localhost:3000/auth/google 开始Google登录

👤 用户信息：{
  id: '123456789',
  displayName: '张三',
  emails: [ { value: 'zhangsan@gmail.com', type: 'account' } ],
  photos: [ { value: 'https://lh3.googleusercontent.com/...' } ]
}
```

## 常见问题解答

**Q1: 出现 `Missing client ID` 错误？**
A: 检查 `.env` 文件是否正确配置 `GOOGLE_CLIENT_ID` 和 `GOOGLE_CLIENT_SECRET`，并确保已安装 `dotenv`。

**Q2: 回调URL未注册？**
A: 登录 [Google Cloud Console](https://console.cloud.google.com/)，在OAuth同意屏幕中添加 `http://localhost:3000/auth/google/callback` 到授权重定向URI列表。

**Q3: 页面卡住无响应？**
A: 确保Node.js服务正在运行，并检查防火墙是否阻止了3000端口。

## 扩展学习建议
- 【必做】前往 [Google Cloud Platform](https://console.cloud.google.com/apis/credentials) 创建OAuth2.0客户端ID和密钥
- 将用户信息持久化存储到MongoDB或SQLite
- 添加更多OAuth提供商如GitHub、Facebook
- 实现JWT替代Session进行状态管理
- 使用HTTPS部署到线上环境（如Vercel、Heroku）