"""
文件: code/example2.py
功能: 创建斐波那契数列迭代器，生成前N项
"""

class FibonacciIterator:
    """
    自定义迭代器：按顺序生成斐波那契数列的每一项
    数列定义：F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)
    """

    def __init__(self, count):
        """
        初始化斐波那契迭代器

        参数:
            count (int): 要生成的斐波那契数的总数量
        """
        self.count = count      # 总共要生成多少项
        self.current_count = 0  # 已生成的项数
        self.a, self.b = 0, 1   # 初始两项：F(0)=0, F(1)=1

    def __iter__(self):
        """
        返回迭代器自身

        返回:
            self: 当前实例
        """
        return self

    def __next__(self):
        """
        返回下一个斐波那契数

        返回:
            int: 下一个斐波那契数值

        引发:
            StopIteration: 当已生成足够多的项时抛出
        """
        if self.current_count >= self.count:
            raise StopIteration  # 已完成指定数量，停止迭代

        value = self.a  # 当前要返回的值
        self.a, self.b = self.b, self.a + self.b  # 更新为下一对值
        self.current_count += 1  # 计数加一
        return value


# 主程序执行部分
if __name__ == "__main__":
    print("斐波那契迭代器前10项：")
    fib_iter = FibonacciIterator(10)
    for value in fib_iter:
        print(value)