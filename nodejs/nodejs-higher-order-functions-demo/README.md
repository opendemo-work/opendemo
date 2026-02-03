# Node.js高阶函数实战演示

## 简介
本演示项目展示了在Node.js中如何使用高阶函数（如 map、filter、reduce）处理数据集合。通过三个独立示例，帮助开发者理解函数式编程的核心概念。

## 学习目标
- 理解高阶函数的基本概念
- 掌握 map、filter、reduce 的实际应用场景
- 学会链式调用多个高阶函数处理复杂逻辑

## 环境要求
- Node.js >= 14.0.0
- npm（随Node.js自动安装）

## 安装依赖的详细步骤
1. 打开终端或命令行工具
2. 进入项目目录：`cd path/to/demo`
3. 安装依赖（本项目无外部依赖，无需额外安装）

## 文件说明
- `examples/map-filter.js`: 使用 map 和 filter 处理用户数据
- `examples/reduce-analytics.js`: 使用 reduce 实现数据聚合分析
- `examples/composition.js`: 展示函数组合与链式调用

## 逐步实操指南

### 步骤1: 创建项目结构
```bash
mkdir higher-order-demo
cd higher-order-demo
mkdir examples
```

### 步骤2: 运行第一个示例
```bash
node examples/map-filter.js
```
**预期输出**：
```
成年人姓名: [ 'Alice', 'Charlie' ]
加薪后工资: [ 60000, 70000, 90000 ]
```

### 步骤3: 运行第二个示例
```bash
node examples/reduce-analytics.js
```
**预期输出**：
```
总薪资: 220000
平均年龄: 31.67
最年轻员工: 25
```

### 步骤4: 运行第三个示例
```bash
node examples/composition.js
```
**预期输出**：
```
高级工程师总薪资: 160000
符合条件的员工姓名: [ 'Alice', 'Charlie' ]
```

## 代码解析

### map-filter.js
```js
// filter 过滤出年龄 >= 30 的员工
// map 提取姓名字段
const adultNames = employees.filter(e => e.age >= 30).map(e => e.name);
```

### reduce-analytics.js
```js
// reduce 累积所有薪资
const totalSalary = employees.reduce((sum, emp) => sum + emp.salary, 0);
```

### composition.js
```js
// 链式调用多个高阶函数实现复杂筛选和计算
const result = employees
  .filter(e => e.position === 'Senior Engineer')
  .map(e => e.salary)
  .reduce((sum, salary) => sum + salary, 0);
```

## 预期输出示例
见各步骤的“预期输出”部分。

## 常见问题解答

**Q: 为什么没有 package.json？**
A: 本项目仅使用Node.js内置功能，无需第三方依赖，因此无需生成 package.json。

**Q: 如何升级到使用 Lodash？**
A: 可运行 `npm init -y && npm install lodash`，然后在代码中导入 _.map 等函数进行实验。

**Q: 高阶函数性能如何？**
A: 在大多数业务场景下性能足够。若处理超大数据集，可考虑流式处理或分块操作。

## 扩展学习建议
- 学习 Ramda.js 函数式编程库
- 尝试将回调函数提取为命名函数以提高可读性
- 探索 Array.prototype.flatMap 等现代数组方法
- 阅读《JavaScript函数式编程》书籍深入理论