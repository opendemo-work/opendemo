"""
文件: example2.py
功能: 演示学生成绩与出勤率综合判断逻辑
场景: 奖学金资格评审
"""

def is_eligible_for_scholarship(score, attendance_rate):
    """
    判断学生是否有资格获得奖学金

    资格规则:
    - 成绩必须达到80分及以上
    - 出勤率必须达到90%及以上
    - 两个条件必须同时满足

    参数:
        score (int): 学生成绩 (0-100)
        attendance_rate (float): 出勤率 (0.0 - 1.0)

    返回:
        bool: 是否有奖学金资格
    """
    # 使用逻辑与(and)连接两个必要条件
    # 两个条件都为True时整体才为True
    return score >= 80 and attendance_rate >= 0.9


# 测试用例
if __name__ == "__main__":
    print("\n=== 示例2：奖学金资格 ===")
    
    # 学生Alice：高分高出席
    eligible = is_eligible_for_scholarship(85, 0.92)
    print(f"学生Alice (成绩: 85, 出勤率: 0.92) 是否有奖学金资格: {eligible}")
    
    # 学生Bob：成绩一般，出席一般
    not_eligible = is_eligible_for_scholarship(70, 0.85)
    print(f"学生Bob (成绩: 70, 出勤率: 0.85) 是否有奖学金资格: {not_eligible}")