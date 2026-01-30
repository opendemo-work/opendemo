"""
文件: example3.py
功能: 演示电商订单发货可行性判断逻辑
场景: 订单处理系统
"""

def can_ship_order(order_amount, is_vip, shipping_region):
    """
    判断订单是否可以发货

    发货规则:
    - 订单金额超过200元 OR 是VIP客户
    - 并且 配送地区是国内或国际通用区域

    参数:
        order_amount (float): 订单金额
        is_vip (bool): 是否为VIP客户
        shipping_region (str): 配送地区

    返回:
        bool: 是否可以发货
    """
    # 复合逻辑：价值条件 或 特权身份
    value_or_privilege = order_amount > 200 or is_vip
    
    # 配送区域有效性判断
    valid_region = shipping_region in ["国内", "international"]
    
    # 必须同时满足：(高价值或VIP) 且 区域有效
    return value_or_privilege and valid_region


# 测试用例
if __name__ == "__main__":
    print("\n=== 示例3：订单发货 ===")
    
    # 高金额订单，国内配送
    can_ship1 = can_ship_order(300, True, "国内")
    print(f"订单1（金额: 300, VIP: True, 地区: 国内）是否可发货: {can_ship1}")
    
    # 低金额非VIP，国外配送
    can_ship2 = can_ship_order(100, False, "国外")
    print(f"订单2（金额: 100, VIP: False, 地区: 国外）是否可发货: {can_ship2}")