# 用 AI Debug 的方法

## 核心理念：AI 是最强的 debug 合伙人

传统 debug：你 → 看报错 → 搜索 → 试修复 → 再看报错
AI debug：你 → 把报错+代码给 AI → AI 分析原因 → 给出修复 → 你验证

## 五种 AI Debug 模式

### 模式一：报错堆栈分析

```
运行报错：

[粘贴完整错误堆栈]

相关代码：
[粘贴相关函数]

分析原因并给出修复方案。不要只改表面的错误，找到根本原因。
```

**关键**：粘贴完整的错误堆栈，不要截断。

### 模式二：行为不符预期

```
这段代码应该：每秒打印一次 "heartbeat"
实际行为：只打印了一次就停了

代码：
[paste]

运行输出：
[paste]

分析为什么循环没有继续。
```

**关键**：描述"期望行为"和"实际行为"的差异。

### 模式三：测试失败分析

```
测试失败：

=== RUN   TestWorkerPool
    worker_pool_test.go:45: expected 100 tasks completed, got 97
    worker_pool_test.go:46: expected no errors, got 3 errors: [task timeout, task timeout, task timeout]

被测代码：[paste]
测试代码：[paste]

不要修改测试，修复被测代码让测试通过。
```

**关键**：告诉 AI "不要改测试"，否则它可能通过放松断言来"修复"。

### 模式四：性能问题定位

```
这个 API 接口响应时间从 50ms 涨到了 2s。
代码如下：[paste]

数据库查询：[paste]

分析可能的性能瓶颈，给出优化建议。重点关注 N+1 查询和缺少索引的问题。
```

**关键**：给 AI 一个方向（如 N+1 查询），缩小排查范围。

### 模式五：竞态条件 / 并发 Bug

```
用 go race detector 检测到竞态条件：

==================
WARNING: DATA RACE
Write at 0x00c0000b6018 by goroutine 8:
  main.(*Pool).Submit()
      pool.go:42 +0x123

Previous read at 0x00c0000b6018 by goroutine 7:
  main.(*Pool).Status()
      pool.go:58 +0x45
==================

相关代码：[paste pool.go]

分析哪个变量存在竞态，给出加锁方案。
```

**关键**：粘贴完整的 race detector 输出，AI 可以精确定位到行号。

## Debug 的元技巧

### 1. 让 AI 先分析，再修改
```
先不要修改代码，只分析：
1. 错误的根本原因是什么？
2. 有哪些可能的修复方案？
3. 每种方案的 trade-off 是什么？

分析完后再选择方案实施。
```

### 2. 缩小范围
```
我怀疑问题出在这个函数的第 30-45 行之间。
请只看这段代码：[paste]
```

### 3. 构造最小复现
```
帮我写一个最小可运行的示例来复现这个 bug：
[描述 bug 现象]
```

## 实战练习

- [Go Docker SDK](../../practices/go/go-dockersdkgo-container-management/CHALLENGE.md) — 容器操作常见错误
- [Node.js 熔断器](../../practices/nodejs/nodejs-circuit-breaker-demo/CHALLENGE.md) — 异步错误处理
- [Go gRPC](../../practices/go/go-grpc-protobuf-go-demo/CHALLENGE.md) — proto 代码生成问题
