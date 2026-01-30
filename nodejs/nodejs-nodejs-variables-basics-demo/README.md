# NodeJS变量基础演示

## 简介
本演示项目展示了在Node.js环境中使用`var`、`let`和`const`声明变量的不同方式，帮助初学者理解JavaScript中的变量作用域、提升（hoisting）以及最佳实践。

## 学习目标
- 理解 `var`、`let` 和 `const` 的区别
- 掌握块级作用域与函数作用域的概念
- 避免常见变量声明陷阱
- 遵循现代JavaScript编码规范

## 环境要求
- Node.js 版本：14.x 或更高（推荐使用 LTS 版本，如 18.x 或 20.x）
- 操作系统：Windows、macOS、Linux 均支持

## 安装依赖的详细步骤
此项目无需第三方依赖，仅使用Node.js内置功能。

1. 打开终端或命令提示符
2. 进入项目目录
3. 无需运行 `npm install`，可直接执行脚本

## 文件说明
- `variables-var.js`: 演示使用 `var` 声明变量的行为，包括作用域和变量提升
- `variables-let-const.js`: 展示 `let` 和 `const` 的块级作用域特性及不可重复声明行为
- `example-scopes.js`: 综合示例，比较不同作用域下的变量表现

## 逐步实操指南

### 步骤 1: 创建项目目录并进入
```bash
mkdir nodejs-variables-demo
cd nodejs-variables-demo
```

### 步骤 2: 创建并运行第一个示例
创建文件：
```bash
node variables-var.js
```

**预期输出**：
```
var 在函数内被提升: undefined
var 可以重新声明
var 是函数作用域: Hello World
```

### 步骤 3: 运行 let 和 const 示例
```bash
node variables-let-const.js
```

**预期输出**：
```
let 支持块级作用域
if 块内的值: true
循环后仍可访问 i: 5
const 必须初始化且不可重新赋值
对象属性可以修改
```

### 步骤 4: 运行综合作用域示例
```bash
node example-scopes.js
```

**预期输出**：
```
全局变量: I am global
函数内访问全局变量: I am global
块级作用域中 let 被屏蔽
for 循环使用 let 是安全的: i = 0
tempVar 在块外不可访问
```

## 代码解析

### variables-var.js
- 使用 `var` 声明的变量会被提升到函数顶部
- `var` 允许重复声明，容易造成意外覆盖
- 函数作用域意味着在函数内部任意位置声明都会影响整个函数

### variables-let-const.js
- `let` 和 `const` 具有块级作用域（由 `{}` 定义）
- `let` 可以重新赋值但不能重复声明
- `const` 必须初始化，且不能重新赋值（但对象/数组内容可变）

### example-scopes.js
- 演示了全局、函数、块级作用域之间的优先级关系
- 强调使用 `let/const` 避免变量污染

## 预期输出示例
完整输出见各步骤说明。所有脚本应无错误运行，并清晰打印变量行为。

## 常见问题解答

**Q: 为什么不要使用 `var`？**
A: `var` 存在变量提升和函数作用域，容易导致逻辑错误。现代开发推荐使用 `let` 和 `const`。

**Q: `const` 对象真的不可变吗？**
A: `const` 防止重新赋值，但不冻结对象结构。要完全不可变，需使用 `Object.freeze()`。

**Q: 我可以在 if 块中用 let 声明同名变量吗？**
A: 可以，只要不在同一作用域内重复声明即可。

## 扩展学习建议
- 学习 `Temporal Dead Zone (TDZ)` 概念
- 尝试使用 ESLint 规则强制使用 `let/const`
- 阅读 MDN 文档关于 [变量提升](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/var) 和 [作用域](https://developer.mozilla.org/zh-CN/docs/Glossary/Scope)
- 实践使用 `const` 作为默认选择，仅在需要重新赋值时使用 `let`