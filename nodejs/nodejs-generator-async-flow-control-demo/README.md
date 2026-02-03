# Generator异步流控制演示

## 简介
本演示展示了如何使用JavaScript的Generator函数结合Promise，实现对异步操作的精确流程控制。通过三个实际场景，帮助理解Generator在复杂异步逻辑中的高级应用。

## 学习目标
- 理解Generator函数的基本机制和执行流程
- 掌握Generator与Promise结合处理异步操作的方法
- 学会使用Generator实现复杂的异步流程控制
- 理解`next()`方法和`yield`表达式的协同工作原理

## 环境要求
- Node.js >= 14.0.0（推荐使用LTS版本）
- 操作系统：Windows、Linux或macOS
- 命令行工具（如终端、PowerShell等）

## 安装依赖
本项目不依赖第三方包，仅使用Node.js原生功能。无需安装额外依赖。

```bash
# 检查Node.js版本
node --version
```

确保输出版本号不低于v14.0.0。

## 文件说明
- `async-flow-generator.js`: 主要示例，展示基本的异步任务序列控制
- `progressive-loader.js`: 模拟分步资源加载器，展示进度控制
- `retry-mechanism.js`: 实现带重试机制的异步操作控制器

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir generator-demo && cd generator-demo
```

### 步骤2：复制代码文件
将以下三个文件内容分别保存到对应路径：
- `async-flow-generator.js`
- `progressive-loader.js`
- `retry-mechanism.js`

### 步骤3：运行第一个示例
```bash
node async-flow-generator.js
```

**预期输出**：
```
开始异步流程...
执行第一步：初始化系统
延迟2秒...
第一步完成
执行第二步：加载配置
延迟1.5秒...
第二步完成
执行第三步：启动服务
延迟1秒...
第三步完成
所有步骤执行完毕
```

### 步骤4：运行第二个示例
```bash
node progressive-loader.js
```

**预期输出**：
```
开始分步加载...
[步骤1/3] 加载用户数据... 完成 (30%)
[步骤2/3] 加载配置文件... 完成 (60%)
[步骤3/3] 初始化界面... 完成 (100%)
加载完成！
```

### 步骤5：运行第三个示例
```bash
node retry-mechanism.js
```

**预期输出**：
```
尝试执行可能失败的操作...
第1次尝试：操作失败，500ms后重试
第2次尝试：操作失败，1000ms后重试
第3次尝试：操作成功！
最终结果：操作成功
```

## 代码解析

### async-flow-generator.js
```js
function* asyncFlow() {
  yield new Promise(...); // yield返回Promise对象
}
```
- Generator函数用`*`标识
- `yield`暂停执行并返回Promise
- 外部通过`.next()`恢复执行

### progressive-loader.js
```js
const progress = yield loadStep(...);
```
- 利用yield接收每一步的返回值（进度信息）
- 实现动态进度反馈

### retry-mechanism.js
```js
while(attempts < 3) {
  try { ... } catch { ... }
}
```
- 在Generator内部实现重试循环
- 结合try/catch处理异步错误

## 预期输出示例
见各步骤的“预期输出”部分。

## 常见问题解答

**Q: Generator现在还常用吗？**
A: 虽然async/await更流行，但Generator提供了更精细的控制能力，适合复杂流程编排、状态机等场景。

**Q: 为什么不用async/await？**
A: Generator允许外部控制执行时机，可用于实现自定义运行时、协程调度等高级模式，灵活性更高。

**Q: 如何调试Generator？**
A: 可以在`yield`语句处设置断点，或使用`console.log`输出中间状态。

## 扩展学习建议
- 学习Koa.js框架（基于Generator的Web框架）
- 研究Redux-Saga中的Generator应用
- 探索生成器在状态机和游戏开发中的用途
- 对比Generator与AsyncIterator的差异