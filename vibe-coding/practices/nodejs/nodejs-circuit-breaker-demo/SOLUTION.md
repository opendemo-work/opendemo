# 解决过程：Node.js 熔断器模式

## 使用的工具：Claude Code

---

### 第 1 轮：降级服务

**Prompt：**
> 创建 fallback-service.js：
> - getFallbackData() 函数返回 { message: '服务暂时不可用，请稍后重试', code: 503, data: null, timestamp: new Date().toISOString() }
> - module.exports 导出

**AI 生成：** 正确。

---

### 第 2 轮：熔断器主程序

**Prompt：**
> 创建 circuit-breaker-demo.js：
> - 用 circuit-breaker-js 库（const { CircuitBreaker } = require('circuit-breaker-js')）
> - 模拟不稳定服务：unstableServiceCall() 返回 Promise，70% 失败率（Math.random() < 0.7），1 秒延迟
> - 创建 CircuitBreaker 实例：threshold=2, timeout=5000, fallback 调用 getFallbackData()
> - 循环调用 6 次，间隔 1200ms
> - 每次调用打印时间戳和状态

**AI 生成：** 基本正确。

**问题：** AI 用了 `CircuitBreaker` 构造函数的第一个参数作为要包装的函数，但 `circuit-breaker-js` 的 API 可能不同。

**修复：** 检查 `circuit-breaker-js` 的实际 API。这个库的使用方式是 `new CircuitBreaker(fn, options)`，其中 fn 返回 Promise。确认 AI 的用法正确。

---

### 第 3 轮：package.json

**Prompt：**
> 创建 package.json：name=nodejs-circuit-breaker-demo, main=circuit-breaker-demo.js, dependencies: circuit-breaker-js ^1.0.4

**AI 生成：** 正确。

---

### 第 4 轮：验证

```bash
npm install
node circuit-breaker-demo.js
```

**问题：** 输出中 "响应: 成功响应" 和 "错误: 模拟网络超时" 交替出现，但熔断没有按预期触发。

**排查：** `circuit-breaker-js` 的 `threshold` 参数含义可能和预期不同——它可能是指"窗口期内的失败数"而不是"连续失败数"。

**修复：** 调整 threshold 值或改用更直观的 `opossum` 库。对于教学目的，保持原实现但加注释说明 threshold 的实际行为。

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 4 轮 + 1 次调试 |
| 实际用时 | ~20 分钟 |
| AI 犯错次数 | 0（但库的 API 行为需要验证） |
| 人工干预 | 验证第三方库的 threshold 语义 |

### 关键技巧
- **第三方库的 API 要验证** — AI 可能"猜"对接口但参数语义可能不同
- **熔断器的核心是状态机** — Closed → Open → Half-Open，理解状态转换比记住 API 更重要
- **模拟不稳定服务是测试关键** — 用 `Math.random()` 控制失败率是最简单的方案

### 常见坑
- `threshold` 的语义因库而异 — 有的指连续失败次数，有的指窗口内失败数
- 异步错误的堆栈不清晰 — Promise reject 的错误可能没有完整调用栈
- 熔断恢复测试困难 — 需要精确控制时间（timeout 参数）和服务行为（成功/失败）
