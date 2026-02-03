# Node.js中间件处理链演示

## 简介
本示例演示如何在Node.js中使用Express框架构建灵活、可维护的中间件请求处理链。通过多个场景展示中间件的执行顺序、数据传递和错误处理机制。

## 学习目标
- 理解中间件的概念及其在请求处理中的作用
- 掌握编写自定义中间件的方法
- 学会使用中间件链进行请求预处理、日志记录和错误捕获
- 理解`next()`函数的作用与控制流

## 环境要求
- Node.js 版本：v16.x 或更高（推荐 v18+）
- npm 包管理工具（随Node.js自动安装）
- 终端或命令行工具（支持Windows PowerShell、Linux/macOS Terminal）

## 安装依赖的详细步骤
1. 打开终端并进入项目目录
2. 运行以下命令安装所需依赖：
   ```bash
   npm install
   ```

## 文件说明
- `app.js`: 主应用文件，定义服务器和路由
- `middleware/logger.js`: 日志记录中间件
- `middleware/auth.js`: 模拟身份验证中间件
- `package.json`: 项目依赖和脚本配置

## 逐步实操指南

### 步骤1: 初始化项目（如未提供package.json）
```bash
npm init -y
```

### 步骤2: 安装Express
```bash
npm install express@^4.18.0
```

### 步骤3: 启动应用
```bash
node app.js
```

### 步骤4: 发送测试请求
打开新终端窗口，运行：
```bash
# 测试普通请求
curl http://localhost:3000/

# 测试需要认证的路由
curl http://localhost:3000/protected

# 带模拟token的认证请求
curl -H "Authorization: Bearer fake-token" http://localhost:3000/protected
```

## 代码解析

### `app.js`
- 使用`express()`创建服务器实例
- 应用全局中间件（如日志）
- 定义路由及局部中间件链
- 设置错误处理中间件

### `middleware/logger.js`
- 记录每次请求的时间、方法和URL
- 展示中间件如何共享请求上下文

### `middleware/auth.js`
- 验证请求头中的Authorization字段
- 成功时调用`next()`，失败时返回401并终止流程

## 预期输出示例
启动服务后输出：
```
服务器运行在 http://localhost:3000
```

访问 `/` 的curl响应：
```
欢迎主页！\n```

访问 `/protected` 无token时：
```
{\"error\":\"未提供认证令牌\"}
```

带token访问 `/protected`：
```
受保护资源已访问\n```

## 常见问题解答

**Q: 修改代码后需要重启服务器吗？**
A: 是的，Node.js不会自动热重载。可使用`nodemon`提升开发体验：`npm install -g nodemon && nodemon app.js`

**Q: 中间件为什么不执行？**
A: 检查是否忘记调用`next()`，或提前发送了响应（如res.send后仍调用next）

**Q: 如何添加更多中间件？**
A: 在`.use()`或路由中按需添加，注意顺序影响执行流程

## 扩展学习建议
- 尝试添加速率限制中间件（如express-rate-limit）
- 实现基于角色的访问控制（RBAC）
- 使用Express Generator生成完整项目结构
- 学习异步中间件与Promise处理