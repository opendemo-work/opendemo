# 挑战：Node.js 闭包实战

## 难度：intermediate | 预计用时：20 分钟 | 推荐工具：任何 AI 编码工具

## 目标

用 JavaScript 闭包实现三个实用场景：

1. **计数器**（`closures-counter.js`）— `createCounter()` 返回一个函数，每次调用递增并返回计数值。创建两个独立计数器，验证状态互不干扰。

2. **模块模式**（`closures-module.js`）— `createUser(name, pwd)` 返回一个对象，包含：
   - `getName()` — 返回用户名
   - `setName(newName)` — 修改用户名
   - `checkPasswordLength()` — 返回密码长度
   - 密码本身不可直接访问（私有变量）

3. **事件模拟**（`closures-event-simulator.js`）— `createClickHandler(buttonId)` 返回点击处理函数，每个按钮独立维护点击次数。

## 约束

- Node.js 14+，不使用任何第三方库
- 每个场景一个独立文件
- 不使用 class，只用函数 + 闭包
- 代码注释使用中文

## 验证

```bash
# 计数器
node closures-counter.js
# 计数器1: 1
# 计数器1: 2
# 计数器2: 1  ← 独立状态
# 计数器1: 3

# 模块模式
node closures-module.js
# 用户名: Alice
# 密码长度: 6
# 更新用户名成功
# 新用户名: Bob
# 尝试直接访问密码: undefined  ← 私有变量

# 事件模拟
node closures-event-simulator.js
# 按钮 1 被点击了 1 次
# 按钮 2 被点击了 1 次
# 按钮 1 被点击了 2 次
# 按钮 1 被点击了 3 次
```

## 提示（卡住时再看）

<details>
<summary>提示 1：闭包的核心模式</summary>

外层函数定义局部变量，返回内层函数引用该变量。内层函数"记住"了外层函数的变量环境。

</details>

<details>
<summary>提示 2：模块模式的关键</summary>

返回一个对象，对象的属性是函数（getter/setter），这些函数共享同一个闭包环境中的私有变量。

</details>

<details>
<summary>提示 3：关键 Prompt</summary>

"用 JS 闭包实现三个示例：1) createCounter 计数器，每次调用递增，多个实例独立；2) createUser 模块模式，隐藏密码，暴露 getName/setName/checkPasswordLength；3) createClickHandler 事件处理器，每个按钮独立计数。不用 class，不用第三方库。"

</details>

## 对应原 Demo

完成后对比参考实现：`nodejs/nodejs-closures-demo/`
