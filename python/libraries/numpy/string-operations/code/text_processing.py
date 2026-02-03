"""
文本搜索与替换操作示例

演示字符串的查找、替换、大小写转换等处理方法
"""

# 原始文本示例
text = "Python是最受欢迎的编程语言之一，我爱Python！"

print("--- 文本搜索与替换 ---")
print(f"原始文本：{text}")

# 检查是否包含某个子串
contains_python = "Python" in text
print(f"是否包含'Python'：{contains_python}")

# 查找子串位置（返回首次出现的索引）
position = text.find("Python")
print(f"第一次出现位置：{position}")

# 统计子串出现次数
count = text.count("Python")
print(f"总共出现次数：{count}")

# 字符串替换：将所有'Python'替换为'Java'
replaced_text = text.replace("Python", "Java")
print(f"替换后的文本：{replaced_text}")

# 大小写转换
capitalized = text.upper()
print(f"大写转换：{capitalized}")

# 其他常用方法演示
description = "  学习Python编程非常有趣  "

# 去除首尾空白字符
stripped = description.strip()
print(f"去除空白后：'{stripped}'")

# 检查字符串类型
is_alpha = "HelloWorld".isalpha()  # 是否全是字母
is_digit = "12345".isdigit()      # 是否全是数字
print(f"'HelloWorld'是否全字母：{is_alpha}")
print(f"'12345'是否全数字：{is_digit}")