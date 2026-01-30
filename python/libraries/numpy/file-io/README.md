# Python文件读写操作演示

## 简介
本项目演示了在Python中如何进行基本的文件读写操作，涵盖普通文本文件、CSV格式数据以及使用NumPy进行数值数组的保存与加载。通过三个示例脚本帮助初学者掌握数据持久化的基本技能。

## 学习目标
- 掌握Python内置`open()`函数进行文本文件的读写
- 学会使用`csv`模块处理表格型数据
- 理解如何用NumPy高效地保存和加载数值数组
- 培养良好的文件操作习惯（如使用上下文管理器）

## 环境要求
- Python 3.6 或更高版本
- 支持跨平台运行（Windows / Linux / macOS）

## 安装依赖
1. 确保已安装Python：打开终端输入 `python --version` 或 `python3 --version`
2. 安装所需依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 文件说明
- `code/example1.py`：基础文本文件的读写操作
- `code/example2.py`：使用csv模块读写结构化数据
- `code/example3.py`：利用NumPy保存和加载数值数组
- `requirements.txt`：项目依赖声明文件

## 逐步实操指南

### 步骤1：克隆或创建项目目录
```bash
mkdir file_io_demo
cd file_io_demo
# 创建必要子目录
mkdir code
```

### 步骤2：复制代码文件
将以下三个文件分别保存到对应路径：
- 将example1.py内容保存为 `code/example1.py`
- 将example2.py内容保存为 `code/example2.py`
- 将example3.py内容保存为 `code/example3.py`

### 步骤3：安装依赖
```bash
pip install -r requirements.txt
```

### 步骤4：运行示例
```bash
python code/example1.py
python code/example2.py
python code/example3.py
```

#### 预期输出（部分）
运行example1.py应看到：
```
文本已成功写入 data.txt
读取内容：Hello, 我是通过Python写入的文本！
```

## 代码解析

### example1.py 关键点
```python
with open('data.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, 我是通过Python写入的文本！')
```
- 使用`with`语句确保文件自动关闭
- 指定`encoding='utf-8'`避免中文乱码

### example2.py 关键点
```python
import csv
...
writer.writerow(['姓名', '年龄', '城市'])
```
- `csv.writer`用于写入逗号分隔值
- 数据以列表形式逐行写入

### example3.py 关键点
```python
np.savetxt('array_data.txt', arr)
loaded = np.loadtxt('array_data.txt')
```
- `savetxt`和`loadtxt`是NumPy提供的便捷方法
- 适合处理纯数字矩阵数据

## 预期输出示例
每个脚本执行后都会打印成功信息，并生成对应的输出文件，例如：
- data.txt
- users.csv
- array_data.txt

## 常见问题解答

**Q: 运行时报错 `ModuleNotFoundError: No module named 'numpy'` 怎么办？**
A: 请确认是否已正确执行 `pip install -r requirements.txt` 安装所有依赖。

**Q: 中文写入文件出现乱码怎么办？**
A: 确保在`open()`函数中指定`encoding='utf-8'`参数。

**Q: 能否读取Excel文件？**
A: 本示例不包含Excel支持，可后续学习`pandas`库结合`openpyxl`实现。

## 扩展学习建议
- 学习使用`json`模块保存复杂结构数据
- 探索`pandas`的`to_csv()`和`read_csv()`方法
- 了解二进制文件读写（pickle模块）
- 实践异常处理（try-except）保护文件操作