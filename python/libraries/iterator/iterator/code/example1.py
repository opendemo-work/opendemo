"""
文件: code/example1.py
功能: 创建一个简单的计数迭代器，从1递增到指定数值
"""

class CountIterator:
    """
    自定义迭代器类：从1开始逐个返回整数，直到达到设定的最大值
    """

    def __init__(self, max_value):
        """
        初始化迭代器

        参数:
            max_value (int): 最大计数值，迭代将在达到此值后停止
        """
        self.max_value = max_value  # 设置最大值
        self.current = 0             # 当前计数初始化为0

    def __iter__(self):
        """
        返回迭代器自身，使该对象可用于 for/in 语句

        返回:
            self: 当前实例
        """
        return self

    def __next__(self):
        """
        获取下一个值

        返回:
            int: 下一个整数

        引发:
            StopIteration: 当计数超过最大值时抛出，表示迭代结束
        """
        self.current += 1  # 自增当前计数
        if self.current > self.max_value:
            raise StopIteration  # 达到上限，停止迭代
        return self.current     # 返回当前值


# 主程序执行部分
if __name__ == "__main__":
    print("计数迭代器输出前5个数字：")
    # 创建一个最多输出5个数字的迭代器
    counter = CountIterator(5)
    # 使用for循环自动调用迭代器
    for number in counter:
        print(number)