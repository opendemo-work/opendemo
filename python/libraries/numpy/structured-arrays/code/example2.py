"""
文件: example2.py
功能: 演示结构化数组的排序与条件筛选
作者: Python导师
日期: 2024
"""

import numpy as np


def main():
    # 复用相同的结构化类型定义
    student_dtype = [
        ('id', 'i4'),
        ('name', 'U10'),
        ('score', 'f4')
    ]

    # 创建原始数据
    students = np.array([
        (1, 'Alice', 85.5),
        (2, 'Bob', 90.2),
        (3, 'Charlie', 78.0)
    ], dtype=student_dtype)

    # 示例1：按成绩降序排序
    # 使用 order 参数指定排序依据的字段
    sorted_students = np.sort(students, order='score')[::-1]
    print("按成绩降序排列：\n", sorted_students)

    # 示例2：筛选成绩高于80分的学生
    high_scorers = students[students['score'] > 80]
    print("\n成绩高于 80 的学生：\n", high_scorers)

    # 示例3：批量更新数据（例如加分5分）
    students['score'] += 5.0
    print("\n加分后所有学生成绩：\n", students[['name', 'score']])


if __name__ == "__main__":
    main()
