"""
search 命令模块

搜索demo的命令实现。
"""

import sys

import click
from rich.console import Console
from rich.table import Table
from rich import box

from services.config_service import ConfigService
from services.storage_service import StorageService
from core.demo_repository import DemoRepository
from core.demo_search import DemoSearch
from utils.formatters import print_info, print_error
from .base import SUPPORTED_LANGUAGES, scan_output_demos


@click.command()
@click.argument("language", required=False)
@click.argument("keywords", nargs=-1)
def search(language, keywords):
    """搜索demo

    示例:
        opendemo search python          # 列出所有python demo
        opendemo search python logging  # 搜索python logging相关demo
        opendemo search                 # 列出所有demo
    """
    # 初始化服务
    config = ConfigService()
    storage = StorageService(config)
    repository = DemoRepository(storage, config)
    demo_search = DemoSearch(repository)

    console = Console()

    # 如果没有指定语言，显示所有语言统计
    if not language:
        print_info("所有可用demo：\n")

        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("语言", style="cyan", min_width=12)
        table.add_column("Demo数量", justify="right", width=10)
        table.add_column("说明", min_width=30)

        lang_info = {
            "python": "Python基础语法和标准库",
            "go": "Go语言核心功能",
            "nodejs": "Node.js/JavaScript",
            "java": "Java基础语法",
            "kubernetes": "Kubernetes部署配置",
        }

        for lang in SUPPORTED_LANGUAGES:
            # 计算该语言的demo数量
            output_dir = storage.get_output_directory()
            demos = scan_output_demos(output_dir, lang)
            count = len(demos)

            table.add_row(lang, str(count), lang_info.get(lang, ""))

        console.print(table)
        console.print("\n使用 [bold]'opendemo search <语言> [关键字]'[/bold] 搜索特定demo\n")
        return

    # 验证语言
    if language.lower() not in SUPPORTED_LANGUAGES:
        print_error(f"不支持的语言: {language}")
        return

    # 搜索demo
    results = demo_search.search_demos(
        language=language, keywords=list(keywords) if keywords else None
    )

    if not results:
        print_info(f"未找到匹配的demo")
        return

    # 显示结果
    print_info(f"找到 {len(results)} 个demo：\n")

    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("#", style="dim", width=4)
    table.add_column("名称", min_width=20)
    table.add_column("标题", min_width=15)
    table.add_column("描述", min_width=30)
    table.add_column("难度", width=12)

    for i, demo in enumerate(results[:20], 1):  # 最多显示20个
        difficulty_style = {
            "beginner": "green",
            "intermediate": "yellow",
            "advanced": "red",
        }.get(demo.difficulty.lower(), "white")

        table.add_row(
            str(i),
            demo.name,
            demo.title or demo.name,
            (demo.description or "")[:50] + "..."
            if len(demo.description or "") > 50
            else (demo.description or ""),
            f"[{difficulty_style}]{demo.difficulty}[/{difficulty_style}]",
        )

    console.print(table)
    console.print(f"\n使用 [bold]'opendemo get {language} <demo名称>'[/bold] 获取demo\n")
