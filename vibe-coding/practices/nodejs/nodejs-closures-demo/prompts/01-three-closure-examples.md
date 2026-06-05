# Prompt 01: 三个闭包示例

用 JavaScript 闭包实现三个文件：

closures-counter.js：
- createCounter() 函数，let count = 0，返回闭包 count++ 并返回
- 创建 counter1 和 counter2 两个独立实例
- 验证独立状态

closures-module.js：
- createUser(name, pwd) 函数
- 私有变量 username 和 password
- 返回 { getName, setName, checkPasswordLength }
- 测试密码不可访问

closures-event-simulator.js：
- createClickHandler(buttonId)，let clickCount = 0
- 返回闭包打印 "按钮 {buttonId} 被点击了 {clickCount} 次"
- 创建 handler1 和 handler2 模拟点击

---
## 背景
- 工具：Cursor（Cmd+K）
- 阶段：第 1-3 轮
- 结果：一次正确，无需修改
