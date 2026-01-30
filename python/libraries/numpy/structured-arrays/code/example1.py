"""
文件: example1.py
功能: 演示结构化数组的基础创建与访问
作者: Python导师
日期: 2024
"""

import numpy as np


def main():
    # 定义结构化数据类型：包含学号(id)、姓名(name)、成绩(score)
    # 使用列表形式定义每个字段的名称和类型
    student_dtype = [
        ('id', 'i4'),      # 32位整数
        ('name', 'U10'),   # 最多10个字符的Unicode字符串
        ('score', 'f4')    # 32位浮点数
    ]

    # 创建结构化数组，传入数据列表和自定义数据类型
    students = np.array([
        (1, 'Alice', 85.5),
        (2, 'Bob', 90.2),
        (3, 'Charlie', 78.0)
    ], dtype=student_dtype)

    # 输出整个数组
    print("所有学生数据：\n", students)

    # 通过字段名访问特定列数据
    names = students['name']
    print("\n学生姓名：", names)

    # 访问单个记录的特定字段
    second_student_score = students[1]['score']
    print("\n第二名学生的成绩：", second_student_score)

    # 查看数组的结构信息
    print("\n数据类型字段：", students.dtype.names)


if __name__ == "__main__":
    main()
