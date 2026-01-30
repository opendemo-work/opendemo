"""
文件名: example2.py
功能: 使用csv模块读写结构化数据
使用场景: 用户信息表、销售数据导出等
"""

import csv

# 要写入的数据（模拟用户信息）
data = [
    ['姓名', '年龄', '城市'],
    ['张三', 25, '北京'],
    ['李四', 30, '上海'],
    ['王五', 28, '广州']
]

# 写入CSV文件
with open('users.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # 逐行写入数据
    for row in data:
        writer.writerow(row)

print("用户数据已成功写入 users.csv")

# 读取CSV文件验证结果
with open('users.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    print("从CSV读取的内容：")
    for row in reader:
        print(row)