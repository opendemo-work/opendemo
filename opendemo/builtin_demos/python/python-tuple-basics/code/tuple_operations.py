"""
Python元组高级操作示例

演示元组的高级用法,包括计数、索引查找、与其他数据类型的转换等。
"""


def main():
    """主函数"""
    print("=== 元组高级操作 ===\n")
    
    # 1. 元组方法
    print("1. 元组方法")
    my_tuple = (1, 2, 2, 3, 2, 4, 5)
    print(f"   原始元组: {my_tuple}")
    print(f"   count(2): {my_tuple.count(2)}")  # 统计2出现的次数
    print(f"   index(3): {my_tuple.index(3)}")  # 查找3的索引
    
    try:
        print(f"   index(10): {my_tuple.index(10)}")
    except ValueError:
        print(f"   index(10): 元素不存在\n")
    
    # 2. 元组与列表转换
    print("2. 元组与列表转换")
    tuple_data = (1, 2, 3, 4, 5)
    list_data = list(tuple_data)
    print(f"   元组转列表: {list_data}")
    
    list_data.append(6)
    new_tuple = tuple(list_data)
    print(f"   列表转元组: {new_tuple}\n")
    
    # 3. 元组推导式(实际是生成器)
    print("3. 使用生成器创建元组")
    gen = (x * 2 for x in range(5))
    result_tuple = tuple(gen)
    print(f"   生成的元组: {result_tuple}\n")
    
    # 4. 元组作为字典键
    print("4. 元组作为字典键")
    coordinates = {}
    coordinates[(0, 0)] = "原点"
    coordinates[(1, 2)] = "点A"
    coordinates[(3, 4)] = "点B"
    print(f"   坐标字典: {coordinates}")
    print(f"   查找 (1,2): {coordinates[(1, 2)]}\n")
    
    # 5. 返回多个值(实际返回元组)
    print("5. 函数返回多个值")
    def get_stats(numbers):
        """返回统计信息"""
        return min(numbers), max(numbers), sum(numbers) / len(numbers)
    
    numbers = [1, 2, 3, 4, 5]
    min_val, max_val, avg_val = get_stats(numbers)
    print(f"   最小值: {min_val}")
    print(f"   最大值: {max_val}")
    print(f"   平均值: {avg_val}\n")
    
    # 6. 元组的不可变性
    print("6. 元组的不可变性")
    tuple_with_list = (1, 2, [3, 4])
    print(f"   原始元组: {tuple_with_list}")
    
    # 元组本身不可变,但内部的可变对象可以修改
    tuple_with_list[2].append(5)
    print(f"   修改列表后: {tuple_with_list}")
    
    try:
        tuple_with_list[0] = 10  # 这会报错
    except TypeError as e:
        print(f"   尝试修改元组: {e}\n")
    
    # 7. 命名元组
    print("7. 命名元组")
    from collections import namedtuple
    
    Point = namedtuple('Point', ['x', 'y'])
    p1 = Point(10, 20)
    print(f"   命名元组: {p1}")
    print(f"   访问 x: {p1.x}")
    print(f"   访问 y: {p1.y}")
    print(f"   通过索引访问: {p1[0]}\n")
    
    # 8. 元组排序
    print("8. 元组排序")
    tuple_list = [(3, 'c'), (1, 'a'), (2, 'b')]
    sorted_list = sorted(tuple_list)  # 默认按第一个元素排序
    print(f"   原始: {tuple_list}")
    print(f"   排序后: {sorted_list}")
    
    # 按第二个元素排序
    sorted_by_second = sorted(tuple_list, key=lambda x: x[1])
    print(f"   按第二元素排序: {sorted_by_second}\n")
    
    # 9. 元组解包的高级用法
    print("9. 元组解包高级用法")
    data = (1, 2, 3, 4, 5, 6)
    first, second, *middle, last = data
    print(f"   first: {first}")
    print(f"   second: {second}")
    print(f"   middle: {middle}")
    print(f"   last: {last}\n")
    
    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
