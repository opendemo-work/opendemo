#!/usr/bin/env python3
"""
OpenDemo CLI 入口

命令行接口主入口，负责注册所有子命令。
"""

import sys
from pathlib import Path

import click

# 添加包路径
sys.path.insert(0, str(Path(__file__).parent))

from commands.get import get
from commands.search import search
from commands.new import new
from commands.config import config
from commands.check import check
from utils.logger import setup_logger
from utils.formatters import print_error, print_warning

__version__ = "0.3.0"


@click.group()
@click.version_option(version=__version__, prog_name="opendemo")
def cli():
    """Open Demo - 智能化的编程学习辅助CLI工具
    
    主要功能:
    - get: 获取已有demo或生成新demo
    - search: 搜索demo
    - new: 创建新demo
    - config: 配置管理
    - check: 运行质量检查
    
    示例:
        opendemo get python logging
        opendemo search python
        opendemo new go goroutines
        opendemo config set ai.api_key YOUR_KEY
    """
    # 初始化日志
    log_file = Path.home() / ".opendemo" / "logs" / "opendemo.log"
    setup_logger(log_file=str(log_file))


# 注册命令
cli.add_command(get)
cli.add_command(search)
cli.add_command(new)
cli.add_command(config)
cli.add_command(check)


def main():
    """主入口"""
    try:
        cli()
    except KeyboardInterrupt:
        print_warning("\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print_error(f"发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
