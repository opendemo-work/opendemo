#!/usr/bin/env python
"""
Open Demo CLI 快速启动脚本
"""

import sys
import subprocess


def main():
    """主函数"""
    print("=" * 60)
    print(" Open Demo CLI - 智能化的编程学习辅助CLI工具")
    print("=" * 60)
    print()
    
    # 检查是否已安装
    try:
        import opendemo
        print("✓ Open Demo CLI 已安装")
        print(f"  版本: {opendemo.__version__}")
        print()
    except ImportError:
        print("✗ Open Demo CLI 未安装")
        print()
        install = input("是否立即安装? (y/n): ").strip().lower()
        
        if install in ('y', 'yes', '是'):
            print("\n正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."])
            print("\n✓ 安装完成!")
        else:
            print("\n请先运行: pip install -e .")
            return
    
    # 显示菜单
    while True:
        print("\n" + "=" * 60)
        print("请选择操作:")
        print("  1. 搜索demo")
        print("  2. 获取demo")
        print("  3. 创建新demo")
        print("  4. 配置管理")
        print("  5. 查看帮助")
        print("  0. 退出")
        print("=" * 60)
        
        choice = input("\n请输入选项 (0-5): ").strip()
        
        if choice == '0':
            print("\n再见!")
            break
        elif choice == '1':
            language = input("输入语言 (如 python): ").strip()
            keywords = input("输入关键字 (可选,空格分隔): ").strip()
            
            cmd = ["python", "-m", "opendemo.cli", "search", language]
            if keywords:
                cmd.extend(keywords.split())
            subprocess.run(cmd)
            
        elif choice == '2':
            language = input("输入语言 (如 python): ").strip()
            topic = input("输入主题 (如 元组): ").strip()
            verify = input("是否启用验证? (y/n): ").strip().lower()
            
            cmd = ["python", "-m", "opendemo.cli", "get", language, topic]
            if verify in ('y', 'yes', '是'):
                cmd.append("--verify")
            subprocess.run(cmd)
            
        elif choice == '3':
            language = input("输入语言 (如 python): ").strip()
            topic = input("输入主题 (如 装饰器): ").strip()
            difficulty = input("难度级别 (beginner/intermediate/advanced, 默认beginner): ").strip()
            verify = input("是否启用验证? (y/n): ").strip().lower()
            
            cmd = ["python", "-m", "opendemo.cli", "new", language, topic]
            if difficulty:
                cmd.extend(["--difficulty", difficulty])
            if verify in ('y', 'yes', '是'):
                cmd.append("--verify")
            subprocess.run(cmd)
            
        elif choice == '4':
            print("\n配置操作:")
            print("  1. 初始化配置")
            print("  2. 设置API密钥")
            print("  3. 查看所有配置")
            print("  4. 返回")
            
            config_choice = input("\n请选择 (1-4): ").strip()
            
            if config_choice == '1':
                subprocess.run(["python", "-m", "opendemo.cli", "config", "init"])
            elif config_choice == '2':
                api_key = input("输入API密钥: ").strip()
                subprocess.run(["python", "-m", "opendemo.cli", "config", "set", "ai.api_key", api_key])
            elif config_choice == '3':
                subprocess.run(["python", "-m", "opendemo.cli", "config", "list"])
            
        elif choice == '5':
            subprocess.run(["python", "-m", "opendemo.cli", "--help"])
        else:
            print("\n无效选项,请重试")
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)
