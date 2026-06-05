# 挑战：Node.js 熔断器模式

## 难度：advanced | 预计用时：30 分钟 | 推荐工具：Cursor / Claude Code

## 目标

实现一个熔断器（Circuit Breaker）保护不稳定的服务调用：

1. **主程序**（`circuit-breaker-demo.js`）— 模拟远程服务调用，70% 失败率，使用熔断器包装
2. **降级服务**（`fallback-service.js`）— 熔断开启时返回默认安全响应
3. **熔断行为** — 连续 2 次失败后熔断开启，后续请求直接走降级，5 秒后尝试恢复

## 约束

- Node.js 14+
- 使用 `circuit-breaker-js` 库
- 熔断器配置：`threshold: 2`（失败次数），`timeout: 5000`（熔断持续时间）
- 模拟服务：1000ms 延迟，70% 失败率
- 降级响应包含 `message`、`code: 503`、`timestamp`
- 演示循环调用 6 次，间隔 1200ms

## 验证

```bash
npm install
node circuit-breaker-demo.js
```

预期输出（因随机性可能不完全一致，但应展示完整的状态转换）：
```
调用服务... 响应: 成功响应
调用服务... 错误: 模拟网络超时
调用服务... 错误: 模拟网络超时
调用服务... 熔断器已开启，执行降级逻辑    ← 触发熔断
调用服务... 熔断器已开启，执行降级逻辑
调用服务... 熔断器已开启，执行降级逻辑
```

## 提示（卡住时再看）

<details>
<summary>提示 1：熔断器状态机</summary>

三种状态：Closed（正常）→ 连续失败达到阈值 → Open（熔断，直接走 fallback）→ 超时后 → Half-Open（尝试放行一个请求）→ 成功则 Closed，失败则 Open。

</details>

<details>
<summary>提示 2：模拟不稳定服务</summary>

用 `Math.random() < 0.7` 控制 70% 失败率，`setTimeout` 模拟延迟。

</details>

<details>
<summary>提示 3：关键 Prompt</summary>

"用 Node.js 实现熔断器模式。模拟一个 70% 失败率的远程服务。用 circuit-breaker-js 库，threshold=2，timeout=5000ms。连续 2 次失败后触发熔断，走 fallback 返回 503。循环调用 6 次观察状态变化。"

</details>

## 对应原 Demo

完成后对比参考实现：`nodejs/nodejs-circuit-breaker-demo/`
