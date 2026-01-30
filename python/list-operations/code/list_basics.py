#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python列表操作演示
展示列表的创建、索引、切片、常用方法和列表推导式
"""

def demo_list_creation():
    """列表创建方式"""
    print("=" * 50)
    print("1. 列表创建方式")
    print("=" * 50)
    
    # 直接创建
    list1 = [1, 2, 3, 4, 5]
    print(f"直接创建: {list1}")
    
    # 混合类型
    list2 = [1, "hello", 3.14, True, None]
    print(f"混合类型: {list2}")
    
    # list()构造函数
    list3 = list("hello")
    print(f"list('hello'): {list3}")
    
    # range生成
    list4 = list(range(1, 6))
    print(f"list(range(1, 6)): {list4}")
    
    # 列表推导式
    list5 = [x**2 for x in range(1, 6)]
    print(f"[x**2 for x in range(1, 6)]: {list5}")
    
    # 空列表
    list6 = []
    list7 = list()
    print(f"空列表: [] 或 list() -> {list6}, {list7}")


def demo_list_access():
    """列表访问和切片"""
    print("\n" + "=" * 50)
    print("2. 列表访问和切片")
    print("=" * 50)
    
    nums = [10, 20, 30, 40, 50, 60, 70]
    print(f"原列表: {nums}")
    
    # 索引访问
    print(f"nums[0]: {nums[0]}")
    print(f"nums[-1]: {nums[-1]}")
    print(f"nums[2]: {nums[2]}")
    
    # 切片
    print(f"nums[1:4]: {nums[1:4]}")
    print(f"nums[:3]: {nums[:3]}")
    print(f"nums[4:]: {nums[4:]}")
    print(f"nums[::2]: {nums[::2]}")
    print(f"nums[::-1]: {nums[::-1]}")
    
    # 嵌套列表访问
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"\n嵌套列表: {matrix}")
    print(f"matrix[1][2]: {matrix[1][2]}")


def demo_list_modify():
    """列表修改操作"""
    print("\n" + "=" * 50)
    print("3. 列表修改操作")
    print("=" * 50)
    
    nums = [1, 2, 3, 4, 5]
    print(f"原列表: {nums}")
    
    # 添加元素
    nums.append(6)
    print(f"append(6): {nums}")
    
    nums.insert(0, 0)
    print(f"insert(0, 0): {nums}")
    
    nums.extend([7, 8])
    print(f"extend([7, 8]): {nums}")
    
    # 删除元素
    nums.remove(0)
    print(f"remove(0): {nums}")
    
    popped = nums.pop()
    print(f"pop(): 弹出 {popped}, 剩余 {nums}")
    
    popped = nums.pop(0)
    print(f"pop(0): 弹出 {popped}, 剩余 {nums}")
    
    # 修改元素
    nums[0] = 100
    print(f"nums[0] = 100: {nums}")
    
    # 批量修改
    nums[1:3] = [200, 300]
    print(f"nums[1:3] = [200, 300]: {nums}")
    
    # 清空列表
    nums_copy = nums.copy()
    nums_copy.clear()
    print(f"clear(): {nums_copy}")


def demo_list_methods():
    """列表常用方法"""
    print("\n" + "=" * 50)
    print("4. 列表常用方法")
    print("=" * 50)
    
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    print(f"原列表: {nums}")
    
    # 查找
    print(f"index(5): {nums.index(5)}")
    print(f"count(1): {nums.count(1)}")
    print(f"5 in nums: {5 in nums}")
    
    # 排序
    nums_sorted = sorted(nums)
    print(f"sorted(nums): {nums_sorted}")
    
    nums_sorted_desc = sorted(nums, reverse=True)
    print(f"sorted(nums, reverse=True): {nums_sorted_desc}")
    
    nums.sort()
    print(f"nums.sort(): {nums}")
    
    # 反转
    nums.reverse()
    print(f"nums.reverse(): {nums}")
    
    # 统计
    print(f"len(nums): {len(nums)}")
    print(f"max(nums): {max(nums)}")
    print(f"min(nums): {min(nums)}")
    print(f"sum(nums): {sum(nums)}")


def demo_list_comprehension():
    """列表推导式"""
    print("\n" + "=" * 50)
    print("5. 列表推导式")
    print("=" * 50)
    
    # 基本推导式
    squares = [x**2 for x in range(1, 6)]
    print(f"[x**2 for x in range(1, 6)]: {squares}")
    
    # 带条件的推导式
    evens = [x for x in range(10) if x % 2 == 0]
    print(f"[x for x in range(10) if x % 2 == 0]: {evens}")
    
    # 带转换的推导式
    words = ['Hello', 'World', 'Python']
    lower_words = [w.lower() for w in words]
    print(f"[w.lower() for w in words]: {lower_words}")
    
    # 嵌套推导式
    matrix = [[i*3+j for j in range(3)] for i in range(3)]
    print(f"嵌套推导式生成矩阵: {matrix}")
    
    # 展平嵌套列表
    flat = [x for row in matrix for x in row]
    print(f"展平嵌套列表: {flat}")


if __name__ == "__main__":
    demo_list_creation()
    demo_list_access()
    demo_list_modify()
    demo_list_methods()
    demo_list_comprehension()
    print("\n[OK] 列表操作演示完成!")
