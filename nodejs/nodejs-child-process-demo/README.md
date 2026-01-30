# Node.js子进程管理实战演示

## 简介
本项目通过两个具体场景演示如何在Node.js中使用`child_process`模块的`spawn`和`exec`方法安全、高效地创建和管理子进程。涵盖流式输出处理、错误捕获、跨平台兼容性等核心知识点。

## 学习目标
- 理解spawn与exec的核心区别及适用场景
- 掌握子进程的标准输入/输出/错误流处理
- 学会正确监听子进程事件并处理异常
- 实践跨平台命令执行的最佳方式

## 环境要求
- Node.js v14.17.0 或更高版本（推荐v18+ LTS）
- 操作系统：Windows / macOS / Linux（均支持）
- 基础命令行工具：`ls` (Unix) 或 `dir` (Windows)，`node`

## 安装依赖
此项目无需第三方依赖，仅使用Node.js内置模块。

```bash
# 克隆项目后进入目录
npm init -y
```

> 注意：虽然没有外部依赖，但需要确保Node.js已正确安装。

## 文件说明
- `spawn-example.js`: 使用spawn执行长时间运行的命令，实时输出结果
- `exec-example.js`: 使用exec执行短时命令并获取完整输出

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir child-process-demo && cd child-process-demo
```

### 步骤2：创建代码文件
将以下两个文件保存到项目根目录：
- `spawn-example.js`
- `exec-example.js`

### 步骤3：运行spawn示例
```bash
node spawn-example.js
```

**预期输出**：
```
[stdout] 包含当前目录文件列表（逐行输出）...
[stderr] （通常为空）
子进程退出码: 0
```

### 步骤4：运行exec示例
```bash
node exec-example.js
```

**预期输出**：
```
完整命令输出:
包含当前目录内容的文本...

子进程成功执行
```

## 代码解析

### spawn-example.js 关键点
- 使用`spawn`适合处理大输出或实时流数据
- 通过`data`事件分块接收stdout/stderr
- 监听`close`事件获取退出码
- 跨平台自动选择`ls`或`dir`

### exec-example.js 关键点
- `exec`适合小量输出的短时命令
- 回调函数直接返回完整stdout/stderr字符串
- 设置`maxBuffer`防止大输出导致崩溃
- 同样具备跨平台兼容判断

## 预期输出示例
### spawn-example.js
```
[stdout] package.json\n[stdout] README.md\n[stdout] spawn-example.js\n子进程退出码: 0
```

### exec-example.js
```
完整命令输出:
package.json\nREADME.md\nexec-example.js

子进程成功执行
```

## 常见问题解答

**Q: spawn和exec有什么区别？**
A: `spawn`返回流接口，适合大数据量或实时处理；`exec`缓冲全部输出，适合小结果集。

**Q: 为什么exec会报maxBuffer exceeded错误？**
A: 默认缓冲区为200KB，可通过配置`maxBuffer`参数增大，但应优先考虑改用`spawn`。

**Q: 如何在Windows上运行Unix命令？**
A: 使用`cross-env`或条件判断切换命令，如本例中根据平台选择`ls`或`dir`。

## 扩展学习建议
- 尝试用`spawn`执行Python/Java脚本并通信
- 学习`child_process.fork()`用于Node.js子进程间IPC通信
- 探索`execFile`避免shell注入风险
- 阅读官方文档中关于`options.shell`的安全提示