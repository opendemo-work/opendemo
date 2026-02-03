#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python命令行工具演示
展示argparse模块的常用功能
"""
import argparse
import sys


def demo_basic_argparse():
    """基础argparse使用"""
    print("=" * 50)
    print("1. 基础argparse使用")
    print("=" * 50)
    
    # 创建解析器
    parser = argparse.ArgumentParser(
        description='文件处理工具',
        epilog='示例: python cli.py input.txt -o output.txt'
    )
    
    # 位置参数
    parser.add_argument('filename', help='输入文件名')
    
    # 可选参数
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    
    # 模拟命令行参数
    args = parser.parse_args(['input.txt', '-o', 'output.txt', '-v'])
    
    print(f"解析结果:")
    print(f"  filename: {args.filename}")
    print(f"  output: {args.output}")
    print(f"  verbose: {args.verbose}")
    
    # 显示帮助信息
    print(f"\n帮助信息预览:")
    parser.print_help()


def demo_argument_types():
    """参数类型"""
    print("\n" + "=" * 50)
    print("2. 参数类型")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description='参数类型演示')
    
    # 字符串(默认)
    parser.add_argument('--name', type=str, help='名称')
    
    # 整数
    parser.add_argument('--count', type=int, default=10, help='数量')
    
    # 浮点数
    parser.add_argument('--rate', type=float, default=0.1, help='比率')
    
    # 布尔标志
    parser.add_argument('--debug', action='store_true', help='调试模式')
    parser.add_argument('--no-cache', action='store_false', dest='cache', help='禁用缓存')
    
    # 选项(choices)
    parser.add_argument('--level', choices=['debug', 'info', 'error'], 
                       default='info', help='日志级别')
    
    # 多值参数(nargs)
    parser.add_argument('--files', nargs='+', help='多个文件')
    parser.add_argument('--range', nargs=2, type=int, metavar=('START', 'END'),
                       help='范围')
    
    # 模拟解析
    args = parser.parse_args([
        '--name', 'test',
        '--count', '20',
        '--debug',
        '--level', 'error',
        '--files', 'a.txt', 'b.txt', 'c.txt',
        '--range', '1', '100'
    ])
    
    print(f"解析结果:")
    print(f"  name: {args.name}")
    print(f"  count: {args.count} (type: {type(args.count).__name__})")
    print(f"  rate: {args.rate}")
    print(f"  debug: {args.debug}")
    print(f"  cache: {args.cache}")
    print(f"  level: {args.level}")
    print(f"  files: {args.files}")
    print(f"  range: {args.range}")


def demo_subcommands():
    """子命令"""
    print("\n" + "=" * 50)
    print("3. 子命令")
    print("=" * 50)
    
    # 主解析器
    parser = argparse.ArgumentParser(description='用户管理工具')
    parser.add_argument('--verbose', '-v', action='store_true')
    
    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # list命令
    list_parser = subparsers.add_parser('list', help='列出用户')
    list_parser.add_argument('--limit', type=int, default=10)
    
    # add命令
    add_parser = subparsers.add_parser('add', help='添加用户')
    add_parser.add_argument('name', help='用户名')
    add_parser.add_argument('--email', required=True, help='邮箱')
    
    # delete命令
    del_parser = subparsers.add_parser('delete', help='删除用户')
    del_parser.add_argument('user_id', type=int, help='用户ID')
    del_parser.add_argument('--force', action='store_true')
    
    # 模拟不同命令
    print("解析 'list --limit 20':")
    args = parser.parse_args(['list', '--limit', '20'])
    print(f"  command: {args.command}, limit: {args.limit}")
    
    print("\n解析 'add alice --email alice@example.com':")
    args = parser.parse_args(['add', 'alice', '--email', 'alice@example.com'])
    print(f"  command: {args.command}, name: {args.name}, email: {args.email}")
    
    print("\n解析 'delete 123 --force':")
    args = parser.parse_args(['delete', '123', '--force'])
    print(f"  command: {args.command}, user_id: {args.user_id}, force: {args.force}")


def demo_argument_groups():
    """参数分组"""
    print("\n" + "=" * 50)
    print("4. 参数分组")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description='数据库工具')
    
    # 数据库连接参数组
    db_group = parser.add_argument_group('数据库连接')
    db_group.add_argument('--host', default='localhost', help='主机地址')
    db_group.add_argument('--port', type=int, default=5432, help='端口')
    db_group.add_argument('--database', required=True, help='数据库名')
    
    # 认证参数组
    auth_group = parser.add_argument_group('认证信息')
    auth_group.add_argument('--user', default='postgres', help='用户名')
    auth_group.add_argument('--password', help='密码')
    
    # 互斥参数组
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('--json', action='store_true', help='JSON输出')
    output_group.add_argument('--csv', action='store_true', help='CSV输出')
    output_group.add_argument('--table', action='store_true', help='表格输出')
    
    print("帮助信息(显示分组):")
    parser.print_help()
    
    print("\n解析结果:")
    args = parser.parse_args(['--database', 'mydb', '--json'])
    print(f"  host: {args.host}")
    print(f"  database: {args.database}")
    print(f"  json: {args.json}")


def demo_custom_actions():
    """自定义动作"""
    print("\n" + "=" * 50)
    print("5. 自定义动作和验证")
    print("=" * 50)
    
    # 自定义类型验证
    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} 必须是正整数")
        return ivalue
    
    def valid_file(path):
        import os
        if not path.endswith(('.txt', '.json', '.csv')):
            raise argparse.ArgumentTypeError(f"不支持的文件类型: {path}")
        return path
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=positive_int, help='正整数')
    parser.add_argument('--file', type=valid_file, help='文件路径')
    
    print("验证正整数:")
    try:
        args = parser.parse_args(['--count', '10'])
        print(f"  --count 10: 通过, 值={args.count}")
    except SystemExit:
        pass
    
    print("\n验证文件类型:")
    try:
        args = parser.parse_args(['--file', 'data.json'])
        print(f"  --file data.json: 通过")
    except SystemExit:
        pass


def demo_complete_cli():
    """完整CLI示例"""
    print("\n" + "=" * 50)
    print("6. 完整CLI工具模板")
    print("=" * 50)
    
    template = '''
#!/usr/bin/env python3
"""我的CLI工具"""
import argparse
import sys

def cmd_list(args):
    """列表命令处理"""
    print(f"列出数据, limit={args.limit}")

def cmd_add(args):
    """添加命令处理"""
    print(f"添加: {args.name}")

def cmd_delete(args):
    """删除命令处理"""
    if args.force or input("确认删除? [y/N]: ").lower() == 'y':
        print(f"删除: {args.id}")

def main():
    parser = argparse.ArgumentParser(
        prog='mytool',
        description='我的CLI工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  mytool list --limit 20
  mytool add "新项目"
  mytool delete 123 --force
        """
    )
    parser.add_argument('--version', action='version', version='1.0.0')
    parser.add_argument('-v', '--verbose', action='store_true')
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # list子命令
    p_list = subparsers.add_parser('list', help='列出项目')
    p_list.add_argument('--limit', type=int, default=10)
    p_list.set_defaults(func=cmd_list)
    
    # add子命令
    p_add = subparsers.add_parser('add', help='添加项目')
    p_add.add_argument('name', help='项目名称')
    p_add.set_defaults(func=cmd_add)
    
    # delete子命令
    p_del = subparsers.add_parser('delete', help='删除项目')
    p_del.add_argument('id', type=int, help='项目ID')
    p_del.add_argument('-f', '--force', action='store_true')
    p_del.set_defaults(func=cmd_delete)
    
    args = parser.parse_args()
    args.func(args)  # 调用对应的处理函数

if __name__ == '__main__':
    main()
'''
    print(template)


if __name__ == "__main__":
    demo_basic_argparse()
    demo_argument_types()
    demo_subcommands()
    demo_argument_groups()
    demo_custom_actions()
    demo_complete_cli()
    print("\n[OK] 命令行工具演示完成!")

