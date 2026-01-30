# Node.js Proxy与Reflect元编程实战演示

## 简介
本演示项目展示了JavaScript中`Proxy`和`Reflect`对象的强大功能，通过三个具体场景：属性访问拦截、函数调用代理和响应式数据系统，帮助开发者深入理解元编程的核心概念。

## 学习目标
- 掌握Proxy的基本语法和常用陷阱（traps）
- 理解Reflect的作用及其与Proxy的协作机制
- 实现数据监听与响应式更新
- 应用元编程解决实际开发问题

## 环境要求
- Node.js 版本：14.0.0 或更高（推荐使用 LTS 版本 16+）
- 操作系统：Windows、macOS、Linux 均可
- 包管理器：npm（随Node.js自动安装）

## 安装依赖的详细步骤
```bash
# 克隆项目或创建新目录后进入
npm init -y
```
> 本示例不依赖第三方库，仅使用原生Node.js API。

## 文件说明
- `proxy-basic.js`：基础属性拦截示例
- `proxy-function.js`：函数调用代理与日志记录
- `reactive-system.js`：简易响应式数据系统实现

## 逐步实操指南

### 步骤1：运行基础代理示例
```bash
node proxy-basic.js
```
**预期输出**：
```
读取属性 'name' -> 返回 'Alice'
调用方法 getAge() -> 返回 25
尝试写入只读属性 name
警告：禁止修改只读属性 'name'
```

### 步骤2：运行函数代理示例
```bash
node proxy-function.js
```
**预期输出**：
```
调用 greet('Bob')，参数长度: 1
执行原始函数：Hello, Bob!
调用 calc.sum(2,3)，路径: calc.sum
结果: 5
```

### 步骤3：运行响应式系统示例
```bash
node reactive-system.js
```
**预期输出**：
```
姓名已更新为：Charlie
年龄增加到：31
```

## 代码解析

### proxy-basic.js 关键点
```js
const handler = {
  get(target, property) {
    console.log(`读取属性 '${property}'`);
    return Reflect.get(target, property);
  }
}
```
使用`Reflect.get`安全地获取原始值，避免this指向丢失。

### reactive-system.js 核心逻辑
利用`set`陷阱在数据变化时触发回调，模拟Vue等框架的响应式原理。

## 预期输出示例
见各步骤中的“预期输出”部分。

## 常见问题解答

**Q: Proxy兼容性如何？**
A: Node.js 6+ 支持，现代浏览器均支持。不支持IE。

**Q: 为什么需要Reflect？**
A: Reflect提供了一套统一的方法来执行JavaScript操作，并确保与Proxy配合时行为一致。

**Q: 可以代理数组吗？**
A: 可以！Proxy能拦截push、pop等操作，常用于实现可观测数组。

## 扩展学习建议
- 阅读MDN文档中关于[Proxy](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy)和[Reflect](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Reflect)
- 研究Vue 3的reactivity源码
- 尝试实现一个带验证功能的表单模型