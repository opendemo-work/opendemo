# 🐍 Python技术栈完整指南

> Python编程语言从基础到高级的完整学习体系，包含56个基础语法案例和25个NumPy库案例

## 🚀 快速入门

想要快速上手Python开发？查看我们的 [Python CLI 命令行速查表](./cli/python-cli.md) 获取包管理、虚拟环境和调试工具！

## 📋 技术栈概述

Python是一种高级编程语言，以其简洁易读的语法和强大的生态系统而闻名。本技术栈提供从基础语法到科学计算的完整学习路径。

### 🔧 核心技能覆盖

- **基础语法**: 变量、数据类型、控制流、函数、面向对象编程
- **标准库**: collections、itertools、functools、pathlib等模块
- **文件操作**: 文件读写、路径处理、序列化
- **网络编程**: Socket编程、HTTP请求处理
- **并发编程**: 多线程、多进程、异步编程
- **科学计算**: NumPy数组操作、数学运算、数据分析

### 🎯 适用人群

- Python初学者
- 数据科学从业者
- 后端开发工程师
- 自动化测试工程师
- 科学计算研究人员

---

## 📚 学习路径

### 基础语法系列 (51个案例)
从最基本的变量类型到高级的元类编程，循序渐进掌握Python核心概念。

### NumPy科学计算系列 (25个案例)
深入学习NumPy库，掌握数组操作、数学运算、科学计算等高级功能。

---

## 🚀 快速开始

```bash
# 查看所有Python案例
opendemo search python

# 获取基础语法案例
opendemo get python variables-types

# 获取NumPy案例
opendemo get python numpy array-creation
```

---

## 📊 案例统计

| 分类 | 案例数量 | 状态 |
|------|----------|------|
| 基础语法 | 51 | ✅ 全部完成 |
| NumPy库 | 25 | ✅ 全部完成 |
| 排查工具 | 1 | ✅ 新增 |
| **总计** | **77** | ✅ |

---

## 📚 详细目录

### 基础语法 (51个)
<details>
<summary>点击查看完整列表</summary>

1. `abc-interfaces` - 抽象基类与接口
2. `async-programming` - 异步编程 async/await
3. `bitwise-operations` - 位运算操作
4. `caching` - 缓存机制
5. `cli-argparse` - 命令行参数解析
6. `collections-module` - collections模块
7. `comprehensions` - 列表/字典/集合推导式
8. `config-management` - 配置文件管理
9. `context-managers` - 上下文管理器 with
10. `control-flow` - 控制流语句
... (共51个案例)

</details>

### NumPy库 (25个)
<details>
<summary>点击查看完整列表</summary>

1. `aggregate-functions` - 聚合函数 sum/mean/std
2. `array-concatenation` - 数组拼接 concatenate/stack
3. `array-creation` - 数组创建 zeros/ones/arange
4. `array-indexing` - 索引与切片
5. `array-reshape` - 形状操作 reshape/transpose
... (共25个案例)

</details>

---

## 🛠️ 开发环境配置

```bash
# 安装Python
# 推荐版本: Python 3.8+

# 安装必要依赖
pip install numpy pandas matplotlib jupyter

# 验证安装
python --version
numpy.__version__
```

---

## 📖 学习建议

1. **循序渐进**: 按照基础语法 → 标准库 → 科学计算的顺序学习
2. **动手实践**: 每个案例都要亲自运行和修改代码
3. **项目驱动**: 结合实际项目应用所学知识
4. **持续练习**: 定期回顾和练习重点概念

---

## 🤝 贡献指南

欢迎提交新的Python案例或改进现有案例：
- 遵循统一的目录结构和文档格式
- 提供完整的代码示例和详细说明
- 确保案例的可运行性和实用性

---

> **💡 提示**: Python是数据科学和人工智能领域的主流语言，掌握好基础语法和科学计算库对职业发展非常重要。

## 🔗 相关技术栈交叉引用

### 与Java的关联
- [Java基础语法](../java/README.md) - 面向对象编程概念
- [Java类与对象](../java/java-classes-objects-demo/) - 对应的Java实现

### 与Go的关联
- [Go基础语法](../go/README.md) - 静态类型vs动态类型
- [Go并发模型](../go/go-goroutines-demo/) - CSP并发模型

### 与Node.js的关联
- [Node.js基础语法](../nodejs/README.md) - JavaScript语法特性
- [Node.js异步编程](../nodejs/nodejs-promises-demo/) - 异步处理机制