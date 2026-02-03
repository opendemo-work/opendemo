# Node.js Worker Threads 多线程编程实战示例

## 简介
本示例演示了如何使用 Node.js 的 `worker_threads` 模块来实现多线程编程，提升 CPU 密集型任务（如计算斐波那契数列、数据加密）的执行效率。通过创建多个工作线程并行处理任务，有效避免主线程阻塞。

## 学习目标
- 理解 Node.js 单线程模型的局限性
- 掌握 `worker_threads` 模块的基本用法
- 学会在线程间安全传递数据
- 实践多线程并发编程的最佳实践

## 环境要求
- Node.js 版本 >= 14.0.0（推荐使用 LTS 版本）
- 操作系统：Windows / Linux / macOS（跨平台兼容）

## 安装依赖的详细步骤
1. 确保已安装 Node.js 和 npm
   ```bash
   node --version
   # 输出应为 v14.0.0 或更高版本
   ```

2. 克隆或创建项目目录，并进入该目录
   ```bash
   mkdir worker-threads-demo && cd worker-threads-demo
   ```

3. 初始化 npm 项目（可选，仅用于管理元信息）
   ```bash
   npm init -y
   ```

> 注意：本示例不依赖第三方包，仅使用 Node.js 内置模块。

## 文件说明
- `fibonacci-worker.js`: 执行斐波那契计算的工作线程逻辑
- `main.js`: 主线程入口，创建多个工作线程并汇总结果

## 逐步实操指南

### 步骤 1: 创建工作线程文件
```bash
cat > fibonacci-worker.js << 'EOF'
$(cat fibonacci-worker.js)
EOF
```

### 步骤 2: 创建主程序文件
```bash
cat > main.js << 'EOF'
$(cat main.js)
EOF
```

### 步骤 3: 运行程序
```bash
node main.js
```

### 预期输出
```bash
启动 4 个线程进行斐波那契计算...
线程 #1 完成，结果: 10946
线程 #3 完成，结果: 10946
线程 #2 完成，结果: 10946
线程 #4 完成，结果: 10946
✅ 所有线程执行完毕，总耗时: 850ms
```

## 代码解析

### `fibonacci-worker.js`
- 使用 `parentPort` 接收主线程传入的任务数据
- 计算斐波那契数列（模拟 CPU 密集型任务）
- 通过 `parentPort.postMessage()` 返回结果

### `main.js`
- 创建多个 `Worker` 实例，每个运行独立的 JS 文件
- 使用 Promise 封装异步通信，等待所有线程完成
- 监听 `message` 和 `error` 事件确保健壮性
- 利用 `performance.now()` 统计执行时间，体现并发优势

## 预期输出示例
```
启动 4 个线程进行斐波那契计算...
线程 #1 完成，结果: 10946
线程 #3 完成，结果: 10946
线程 #2 完成，结果: 10946
线程 #4 完成，结果: 10946
✅ 所有线程执行完毕，总耗时: 850ms
```

## 常见问题解答

**Q: 为什么不能直接在主线程中进行大量计算？**
A: Node.js 是单线程事件循环模型，长时间运行的计算会阻塞事件循环，导致无法响应 I/O 请求或其他操作。

**Q: 如何在线程之间共享数据？**
A: 可以使用 `SharedArrayBuffer` 实现内存共享，但需注意同步问题。普通数据通过 `postMessage` 拷贝传递更安全。

**Q: 是否可以传递函数或复杂对象给 Worker？**
A: 不可以。只能传递可结构化克隆的数据类型（如 JSON 对象），函数和某些原生对象无法序列化。

**Q: Worker 线程适合哪些场景？**
A: 适合图像处理、大数据分析、加密解密、科学计算等 CPU 密集型任务。

## 扩展学习建议
- 尝试使用 `Piscina` 库管理 Worker Pool，提高复用性和性能
- 结合 `cluster` 模块实现多进程 + 多线程混合架构
- 学习 `Atomics` API 实现线程间同步控制
- 探索 `worker_threads` 与 Express/Koa 集成处理高负载请求
