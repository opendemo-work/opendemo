"""
文件: example1.py
功能: 演示基于用户名和角色的访问控制逻辑
场景: 系统权限验证
"""

def has_access(username, is_active, role):
    """
    判断用户是否有系统访问权限

    权限规则:
    - 用户必须处于激活状态 (is_active 为 True)
    - 并且必须是管理员(role=='admin') 或者 是特殊用户 'alice'

    参数:
        username (str): 用户名
        is_active (bool): 是否激活
        role (str): 用户角色

    返回:
        bool: 是否有访问权限
    """
    # 使用逻辑与(and)确保两个条件都满足
    # 使用逻辑或(or)实现多路径授权
    # 括号保证 or 表达式先计算
    return is_active and (role == "admin" or username == "alice")


# 测试用例
if __name__ == "__main__":
    print("=== 示例1：权限验证 ===")
    
    # 测试用户alice（即使不是admin也允许）
    result1 = has_access("alice", True, "user")
    print(f"用户 'alice' 权限检查结果: {result1}")
    
    # 测试普通用户bob（未被特别授权）
    result2 = has_access("bob", True, "user")
    print(f"用户 'bob' 权限检查结果: {result2}")