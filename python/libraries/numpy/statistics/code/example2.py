"""
文件: grouped_data_stats.py
功能: 对分组数据（如频数表）进行统计分析
作者: Python编程导师
日期: 2024
"""

import statistics
from collections import Counter


def expand_grouped_data(distribution):
    """
    将分组数据（字典形式）展开为原始数据列表

    参数:
        distribution (dict): 键为类别，值为频数

    返回:
        list: 展开后的数据列表
    """
    expanded = []
    for value, count in distribution.items():
        expanded.extend([value] * count)
    return expanded


def main():
    """主函数：演示分组数据的统计分析"""
    # 示例数据：某班级学生考试成绩等级分布
    grade_distribution = {
        'A': 5,
        'B': 12,
        'C': 8,
        'D': 3
    }

    print("=== 分组数据统计 ===")
    print(f"学生成绩分布: {grade_distribution}")

    # 展开数据以便进行统计分析
    expanded_grades = expand_grouped_data(grade_distribution)
    print(f"成绩列表展开后: {expanded_grades[:10]}... (共{len(expanded_grades)}项)")

    # 找出众数（最常见的成绩）
    # multimode 返回所有众数，避免抛出异常
    modes = statistics.multimode(expanded_grades)
    print(f"最常见成绩: {modes[0] if modes else '无'}")

    # 为分类数据分配数值以便计算中位数等级
    # 定义等级映射（数值越高表示成绩越好）
    grade_to_num = {'D': 1, 'C': 2, 'B': 3, 'A': 4}
    num_to_grade = {v: k for k, v in grade_to_num.items()}

    # 将成绩转换为数值
    numeric_grades = [grade_to_num[grade] for grade in expanded_grades]

    # 计算中位数对应的等级
    median_numeric = statistics.median(numeric_grades)
    # 四舍五入到最近的整数等级
    median_grade_num = round(median_numeric)
    median_grade = num_to_grade[median_grade_num]

    print(f"成绩中位等级: {median_grade}")


if __name__ == "__main__":
    main()
