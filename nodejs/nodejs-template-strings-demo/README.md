# 模板字符串实战演示

## 简介
本项目通过多个简单示例，展示JavaScript中模板字符串（Template Strings）的强大功能。模板字符串是ES6引入的重要特性，支持多行文本、变量插值和表达式嵌入，极大提升了字符串处理的可读性和灵活性。

## 学习目标
- 掌握模板字符串的基本语法
- 理解如何在字符串中嵌入变量和表达式
- 学会使用模板字符串构建HTML片段和日志信息

## 环境要求
- Node.js 版本：14.x 或更高（推荐使用 LTS 版本）
- 操作系统：Windows / Linux / macOS（任意）

## 安装依赖的详细步骤
此项目不依赖外部库，仅使用Node.js原生功能，无需安装额外依赖。

## 文件说明
- `basic-interpolation.js`：基础变量插值示例
- `advanced-usage.js`：高级用法，包括表达式和HTML生成
- `tagged-templates.js`：标签模板函数的简单演示

## 逐步实操指南

### 步骤 1: 创建项目目录
```bash
mkdir template-strings-demo
cd template-strings-demo
```

### 步骤 2: 复制代码文件
将以下三个文件内容复制到对应路径：
- `basic-interpolation.js`
- `advanced-usage.js`
- `tagged-templates.js`

### 步骤 3: 运行每个示例

运行基础插值示例：
```bash
node basic-interpolation.js
```
**预期输出**：
```
你好，张三！你今年25岁。
```

运行高级用法示例：
```bash
node advanced-usage.js
```
**预期输出**：
```
计算结果：3 + 5 = 8
生成的HTML：<div><h1>欢迎</h1><p>这是内容</p></div>
```

运行标签模板示例：
```bash
node tagged-templates.js
```
**预期输出**：
```
日志级别: INFO - 时间: 2025-04-05T10:00:00.000Z - 消息: 用户登录成功
```

## 代码解析

### `basic-interpolation.js`
使用 `${variable}` 语法将变量插入字符串中，替代传统的字符串拼接，提升可读性。

### `advanced-usage.js`
展示了模板字符串中嵌入表达式（如数学运算）以及构建多行HTML结构的能力，避免繁琐的引号和加号拼接。

### `tagged-templates.js`
介绍标签模板（Tagged Templates）的概念：通过函数处理模板字符串的各个部分，适用于国际化、SQL注入防护等场景。

## 预期输出示例
所有文件运行后应分别输出如上所述的清晰文本信息，无错误提示。

## 常见问题解答

**Q: 模板字符串必须用反引号吗？**
A: 是的，只有反引号（`` ` ``）支持模板字符串功能，单引号或双引号不支持变量插值。

**Q: 可以在模板字符串中调用函数吗？**
A: 可以！`${myFunction()}` 是完全合法的用法。

**Q: 模板字符串性能如何？**
A: 在现代JavaScript引擎中性能良好，适合大多数场景。极端高频场景可考虑缓存优化。

## 扩展学习建议
- 学习 `String.raw` 标签模板的使用
- 探索模板字符串在构建SQL查询中的安全用法（配合参数化查询）
- 尝试使用模板字符串实现简单的模板引擎