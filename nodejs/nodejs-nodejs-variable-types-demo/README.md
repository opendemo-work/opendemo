# NodeJS变量类型演示

## 简介
本示例演示了在Node.js环境中JavaScript的基本变量类型（如字符串、数字、布尔值、对象、数组和null/undefined）的声明与使用方法。通过三个不同的代码文件，帮助初学者理解变量类型的动态特性及最佳实践。

## 学习目标
- 掌握JavaScript中常见的变量类型
- 理解`let`、`const`和`var`的区别
- 学会使用`typeof`检查变量类型
- 了解变量提升和块级作用域的概念

## 环境要求
- Node.js v14 或更高版本（推荐v18+）
- 操作系统：Windows、macOS 或 Linux 均可

## 安装依赖的详细步骤
本项目无需第三方依赖，仅使用Node.js内置功能。

1. 打开终端或命令行工具
2. 运行以下命令检查Node.js版本：
   ```bash
   node -v
   ```
   预期输出：`v18.x.x` 或类似版本号
3. 若未安装，请前往 [https://nodejs.org](https://nodejs.org) 下载并安装LTS版本

## 文件说明
- `variables_basics.js`：演示基本变量类型的声明与typeof使用
- `variable_scope.js`：展示不同关键字（var/let/const）的作用域差异
- `dynamic_typing.js`：展示JavaScript动态类型的特点

## 逐步实操指南

### 第一步：创建项目目录
```bash
mkdir nodejs-variables-demo
cd nodejs-variables-demo
```

### 第二步：复制代码文件内容
将以下三个文件分别保存到项目目录中：
- `variables_basics.js`
- `variable_scope.js`
- `dynamic_typing.js`

### 第三步：运行每个示例

运行第一个示例：
```bash
node variables_basics.js
```
预期输出：各种变量类型的值和类型信息

运行第二个示例：
```bash
node variable_scope.js
```
预期输出：展示作用域和变量提升的行为差异

运行第三个示例：
```bash
node dynamic_typing.js
```
预期输出：显示同一变量在不同时刻的不同类型

## 代码解析

### variables_basics.js
关键点：使用`const`声明不可变绑定，`typeof`操作符检测类型，区分原始类型与引用类型。

### variable_scope.js
关键点：对比`var`的函数作用域与`let/const`的块级作用域，避免意外的变量提升问题。

### dynamic_typing.js
关键点：展示JavaScript是动态类型语言，变量可在运行时改变类型，无需显式声明。

## 预期输出示例
```
--- 基本变量类型 ---
姓名: 张三, 类型: string
年龄: 25, 类型: number
是否学生: true, 类型: boolean
分数: null, 类型: object
未定义值: undefined, 类型: undefined

--- 数组与对象 ---
爱好: ['读书','游泳'], 类型: object
个人信息: {name: '李四', age: 30}, 类型: object

--- 变量作用域演示 ---
块外: undefined
块内: 我是let变量
var变量在函数内: 我是var

--- 动态类型演示 ---
初始为字符串: Hello, 类型: string
变为数字: 42, 类型: number
变为布尔值: true, 类型: boolean
```

## 常见问题解答

**Q: 为什么`typeof null`返回`object`？**
A: 这是一个历史遗留bug，自JavaScript诞生以来就存在，但为了兼容性一直保留。

**Q: 应该使用`let`还是`const`？**
A: 默认使用`const`，只有当你明确需要重新赋值时才用`let`。

**Q: `var`还能用吗？**
A: 可以，但不推荐，因其容易引发作用域混乱问题。

## 扩展学习建议
- 阅读《你不知道的JavaScript（上卷）》了解变量机制底层原理
- 尝试使用TypeScript增强类型安全
- 学习ES6+的新特性如解构赋值、模板字符串等