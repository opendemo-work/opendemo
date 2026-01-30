# NodeJS日志管理Demo

## 简介
本项目演示了如何在Node.js应用中使用Winston和Bunyan两个流行的日志库来实现结构化日志记录。通过两个独立的例子，展示各自的最佳实践用法，适用于开发、测试和生产环境。

## 学习目标
- 掌握Winston的基本配置与自定义日志级别
- 理解Bunyan的JSON格式结构化日志输出
- 学会将日志输出到控制台和文件
- 了解结构化日志对监控和调试的重要性

## 环境要求
- Node.js v14 或更高版本（推荐v16+）
- npm 包管理器（随Node.js自动安装）
- 操作系统：Windows、Linux、macOS 均支持

## 安装依赖的详细步骤

1. 打开终端或命令行工具
2. 进入项目根目录
3. 执行以下命令安装所需依赖：

```bash
npm install
```

## 文件说明
- `winston-logger.js`：使用Winston实现多传输方式（控制台+文件）的日志记录
- `bunyan-logger.js`：使用Bunyan生成标准JSON格式的结构化日志
- `package.json`：包含项目元数据和依赖声明

## 逐步实操指南

### 步骤1：初始化项目（如未提供package.json）

```bash
npm init -y
```

### 步骤2：安装依赖

```bash
npm install winston@^3.8.2 bunyan@^1.8.15
```

### 步骤3：运行Winston示例

```bash
node winston-logger.js
```

**预期输出**：
```
[INFO] 应用启动成功 - 用户ID: 123, 模块: auth
[ERROR] 数据库连接失败 - 错误: Connection timeout, 重试次数: 3
日志已保存至 ./logs/app.log
```

同时会在项目目录下创建 `logs/app.log` 文件，内容类似：
```
[INFO] 应用启动成功 - 用户ID: 123, 模块: auth
[ERROR] 数据库连接失败 - 错误: Connection timeout, 重试次数: 3
```

### 步骤4：运行Bunyan示例

```bash
node bunyan-logger.js
```

**预期输出（JSON格式）**：
```json
{"name":"UserService","hostname":"localhost","pid":12345,"level":30,"msg":"用户登录成功","userId":1001,"ip":"192.168.1.10","time":"2023-04-05T10:00:00.000Z","v":0}
{"name":"UserService","hostname":"localhost","pid":12345,"level":50,"msg":"数据库查询异常","query":"SELECT * FROM users","error":"ETIMEDOUT","time":"2023-04-05T10:00:05.000Z","v":0}
```

## 代码解析

### winston-logger.js 关键点
- 使用 `winston.createLogger()` 创建日志器实例
- 配置 `transports` 实现同时输出到控制台和文件
- 自定义日志格式：时间、级别、消息及元数据
- 确保日志目录存在，避免写入失败

### bunyan-logger.js 关键点
- Bunyan 默认输出为JSON，天然支持结构化日志
- 支持嵌套字段如 `src: true` 可追踪代码位置
- 日志级别清晰（trace=10, debug=20, info=30, warn=40, error=50, fatal=60）
- 元数据可直接作为参数传入，自动合并到输出中

## 预期输出示例
见“逐步实操指南”中的输出样例。

## 常见问题解答

**Q: 运行时报错 'Cannot find module'？**
A: 请确认是否已执行 `npm install` 并正确安装所有依赖。

**Q: logs目录没有被创建？**
A: 检查当前用户是否有写权限，或手动创建 `logs/` 目录再运行。

**Q: Bunyan输出太冗长怎么办？**
A: 可使用 `bunyan` CLI 工具美化输出：`npm install -g bunyan && node bunyan-logger.js | bunyan`

**Q: 如何将日志发送到ELK或Splunk？**
A: Winston可通过`winston-elasticsearch`等传输插件集成；Bunyan日志因是JSON格式，易于被Logstash采集。

## 扩展学习建议
- 尝试将日志写入Elasticsearch或Syslog
- 使用PM2配合日志轮转功能
- 集成Sentry进行错误追踪
- 学习使用Winston的日志过滤和格式化函数
- 探索Bunyan的子记录器（child logger）用于模块化日志