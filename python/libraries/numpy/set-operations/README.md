# Python集合操作实战演示

## 简介
本项目通过两个实用场景，帮助初学者掌握Python中`set`（集合）的核心操作，包括去重、交集、并集、差集等。代码简洁清晰，适合零基础学习者快速上手。

## 学习目标
- 理解集合的概念及其无序、唯一性特点
- 掌握集合的创建与基本操作（添加、删除）
- 熟练使用交集、并集、差集、对称差集解决实际问题
- 学会在去重和用户行为分析中应用集合

## 环境要求
- Python 3.6 或更高版本（推荐3.8+）
- 操作系统：Windows / Linux / macOS 均可

## 安装依赖
本项目无需第三方库，仅使用Python标准库，无需额外安装依赖。

```bash
# 可选：创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\\Scripts\\activate     # Windows
```

## 文件说明
- `code/example1.py`：演示如何使用集合进行数据去重和集合运算
- `code/example2.py`：模拟用户兴趣标签匹配的应用场景
- `requirements.txt`：依赖声明文件（当前为空）

## 逐步实操指南

### 步骤1：运行去重与集合运算示例
```bash
python code/example1.py
```

**预期输出**：
```
原始列表: [1, 2, 2, 3, 4, 4, 5]
去重后集合: {1, 2, 3, 4, 5}
A与B的交集: {3, 4}
A与B的并集: {1, 2, 3, 4, 5, 6, 7}
A与B的差集 (A-B): {1, 2}
A与B的对称差集: {1, 2, 5, 6, 7}
```

### 步骤2：运行用户兴趣匹配示例
```bash
python code/example2.py
```

**预期输出**：
```
用户Alice的兴趣: {'音乐', '电影', '阅读', '旅行'}
用户Bob的兴趣: {'运动', '电影', '游戏', '旅行'}
共同兴趣: {'电影', '旅行'}
推荐给Alice的新兴趣: {'运动', '游戏'}
```

## 代码解析

### example1.py 关键点
```python
unique_set = set(data_list)
```
将列表转为集合，自动去除重复元素。

```python
intersection = set_a & set_b
```
使用`&`操作符求交集，等价于`set_a.intersection(set_b)`。

### example2.py 关键点
```python
common_interests = alice_interests & bob_interests
```
找出两位用户的共同兴趣，可用于社交推荐系统。

```python
recommendations = bob_interests - alice_interests
```
使用差集找出Bob有但Alice没有的兴趣，作为推荐依据。

## 预期输出示例
见“逐步实操指南”中的输出内容。

## 常见问题解答

**Q1：集合是有序的吗？**
A：不是。集合是无序的，不能通过索引访问元素。如需有序去重，请考虑使用`dict.fromkeys()`。

**Q2：如何向集合添加多个元素？**
A：使用`update()`方法，例如：`s.update([1,2,3])`。

**Q3：集合能包含列表吗？**
A：不能。集合中的元素必须是可哈希的（hashable），列表不可哈希。可以使用元组代替。

## 扩展学习建议
- 尝试实现一个好友推荐系统，基于共同好友或兴趣计算相似度
- 使用`frozenset`了解不可变集合的用途
- 结合字典统计词频后，用集合筛选高频词
- 学习集合推导式：`{x for x in range(10) if x % 2 == 0}`