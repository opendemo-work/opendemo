# Prompt 01: 降级服务 + 熔断器主程序

创建两个文件：

fallback-service.js：
- getFallbackData() 返回 { message: '服务暂时不可用...', code: 503, data: null, timestamp }
- module.exports 导出

circuit-breaker-demo.js：
- 用 circuit-breaker-js 的 CircuitBreaker
- unstableServiceCall()：70% 失败率（Math.random() < 0.7），1 秒延迟
- 熔断配置：threshold=2, timeout=5000, fallback 调用 getFallbackData()
- 循环 6 次，间隔 1200ms
- 打印时间戳和状态

package.json：dependencies 包含 circuit-breaker-js ^1.0.4

验证：npm install && node circuit-breaker-demo.js

---
## 背景
- 工具：Claude Code
- 阶段：第 1-4 轮
- 结果：circuit-breaker-js 的 threshold 语义需要验证
