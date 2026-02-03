"""
文件: permissions.py
功能: 使用位运算实现用户权限控制系统
作者: Python导师
日期: 2023
"""

# 定义权限常量，每个权限对应一个唯一的二进制位
READ = 1 << 0    # 0b0001
WRITE = 1 << 1   # 0b0010
EXECUTE = 1 << 2 # 0b0100
DELETE = 1 << 3  # 0b1000


def display_permissions(perms):
    """
    显示用户的当前权限状态
    :param perms: 权限整数值
    """
    read_status = '✔' if perms & READ else '✘'
    write_status = '✔' if perms & WRITE else '✘'
    execute_status = '✔' if perms & EXECUTE else '✘'
    delete_status = '✔' if perms & DELETE else '✘'
    
    print(f"用户当前权限: read({read_status}) write({write_status}) execute({execute_status}) delete({delete_status})")


def has_permission(perms, permission):
    """
    检查用户是否具有指定权限
    使用按位与操作：只有当对应位为1时结果非零
    :param perms: 当前权限值
    :param permission: 要检查的权限
    :return: 布尔值
    """
    return (perms & permission) != 0


def add_permission(perms, permission):
    """
    为用户添加指定权限
    使用按位或操作将对应位置1
    :param perms: 当前权限值
    :param permission: 要添加的权限
    :return: 新的权限值
    """
    return perms | permission


def remove_permission(perms, permission):
    """
    撤销用户的指定权限
    使用按位与和取反：将对应位置0
    :param perms: 当前权限值
    :param permission: 要移除的权限
    :return: 新的权限值
    """
    return perms & (~permission)


# 主程序演示
if __name__ == "__main__":
    # 初始化用户权限：仅拥有读取权限
    user_perms = READ
    
    print("用户当前权限: read(✔) write(✘) execute(✘) delete(✘)")
    
    # 授予写入和删除权限
    print("授予写入和删除权限...")
    user_perms = add_permission(user_perms, WRITE)
    user_perms = add_permission(user_perms, DELETE)
    display_permissions(user_perms)
    
    # 检查是否具有删除权限
    print(f"用户是否有删除权限? {has_permission(user_perms, DELETE)}")
    
    # 撤销读取权限
    print("撤销读取权限...")
    user_perms = remove_permission(user_perms, READ)
    display_permissions(user_perms)