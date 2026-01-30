#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python正则表达式演示
展示re模块的常用功能
"""
import re


def demo_basic_patterns():
    """基本模式"""
    print("=" * 50)
    print("1. 基本模式匹配")
    print("=" * 50)
    
    text = "Hello World 123 Python 456"
    
    # 查找
    match = re.search(r'\d+', text)
    print(f"文本: '{text}'")
    print(f"search(r'\\d+'): {match.group() if match else None}")
    
    # 匹配开头
    match = re.match(r'Hello', text)
    print(f"match(r'Hello'): {match.group() if match else None}")
    
    # 查找所有
    all_nums = re.findall(r'\d+', text)
    print(f"findall(r'\\d+'): {all_nums}")
    
    # 替换
    result = re.sub(r'\d+', '#', text)
    print(f"sub(r'\\d+', '#'): '{result}'")


def demo_special_characters():
    """特殊字符"""
    print("\n" + "=" * 50)
    print("2. 特殊字符")
    print("=" * 50)
    
    text = "Hello World 123\nPython 3.11"
    print(f"文本: {repr(text)}")
    
    patterns = [
        (r'.', '任意字符(除换行)'),
        (r'\d', '数字'),
        (r'\D', '非数字'),
        (r'\w', '单词字符'),
        (r'\W', '非单词字符'),
        (r'\s', '空白字符'),
        (r'\S', '非空白字符'),
    ]
    
    for pattern, desc in patterns:
        matches = re.findall(pattern, text)
        print(f"  {pattern} ({desc}): {matches[:10]}{'...' if len(matches)>10 else ''}")


def demo_quantifiers():
    """量词"""
    print("\n" + "=" * 50)
    print("3. 量词")
    print("=" * 50)
    
    text = "aaa ab abbb a123 a12345"
    print(f"文本: '{text}'")
    
    patterns = [
        (r'a+', '一个或多个a'),
        (r'ab*', 'a后跟零或多个b'),
        (r'ab?', 'a后跟零或一个b'),
        (r'a{3}', '恰好3个a'),
        (r'\d{2,4}', '2到4个数字'),
        (r'\d+?', '非贪婪匹配数字'),
    ]
    
    for pattern, desc in patterns:
        matches = re.findall(pattern, text)
        print(f"  {pattern} ({desc}): {matches}")


def demo_groups():
    """分组"""
    print("\n" + "=" * 50)
    print("4. 分组")
    print("=" * 50)
    
    # 基本分组
    text = "John Smith, Jane Doe, Bob Wilson"
    pattern = r'(\w+)\s+(\w+)'
    
    print(f"文本: '{text}'")
    print(f"模式: r'(\\w+)\\s+(\\w+)'")
    
    matches = re.findall(pattern, text)
    print(f"findall结果: {matches}")
    
    for match in re.finditer(pattern, text):
        print(f"  全匹配: {match.group()}, 组1: {match.group(1)}, 组2: {match.group(2)}")
    
    # 命名分组
    print("\n命名分组:")
    pattern = r'(?P<first>\w+)\s+(?P<last>\w+)'
    match = re.search(pattern, text)
    if match:
        print(f"  first: {match.group('first')}, last: {match.group('last')}")
    
    # 非捕获分组
    print("\n非捕获分组 (?:...):")
    pattern = r'(?:\w+)\s+(\w+)'  # 第一个分组不捕获
    matches = re.findall(pattern, text)
    print(f"  结果: {matches}")


def demo_assertions():
    """断言"""
    print("\n" + "=" * 50)
    print("5. 断言")
    print("=" * 50)
    
    # 边界匹配
    text = "cat catch concatenate"
    print(f"文本: '{text}'")
    
    print(f"  r'\\bcat\\b' (单词边界): {re.findall(r'\\bcat\\b', text)}")
    print(f"  r'cat' (无边界): {re.findall(r'cat', text)}")
    print(f"  r'^cat' (开头): {re.findall(r'^cat', text)}")
    
    # 前瞻和后顾
    text = "100USD 200EUR 300USD"
    print(f"\n文本: '{text}'")
    
    # 正向前瞻 - 后面跟着USD的数字
    print(f"  正向前瞻 r'\\d+(?=USD)': {re.findall(r'\\d+(?=USD)', text)}")
    
    # 负向前瞻 - 后面不跟USD的数字
    print(f"  负向前瞻 r'\\d+(?!USD)': {re.findall(r'\\d+(?!USD)', text)}")
    
    # 正向后顾 - 前面是$的数字
    text = "$100 200 $300"
    print(f"\n文本: '{text}'")
    print(f"  正向后顾 r'(?<=\\$)\\d+': {re.findall(r'(?<=\\$)\\d+', text)}")


def demo_flags():
    """标志位"""
    print("\n" + "=" * 50)
    print("6. 标志位")
    print("=" * 50)
    
    text = "Hello\nHELLO\nhello"
    print(f"文本: {repr(text)}")
    
    # 忽略大小写
    print(f"  无标志 r'hello': {re.findall(r'hello', text)}")
    print(f"  re.IGNORECASE: {re.findall(r'hello', text, re.IGNORECASE)}")
    
    # 多行模式
    print(f"  re.MULTILINE r'^h': {re.findall(r'^h', text, re.MULTILINE | re.IGNORECASE)}")
    
    # 点匹配换行
    print(f"  re.DOTALL r'H.*o': {re.findall(r'H.*o', text, re.DOTALL | re.IGNORECASE)}")


def demo_practical_examples():
    """实用示例"""
    print("\n" + "=" * 50)
    print("7. 实用示例")
    print("=" * 50)
    
    # 邮箱验证
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    emails = ["test@example.com", "invalid-email", "user@domain.co.uk"]
    print("邮箱验证:")
    for email in emails:
        is_valid = bool(re.match(email_pattern, email))
        print(f"  {email}: {'有效' if is_valid else '无效'}")
    
    # 手机号提取
    phone_pattern = r'1[3-9]\d{9}'
    text = "联系电话: 13812345678, 备用: 15987654321"
    phones = re.findall(phone_pattern, text)
    print(f"\n手机号提取: {phones}")
    
    # URL提取
    url_pattern = r'https?://[^\s]+'
    text = "访问 https://example.com 或 http://test.org/page 获取更多信息"
    urls = re.findall(url_pattern, text)
    print(f"\nURL提取: {urls}")
    
    # 日期提取
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    text = "会议日期: 2024-01-15, 截止日期: 2024-02-28"
    dates = re.findall(date_pattern, text)
    print(f"\n日期提取: {dates}")
    
    # HTML标签清理
    html = "<p>Hello <b>World</b></p>"
    clean_text = re.sub(r'<[^>]+>', '', html)
    print(f"\nHTML清理: '{html}' -> '{clean_text}'")


def demo_compile():
    """预编译正则"""
    print("\n" + "=" * 50)
    print("8. 预编译正则")
    print("=" * 50)
    
    # 预编译提高重复使用效率
    email_re = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    
    emails = ["a@b.com", "test@example.org", "invalid"]
    print("预编译正则验证邮箱:")
    for email in emails:
        is_valid = bool(email_re.match(email))
        print(f"  {email}: {'有效' if is_valid else '无效'}")
    
    # 编译时可以包含标志
    pattern = re.compile(r'hello', re.IGNORECASE)
    print(f"\n预编译(忽略大小写): {pattern.findall('Hello HELLO hello')}")


if __name__ == "__main__":
    demo_basic_patterns()
    demo_special_characters()
    demo_quantifiers()
    demo_groups()
    demo_assertions()
    demo_flags()
    demo_practical_examples()
    demo_compile()
    print("\n[OK] 正则表达式演示完成!")
