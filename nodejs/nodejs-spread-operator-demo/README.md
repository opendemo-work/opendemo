# NodeJS展开运算符实战演示

## 简介
本演示项目通过多个实例展示JavaScript中展开运算符（Spread Operator）的常见用法。展开运算符（...）是ES6引入的重要特性，可用于数组、对象、函数参数等场景，使代码更简洁易读。

## 学习目标
- 理解展开运算符的基本语法
- 掌握在数组合并、复制中的应用
- 学会在对象操作中使用展开运算符
- 了解函数参数中的剩余参数与展开结合使用

## 环境要求
- Node.js 版本：14.x 或更高（推荐 LTS 版本）
- 操作系统：Windows / macOS / Linux（任意）
- 命令行工具（如：终端、PowerShell、bash）

## 安装依赖
本项目无需外部依赖，仅使用原生Node.js环境即可运行。

```bash
# 检查Node.js版本
node --version
```

确保输出类似 `v14.18.0` 或更高版本。

## 文件说明
- `spread-array.js`: 演示数组中的展开运算符用法
- `spread-object.js`: 演示对象中的展开运算符用法
- `spread-function.js`: 演示函数参数中展开与剩余参数的使用

## 逐步实操指南

### 步骤1：克隆或创建项目目录
```bash
mkdir spread-demo && cd spread-demo
```

### 步骤2：创建并保存以下三个文件
将对应代码粘贴保存为同名文件。

### 步骤3：运行每个示例

运行数组示例：
```bash
node spread-array.js
```
**预期输出**：
```
合并后的数组: [1, 2, 3, 4, 5, 6]
复制的数组: [a, b, c]
展开字符串: [ 'h', 'e', 'l', 'l', 'o' ]
```

运行对象示例：
```bash
node spread-object.js
```
**预期输出**：
```
合并后的用户信息: { name: 'Alice', age: 25, city: 'Beijing', role: 'Developer' }
浅拷贝对象: { x: 1, y: 2 }
```

运行函数示例：
```bash
node spread-function.js
```
**预期输出**：
```
求和结果: 15
最大值: 8
函数调用拆分: [1, 2] 和 [3, 4]
```

## 代码解析

### `spread-array.js`
- 使用 `...arr` 将数组元素展开，实现无副作用合并
- 利用展开复制数组，避免引用共享
- 字符串也可被展开为字符数组

### `spread-object.js`
- 展开对象属性用于合并配置或覆盖字段
- 实现对象浅拷贝，修改副本不影响原对象

### `spread-function.js`
- 剩余参数 `...nums` 收集函数参数为数组
- 调用时使用 `...args` 将数组展开为独立参数

## 预期输出示例
完整运行三个脚本后，应看到上述各部分的输出结果，无错误信息。

## 常见问题解答

**Q: 展开运算符是深拷贝吗？**
A: 不是，它只做浅拷贝。嵌套对象仍共享引用。

**Q: 可以在哪些数据类型上使用展开？**
A: 所有可迭代对象（数组、字符串、Map、Set）和对象（非可迭代但语法支持）。

**Q: 与 `apply()` 相比有何优势？**
A: 语法更简洁，可读性更强，且不限于函数调用场景。

## 扩展学习建议
- 学习剩余参数（Rest Parameters）与展开运算符的区别
- 探索 `Object.assign()` 与展开运算符的对比
- 阅读 MDN 文档：https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Spread_syntax