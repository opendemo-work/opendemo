# 解决过程：Node.js 闭包实战

## 使用的工具：Cursor（Cmd+K 行内编辑）

---

### 第 1 轮：计数器

**Prompt：**
> 创建 closures-counter.js：
> - createCounter() 函数，内部有 let count = 0
> - 返回一个闭包函数，每次调用 count++ 并返回 count
> - 创建 counter1 和 counter2 两个独立实例
> - 调用 counter1() 两次（输出 1, 2），counter2() 一次（输出 1），counter1() 一次（输出 3）

**AI 生成：** 完全正确。一次性生成，无需修改。

---

### 第 2 轮：模块模式

**Prompt：**
> 创建 closures-module.js：
> - createUser(name, pwd) 函数
> - 内部私有变量 username 和 password
> - 返回对象：getName(), setName(newName), checkPasswordLength()
> - 没有 getPassword 方法（密码不可访问）
> - setName 要验证非空字符串
> - 测试：创建 user('Alice', 'secret')，获取名字，改名为 Bob，尝试访问 user.password

**AI 生成：** 正确。

**注意：** AI 的 setName 验证用了 `newName.trim().length === 0`，原实现用 `typeof newName === 'string' && newName.length > 0`。两种都可以，保持 AI 版本。

---

### 第 3 轮：事件模拟

**Prompt：**
> 创建 closures-event-simulator.js：
> - createClickHandler(buttonId) 函数
> - 内部 let clickCount = 0
> - 返回闭包：clickCount++ 并打印 "按钮 {buttonId} 被点击了 {clickCount} 次"
> - 创建 handler1(1) 和 handler2(2)
> - 模拟点击序列：handler1, handler2, handler1, handler1

**AI 生成：** 正确。

---

### 第 4 轮：验证

```bash
node closures-counter.js
node closures-module.js
node closures-event-simulator.js
```

**结果：** 三个文件全部正确 ✅

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 4 轮 |
| 实际用时 | ~8 分钟 |
| AI 犯错次数 | 0 |
| 人工干预 | 无 |

### 关键技巧
- **闭包 demo 是 AI 最容易生成的** — 概念清晰、代码简短、无外部依赖
- **每个文件独立** — 不需要 package.json 管理，直接 `node xxx.js` 运行
- **适合初学 vibe coding** — 快速获得成功体验

### 常见坑
- 闭包中的 `for` 循环 `var` vs `let` — 用 `let` 才能正确捕获每次迭代的变量
- `this` 在闭包中的指向 — 箭头函数捕获外层 `this`，普通函数的 `this` 取决于调用方式
- 内存泄漏 — 闭包持有外部变量引用，如果闭包长期存在（如事件监听器），变量不会被 GC
