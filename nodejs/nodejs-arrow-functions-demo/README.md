# Arrow Functions Demo

## 简介
本示例演示了在 Node.js 中使用箭头函数（Arrow Functions）的几种常见场景。箭头函数是 ES6 引入的重要特性，提供了更简洁的语法，并解决了传统函数中 `this` 指向的问题。

## 学习目标
- 理解箭头函数的基本语法
- 掌握箭头函数在数组处理中的应用
- 理解箭头函数与普通函数在 `this` 绑定上的区别

## 环境要求
- Node.js 版本：14.x 或更高（推荐 LTS 版本 16+）
- 操作系统：Windows、Linux、macOS 均可

## 安装依赖
本项目无需第三方依赖，仅使用 Node.js 内置模块。

## 文件说明
- `basic-arrow-example.js`：基础箭头函数语法演示
- `array-methods-with-arrows.js`：在数组方法中使用箭头函数
- `this-binding-comparison.js`：对比箭头函数与普通函数的 this 行为

## 逐步实操指南

### 步骤 1: 检查 Node.js 版本
运行以下命令检查是否已安装 Node.js 及其版本：
```bash
node --version
```
**预期输出**：
```bash
v16.14.0  # 或类似版本号
```

### 步骤 2: 创建项目目录并放入文件
创建一个新目录并保存所有 .js 文件：
```bash
mkdir arrow-demo && cd arrow-demo
# 将 basic-arrow-example.js, array-methods-with-arrows.js, this-binding-comparison.js 复制到此目录
```

### 步骤 3: 运行第一个示例
```bash
node basic-arrow-example.js
```
**预期输出**：
```bash
加法结果: 8
问候语: Hello, Alice
```

### 步骤 4: 运行数组方法示例
```bash
node array-methods-with-arrows.js
```
**预期输出**：
```bash
偶数: [2, 4, 6]
平方: [1, 4, 9, 16]
总和: 10
```

### 步骤 5: 运行 this 绑定对比示例
```bash
node this-binding-comparison.js
```
**预期输出**：
```bash
普通函数中的 this.name: undefined
箭头函数中的 this.name: 张三
```

## 代码解析

### basic-arrow-example.js
```js
const add = (a, b) => a + b;
```
- 使用箭头语法定义单行函数，省略 `return` 关键字
- 适用于简单表达式

### array-methods-with-arrows.js
```js
const evens = numbers.filter(n => n % 2 === 0);
```
- 在 `filter`, `map`, `reduce` 中广泛使用箭头函数，使代码更清晰

### this-binding-comparison.js
```js
setTimeout(() => { console.log('箭头函数中的 this.name:', this.name); }, 100);
```
- 箭头函数不绑定自己的 `this`，而是继承外层作用域的 `this`
- 在对象方法中使用时避免了常见的 `this` 丢失问题

## 预期输出汇总
所有脚本运行后应分别输出对应结果，无错误信息。

## 常见问题解答

**Q: 为什么箭头函数不能用作构造函数？**
A: 箭头函数没有 `prototype` 属性，也不绑定 `this`，因此调用 `new` 会抛出错误。

**Q: 何时不应使用箭头函数？**
A: 不应在需要动态 `this` 的场景使用，如对象方法（需谨慎）、构造函数、或事件处理器中需要访问 DOM 元素时。

## 扩展学习建议
- 阅读 MDN 文档：[Arrow function expressions](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
- 学习闭包与箭头函数的结合使用
- 实践在异步编程（Promise、async/await）中使用箭头函数