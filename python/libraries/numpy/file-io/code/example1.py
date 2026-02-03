"""
文件名: example1.py
功能: 演示基础文本文件的读写操作
使用场景: 日志记录、配置文件读写等
"""

# 打开一个文本文件并写入内容
# 使用 with 语句可以自动关闭文件，推荐做法
with open('data.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, 我是通过Python写入的文本！')

print("文本已成功写入 data.txt")

# 读取刚刚写入的文件内容
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"读取内容：{content}")