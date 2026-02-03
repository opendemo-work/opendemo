import numpy as np


def main():
    """
    演示索引排序（argsort）的实际应用
    场景：根据学生成绩排序，但要保留对应的姓名
    """
    # 定义学生成绩字典，键为姓名，值为分数
    grades = {
        'Alice': 88,
        'Bob': 95,
        'Charlie': 70,
        'Diana': 92
    }
    
    # 提取成绩列表用于排序
    grade_values = list(grades.values())
    
    # 使用argsort获取按成绩升序排列的索引
    # 例如：[70,88,92,95] -> 对应原列表索引 [2,0,3,1]
    sorted_indices = np.argsort(grade_values)
    
    # 获取对应的学生姓名（按成绩排序后的顺序）
    student_names = list(grades.keys())
    sorted_names = [student_names[i] for i in sorted_indices]
    
    print("学生成绩:", grades)
    print("排序后的姓名顺序:", sorted_names)
    
    # 构造最终输出
    result = ", ".join([
        f"{name}({grades[name]})" for name in sorted_names
    ])
    print(f"按成绩从低到高排列的学生名单: {result}")


if __name__ == "__main__":
    main()