#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python上下文管理器演示
展示with语句、自定义上下文管理器、contextlib等
"""
from contextlib import contextmanager, suppress, redirect_stdout
import io
import tempfile
import os


def demo_with_statement():
    """with语句基础"""
    print("=" * 50)
    print("1. with语句基础")
    print("=" * 50)
    
    # 文件操作
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write("测试内容")
    temp_file.close()
    
    # 使用with自动关闭文件
    with open(temp_file.name, 'r') as f:
        content = f.read()
        print(f"读取内容: {content}")
    print(f"文件已自动关闭: {f.closed}")
    
    os.unlink(temp_file.name)
    
    # 多个上下文管理器
    temp1 = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp2 = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp1.write("文件1"); temp1.close()
    temp2.write("文件2"); temp2.close()
    
    print("\n多个上下文管理器:")
    with open(temp1.name) as f1, open(temp2.name) as f2:
        print(f"  f1: {f1.read()}, f2: {f2.read()}")
    
    os.unlink(temp1.name)
    os.unlink(temp2.name)


def demo_custom_context_manager_class():
    """类实现上下文管理器"""
    print("\n" + "=" * 50)
    print("2. 类实现上下文管理器")
    print("=" * 50)
    
    class Timer:
        """计时器上下文管理器"""
        def __init__(self, name="Timer"):
            self.name = name
        
        def __enter__(self):
            import time
            self.start = time.time()
            print(f"  [{self.name}] 开始计时")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            import time
            self.elapsed = time.time() - self.start
            print(f"  [{self.name}] 耗时: {self.elapsed:.4f}秒")
            return False  # 不抑制异常
    
    print("计时器示例:")
    with Timer("测试") as t:
        total = sum(range(1000000))
    print(f"  计算结果: {total}")
    
    # 带异常处理的上下文管理器
    class ErrorHandler:
        def __init__(self, suppress_errors=False):
            self.suppress = suppress_errors
        
        def __enter__(self):
            print("  进入上下文")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                print(f"  捕获异常: {exc_type.__name__}: {exc_val}")
                return self.suppress  # True则抑制异常
            print("  正常退出")
            return False
    
    print("\n异常处理示例(抑制异常):")
    with ErrorHandler(suppress_errors=True):
        raise ValueError("测试错误")
    print("  程序继续运行")


def demo_contextmanager_decorator():
    """@contextmanager装饰器"""
    print("\n" + "=" * 50)
    print("3. @contextmanager装饰器")
    print("=" * 50)
    
    @contextmanager
    def managed_resource(name):
        print(f"  获取资源: {name}")
        try:
            yield f"Resource<{name}>"
        finally:
            print(f"  释放资源: {name}")
    
    print("使用@contextmanager:")
    with managed_resource("Database") as db:
        print(f"  使用资源: {db}")
    
    # 临时改变工作目录
    @contextmanager
    def change_dir(path):
        old_dir = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(old_dir)
    
    print(f"\n临时改变目录:")
    print(f"  当前目录: {os.getcwd()}")
    with change_dir(tempfile.gettempdir()):
        print(f"  临时目录: {os.getcwd()}")
    print(f"  恢复目录: {os.getcwd()}")


def demo_contextlib_utilities():
    """contextlib工具函数"""
    print("\n" + "=" * 50)
    print("4. contextlib工具函数")
    print("=" * 50)
    
    # suppress - 抑制指定异常
    print("suppress示例:")
    with suppress(FileNotFoundError):
        os.remove("不存在的文件.txt")
    print("  FileNotFoundError被抑制")
    
    # redirect_stdout - 重定向标准输出
    print("\nredirect_stdout示例:")
    f = io.StringIO()
    with redirect_stdout(f):
        print("这段输出会被重定向")
    output = f.getvalue()
    print(f"  捕获的输出: {output.strip()}")
    
    # closing - 确保对象关闭
    from contextlib import closing
    
    class Connection:
        def __init__(self, host):
            self.host = host
            print(f"  连接到: {host}")
        def close(self):
            print(f"  断开连接: {self.host}")
        def query(self, sql):
            return f"执行: {sql}"
    
    print("\nclosing示例:")
    with closing(Connection("localhost")) as conn:
        result = conn.query("SELECT 1")
        print(f"  {result}")


def demo_nested_context():
    """嵌套上下文管理器"""
    print("\n" + "=" * 50)
    print("5. 嵌套上下文管理器")
    print("=" * 50)
    
    @contextmanager
    def level(name):
        print(f"  进入: {name}")
        yield name
        print(f"  退出: {name}")
    
    print("嵌套示例:")
    with level("外层") as outer:
        with level("中层") as middle:
            with level("内层") as inner:
                print(f"  当前层级: {outer} > {middle} > {inner}")


def demo_reentrant_context():
    """可重入上下文管理器"""
    print("\n" + "=" * 50)
    print("6. ExitStack动态管理")
    print("=" * 50)
    
    from contextlib import ExitStack
    
    @contextmanager
    def resource(name):
        print(f"  获取: {name}")
        yield name
        print(f"  释放: {name}")
    
    print("ExitStack动态管理多个资源:")
    with ExitStack() as stack:
        resources = []
        for i in range(3):
            r = stack.enter_context(resource(f"res_{i}"))
            resources.append(r)
        print(f"  所有资源: {resources}")
    print("  所有资源已释放")


if __name__ == "__main__":
    demo_with_statement()
    demo_custom_context_manager_class()
    demo_contextmanager_decorator()
    demo_contextlib_utilities()
    demo_nested_context()
    demo_reentrant_context()
    print("\n[OK] 上下文管理器演示完成!")
