# NodeJS对象操作实战：深拷贝、冻结与遍历

## 简介
本示例演示了在Node.js环境中对JavaScript对象进行三种关键操作：
- 深拷贝（Deep Clone）避免引用共享
- 对象冻结（Freeze）防止意外修改
- 安全遍历（Safe Iteration）获取对象属性

通过三个独立文件，逐步展示这些操作的最佳实践。

## 学习目标
- 理解浅拷贝与深拷贝的区别
- 掌握使用 `Object.freeze()` 冻结对象
- 学会安全遍历对象的可枚举属性
- 避免常见对象操作陷阱

## 环境要求
- Node.js 版本：14.x 或更高（推荐 LTS 版本，如 18.x）
- 操作系统：Windows / Linux / macOS（跨平台兼容）
- 包管理器：npm（随Node.js自动安装）

## 安装依赖的详细步骤
1. 确保已安装Node.js：打开终端运行以下命令检查版本
   ```bash
   node -v
   ```
   输出应类似：`v18.17.0`

2. 本项目无外部依赖，无需额外安装包。

## 文件说明
- `deepClone.js`：演示嵌套对象的深拷贝技术
- `freezeObject.js`：展示如何冻结对象及其限制
- `iterateObject.js`：安全遍历对象属性并区分自身属性

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir object-demo && cd object-demo
```

### 步骤2：创建代码文件
将以下三个文件内容分别保存到对应路径：
- `deepClone.js`
- `freezeObject.js`
- `iterateObject.js`

### 步骤3：运行每个示例

运行深拷贝示例：
```bash
node deepClone.js
```
**预期输出**：
```
原始对象修改后，副本未受影响 → 深拷贝成功！
```

运行冻结对象示例：
```bash
node freezeObject.js
```
**预期输出**：
```
尝试修改冻结对象失败 → 冻结生效！
```

运行遍历对象示例：
```bash
node iterateObject.js
```
**预期输出**：
```
键: name, 值: Alice
键: age, 值: 30
```

## 代码解析

### deepClone.js
使用 `JSON.parse(JSON.stringify(obj))` 实现简单深拷贝，适用于不含函数、undefined、Symbol 的纯数据对象。修改副本不会影响原对象。

### freezeObject.js
`Object.freeze()` 使对象不可变。在严格模式下尝试修改会抛出错误，非严格模式静默失败。

### iterateObject.js
使用 `for...in` 遍历所有可枚举属性，结合 `hasOwnProperty` 过滤继承属性，确保只处理对象自身的键值。

## 预期输出示例
```bash
$ node deepClone.js
原始对象修改后，副本未受影响 → 深拷贝成功！

$ node freezeObject.js
尝试修改冻结对象失败 → 冻结生效！

$ node iterateObject.js
键: name, 值: Alice
键: age, 值: 30
```

## 常见问题解答

**Q1: 为什么不用 `...` 扩展运算符做深拷贝？**
A: 因为扩展运算符仅做浅拷贝，嵌套对象仍为引用。

**Q2: `Object.freeze()` 能冻结嵌套对象吗？**
A: 不能，需递归冻结才能完全冻结深层结构。

**Q3: 深拷贝方法有缺陷吗？**
A: 是的，`JSON` 方法不支持函数、日期、RegExp 等类型。生产环境建议使用 lodash 的 `cloneDeep`。

## 扩展学习建议
- 学习使用 `structuredClone()`（Node.js 17+）进行更安全的深拷贝
- 探索 `Object.seal()` 与 `Object.preventExtensions()` 的差异
- 阅读 MDN 文档：[JavaScript Object Static Methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
