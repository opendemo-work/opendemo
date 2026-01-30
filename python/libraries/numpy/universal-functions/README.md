# NumPy ufunc 实战演示

## 简介
本项目通过两个具体场景演示 NumPy 中的通用函数（ufunc）的使用方式。ufunc 是 NumPy 的核心特性之一，支持对数组进行高效、向量化的数学运算，避免显式循环，显著提升计算性能。

## 学习目标
- 理解什么是 ufunc 及其优势
- 掌握常见内置 ufunc 的使用（如加法、三角函数等）
- 学会创建自定义 ufunc 函数
- 理解广播机制在 ufunc 中的作用

## 环境要求
- Python 3.8 或更高版本
- 操作系统：Windows、Linux、macOS 均可

## 安装依赖的详细步骤

1. 打开终端（或命令提示符）
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   ```
3. 激活虚拟环境：
   - Windows:
     ```bash
     venv\\Scripts\\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
4. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/example1.py`: 演示内置 ufunc 和广播机制的基础用法
- `code/example2.py`: 演示如何使用 `np.frompyfunc` 创建自定义 ufunc
- `requirements.txt`: 项目依赖声明文件
- `README.md`: 本实操文档

## 逐步实操指南

### 步骤 1: 运行第一个示例
```bash
python code/example1.py
```

**预期输出**：
```
原始数组 a: [1 2 3 4]
原始数组 b: [5 6 7 8]
加法结果: [ 6  8 10 12]
平方根结果: [1.         1.41421356 1.73205081 2.        ]
角度数组（度）: [  0.  30.  45.  60.  90.]
正弦值: [0.         0.5        0.70710678 0.8660254  1.        ]
```

### 步骤 2: 运行第二个示例
```bash
python code/example2.py
```

**预期输出**：
```
数组 x: [1 2 3 4 5]
数组 y: [2 0 2 1 0]
自定义幂运算结果: [1 1 9 4 1]
```

## 代码解析

### example1.py 关键点
- 使用 `np.add` 和 `+` 实现数组逐元素相加
- `np.sqrt` 展示一元 ufunc 的应用
- 使用 `np.radians` 转换角度制为弧度制
- `np.sin` 计算正弦值，体现 ufunc 对整个数组的向量化操作

### example2.py 关键点
- `def custom_power(x, y):` 定义普通 Python 函数
- `np.frompyfunc(custom_power, 2, 1)` 将其转换为 ufunc，支持两个输入、一个输出
- 自动支持广播和数组操作

## 预期输出示例
见“逐步实操指南”中的输出内容。

## 常见问题解答

**Q: 为什么使用 ufunc 比 for 循环更快？**
A: ufunc 是用 C 编写的底层实现，避免了 Python 解释器的循环开销，具有更高的执行效率。

**Q: 自定义 ufunc 返回的是什么类型？**
A: 使用 `frompyfunc` 创建的 ufunc 返回的是 `object` 类型数组，若需数值类型，应使用 `vectorize` 或 Numba 等工具优化。

**Q: 广播是什么意思？**
A: 广播是 NumPy 在不同形状数组间进行运算的机制，例如标量与数组相加时，标量会被‘扩展’到与数组相同形状。

## 扩展学习建议
- 学习 `np.vectorize` 以获得更高效的自定义函数支持
- 探索 NumPy 的广播规则（Broadcasting Rules）
- 了解 ufunc 的方法如 `.reduce`, `.accumulate`
- 查阅官方文档：https://numpy.org/doc/stable/reference/ufuncs.html