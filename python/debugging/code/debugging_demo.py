#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python代码调试技巧演示
展示各种调试方法和工具
"""
import sys
import traceback
import inspect
import time
from functools import wraps


def demo_print_debugging():
    """print调试"""
    print("=" * 50)
    print("1. print调试")
    print("=" * 50)
    
    def calculate(a, b, operation):
        print(f"DEBUG: calculate({a}, {b}, '{operation}')")
        
        if operation == 'add':
            result = a + b
        elif operation == 'multiply':
            result = a * b
        else:
            result = None
        
        print(f"DEBUG: result = {result}")
        return result
    
    calculate(10, 5, 'add')
    
    print("\n更好的print调试:")
    
    # 使用f-string调试表达式
    x, y = 10, 20
    print(f"{x=}, {y=}, {x+y=}")  # Python 3.8+
    
    # 带颜色的调试输出(终端支持)
    def debug_print(msg, color='blue'):
        colors = {'red': '\033[91m', 'green': '\033[92m', 
                  'blue': '\033[94m', 'reset': '\033[0m'}
        print(f"{colors.get(color, '')}{msg}{colors['reset']}")
    
    debug_print("这是蓝色调试信息", 'blue')
    debug_print("这是绿色调试信息", 'green')


def demo_assert_debugging():
    """断言调试"""
    print("\n" + "=" * 50)
    print("2. 断言调试")
    print("=" * 50)
    
    def divide(a, b):
        assert b != 0, "除数不能为零"
        assert isinstance(a, (int, float)), f"a必须是数字,得到{type(a)}"
        assert isinstance(b, (int, float)), f"b必须是数字,得到{type(b)}"
        return a / b
    
    print("正常断言:")
    result = divide(10, 2)
    print(f"  divide(10, 2) = {result}")
    
    print("\n断言失败:")
    try:
        divide(10, 0)
    except AssertionError as e:
        print(f"  AssertionError: {e}")
    
    print("\n注意: 使用 python -O 运行会禁用断言!")


def demo_logging_debugging():
    """日志调试"""
    print("\n" + "=" * 50)
    print("3. 日志调试")
    print("=" * 50)
    
    import logging
    
    # 配置调试日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    def process_data(data):
        logger.debug(f"开始处理数据: {data}")
        
        if not data:
            logger.warning("数据为空")
            return []
        
        result = [x * 2 for x in data]
        logger.debug(f"处理完成: {result}")
        
        return result
    
    print("日志调试输出:")
    process_data([1, 2, 3])
    process_data([])


def demo_pdb_debugging():
    """pdb调试器"""
    print("\n" + "=" * 50)
    print("4. pdb调试器")
    print("=" * 50)
    
    pdb_commands = """
pdb常用命令:
  l (list)     - 显示当前代码
  n (next)     - 执行下一行
  s (step)     - 进入函数
  c (continue) - 继续执行
  r (return)   - 执行到函数返回
  p expr       - 打印表达式值
  pp expr      - 美化打印
  w (where)    - 显示调用栈
  u (up)       - 向上移动栈帧
  d (down)     - 向下移动栈帧
  b line       - 设置断点
  cl           - 清除断点
  q (quit)     - 退出调试
  h (help)     - 帮助

使用方式:
  1. 代码中插入: import pdb; pdb.set_trace()
  2. Python 3.7+: breakpoint()
  3. 命令行: python -m pdb script.py
"""
    print(pdb_commands)
    
    # 示例函数
    def buggy_function():
        x = 10
        y = 20
        # breakpoint()  # 在此处暂停
        z = x + y
        return z
    
    result = buggy_function()
    print(f"buggy_function() = {result}")


def demo_traceback_analysis():
    """堆栈追踪分析"""
    print("\n" + "=" * 50)
    print("5. 堆栈追踪分析")
    print("=" * 50)
    
    def level3():
        raise ValueError("深层错误")
    
    def level2():
        level3()
    
    def level1():
        level2()
    
    try:
        level1()
    except ValueError:
        print("捕获异常,分析堆栈:")
        
        # 获取异常信息
        exc_type, exc_value, exc_tb = sys.exc_info()
        
        print(f"\n异常类型: {exc_type.__name__}")
        print(f"异常信息: {exc_value}")
        
        # 格式化堆栈
        print("\n堆栈追踪:")
        for line in traceback.format_tb(exc_tb):
            print(f"  {line.strip()}")
        
        # 提取帧信息
        print("\n调用链:")
        tb = exc_tb
        while tb:
            frame = tb.tb_frame
            print(f"  {frame.f_code.co_filename}:{tb.tb_lineno} in {frame.f_code.co_name}")
            tb = tb.tb_next


def demo_inspect_module():
    """inspect模块"""
    print("\n" + "=" * 50)
    print("6. inspect模块")
    print("=" * 50)
    
    def example_function(a: int, b: str = "default") -> str:
        """示例函数的文档字符串"""
        return f"{a}: {b}"
    
    class ExampleClass:
        """示例类"""
        def method(self, x):
            return x * 2
    
    # 获取函数信息
    print("函数信息:")
    print(f"  名称: {example_function.__name__}")
    print(f"  文档: {inspect.getdoc(example_function)}")
    print(f"  签名: {inspect.signature(example_function)}")
    
    # 获取参数信息
    sig = inspect.signature(example_function)
    print("\n参数详情:")
    for name, param in sig.parameters.items():
        print(f"  {name}: default={param.default}, annotation={param.annotation}")
    
    # 获取源代码
    print("\n源代码:")
    source = inspect.getsource(example_function)
    for line in source.split('\n')[:3]:
        print(f"  {line}")
    
    # 获取类成员
    print("\n类成员:")
    for name, value in inspect.getmembers(ExampleClass):
        if not name.startswith('_'):
            print(f"  {name}: {type(value).__name__}")


def demo_timing_debugging():
    """性能计时调试"""
    print("\n" + "=" * 50)
    print("7. 性能计时调试")
    print("=" * 50)
    
    # 简单计时
    def simple_timing():
        start = time.time()
        # 模拟工作
        time.sleep(0.1)
        elapsed = time.time() - start
        print(f"耗时: {elapsed:.4f}秒")
    
    print("简单计时:")
    simple_timing()
    
    # 计时装饰器
    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"[TIMER] {func.__name__}: {elapsed:.6f}秒")
            return result
        return wrapper
    
    @timer
    def slow_function():
        time.sleep(0.05)
        return "done"
    
    print("\n计时装饰器:")
    slow_function()
    
    # 上下文管理器计时
    from contextlib import contextmanager
    
    @contextmanager
    def timer_context(name=""):
        start = time.perf_counter()
        yield
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {name}: {elapsed:.6f}秒")
    
    print("\n上下文管理器计时:")
    with timer_context("代码块"):
        time.sleep(0.03)


def demo_memory_debugging():
    """内存调试"""
    print("\n" + "=" * 50)
    print("8. 内存调试")
    print("=" * 50)
    
    # 对象大小
    import sys
    
    objects = {
        "空列表": [],
        "10元素列表": list(range(10)),
        "1000元素列表": list(range(1000)),
        "空字典": {},
        "字符串'hello'": "hello",
        "整数1000": 1000,
    }
    
    print("对象大小 (sys.getsizeof):")
    for name, obj in objects.items():
        size = sys.getsizeof(obj)
        print(f"  {name}: {size} bytes")
    
    # 引用计数
    print("\n引用计数 (sys.getrefcount):")
    x = [1, 2, 3]
    print(f"  x = [1,2,3]: {sys.getrefcount(x)} 个引用")
    y = x
    print(f"  y = x 后: {sys.getrefcount(x)} 个引用")
    
    print("\n更多工具:")
    print("  - memory_profiler: 逐行内存分析")
    print("  - tracemalloc: 内存分配追踪")
    print("  - objgraph: 对象关系图")


def demo_debugging_tips():
    """调试技巧总结"""
    print("\n" + "=" * 50)
    print("9. 调试技巧总结")
    print("=" * 50)
    
    tips = """
调试技巧总结:

1. 复现问题
   - 找到最小可复现案例
   - 记录输入和环境

2. 二分法定位
   - 注释一半代码
   - 逐步缩小范围

3. 橡皮鸭调试
   - 向别人(或橡皮鸭)解释代码
   - 解释过程中发现问题

4. 日志策略
   - DEBUG: 详细诊断信息
   - INFO: 确认程序工作
   - WARNING: 潜在问题
   - ERROR: 运行时错误

5. 断点调试
   - 在关键位置设置断点
   - 检查变量状态
   - 单步执行观察流程

6. 单元测试
   - 编写测试用例
   - 隔离问题代码

7. 代码审查
   - 第二双眼睛
   - 发现盲点

8. Git bisect
   - 二分查找引入bug的提交
"""
    print(tips)


if __name__ == "__main__":
    demo_print_debugging()
    demo_assert_debugging()
    demo_logging_debugging()
    demo_pdb_debugging()
    demo_traceback_analysis()
    demo_inspect_module()
    demo_timing_debugging()
    demo_memory_debugging()
    demo_debugging_tips()
    print("\n[OK] 代码调试技巧演示完成!")
