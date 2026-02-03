# 排序与索引排序实战演示

## 简介
本项目通过两个具体的Python示例，深入浅出地展示`sort`和`argsort`函数在数据处理中的核心应用。重点讲解它们的区别：`sort`直接对数组排序，而`argsort`返回排序后的索引位置，适用于需要保留原始数据顺序的场景。

## 学习目标
- 理解`numpy.sort()`和`numpy.argsort()`的基本功能
- 掌握`argsort`在排序后仍能关联原始数据的应用技巧
- 学会在实际问题中选择合适的排序方法
- 提升对数组索引操作的理解

## 环境要求
- Python 3.7 或更高版本
- 操作系统：Windows、Linux、macOS 均可

## 安装依赖
1. 确保已安装Python（推荐使用[Anaconda](https://www.anaconda.com/products/distribution)或标准CPython）
2. 打开终端（命令提示符/PowerShell/Terminal）
3. 运行以下命令安装所需库：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/sort_example.py`: 演示普通排序及其应用场景
- `code/argsort_example.py`: 展示如何使用argsort进行索引排序并还原原始数据
- `requirements.txt`: 项目依赖声明文件
- `README.md`: 本说明文档

## 逐步实操指南

### 步骤1：克隆或创建项目目录
```bash
mkdir sort-demo && cd sort-demo
# 将本项目所有文件复制到该目录
```

### 步骤2：创建并安装依赖
将以下内容保存为`requirements.txt`：
```txt
numpy>=1.21.0
```
然后运行：
```bash
pip install -r requirements.txt
```

### 步骤3：运行第一个示例
```bash
python code/sort_example.py
```
**预期输出**：
```
原始数组: [3.5 1.2 4.8 2.1 3.9]
排序后数组: [1.2 2.1 3.5 3.9 4.8]
```

### 步骤4：运行第二个示例
```bash
python code/argsort_example.py
```
**预期输出**：
```
学生成绩: {'Alice': 88, 'Bob': 95, 'Charlie': 70, 'Diana': 92}
排序后的姓名顺序: ['Charlie', 'Alice', 'Diana', 'Bob']
按成绩从低到高排列的学生名单: Charlie(70), Alice(88), Diana(92), Bob(95)
```

## 代码解析

### `sort_example.py`
```python
np.sort(scores)
```
直接对数值数组进行升序排序，返回新的有序数组。

### `argsort_example.py`
```python
sorted_indices = np.argsort(list(grades.values()))
```
获取成绩排序后的索引，再用这些索引去访问原始字典的键（学生姓名），实现按成绩排序却不丢失姓名信息。

## 预期输出示例
完整输出见“逐步实操指南”部分。

## 常见问题解答

**Q1: 运行时报错 `ModuleNotFoundError: No module named 'numpy'`？**
A: 请确保已正确执行 `pip install -r requirements.txt`，并检查是否在正确的Python环境中安装。

**Q2: 如何改为降序排序？**
A: 使用 `[::-1]` 反转数组，例如：`np.sort(arr)[::-1]` 或 `np.argsort(arr)[::-1]`。

**Q3: argsort 返回的是什么？**
A: 返回的是排序后元素在原数组中的**索引位置**，不是值本身。

## 扩展学习建议
- 尝试对二维数组使用`axis`参数进行行或列排序
- 结合`pandas`的`sort_values()`方法比较差异
- 学习`lexsort`进行多字段排序
- 实践在图像处理中用`argsort`找到前K个最大响应区域