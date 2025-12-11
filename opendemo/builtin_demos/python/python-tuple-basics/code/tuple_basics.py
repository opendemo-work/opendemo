"""
Python元组基础操作示例

本示例演示元组的基本操作,包括创建、访问、切片等。
"""


def main():
    """主函数"""
    print("=== 元组基础操作 ===\n")
    
    # 1. 创建元组
    print("1. 创建元组")
    my_tuple = (1, 2, 3, 4, 5)
    print(f"   创建元组: {my_tuple}")
    
    # 创建空元组
    empty_tuple = ()
    print(f"   空元组: {empty_tuple}")
    
    # 创建单元素元组(注意逗号)
    single_tuple = (1,)
    print(f"   单元素元组: {single_tuple}")
    
    # 不使用括号创建元组
    implicit_tuple = 1, 2, 3
    print(f"   隐式元组: {implicit_tuple}\n")
    
    # 2. 访问元组元素
    print("2. 访问元组元素")
    print(f"   第一个元素: {my_tuple[0]}")
    print(f"   最后一个元素: {my_tuple[-1]}")
    print(f"   第二个元素: {my_tuple[1]}\n")
    
    # 3. 元组切片
    print("3. 元组切片")
    print(f"   切片 [1:4]: {my_tuple[1:4]}")
    print(f"   切片 [:3]: {my_tuple[:3]}")
    print(f"   切片 [2:]: {my_tuple[2:]}")
    print(f"   反转元组 [::-1]: {my_tuple[::-1]}\n")
    
    # 4. 元组长度
    print("4. 元组操作")
    print(f"   元组长度: {len(my_tuple)}")
    print(f"   最大值: {max(my_tuple)}")
    print(f"   最小值: {min(my_tuple)}")
    print(f"   求和: {sum(my_tuple)}\n")
    
    # 5. 元组包含检查
    print("5. 元素检查")
    print(f"   3 在元组中: {3 in my_tuple}")
    print(f"   10 在元组中: {10 in my_tuple}\n")
    
    # 6. 元组连接和重复
    print("6. 元组连接和重复")
    tuple1 = (1, 2, 3)
    tuple2 = (4, 5, 6)
    print(f"   连接: {tuple1 + tuple2}")
    print(f"   重复: {tuple1 * 3}\n")
    
    # 7. 元组解包
    print("7. 元组解包")
    a, b, c = (1, 2, 3)
    print(f"   解包后: a={a}, b={b}, c={c}")
    
    # 使用*收集剩余元素
    first, *rest = (1, 2, 3, 4, 5)
    print(f"   first={first}, rest={rest}\n")
    
    # 8. 嵌套元组
    print("8. 嵌套元组")
    nested_tuple = ((1, 2), (3, 4), (5, 6))
    print(f"   嵌套元组: {nested_tuple}")
    print(f"   访问嵌套元素: {nested_tuple[0][1]}\n")
    
    # 9. 混合类型元组
    print("9. 混合类型元组")
    mixed_tuple = (1, "hello", 3.14, True, [1, 2, 3])
    print(f"   混合元组: {mixed_tuple}")
    print(f"   类型: {[type(x).__name__ for x in mixed_tuple]}\n")
    
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
