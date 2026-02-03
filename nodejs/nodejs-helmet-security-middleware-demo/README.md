# Helmet安全中间件防护示例

## 简介
本演示项目展示了如何在Node.js的Express应用中使用`helmet`中间件来增强Web应用的安全性。通过设置恰当的HTTP响应头，防止跨站脚本（XSS）、点击劫持、MIME类型嗅探等常见安全威胁。

## 学习目标
- 理解HTTP安全头的作用与重要性
- 掌握Helmet中间件的基本和高级用法
- 能够为Express应用配置安全防护

## 环境要求
- Node.js 版本：v16 或更高（推荐 v18+）
- npm 包管理工具（随Node.js自动安装）
- 操作系统：Windows、macOS、Linux 均可

## 安装依赖的详细步骤

1. 确保已安装Node.js和npm：
   ```bash
   node -v
   npm -v
   ```
   预期输出示例：
   ```
   v18.17.0
   9.6.7
   ```

2. 在项目根目录执行以下命令安装依赖：
   ```bash
   npm install
   ```

## 文件说明
- `app.js`: 主应用文件，包含使用Helmet的基础配置
- `advanced.js`: 高级配置示例，自定义部分安全头
- `package.json`: 项目依赖声明文件
- `README.md`: 本说明文档

## 逐步实操指南

### 步骤1：启动基础安全服务
```bash
node app.js
```
预期输出：
```
✅ 基础安全服务器运行在 http://localhost:3000
```

访问 `http://localhost:3000`，打开浏览器开发者工具 → Network 标签，查看响应头是否包含：
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

### 步骤2：启动高级配置服务
```bash
node advanced.js
```
预期输出：
```
✅ 高级安全服务器运行在 http://localhost:3001
```

检查响应头中是否包含自定义的`Content-Security-Policy`等策略。

## 代码解析

### `app.js` 关键代码段
```js
app.use(helmet());
```
启用Helmet默认的全部安全头设置，一键提升安全性。

### `advanced.js` 关键代码段
```js
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"]
      }
    },
    hsts: { maxAge: 31536000, includeSubDomains: true }
  })
);
```
自定义内容安全策略（CSP）和HSTS策略，实现更精细控制。

## 预期输出示例
启动服务后访问页面，响应头应包含：
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## 常见问题解答

**Q: 启动时报错“Cannot find module 'helmet'”？**
A: 请确认是否已运行 `npm install` 安装依赖。

**Q: Helmet会影响静态资源加载吗？**
A: 默认不会。若启用CSP，请根据实际资源来源调整策略。

**Q: 如何禁用某项安全头？**
A: 可通过配置 `{ noSniff: false }` 等方式关闭特定功能。

## 扩展学习建议
- 阅读 [Helmet官方文档](https://helmetjs.github.io/)
- 学习OWASP Top 10安全风险
- 实践在HTTPS环境下部署并启用HSTS