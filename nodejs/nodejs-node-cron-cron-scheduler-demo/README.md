# Node-Cron定时任务调度演示

## 简介
本演示项目展示了如何使用 `node-cron` 库在 Node.js 中实现定时任务调度。通过多个实际场景，帮助开发者掌握定时执行脚本、日志记录和周期性任务管理的技巧。

## 学习目标
- 理解 cron 表达式的语法结构
- 掌握 node-cron 的基本与高级用法
- 实现不同频率的定时任务（每分钟、每天、每周等）
- 学会正确启动和停止定时任务

## 环境要求
- Node.js 版本：v14.x 或更高（推荐 v16+）
- npm 包管理器（随 Node.js 自动安装）
- 操作系统：Windows / Linux / macOS 均可

## 安装依赖的详细步骤

1. 确保已安装 Node.js 和 npm：
   ```bash
   node -v
   npm -v
   ```
   预期输出示例：
   ```
   v16.15.0
   8.11.0
   ```

2. 初始化项目（如果尚未初始化）：
   ```bash
   npm init -y
   ```

3. 安装 node-cron 依赖：
   ```bash
   npm install node-cron
   ```

## 文件说明
- `cron-basic.js`：基础示例——每分钟执行一次任务
- `cron-advanced.js`：进阶示例——每天上午9点发送提醒
- `cron-dynamic.js`：动态控制示例——可启动/停止的任务

## 逐步实操指南

### 步骤 1：运行基础定时任务
```bash
node cron-basic.js
```
预期输出（每分钟打印一次）：
```log
[定时任务] 当前时间: 2023-10-01T08:00:00Z
```

按 Ctrl+C 停止程序。

### 步骤 2：运行每日提醒任务
```bash
node cron-advanced.js
```
预期输出（每天上午9点触发）：
```log
[每日提醒] 早上好！今天是新一天的开始！
```

### 步骤 3：运行可控制的动态任务
```bash
node cron-dynamic.js
```
预期输出：
```log
[动态任务] 已启动，每5秒执行一次...
[动态任务] 执行中: 2023-10-01T08:00:05Z
...（5秒一次）
按 Enter 键停止任务...
```
按回车键后输出：
```log
[动态任务] 已成功停止。
```

## 代码解析

### cron-basic.js
```js
cron.schedule('*/1 * * * *', () => { ... });
```
- 使用标准 cron 表达式 `'*/1 * * * *'` 表示“每分钟”
- 回调函数中使用 `new Date()` 获取当前时间并打印

### cron-advanced.js
```js
cron.schedule('0 9 * * *', () => { ... }, { scheduled: true, timezone: 'Asia/Shanghai' });
```
- `'0 9 * * *'` 表示每天9点整执行
- 设置 `timezone` 为东八区，确保时间准确

### cron-dynamic.js
```js
const task = cron.schedule('*/5 * * * * *', () => { ... });
task.stop();
```
- 创建任务时不立即执行（`scheduled: false`）
- 可通过 `.start()` 和 `.stop()` 动态控制任务生命周期

## 预期输出示例
```log
[定时任务] 当前时间: 2023-10-01T08:00:00Z
[定时任务] 当前时间: 2023-10-01T08:01:00Z
[定时任务] 当前时间: 2023-10-01T08:02:00Z
```

## 常见问题解答

**Q: 为什么我的定时任务没有按预期时间运行？**
A: 检查系统时区设置。建议显式指定 `timezone` 参数，如 `'Asia/Shanghai'`。

**Q: 如何让任务只运行一次？**
A: 可以使用 `setTimeout` 或在回调中调用 `task.stop()` 实现单次执行。

**Q: 能否在 Docker 容器中运行这些任务？**
A: 可以，只要容器内有 Node.js 环境即可，注意时区同步（挂载 `/etc/localtime`）。

## 扩展学习建议
- 学习完整的 cron 表达式语法（5或6字段）
- 结合数据库实现持久化任务调度
- 使用 PM2 进程管理器部署长期运行的定时任务服务
- 探索更复杂的调度库如 `agenda` 或 `bree`