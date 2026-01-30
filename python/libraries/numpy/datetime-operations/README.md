# datetime-operations-demo

## 简介
本项目是一个关于Python `datetime` 模块的实操演示，通过两个具体场景展示如何在实际开发中处理日期和时间：计算时间差与解析/格式化日期字符串。适合初学者学习Python时间处理的基础知识。

## 学习目标
- 掌握Python中`datetime`模块的基本用法
- 学会创建、格式化和解析日期时间对象
- 能够计算两个时间点之间的时间差
- 理解时区无关（naive）与时区感知（aware）时间的区别

## 环境要求
- Python 3.7 或更高版本
- 支持Windows、macOS和Linux系统

## 安装依赖步骤
1. 确保已安装Python：
   ```bash
   python --version
   # 或
   python3 --version
   ```
   输出应为 `Python 3.7.x` 或更高版本。

2. 安装依赖包（本项目仅使用标准库，无需额外安装）：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/example1.py`: 演示如何计算两个时间点之间的差异（如任务耗时）
- `code/example2.py`: 演示如何解析和格式化日期字符串（如日志分析）
- `requirements.txt`: 项目依赖声明文件
- `README.md`: 当前文档

## 逐步实操指南

### 步骤1：运行第一个示例（计算时间差）
```bash
python code/example1.py
```

**预期输出**：
```
当前时间: 2025-04-05 10:30:15.123456
开始时间: 2025-04-05 08:00:00
结束时间: 2025-04-05 18:00:00
工作时长: 10:00:00
程序执行耗时: 0:00:00.000123
```

### 步骤2：运行第二个示例（解析与格式化）
```bash
python code/example2.py
```

**预期输出**：
```
原始字符串: 2025-04-05 10:30:15
解析后的日期对象: 2025-04-05 10:30:15
格式化为中文显示: 2025年04月05日 10时30分15秒
ISO格式输出: 2025-04-05T10:30:15
自定义格式: [05/Apr/2025:10:30:15]
```

## 代码解析

### example1.py 关键代码段
```python
from datetime import datetime, timedelta

# 获取当前时间
current_time = datetime.now()
print(f"当前时间: {current_time}")
```
> 使用 `datetime.now()` 获取本地当前时间。

```python
start = datetime(2025, 4, 5, 8, 0, 0)
end = datetime(2025, 4, 5, 18, 0, 0)
duration = end - start
```
> 通过减法操作得到 `timedelta` 对象，表示时间间隔。

### example2.py 关键代码段
```python
date_str = "2025-04-05 10:30:15"
dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
```
> 使用 `strptime` 将字符串按指定格式解析为 `datetime` 对象。

```python
dt.strftime("%Y年%m月%d日 %H时%M分%S秒")
```
> 使用 `strftime` 将 `datetime` 对象格式化为可读字符串。

## 预期输出示例
见“逐步实操指南”中的输出样例。

## 常见问题解答

**Q1: 运行时报错 `ModuleNotFoundError: No module named 'datetime'`？**
A: `datetime` 是Python标准库，不应出现此错误。请检查是否拼写错误或环境异常。

**Q2: 时间格式字符串中的 `%Y`, `%m` 是什么意思？**
A: 这是格式代码：`%Y`=四位年份，`%m`=两位月份，`%d`=两位日期，`%H`=小时（24小时制），`%M`=分钟，`%S`=秒。

**Q3: 如何处理时区？**
A: 可使用 `zoneinfo` 模块（Python 3.9+）或 `pytz` 库。本示例暂不涉及时区以保持简洁。

## 扩展学习建议
- 学习 `zoneinfo` 模块处理时区
- 尝试使用 `pandas` 处理时间序列数据
- 阅读官方文档：https://docs.python.org/3/library/datetime.html