"""
输出格式化工具模块

提供CLI输出的格式化功能。
"""

from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box


console = Console()


def print_success(message: str):
    """打印成功消息"""
    console.print(f"[green][OK][/green] {message}")


def print_error(message: str):
    """打印错误消息"""
    console.print(f"[red][X][/red] {message}", style="red")


def print_warning(message: str):
    """打印警告消息"""
    console.print(f"[yellow][!][/yellow] {message}", style="yellow")


def print_info(message: str):
    """打印信息消息"""
    console.print(f"[blue][i][/blue] {message}", style="blue")


def print_demo_result(demo_info: Dict[str, Any]):
    """
    打印demo生成结果

    Args:
        demo_info: demo信息字典,包含language, topic, path, files, verified等
    """
    console.print("\n[green][OK] Demo生成成功![/green]\n")

    # 基本信息
    console.print(f"[bold]语言:[/bold] {demo_info.get('language', 'N/A')}")
    console.print(f"[bold]主题:[/bold] {demo_info.get('topic', 'N/A')}")
    console.print(f"[bold]输出位置:[/bold] {demo_info.get('path', 'N/A')}")

    # 文件列表
    files = demo_info.get("files", [])
    if files:
        console.print("\n[bold]包含文件:[/bold]")
        for file_info in files:
            filename = file_info.get("name", "")
            description = file_info.get("description", "")
            console.print(f"  - {filename:<30} ({description})")

    # 验证状态
    verified = demo_info.get("verified", False)
    exec_time = demo_info.get("execution_time", "N/A")
    if verified:
        console.print("\n[bold]验证状态:[/bold] [green][OK] 已验证通过[/green]")
        console.print(f"[bold]执行时间:[/bold] {exec_time}")
    else:
        console.print("\n[bold]验证状态:[/bold] [yellow]未启用验证[/yellow]")

    # 快速开始
    quick_start = demo_info.get("quick_start", [])
    if quick_start:
        console.print("\n[bold]快速开始:[/bold]")
        for i, step in enumerate(quick_start, 1):
            console.print(f"  {i}. {step}")

    # 查看文档提示
    readme_path = demo_info.get("readme_path")
    if readme_path:
        console.print(f"\n[bold]查看完整指南:[/bold] cat {readme_path}")


def print_search_results(results: List[Dict[str, Any]], total: int = None):
    """
    打印搜索结果表格

    Args:
        results: 搜索结果列表
        total: 总结果数量
    """
    if not results:
        print_warning("未找到匹配的demo")
        return

    total_count = total if total is not None else len(results)
    console.print(f"\n找到 [bold]{total_count}[/bold] 个匹配的demo:\n")

    # 创建表格
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("#", style="dim", width=4)
    table.add_column("名称", min_width=20)
    table.add_column("语言", width=10)
    table.add_column("关键字", min_width=20)
    table.add_column("难度", width=12)

    for i, result in enumerate(results, 1):
        name = result.get("name", "N/A")
        language = result.get("language", "N/A")
        keywords = ", ".join(result.get("keywords", []))
        difficulty = result.get("difficulty", "N/A")

        # 难度颜色
        difficulty_style = {"beginner": "green", "intermediate": "yellow", "advanced": "red"}.get(
            difficulty.lower(), "white"
        )

        table.add_row(
            str(i),
            name,
            language,
            keywords,
            f"[{difficulty_style}]{difficulty}[/{difficulty_style}]",
        )

    console.print(table)
    console.print("\n使用 [bold]'opendemo get <语言> <关键字>'[/bold] 获取具体demo\n")


def print_config_list(config: Dict[str, Any]):
    """
    打印配置列表

    Args:
        config: 配置字典
    """
    console.print("\n[bold]当前配置:[/bold]\n")

    def print_config_dict(cfg: Dict[str, Any], prefix: str = ""):
        for key, value in cfg.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                print_config_dict(value, full_key)
            else:
                # 隐藏敏感信息
                if "key" in key.lower() or "password" in key.lower():
                    if value:
                        value = "*" * 8
                console.print(f"  {full_key:<30} = {value}")

    print_config_dict(config)
    console.print()


def print_panel(content: str, title: str = None, style: str = "blue"):
    """
    打印面板

    Args:
        content: 内容
        title: 标题
        style: 样式
    """
    panel = Panel(content, title=title, border_style=style)
    console.print(panel)


def print_markdown(content: str):
    """
    打印markdown内容

    Args:
        content: markdown文本
    """
    md = Markdown(content)
    console.print(md)


def print_progress(message: str):
    """
    打印进度消息

    Args:
        message: 消息内容
    """
    console.print(f"[cyan]>>>[/cyan] {message}...", style="cyan")


def print_library_info(library_info: Dict[str, Any]):
    """
    打印库信息和功能列表

    Args:
        library_info: 库信息字典，包含 metadata 和 features
    """
    metadata = library_info.get("metadata", {})
    features = library_info.get("features", [])

    # 打印库头部信息
    display_name = metadata.get("display_name", metadata.get("name", "Unknown"))
    description = metadata.get("description", "")
    version = metadata.get("version", "")
    install_cmd = metadata.get("install_command", "")
    official_url = metadata.get("official_url", "")

    console.print(f"\n📚 [bold cyan]{display_name}[/bold cyan] - {description}")
    if version:
        console.print(f"版本：{version}")
    if install_cmd:
        console.print(f"安装：[yellow]{install_cmd}[/yellow]")
    if official_url:
        console.print(f"文档：[link]{official_url}[/link]")

    console.print("\n[bold]功能模块列表：[/bold]\n")

    # 按分类分组
    categories_dict = {}
    for feature in features:
        category = feature.get("category", "未分类")
        if category not in categories_dict:
            categories_dict[category] = []
        categories_dict[category].append(feature)

    # 按分类展示
    index = 1
    for category, category_features in sorted(categories_dict.items()):
        console.print(f"【{category}】")
        for feature in sorted(category_features, key=lambda x: x["name"]):
            name = feature["name"]
            title = feature.get("title", name)
            description = feature.get("description", "")
            difficulty = feature.get("difficulty", "beginner")

            # 难度颜色
            difficulty_style = {
                "beginner": "green",
                "intermediate": "yellow",
                "advanced": "red",
            }.get(difficulty.lower(), "white")

            difficulty_text = f"[{difficulty_style}]({difficulty})[/{difficulty_style}]"
            console.print(f"  {index}. [bold]{name}[/bold]  {title} {difficulty_text}")
            if description:
                console.print(f"     {description}")
            index += 1
        console.print()

    # 提示信息
    library_name = metadata.get("name", "")
    console.print("[bold]提示：[/bold]")
    console.print(f"  - 获取具体功能：opendemo get python {library_name} <功能名>")
    console.print(f"  - 搜索相关功能：opendemo get python {library_name} <关键字>")
    console.print(f"  - 查看全部：opendemo search python {library_name}")
    console.print()
