# Python窗口函数实战演示

## 简介
本项目通过两个实际场景演示了pandas中窗口函数（Window Functions）的使用方法。窗口函数是数据分析中的重要工具，能够对数据子集进行计算而不改变原始数据的行数，常用于移动平均、累计统计等场景。

## 学习目标
- 理解窗口函数的基本概念和应用场景
- 掌握pandas中rolling()和expanding()方法的使用
- 学会在时间序列数据中应用移动平均
- 理解累计计算在数据分析中的作用

## 环境要求
- Python 3.7 或更高版本
- 操作系统：Windows、Linux、macOS（跨平台兼容）

## 安装依赖
```bash
# 创建虚拟环境（推荐）
python -m venv window-env

# 激活虚拟环境
# Windows:
window-env\Scripts\activate
# macOS/Linux:
source window-env/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

## 文件说明
- `code/sales_trend_analysis.py`: 销售数据趋势分析，展示移动平均的应用
- `code/cumulative_performance.py`: 累计业绩分析，展示扩展窗口函数的使用
- `requirements.txt`: 项目依赖声明文件

## 逐步实操指南

### 步骤1：克隆或创建项目目录
```bash
mkdir window-functions-demo
cd window-functions-demo
```

### 步骤2：创建代码目录并保存文件
```bash
mkdir code
# 将sales_trend_analysis.py和cumulative_performance.py内容保存到code目录
```

### 步骤3：创建并安装依赖
```bash
# 创建requirements.txt文件并运行安装
pip install -r requirements.txt
```

### 步骤4：运行第一个示例
```bash
python code/sales_trend_analysis.py
```

**预期输出**：
```
=== 销售数据与7天移动平均 ===
日期        销售额  7天移动平均
2023-01-01   100        NaN
2023-01-02   120        NaN
...        ...        ...
2023-01-07   160  138.571429
2023-01-08   180  150.000000
```

### 步骤5：运行第二个示例
```bash
python code/cumulative_performance.py
```

**预期输出**：
```
=== 员工业绩累计统计 ===
         销售额  累计销售额  累计平均销售额
员工A     5000    5000.0     5000.000000
员工B     7500   12500.0     6250.000000
员工C     6200   18700.0     6233.333333
```

## 代码解析

### sales_trend_analysis.py 关键代码
```python
# 创建7天滚动窗口并计算平均值
sales_data['7天移动平均'] = sales_data['销售额'].rolling(window=7).mean()
```
- `rolling(window=7)`：创建一个大小为7的滑动窗口
- `.mean()`：计算每个窗口内的平均值
- 自动处理边界情况，前6天由于数据不足返回NaN

### cumulative_performance.py 关键代码
```python
# 使用扩展窗口计算累计统计
performance_df['累计平均销售额'] = performance_df['销售额'].expanding().mean()
```
- `expanding()`：创建从开始到当前行的扩展窗口
- 适用于计算累计平均、累计和等场景

## 预期输出示例
完整输出将显示格式化的DataFrame表格，包含原始数据和计算后的窗口函数结果，NaN值表示因窗口大小限制无法计算的位置。

## 常见问题解答

**Q: 为什么移动平均的前几行是NaN？**
A: 因为窗口大小设置为7，前6天的数据不足以填满整个窗口，这是正常现象。可以通过`min_periods`参数调整最小观测数。

**Q: 如何处理时间序列中的缺失日期？**
A: 可以先用`resample()`方法重新采样数据，确保时间序列的连续性。

**Q: 除了mean()，还有哪些可用的聚合函数？**
A: 支持sum()、std()、var()、max()、min()、median()等几乎所有pandas聚合函数。

## 扩展学习建议
- 尝试使用加权移动平均（weighted moving average）
- 探索指数加权窗口（ewm()）用于时间序列预测
- 将窗口函数应用于股票价格数据分析
- 结合matplotlib可视化原始数据与移动平均线的趋势对比