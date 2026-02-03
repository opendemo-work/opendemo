"""
基础字符串格式化示例

演示Python中多种字符串格式化方法
"""

from datetime import datetime

# 定义示例变量
name = "张三"
age = 25
product = "笔记本电脑"
price = 5999.0

# 获取当前日期用于演示
now = datetime.now()

print("--- 基础字符串格式化 ---")

# 方法1: f-string (Python 3.6+, 推荐)
# 最现代、最高效的方式，在字符串前加f，直接在{}中写变量或表达式
display_name = f"姓名: {name}, 年龄: {age}"
print(display_name)

# f-string支持表达式和格式化
formatted_price = f"产品: {product}, 价格: ￥{price:.2f}"
print(formatted_price)

# 格式化日期
formatted_date = f"今天的日期是：{now:%Y年%m月%d日}"
print(formatted_date)

# 方法2: .format() 方法 (Python 2.7+/3.x)
# 使用占位符{}，通过.format()传入值
old_style = "用户{name}今年{age}岁了".format(name=name, age=age)
print(old_style)

# 方法3: % 格式化 (较老的方式，不推荐新项目使用)
percent_style = "%s花了%d元买了%s" % (name, price, product)
print(percent_style)

# 小技巧：重复字符串
separator = "-" * 30
print(separator)