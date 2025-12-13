# NodeJS数组方法实战演示

## 简介
本项目通过三个具体的使用场景，演示了JavaScript中常用的数组方法（map、filter、reduce）在实际开发中的应用。每个示例都独立运行，适合初学者理解函数式编程思想和数组操作的最佳实践。

## 学习目标
- 掌握 map、filter、reduce 的基本用法
- 理解链式调用的优势
- 学会在真实数据处理中组合使用数组方法
- 遵循 Node.js 编码规范

## 环境要求
- Node.js 版本：14.x 或更高（推荐 16+）
- 操作系统：Windows / macOS / Linux（跨平台兼容）
- 包管理器：npm（随 Node.js 自动安装）

## 安装依赖
此项目无外部依赖，仅使用 Node.js 内置模块，无需额外安装。

## 文件说明
- `examples/map-example.js`：使用 map 转换数组元素
- `examples/filter-example.js`：使用 filter 筛选符合条件的数据
- `examples/reduce-example.js`：使用 reduce 进行数据聚合统计

## 逐步实操指南

### 步骤 1：创建项目目录并进入
```bash
mkdir array-methods-demo && cd array-methods-demo
```

### 步骤 2：创建示例文件夹和代码文件
```bash
mkdir -p examples
```

将对应代码复制到指定路径下。

### 步骤 3：运行第一个示例
```bash
node examples/map-example.js
```
**预期输出**：\n学生姓名与成绩等级映射列表

### 步骤 4：运行第二个示例
```bash
node examples/filter-example.js
```
**预期输出**：\n所有及格学生的记录

### 步骤 5：运行第三个示例
```bash
node examples/reduce-example.js
```
**预期输出**：\n班级总分、平均分和各等级人数统计

## 代码解析

### map-example.js
```js
const gradedStudents = students.map(...)
```
使用 map 将原始学生成绩数组转换为包含评级的新对象数组，不修改原数组，符合函数式编程原则。

### filter-example.js
```js
const passingStudents = allStudents.filter(s => s.grade >= 60)
```
利用 filter 提取满足条件（成绩 >=60）的学生，返回新数组。

### reduce-example.js
```js
const stats = students.reduce((acc, student) => { ... }, initialAcc)
```
通过 reduce 一次性计算多个统计值，避免多次遍历数组，提升性能。

## 预期输出示例
```
=== Map 示例：成绩评级 ===
Alice: A
Bob: C
Charlie: B
...

=== Filter 示例：及格学生 ===
{ name: 'Alice', grade: 88 }
{ name: 'Charlie', grade: 72 }
...

=== Reduce 示例：统计结果 ===
{ total: 395, average: 79, gradeCounts: { A: 2, B: 1, C: 1, F: 1 } }
```

## 常见问题解答

**Q: 为什么不用 for 循环？**\nA: map/filter/reduce 更具可读性，表达意图更清晰，并且不会产生副作用，是现代 JS 推荐做法。

**Q: 可以链式调用吗？**\nA: 可以！例如 `.filter().map().reduce()` 是常见模式，但注意性能影响。

**Q: 修改了原数组怎么办？**\nA: 这些方法均返回新数组，原数组不变。如需深拷贝，可用 `[...arr]` 或 `Array.from()`。

## 扩展学习建议
- 学习 Array.prototype.flatMap 和 at 方法（ES2022+）
- 阅读 Mozilla MDN 文档中关于函数式编程的部分
- 尝试用 reduce 实现 map 或 filter 功能
- 探索 Lodash 库中的集合操作方法