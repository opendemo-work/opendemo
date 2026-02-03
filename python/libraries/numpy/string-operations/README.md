# 字符串操作实战演示

## 简介
本项目是一个面向初学者的Python字符串操作学习示例，通过三个实际场景展示Python中常见的字符串处理方法，包括格式化、搜索替换和分割合并等核心功能。

## 学习目标
- 掌握Python字符串的基本操作方法
- 理解f-string、format等格式化技术
- 学会使用字符串的查找、替换、分割等常用方法
- 提升文本数据处理能力

## 环境要求
- Python 3.6 或更高版本（推荐3.8+）
- 操作系统：Windows、macOS、Linux 均可

## 安装依赖
本项目无需第三方库，仅使用Python标准库。请确保已安装符合要求的Python版本：

```bash
python --version
```

如果未安装，请前往 [Python官网](https://www.python.org/downloads/) 下载并安装。

## 文件说明
- `code/basic_formatting.py`：基础字符串格式化示例
- `code/text_processing.py`：文本搜索与替换操作示例
- `code/data_parsing.py`：数据解析与分割合并示例

## 逐步实操指南

### 第一步：创建项目目录结构
```bash
mkdir -p string-operations-demo/code
cd string-operations-demo
```

### 第二步：复制代码文件
将对应的Python文件保存到code目录下。

### 第三步：运行第一个示例
```bash
python code/basic_formatting.py
```
**预期输出**：
```
--- 基础字符串格式化 ---
姓名: 张三, 年龄: 25
产品: 笔记本电脑, 价格: ￥5999.00
今天的日期是：2023年11月15日
```

### 第四步：运行第二个示例
```bash
python code/text_processing.py
```
**预期输出**：
```
--- 文本搜索与替换 ---
原始文本：Python是最受欢迎的编程语言之一，我爱Python！
是否包含'Python'：True
第一次出现位置：0
总共出现次数：2
替换后的文本：Java是最受欢迎的编程语言之一，我爱Java！
大写转换：PYTHON是最受欢迎的编程语言之一，我爱PYTHON！
```

### 第五步：运行第三个示例
```bash
python code/data_parsing.py
```
**预期输出**：
```
--- 数据解析与分割合并 ---
原始CSV数据：张三,25,工程师,北京
解析后的数据：['张三', '25', '工程师', '北京']
姓名：张三，职业：工程师
重新组合的路径：folder/subfolder/file.txt
清理后的单词列表：['hello', 'world', 'python', 'coding']
```

## 代码解析

### basic_formatting.py
```python
name = "张三"
age = 25
# 使用f-string进行格式化（Python 3.6+推荐方式）
print(f"姓名: {name}, 年龄: {age}")
```
f-string是目前最高效的字符串格式化方式，直接在字符串中嵌入变量。

### text_processing.py
```python
text.count('Python')  # 统计子串出现次数
text.replace('Python', 'Java')  # 替换所有匹配项
```
这些是文本处理中最常用的内置方法，性能优秀且易于理解。

### data_parsing.py
```python
data.split(',')  # 按逗号分割字符串
'/'.join(path_parts)  # 用指定分隔符连接字符串列表
```
split和join是一对互补操作，广泛用于数据解析和路径构建。

## 预期输出示例
完整运行三个脚本后，应看到上述各部分的输出结果，无任何错误信息。

## 常见问题解答

**Q: 运行时提示'python不是内部或外部命令'？**
A: 请确认Python已正确安装并添加到系统PATH环境变量中。Windows用户建议重新运行安装程序并勾选“Add to PATH”选项。

**Q: f-string在旧版Python中报错怎么办？**
A: f-string需要Python 3.6+。可改用 `.format()` 方法或升级Python版本。

**Q: 中文输出乱码？**
A: 确保终端/控制台编码为UTF-8。Windows用户可在CMD中执行 `chcp 65001` 切换编码。

## 扩展学习建议
- 学习正则表达式（re模块）进行复杂模式匹配
- 探索textwrap模块进行文本排版
- 了解str.encode()和str.decode()处理不同字符编码
- 实践使用string模块中的常量（如string.ascii_letters）