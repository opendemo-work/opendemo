# NodeJS环境变量管理Demo

## 简介
本示例演示如何使用 `dotenv` 库在Node.js项目中加载和管理环境变量，避免将敏感信息（如API密钥、数据库密码）硬编码在代码中。

## 学习目标
- 理解环境变量在应用配置中的作用
- 掌握使用 `dotenv` 加载 `.env` 文件的实践方法
- 学会安全地管理开发/生产环境的配置

## 环境要求
- Node.js 版本：14.x 或更高（推荐 16+）
- npm 包管理器（随Node.js自动安装）
- 操作系统：Windows / macOS / Linux（跨平台兼容）

## 安装依赖步骤
1. 打开终端（命令行工具）
2. 进入项目目录：`cd node-env-demo`
3. 初始化npm项目（如未初始化）：
   ```bash
   npm init -y
   ```
4. 安装 dotenv 依赖：
   ```bash
   npm install dotenv@^16.0.3
   ```

## 文件说明
- `.env`：存储环境变量的私有配置文件（不应提交到版本控制）
- `config.js`：使用 dotenv 加载并导出配置
- `app.js`：主应用，展示如何使用配置
- `secure-app.js`：演示在生产环境中如何安全回退

## 逐步实操指南

### 步骤1：创建 .env 文件
```bash
echo "DATABASE_URL=mongodb://localhost:27017/myapp" > .env
echo "API_KEY=secret123" >> .env
echo "PORT=3000" >> .env
```

### 步骤2：运行基础配置示例
```bash
node config.js
```
**预期输出**：
```
配置已加载：
端口: 3000
数据库: mongodb://localhost:27017/myapp
API密钥: secret123
```

### 步骤3：运行主应用
```bash
node app.js
```
**预期输出**：
```
✅ 服务器启动在端口 3000
正在连接数据库: mongodb://localhost:27017/myapp
```

### 步骤4：运行安全模式示例（模拟生产）
```bash
node secure-app.js
```
**预期输出**：
```
🔐 生产环境：使用系统环境变量或默认值
服务器将在端口 8080 启动
```

## 代码解析

### config.js
```js
require('dotenv').config();
```
- 自动读取 `.env` 文件并注入 `process.env`

```js
if (!process.env.PORT) throw new Error('缺少必要环境变量 PORT');
```
- 添加健壮性检查，确保关键配置存在

### secure-app.js
```js
const port = process.env.PORT || 8080;
```
- 在生产中优先使用系统环境变量，`.env` 仅用于开发

## 预期输出示例
见“逐步实操指南”中的输出描述。

## 常见问题解答

**Q: .env 文件是否应提交到 Git？**
A: 不应该。请将 `.env` 添加到 `.gitignore`，防止敏感信息泄露。

**Q: 如何为不同环境（开发/测试/生产）管理配置？**
A: 可使用 `.env.development`, `.env.production` 并配合 `dotenv.config({ path: '...' })` 加载对应文件。

**Q: dotenv 在生产环境中是否仍被调用？**
A: 是的，但生产中通常通过系统环境变量传入配置，`.env` 仅作为本地开发便利手段。

## 扩展学习建议
- 学习使用 `dotenv-safe` 提供更严格的配置验证
- 结合 `config` 库实现多环境配置分层
- 使用 Docker 时通过 `-e` 参数传递环境变量
- 探索 AWS Parameter Store 或 HashiCorp Vault 等高级配置管理方案