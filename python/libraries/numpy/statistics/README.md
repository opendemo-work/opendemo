# Python Statistics Demo

## 简介
本项目是一个面向初学者的Python统计分析入门示例，使用Python内置的`statistics`模块演示如何计算常见的统计指标，如均值、中位数、众数、标准差等。代码简洁易懂，适合数据分析初学者学习和实践。

## 学习目标
- 掌握Python `statistics` 模块的基本用法
- 理解常见统计量的含义与应用场景
- 学会从数据中提取基本统计信息
- 培养使用Python进行简单数据分析的能力

## 环境要求
- Python 3.8 或更高版本
- 支持 Windows、macOS 和 Linux 系统

## 安装依赖
本项目仅使用Python标准库，无需额外安装第三方包。

如果你使用虚拟环境（推荐），可按以下步骤操作：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# 在 Windows 上：
venv\Scripts\activate
# 在 macOS/Linux 上：
source venv/bin/activate

# 安装依赖（虽然本项目无外部依赖）
pip install -r requirements.txt
```

> 注意：由于只使用标准库，`requirements.txt` 中为空，但保留文件以符合规范。

## 文件说明
- `code/basic_stats.py`: 基础统计量计算示例
- `code/grouped_data_stats.py`: 分组数据的统计分析示例
- `README.md`: 本实操文档
- `requirements.txt`: 依赖声明文件

## 逐步实操指南

### 步骤1：克隆或创建项目目录
```bash
mkdir python-statistics-demo
cd python-statistics-demo
```

将本项目所有文件复制到该目录下。

### 步骤2：运行第一个示例
```bash
python code/basic_stats.py
```

**预期输出**：
```
=== 基础统计数据 ===
数据: [10, 15, 20, 25, 30, 35, 40]
平均值: 25
中位数: 25
众数: 无（所有值唯一）
标准差: 11.18
方差: 125.0
```

### 步骤3：运行第二个示例
```bash
python code/grouped_data_stats.py
```

**预期输出**：
```
=== 分组数据统计 ===
学生成绩分布: {'A': 5, 'B': 12, 'C': 8, 'D': 3}
成绩列表展开后: ['A', 'A', 'A', 'A', 'A', 'B', 'B', ...]
最常见成绩: B
成绩中位等级: B
```

## 代码解析

### `basic_stats.py` 关键代码段
```python
mean(data)           # 计算算术平均值
median(data)         # 计算中位数
mode(data)           # 找出众数，若无则抛出异常
stdev(data)          # 样本标准差
variance(data)       # 样本方差
```
这些函数是 `statistics` 模块的核心方法，适用于数值型数据。

### `grouped_data_stats.py` 关键技巧
```python
from collections import Counter
...
expanded_grades = expand_grouped_data(grade_distribution)
```
当数据以频数形式给出时，可通过重复标签来“展开”数据，再进行统计分析。

## 预期输出示例
见“逐步实操指南”中的输出样例。

## 常见问题解答

**Q1: 运行时报错 `No mode found`？**
A: 当所有数值出现频率相同时，`mode()` 会报错。建议使用 `multimode()` 或捕获异常。

**Q2: 可以处理字符串数据吗？**
A: `median()` 和 `mean()` 仅支持数字；但 `mode()` 和 `multimode()` 可用于分类数据（如字符串）。

**Q3: 如何处理缺失值（None）？**
A: `statistics` 模块不支持 `None` 值，请提前清洗数据。

## 扩展学习建议
- 学习 `pandas` 库进行更强大的数据分析
- 探索 `scipy.stats` 模块进行高级统计检验
- 阅读《利用Python进行数据分析》一书深入理解数据科学流程
- 尝试将本示例扩展为读取CSV文件并分析真实数据集
