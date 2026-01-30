"""
数据解析与分割合并示例

演示字符串的分割、合并、路径处理等数据操作
"""

# 示例CSV格式数据（常见于数据导入导出）
csv_data = "张三,25,工程师,北京"

print("--- 数据解析与分割合并 ---")
print(f"原始CSV数据：{csv_data}")

# 使用split()按分隔符分割字符串，返回列表
parsed_data = csv_data.split(",")
print(f"解析后的数据：{parsed_data}")

# 从解析结果中提取特定字段
name = parsed_data[0]
job = parsed_data[2]
print(f"姓名：{name}，职业：{job}")

# 使用join()将列表元素合并为字符串
# 常用于构建文件路径或SQL查询
path_parts = ["folder", "subfolder", "file.txt"]
file_path = "/".join(path_parts)
print(f"重新组合的路径：{file_path}")

# 处理多个空格分隔的数据
messy_text = "  hello    world   python   coding  "

# 先去除首尾空白，再按任意空白分割，自动过滤多余空格
clean_words = messy_text.strip().split()
print(f"清理后的单词列表：{clean_words}")

# 将单词重新用单个空格连接
sentence = " ".join(clean_words)
print(f"重组句子：{sentence}")

# 分割的高级用法：限制分割次数
log_line = "ERROR:2023-11-15:数据库连接失败"
parts = log_line.split(":", 2)  # 只分割前两次，保留最后一部分完整
print(f"日志解析结果：{parts}")
print(f"级别：{parts[0]}, 日期：{parts[1]}, 详情：{parts[2]}")