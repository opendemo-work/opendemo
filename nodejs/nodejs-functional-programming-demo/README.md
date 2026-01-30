# NodeJS函数编程实战演示

## 简介
本演示项目展示了Node.js中函数的三种核心用法：基础函数定义与调用、高阶函数应用以及异步函数处理。适合初学者理解JavaScript函数在服务端的实际运用。

## 学习目标
- 掌握函数声明、表达式和箭头函数的使用
- 理解高阶函数的概念及其在数据处理中的优势
- 学会使用async/await编写异步操作
- 熟悉模块化开发中的函数导出与导入

## 环境要求
- Node.js 14.x 或更高版本（推荐 LTS 版本）
- npm 6.x 或更高版本
- 操作系统：Windows、macOS、Linux 均支持

## 安装依赖的详细步骤
1. 打开终端或命令行工具
2. 进入项目根目录
3. 执行以下命令安装依赖（本项目无外部依赖，无需安装）

```bash
npm init -y
```

> 注意：此命令仅生成package.json，项目本身不依赖第三方包。

## 文件说明
- `functions/basic.js`：基础函数示例，展示不同函数定义方式
- `functions/higherOrder.js`：高阶函数示例，演示map、filter等函数式编程技巧
- `functions/async.js`：异步函数示例，模拟API请求并处理结果

## 逐步实操指南

### 第一步：创建项目结构
```bash
mkdir -p functions-demo/functions
cd functions-demo
```

### 第二步：复制代码文件
将提供的三个JS文件分别保存到 `functions/` 目录下。

### 第三步：运行每个示例

运行基础函数示例：
```bash
node functions/basic.js
```
**预期输出**：\nHello, 张三\n5 + 3 = 8

运行高阶函数示例：
```bash
node functions/higherOrder.js
```
**预期输出**：\n成年人: [ { name: '李四', age: 25 }, { name: '王五', age: 30 } ]

运行异步函数示例：
```bash
node functions/async.js
```
**预期输出**：\n正在获取用户数据...\n用户数据: { id: 1, name: 'Alice' }

## 代码解析

### basic.js 关键点
```js
// 使用箭头函数简化语法，适合简单逻辑
const add = (a, b) => a + b;
```
箭头函数省略了return关键字和大括号，适用于单行表达式。

### higherOrder.js 关键点
```js
// filter是高阶函数，接受一个函数作为参数
const adults = users.filter(isAdult);
```
高阶函数提升了代码抽象层级，使逻辑更清晰可读。

### async.js 关键点
```js
// async函数自动返回Promise，可用await等待异步操作
const userData = await fetchUser(1);
```
async/await让异步代码像同步一样书写，降低回调地狱风险。

## 预期输出示例
```
# node functions/basic.js
Hello, 张三
5 + 3 = 8

# node functions/higherOrder.js
成年人: [ { name: '李四', age: 25 }, { name: '王五', age: 30 } ]

# node functions/async.js
正在获取用户数据...
用户数据: { id: 1, name: 'Alice' }
```

## 常见问题解答

**Q: 报错 'Cannot find module'？**
A: 请确认文件路径正确，且运行命令时在项目根目录执行。

**Q: async函数为什么不用.then？**
A: async/await是Promise的语法糖，await会自动解包Promise值，比链式调用更直观。

**Q: 箭头函数和普通函数有什么区别？**
A: 箭头函数没有自己的this、arguments，不能用作构造函数，但语法更简洁。

## 扩展学习建议
- 阅读MDN关于[JavaScript函数](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Functions)的指南
- 学习闭包和柯里化提升函数式编程能力
- 尝试使用Lodash库进行复杂数据处理
- 探索Express中间件中的高阶函数模式