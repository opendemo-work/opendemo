#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python异常处理演示
展示异常捕获、自定义异常、上下文管理等
"""


def demo_basic_exception():
    """基本异常处理"""
    print("=" * 50)
    print("1. 基本异常处理")
    print("=" * 50)
    
    # try-except
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"捕获除零错误: {e}")
    
    # 多个except
    def safe_convert(value):
        try:
            return int(value)
        except ValueError:
            return f"无法转换: {value}"
        except TypeError:
            return "类型错误"
    
    print(f"safe_convert('123'): {safe_convert('123')}")
    print(f"safe_convert('abc'): {safe_convert('abc')}")
    print(f"safe_convert(None): {safe_convert(None)}")


def demo_exception_chain():
    """异常链"""
    print("\n" + "=" * 50)
    print("2. 异常处理完整结构")
    print("=" * 50)
    
    def divide(a, b):
        try:
            result = a / b
        except ZeroDivisionError:
            print("  except: 发生除零错误")
            result = None
        else:
            print(f"  else: 计算成功, 结果={result}")
        finally:
            print("  finally: 清理操作(总是执行)")
        return result
    
    print("divide(10, 2):")
    divide(10, 2)
    
    print("\ndivide(10, 0):")
    divide(10, 0)


def demo_multiple_exceptions():
    """多异常处理"""
    print("\n" + "=" * 50)
    print("3. 多异常处理")
    print("=" * 50)
    
    def process_data(data, index):
        try:
            value = data[index]
            result = 100 / value
            return result
        except (IndexError, KeyError) as e:
            return f"索引/键错误: {e}"
        except ZeroDivisionError:
            return "除零错误"
        except Exception as e:
            return f"其他错误: {type(e).__name__}: {e}"
    
    print(f"process_data([1,2,3], 1): {process_data([1,2,3], 1)}")
    print(f"process_data([1,2,3], 10): {process_data([1,2,3], 10)}")
    print(f"process_data([1,0,3], 1): {process_data([1,0,3], 1)}")


def demo_raise_exception():
    """抛出异常"""
    print("\n" + "=" * 50)
    print("4. 抛出异常")
    print("=" * 50)
    
    def validate_age(age):
        if not isinstance(age, int):
            raise TypeError(f"年龄必须是整数, 得到 {type(age).__name__}")
        if age < 0:
            raise ValueError(f"年龄不能为负数: {age}")
        if age > 150:
            raise ValueError(f"年龄不合理: {age}")
        return True
    
    test_cases = [25, -5, "abc", 200]
    for age in test_cases:
        try:
            validate_age(age)
            print(f"validate_age({age!r}): 验证通过")
        except (TypeError, ValueError) as e:
            print(f"validate_age({age!r}): {e}")


def demo_custom_exception():
    """自定义异常"""
    print("\n" + "=" * 50)
    print("5. 自定义异常")
    print("=" * 50)
    
    class ValidationError(Exception):
        """验证错误基类"""
        pass
    
    class EmailError(ValidationError):
        """邮箱验证错误"""
        def __init__(self, email, message="无效的邮箱格式"):
            self.email = email
            self.message = message
            super().__init__(f"{message}: {email}")
    
    class PasswordError(ValidationError):
        """密码验证错误"""
        def __init__(self, message):
            super().__init__(message)
    
    def validate_email(email):
        if "@" not in email:
            raise EmailError(email, "缺少@符号")
        if "." not in email.split("@")[1]:
            raise EmailError(email, "域名格式错误")
        return True
    
    def validate_password(password):
        if len(password) < 8:
            raise PasswordError("密码长度至少8位")
        if not any(c.isdigit() for c in password):
            raise PasswordError("密码必须包含数字")
        return True
    
    test_emails = ["user@example.com", "invalid-email", "user@domain"]
    for email in test_emails:
        try:
            validate_email(email)
            print(f"邮箱 {email}: 验证通过")
        except EmailError as e:
            print(f"邮箱 {email}: {e}")
    
    print()
    test_passwords = ["password123", "short", "nolower"]
    for pwd in test_passwords:
        try:
            validate_password(pwd)
            print(f"密码 '{pwd}': 验证通过")
        except PasswordError as e:
            print(f"密码 '{pwd}': {e}")


def demo_exception_info():
    """异常信息获取"""
    print("\n" + "=" * 50)
    print("6. 获取异常信息")
    print("=" * 50)
    
    import traceback
    import sys
    
    def buggy_function():
        return 1 / 0
    
    try:
        buggy_function()
    except Exception as e:
        print(f"异常类型: {type(e).__name__}")
        print(f"异常信息: {e}")
        print(f"异常参数: {e.args}")
        
        # 获取详细traceback
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(f"\n详细堆栈:")
        for line in traceback.format_exception(exc_type, exc_value, exc_tb):
            print(f"  {line.strip()}")


def demo_context_manager_exception():
    """上下文管理器与异常"""
    print("\n" + "=" * 50)
    print("7. 上下文管理器与异常")
    print("=" * 50)
    
    class ManagedResource:
        def __init__(self, name):
            self.name = name
        
        def __enter__(self):
            print(f"  打开资源: {self.name}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"  关闭资源: {self.name}")
            if exc_type:
                print(f"  处理异常: {exc_type.__name__}: {exc_val}")
                return True  # 返回True表示异常已处理
            return False
        
        def process(self, should_fail=False):
            if should_fail:
                raise RuntimeError("处理失败")
            print(f"  处理资源: {self.name}")
    
    print("正常处理:")
    with ManagedResource("resource1") as r:
        r.process()
    
    print("\n发生异常:")
    with ManagedResource("resource2") as r:
        r.process(should_fail=True)
    
    print("程序继续运行...")


if __name__ == "__main__":
    demo_basic_exception()
    demo_exception_chain()
    demo_multiple_exceptions()
    demo_raise_exception()
    demo_custom_exception()
    demo_exception_info()
    demo_context_manager_exception()
    print("\n[OK] 异常处理演示完成!")
