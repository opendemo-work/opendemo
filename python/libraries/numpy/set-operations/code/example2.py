"""
文件: example2.py
功能: 模拟用户兴趣匹配场景，展示集合在实际中的应用
作者: Python导师
日期: 2024
"""

# 用户兴趣标签（模拟数据）
alice_interests = {"阅读", "电影", "音乐", "旅行"}
bob_interests = {"旅行", "电影", "运动", "游戏"}

print(f"用户Alice的兴趣: {alice_interests}")
print(f"用户Bob的兴趣: {bob_interests}")

# 计算共同兴趣（交集）
common_interests = alice_interests & bob_interests
print(f"共同兴趣: {common_interests}")

# 为Alice推荐Bob有兴趣但她没有的活动（差集）
recommendations = bob_interests - alice_interests
print(f"推荐给Alice的新兴趣: {recommendations}")

# 扩展：计算两人总兴趣范围（并集）
all_interests = alice_interests | bob_interests
print(f"两人的全部兴趣: {all_interests}")