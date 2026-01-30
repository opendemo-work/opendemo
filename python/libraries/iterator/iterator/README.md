# Python迭代器实战演示

## 简介
本项目通过两个具体示例，帮助初学者理解Python中的`迭代器（Iterator）`概念。我们将学习如何创建自定义迭代器、使用内置迭代工具，并掌握`__iter__()`和`__next__()`方法的用法。

## 学习目标
- 理解迭代器与可迭代对象的区别
- 掌握如何实现一个自定义迭代器类
- 学会使用Python内置的迭代机制
- 理解StopIteration异常的作用

## 环境要求
- Python 3.7 或更高版本（推荐使用最新稳定版）
- 操作系统：Windows / Linux / macOS 均支持

## 安装依赖的详细步骤
本项目无需第三方依赖库，仅使用Python标准库。

1. 打开终端或命令行工具
2. 确保已安装Python：
   ```bash
   python --version
   # 或
   python3 --version
   ```
   预期输出：`Python 3.x.x`

3. 克隆或创建项目目录并进入：
   ```bash
   mkdir iterator-demo && cd iterator-demo
   ```

4. 将以下文件复制到当前目录：
   - `code/example1.py`
   - `code/example2.py`

## 文件说明
- `code/example1.py`: 实现一个从1到n的数字计数迭代器
- `code/example2.py`: 实现斐波那契数列的无限迭代器（带限制）

## 逐步实操指南

### 步骤1：运行第一个示例
```bash
python code/example1.py
```

**预期输出**：
```
计数迭代器输出前5个数字：
1
2
3
4
5
```

### 步骤2：运行第二个示例
```bash
python code/example2.py
```

**预期输出**：
```
斐波那契迭代器前10项：
0
1
1
2
3
5
8
13
21
34
```

## 代码解析

### example1.py 关键点
- `CountIterator` 类实现了 `__iter__()` 和 `__next__()` 方法
- 每次调用 `next()` 返回下一个整数，直到达到最大值
- 抛出 `StopIteration` 来终止循环

### example2.py 关键点
- `FibonacciIterator` 生成斐波那契数列
- 使用三变量更新技术高效计算下一项
- 同样通过 `StopIteration` 控制输出数量

## 常见问题解答

**Q: 为什么需要实现 `__iter__()` 方法？**
A: 因为它使得对象可以被 `for` 循环等语法使用，返回自身作为迭代器。

**Q: StopIteration 是做什么的？**
A: 它是Python用来标识迭代结束的内置异常，必须抛出以避免无限循环。

**Q: 迭代器和列表有什么区别？**
A: 迭代器是惰性计算的，节省内存；而列表一次性加载所有数据。

## 扩展学习建议
- 尝试修改斐波那契迭代器，使其只返回偶数项
- 使用生成器函数 `yield` 实现相同功能（更简洁）
- 学习 itertools 模块中的高级迭代工具