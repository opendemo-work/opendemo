# 掩码数组（Masked Arrays）Python 实操教程

## 简介
本示例演示了如何使用 NumPy 的 `masked array` 功能来处理含有缺失值、异常值或无效数据的数组。掩码数组允许我们在不修改原始数据的前提下，标记某些元素为“无效”并对其进行特殊处理。

## 学习目标
- 理解什么是掩码数组及其应用场景
- 学会创建和操作掩码数组
- 掌握在科学计算中忽略无效数据的方法

## 环境要求
- Python 3.7 或更高版本
- 操作系统：Windows、Linux、macOS 均支持

## 安装依赖
打开终端（命令行），执行以下命令安装所需库：
```bash
pip install -r requirements.txt
```

## 文件说明
- `code/example1.py`: 基础掩码数组创建与操作示例
- `code/example2.py`: 使用掩码处理传感器数据中的异常值
- `requirements.txt`: 项目依赖声明文件

## 逐步实操指南

### 第一步：克隆项目或创建文件夹
```bash
mkdir masked-arrays-demo && cd masked-arrays-demo
```

### 第二步：创建代码目录并写入文件
请将以下内容分别保存为对应路径的文件。

### 第三步：安装依赖
```bash
pip install -r requirements.txt
```

### 第四步：运行第一个示例
```bash
python code/example1.py
```
**预期输出**：
```
原始数组: [1 2 -- 4 5]
掩码: [False False  True False False]
均值（忽略掩码）: 3.0
填充后的数组: [1 2 0 4 5]
```

### 第五步：运行第二个示例
```bash
python code/example2.py
```
**预期输出**：
```
原始传感器数据: [23.5 24.1 -999.   25.3 26.0]
掩码后数组: [23.5 24.1 -- 25.3 26.0]
有效数据平均温度: 24.725
```

## 代码解析

### example1.py 关键点
- `ma.array(data, mask=mask)`：手动指定哪些元素被屏蔽
- `ma.mean()`：自动忽略被屏蔽的值进行统计
- `.filled(0)`：用指定值替换被屏蔽元素

### example2.py 关键点
- `ma.masked_equal(data, -999.0)`：自动将等于特定值的元素设为无效
- 在真实场景中，-999 常用于表示缺失数据

## 预期输出示例
见上文“运行示例”部分。

## 常见问题解答

**Q: 为什么不用 NaN 而要用掩码数组？**
A: 因为 NaN 会影响大多数数学运算结果（如 sum 得到 NaN），而掩码数组能智能跳过无效值。

**Q: 掩码数组会影响性能吗？**
A: 对小型数据集影响可忽略；对大型数据建议测试性能表现。

**Q: 如何查看某个元素是否被屏蔽？**
A: 使用 `arr.mask[index]` 判断布尔值即可。

## 扩展学习建议
- 学习 `numpy.ma` 模块更多函数：`masked_where`, `masked_invalid` 等
- 结合 `matplotlib` 绘图时自动忽略掩码数据
- 将掩码数组用于 Pandas 的底层数据处理逻辑理解