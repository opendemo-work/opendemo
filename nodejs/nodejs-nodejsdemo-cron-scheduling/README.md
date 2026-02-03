# NodeJS定时任务调度Demo

## 简介
本示例演示如何在Node.js中使用`node-schedule`库实现强大的定时任务调度功能。涵盖基础定时、Cron表达式和动态任务管理三种常见场景。

## 学习目标
- 掌握Node.js中定时任务的基本实现方式
- 理解Cron表达式的语法和应用
- 学会动态创建和取消定时任务
- 了解生产环境中的最佳实践

## 环境要求
- Node.js 14.x 或更高版本
- npm 6.x 或更高版本
- 操作系统：Windows / Linux / macOS（跨平台兼容）

## 安装依赖步骤

```bash
# 1. 确认Node.js版本
node --version
# 预期输出: v14.0.0 或更高

# 2. 初始化项目（如果尚未初始化）
npm init -y

# 3. 安装必需的依赖
cd code && npm install
```

## 文件说明
- `basic-scheduler.js`: 基础定时任务示例
- `cron-scheduler.js`: 使用Cron表达式的高级调度
- `dynamic-scheduler.js`: 动态任务管理示例

## 逐步实操指南

```bash
# 进入代码目录
cd code

# 运行基础定时任务
node basic-scheduler.js
# 预期输出: 每5秒打印一次当前时间

# 运行Cron表达式任务
node cron-scheduler.js
# 预期输出: 每分钟的第30秒执行一次

# 运行动态任务管理
node dynamic-scheduler.js
# 预期输出: 创建任务后10秒自动取消
```

## 代码解析

### basic-scheduler.js
```javascript
// 使用固定间隔执行任务
// schedule.scheduleJob() 提供比原生setInterval更强大的功能
// 支持日期对象、毫秒数等多种触发方式
```

### cron-scheduler.js
```javascript
// Cron表达式格式: second minute hour dayOfMonth month dayOfWeek
// '30 * * * * *' 表示每分钟的第30秒执行
// 比传统crontab多支持秒级精度
```

### dynamic-scheduler.js
```javascript
// 通过变量保存任务引用
// 调用cancel()方法可动态取消任务
// 适用于需要条件性停止的任务场景
```

## 预期输出示例
```
[基础调度] 当前时间: 2024-01-01T10:30:05.123Z
[基础调度] 当前时间: 2024-01-01T10:30:10.123Z
[Cron调度] 执行时间: 2024-01-01T10:30:30.456Z
[动态调度] 任务已启动
[动态调度] 任务执行中... 1
[动态调度] 任务已取消
```

## 常见问题解答

**Q: 为什么使用node-schedule而不是setInterval？**
A: node-schedule支持Cron表达式、时区设置、更精确的调度控制，且API更友好。

**Q: 如何在生产环境中持久化定时任务？**
A: 建议结合数据库存储任务配置，应用启动时重新加载任务。

**Q: 任务执行时间超过调度间隔会怎样？**
A: node-schedule会等待当前任务完成后再触发下一次，不会并行执行。

## 扩展学习建议
- 学习完整的Cron表达式语法
- 研究分布式任务调度解决方案（如Bull + Redis）
- 了解任务失败重试机制的实现
- 探索与日志系统的集成