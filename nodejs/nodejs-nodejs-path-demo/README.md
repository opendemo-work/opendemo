# Node.js Path模块实战演示

## 简介
本示例展示了如何在Node.js中使用内置的`path`模块处理文件和目录路径。`path`模块提供了跨平台兼容的工具函数，用于处理文件系统路径，无论是在Windows、Linux还是macOS上都能正确运行。

## 学习目标
- 掌握`path.join()`、`path.resolve()`、`path.basename()`、`path.dirname()`和`path.extname()`的基本用法
- 理解相对路径与绝对路径的区别
- 学会编写跨平台兼容的路径处理代码

## 环境要求
- Node.js v14 或更高版本（推荐使用LTS版本）
- 操作系统：Windows、Linux 或 macOS

## 安装依赖的详细步骤
本项目不依赖第三方包，仅使用Node.js内置模块，无需安装额外依赖。

## 文件说明
- `path-demo-basic.js`: 基础路径拼接与解析演示
- `path-demo-advanced.js`: 高级路径操作，如路径规范化和相对路径计算
- `README.md`: 本说明文档

## 逐步实操指南

### 步骤1: 检查Node.js版本
打开终端并运行：
```bash
node --version
```
**预期输出**:
```bash
v18.17.0  # 版本号可能不同，但需大于等于v14
```

### 步骤2: 创建项目目录
```bash
mkdir node-path-demo && cd node-path-demo
```

### 步骤3: 将以下两个代码文件保存到项目目录中
- 保存 `path-demo-basic.js`
- 保存 `path-demo-advanced.js`

### 步骤4: 运行基础示例
```bash
node path-demo-basic.js
```
**预期输出**:
```bash
拼接路径: /home/user/documents/file.txt
文件名: file.txt
扩展名: .txt
目录名: /home/user/documents
解析后的路径对象: {
  root: '/',
  dir: '/home/user/documents',
  base: 'file.txt',
  ext: '.txt',
  name: 'file'
}
```

### 步骤5: 运行高级示例
```bash
node path-demo-advanced.js
```
**预期输出**:
```bash
绝对路径: /Users/username/project/folder\sub\file.txt (Windows风格显示为反斜杠)
规范化路径: /folder/sub/file.txt
从当前目录到目标目录的相对路径: folder/sub/file.txt
路径分隔符（根据系统）: / 或 \\
```

## 代码解析

### `path-demo-basic.js`
- `path.join()`: 安全地拼接路径片段，自动处理斜杠问题
- `path.basename()`: 提取文件名
- `path.extname()`: 获取文件扩展名
- `path.parse()`: 将路径解析为可读的对象

### `path-demo-advanced.js`
- `path.resolve()`: 从左到右解析为绝对路径
- `path.normalize()`: 规范化路径中的`..`和`.`
- `path.relative()`: 计算两个路径之间的相对关系
- `path.sep`: 返回操作系统特定的路径分隔符

## 预期输出示例
见“逐步实操指南”中的输出部分。

## 常见问题解答

**Q: 为什么不用字符串拼接路径？**
A: 字符串拼接容易导致跨平台问题（如Windows用`\`，Unix用`/`），而`path.join()`会自动适配。

**Q: `path.resolve()` 和 `path.join()` 的区别是什么？**
A: `resolve()` 返回绝对路径，`join()` 只是拼接，不保证绝对。

**Q: 如何在Windows上测试Unix路径行为？**
A: 不需要，`path`模块会自动根据运行环境调整分隔符和行为。

## 扩展学习建议
- 阅读官方文档：https://nodejs.org/api/path.html
- 学习`fs`模块如何与`path`模块配合使用
- 尝试使用`path.posix`和`path.win32`子模块进行跨平台路径模拟