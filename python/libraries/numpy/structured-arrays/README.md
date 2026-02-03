# 结构化数组（Structured Arrays）实战演示

## 简介
本示例演示了如何使用 NumPy 的结构化数组（Structured Arrays）来存储和操作具有不同类型字段的记录数据。结构化数组类似于表格，每一行是一个记录，每一列可以是不同的数据类型，非常适合处理结构化数据（如CSV或数据库记录）。

## 学习目标
- 理解结构化数组的概念及其与普通数组的区别
- 掌握定义复合数据类型的语法
- 学会创建、访问和修改结构化数组
- 了解结构化数组在实际数据处理中的应用

## 环境要求
- Python 3.7 或更高版本
- 操作系统：Windows、Linux、macOS 均支持

## 安装依赖
1. 确保已安装 Python：
   ```bash
   python --version
   # 预期输出: Python 3.x.x
   ```

2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate   # Windows
   ```

3. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/example1.py`：基础结构化数组的创建与访问
- `code/example2.py`：结构化数组的排序与条件筛选
- `requirements.txt`：项目依赖声明文件

## 逐步实操指南

### 步骤 1：运行第一个示例
```bash
python code/example1.py
```
**预期输出**：
```
所有学生数据：
[(1, 'Alice', 85.5) (2, 'Bob', 90.2) (3, 'Charlie', 78.0)]

学生姓名： ['Alice' 'Bob' 'Charlie']

第二名学生的成绩： 90.2
```

### 步骤 2：运行第二个示例
```bash
python code/example2.py
```
**预期输出**：
```
按成绩降序排列：
[(2, 'Bob', 90.2) (1, 'Alice', 85.5) (3, 'Charlie', 78. )]

成绩高于 80 的学生：
[(1, 'Alice', 85.5) (2, 'Bob', 90.2)]
```

## 代码解析

### example1.py 关键点
- 使用 `dtype` 定义包含整数、字符串和浮点数的复合类型
- 通过字段名（如 `['id']`, `['name']`）访问特定列
- 展示结构化数组的内存布局优势

### example2.py 关键点
- 使用 `np.sort()` 对结构化数组按指定字段排序
- 利用布尔索引进行条件筛选：`arr[arr['score'] > 80]`
- 体现结构化数组在数据分析中的实用性

## 预期输出示例
完整输出请参考“逐步实操指南”中的内容。

## 常见问题解答

**Q: 为什么使用结构化数组而不是 Pandas DataFrame？**
A: 结构化数组更轻量，适合高性能数值计算场景；而 Pandas 更适合复杂的数据分析任务。

**Q: 字符串字段长度如何设置？**
A: 使用 `'U10'` 表示最多10个字符的Unicode字符串，根据需要调整数字。

**Q: 如何查看结构化数组的字段信息？**
A: 使用 `arr.dtype` 可查看所有字段名称和类型。

## 扩展学习建议
- 尝试添加新字段（如 'age'）并重新运行示例
- 将结构化数组保存到文件（使用 `np.save` / `np.load`）
- 对比结构化数组与 Python 类实例的性能差异
- 学习 NumPy 的 `recarray`（记录数组），支持属性式访问（如 `arr.name`）
