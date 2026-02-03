# Map与Set 实战演示

## 简介
本项目通过两个简单的Node.js脚本，演示了ES6中`Map`和`Set`两种重要数据结构的核心用法。`Map`用于键值对存储（支持任意类型键），`Set`用于唯一值集合（自动去重）。这些是现代JavaScript开发中的基础工具。

## 学习目标
- 理解Map和Set的基本概念与优势
- 掌握Map的增删改查操作
- 使用Set实现数组去重
- 了解Map/Set与普通对象/数组的区别

## 环境要求
- Node.js v14 或更高版本（推荐v16+）
- 操作系统：Windows、macOS、Linux 均可

## 安装依赖
本项目无外部依赖，仅使用Node.js内置功能。

## 文件说明
- `examples/map-demo.js`：演示Map的常用操作
- `examples/set-demo.js`：演示Set的去重和集合操作

## 逐步实操指南

### 步骤1：创建项目目录
```bash
mkdir map-set-demo
cd map-set-demo
```

### 步骤2：初始化npm项目（可选）
npm init -y

### 步骤3：创建代码文件
复制以下两个文件内容到对应路径：
- 创建 `examples/map-demo.js`
- 创建 `examples/set-demo.js`

### 步骤4：运行Map示例
```bash
node examples/map-demo.js
```

**预期输出**：
```
用户信息: {
  name: 'Alice',
  age: 25
}
课程映射: 数学 → A, 英语 → B+
更新后成绩: A+
删除英语成绩后: Map { '数学' => 'A' }
```

### 步骤5：运行Set示例
```bash
node examples/set-demo.js
```

**预期输出**：
```
原始数组: [1, 2, 2, 3, 4, 4, 5]
去重后: [1, 2, 3, 4, 5]
交集: [2, 3]
并集: [1, 2, 3, 4, 5, 6]
差集: [1]
```

## 代码解析

### map-demo.js 关键点
- `new Map()` 创建空映射
- `.set(key, value)` 添加键值对
- `.get(key)` 获取值
- `.delete(key)` 删除条目
- 支持非字符串键（如对象、函数）

### set-demo.js 关键点
- `new Set(array)` 快速去重
- `Array.from()` 或扩展运算符 `[...set]` 转回数组
- 利用Set实现集合运算（交集、并集、差集）

## 预期输出示例
见上文“逐步实操指南”中的输出部分。

## 常见问题解答

**Q: 为什么不用普通对象而用Map？**
A: Map支持任意类型键、保持插入顺序、性能更好（尤其大量数据时），且无需担心原型污染。

**Q: Set如何做到自动去重？**
A: Set内部使用“Same-value-zero”算法判断相等性，能正确识别基本类型重复值。

**Q: 运行时报错“Cannot find module”？**
A: 确保文件路径正确，并在项目根目录下执行命令。

## 扩展学习建议
- 尝试用Map缓存函数计算结果（记忆化）
- 使用WeakMap/WeakSet理解弱引用机制
- 在LeetCode上练习涉及Map/Set的算法题（如两数之和）
- 阅读MDN文档：[Map](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Map), [Set](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Set)
