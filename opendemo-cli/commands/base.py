"""
OpenDemo CLI 公共函数模块

包含所有命令模块共享的辅助函数。
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# 导入工具函数
from utils.formatters import (
    print_success,
    print_error,
    print_warning,
    print_info,
    print_progress,
    print_demo_result,
)
from utils.logger import get_logger
from core.readme_updater import ReadmeUpdater
from core.demo_list_updater import DemoListUpdater

# 常量定义
SUPPORTED_LANGUAGES = ["python", "java", "go", "nodejs", "kubernetes", "database", "networking", "kvm", "virtualization", "sre", "security"]
README_PATH = Path(__file__).parent.parent.parent / "README.md"
DEMO_LIST_PATH = Path(__file__).parent.parent.parent / "demo-list.md"


def scan_output_demos(output_dir: Path, language: str) -> List[Dict[str, Any]]:
    """
    扫描输出目录中的demo

    Args:
        output_dir: 输出目录路径
        language: 语言名称

    Returns:
        demo信息列表
    """
    demos = []
    lang_dir = output_dir / language.lower()

    if not lang_dir.exists():
        return demos

    for item in lang_dir.iterdir():
        if item.is_dir():
            # 尝试读取metadata.json
            metadata_file = item / "metadata.json"
            if metadata_file.exists():
                try:
                    with open(metadata_file, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                    demos.append(
                        {
                            "path": item,
                            "name": item.name,
                            "language": metadata.get("language", language),
                            "keywords": metadata.get("keywords", []),
                            "description": metadata.get("description", ""),
                            "difficulty": metadata.get("difficulty", "beginner"),
                            "verified": metadata.get("verified", False),
                            "metadata": metadata,
                        }
                    )
                except Exception:
                    # 即使没有metadata，也列出目录
                    demos.append(
                        {
                            "path": item,
                            "name": item.name,
                            "language": language,
                            "keywords": [],
                            "description": "",
                            "difficulty": "unknown",
                            "verified": False,
                            "metadata": {},
                        }
                    )
            else:
                # 目录存在但没有metadata，也列出
                demos.append(
                    {
                        "path": item,
                        "name": item.name,
                        "language": language,
                        "keywords": [],
                        "description": "",
                        "difficulty": "unknown",
                        "verified": False,
                        "metadata": {},
                    }
                )

    return demos


def match_demo_in_output(
    output_dir: Path, language: str, keywords: List[str]
) -> Optional[Dict[str, Any]]:
    """
    在输出目录中匹配demo

    优先级:
    1. 精确匹配文件夹名称
    2. 文件夹名称包含关键字
    3. 关键字在metadata的keywords中

    Args:
        output_dir: 输出目录路径
        language: 语言名称
        keywords: 搜索关键字

    Returns:
        匹配的demo信息，未找到返回None
    """
    demos = scan_output_demos(output_dir, language)
    if not demos:
        return None

    # 合并关键字用于匹配
    search_term = "-".join(kw.lower() for kw in keywords)
    search_term_single = keywords[0].lower() if keywords else ""

    # 1. 精确匹配文件夹名称
    for demo in demos:
        folder_name = demo["name"].lower()
        if folder_name == search_term or folder_name == search_term_single:
            return demo

    # 2. 文件夹名称包含任一关键字
    best_match = None
    best_score = 0

    for demo in demos:
        folder_name = demo["name"].lower()
        score = 0

        for keyword in keywords:
            kw_lower = keyword.lower()
            if kw_lower in folder_name:
                score += 10
            # 检查metadata中的keywords
            if any(kw_lower in mk.lower() for mk in demo.get("keywords", [])):
                score += 5

        if score > best_score:
            best_score = score
            best_match = demo

    if best_score > 0:
        return best_match

    return None


def update_demo_list(storage, demo_list_path: Path = DEMO_LIST_PATH) -> None:
    """
    更新 demo-list.md 文件

    Args:
        storage: 存储服务
        demo_list_path: demo列表文件路径
    """
    logger = get_logger(__name__)

    try:
        output_dir = storage.get_output_directory()
        updater = DemoListUpdater(output_dir, demo_list_path)
        success = updater.update()

        if success:
            summary = updater.get_summary()
            print_info(f"demo-list.md 已更新 ({summary})")
        else:
            print_warning("更新 demo-list.md 失败")

    except Exception as e:
        logger.error(f"Failed to update demo-list.md: {e}")
        print_warning(f"更新 demo-list.md 失败: {e}")


def display_output_demo(demo_info: Dict[str, Any], demo_path: Path, language: str) -> None:
    """显示输出目录中的demo信息"""
    from rich.console import Console

    console = Console()

    print_success("Demo已存在!")
    console.print(f"\n[bold]名称:[/bold] {demo_info['name']}")
    console.print(f"[bold]语言:[/bold] {language}")
    console.print(f"[bold]路径:[/bold] {demo_path}")

    if demo_info.get("keywords"):
        console.print(f"[bold]关键字:[/bold] {', '.join(demo_info['keywords'])}")

    if demo_info.get("description"):
        console.print(f"[bold]描述:[/bold] {demo_info['description']}")

    # 列出文件
    console.print("\n[bold]包含文件:[/bold]")
    code_dir = demo_path / "code"
    if code_dir.exists():
        for f in code_dir.iterdir():
            if f.is_file():
                console.print(f"  - code/{f.name}")

    # 快速开始
    console.print("\n[bold]快速开始:[/bold]")
    console.print(f"  1. cd {demo_path}")
    if language.lower() == "python":
        code_files = list(code_dir.glob("*.py")) if code_dir.exists() else []
        if code_files:
            console.print(f"  2. python code/{code_files[0].name}")

    console.print(f"\n[bold]如需重新生成:[/bold] opendemo get {language} {demo_info['name']} new")


def verify_demo(demo, verifier, language, repository) -> None:
    """验证demo"""
    print_progress("验证demo可执行性")
    verification_result = verifier.verify(demo.path, language)

    if verification_result.get("verified"):
        print_success("验证通过")
        # 更新元数据
        repository.update_metadata(demo, {"verified": True})
    elif verification_result.get("skipped"):
        print_warning(verification_result.get("message", "验证已跳过"))
    else:
        print_warning("验证未通过")
        errors = verification_result.get("errors", [])
        for error in errors:
            print_error(f"  - {error}")


def display_demo_result(demo, output_path, repository, verify, verifier, language) -> None:
    """显示demo结果"""
    files = repository.get_demo_files(demo)

    # 生成快速开始步骤
    quick_start = [
        f"cd {output_path}",
    ]

    # 根据语言添加特定步骤
    if language.lower() == "python":
        if (output_path / "requirements.txt").exists():
            quick_start.append("pip install -r requirements.txt")

        # 找到第一个Python文件
        code_files = (
            list((output_path / "code").glob("*.py")) if (output_path / "code").exists() else []
        )
        if code_files:
            quick_start.append(f"python code/{code_files[0].name}")
    elif language.lower() == "java":
        quick_start.append("# 根据项目类型使用Maven或Gradle构建")

    # 准备显示信息
    demo_info = {
        "language": demo.language,
        "topic": demo.name,
        "path": str(output_path),
        "files": files,
        "verified": demo.verified,
        "execution_time": "N/A",
        "quick_start": quick_start,
        "readme_path": str(output_path / "README.md"),
    }

    print_demo_result(demo_info)


def handle_library_command(
    library_command: Dict[str, Any],
    repository,
    search,
    storage,
    verify: bool,
    verifier,
    language: str,
) -> None:
    """
    处理库命令

    Args:
        library_command: 库命令信息
        repository: Demo仓库
        search: 搜索引擎
        storage: 存储服务
        verify: 是否验证
        verifier: 验证器
        language: 编程语言
    """
    library_name = library_command["library"]
    feature_keywords = library_command["feature_keywords"]

    # 如果没有功能关键字，展示库的功能列表
    if not feature_keywords:
        library_info = repository.get_library_info(language, library_name)
        if library_info:
            from utils.formatters import print_library_info
            print_library_info(library_info)
        else:
            print_error(f"未找到库 {library_name} 的信息")
            sys.exit(1)
        return

    # 如果有功能关键字，搜索并匹配功能
    feature_keyword = feature_keywords[0]  # 使用第一个关键字

    # 先尝试精确匹配
    feature_demo = repository.get_library_demo(language, library_name, feature_keyword)

    if feature_demo:
        # 找到精确匹配的功能 demo
        print_success(f"在库 {library_name} 中找到功能: {feature_keyword}")

        # 复制到输出目录
        output_path = repository.copy_library_feature_to_output(
            language, library_name, feature_keyword
        )

        if output_path:
            display_demo_result(feature_demo, output_path, repository, verify, verifier, language)
        else:
            print_error("复制demo失败")
            sys.exit(1)
        return

    # 没有精确匹配，尝试模糊搜索
    search_results = search.search_library_features(language, library_name, feature_keyword)

    if search_results:
        # 显示搜索结果
        if len(search_results) == 1:
            # 只有一个结果，直接获取
            feature_info, score = search_results[0]
            feature_name = feature_info["name"]

            print_success(f"在库 {library_name} 中找到匹配的功能: {feature_name}")

            feature_demo = repository.get_library_demo(language, library_name, feature_name)
            if feature_demo:
                output_path = repository.copy_library_feature_to_output(
                    language, library_name, feature_name
                )
                if output_path:
                    display_demo_result(
                        feature_demo, output_path, repository, verify, verifier, language
                    )
                else:
                    print_error("复制demo失败")
                    sys.exit(1)
            else:
                print_error(f"未找到功能 {feature_name} 的demo")
                sys.exit(1)
        else:
            # 多个结果，展示列表让用户选择
            print_info(f"在库 {library_name} 中找到 {len(search_results)} 个相关功能：\n")

            from rich.console import Console
            from rich.table import Table
            from rich import box

            console = Console()
            table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
            table.add_column("#", style="dim", width=4)
            table.add_column("功能名称", min_width=20)
            table.add_column("标题", min_width=15)
            table.add_column("描述", min_width=30)
            table.add_column("难度", width=12)

            for i, (feature_info, score) in enumerate(search_results[:10], 1):
                name = feature_info["name"]
                title = feature_info.get("title", name)
                description = feature_info.get("description", "")
                difficulty = feature_info.get("difficulty", "beginner")

                difficulty_style = {
                    "beginner": "green",
                    "intermediate": "yellow",
                    "advanced": "red",
                }.get(difficulty.lower(), "white")

                table.add_row(
                    str(i),
                    name,
                    title,
                    description[:50] + "..." if len(description) > 50 else description,
                    f"[{difficulty_style}]{difficulty}[/{difficulty_style}]",
                )

            console.print(table)
            console.print(
                f"\n使用 [bold]'opendemo get python {library_name} <功能名称>'[/bold] 获取具体功能\n"
            )
    else:
        print_warning(f"在库 {library_name} 中未找到匹配 '{feature_keyword}' 的功能")
        print_info(f"使用 'opendemo get python {library_name}' 查看所有可用功能")
        sys.exit(1)


def update_readme_after_new(
    storage, language: str, demo_name: str, library_name: Optional[str] = None
) -> None:
    """
    在生成新demo后更新README.md

    Args:
        storage: 存储服务
        language: 编程语言
        demo_name: demo名称
        library_name: 第三方库名称（如果是库demo）
    """
    logger = get_logger(__name__)

    if not README_PATH.exists():
        logger.warning(f"README.md not found at {README_PATH}")
        return

    try:
        output_dir = storage.get_output_directory()

        # 使用ReadmeUpdater模块更新README
        updater = ReadmeUpdater(output_dir, README_PATH)
        success = updater.update()

        if success:
            summary = updater.get_summary()
            print_info(f"README.md 已更新 ({summary})")
        else:
            print_warning("更新README.md失败")

    except Exception as e:
        logger.error(f"Failed to update README.md: {e}")
        print_warning(f"更新README.md失败: {e}")

    # 2. 更新STATUS.md
    status_path = README_PATH.parent / "STATUS.md"
    if status_path.exists():
        try:
            update_status_md(output_dir, status_path)
            print_info("STATUS.md 已更新")
        except Exception as e:
            logger.error(f"Failed to update STATUS.md: {e}")
            print_warning(f"更新STATUS.md失败: {e}")


def update_status_md(output_dir: Path, status_path: Path) -> None:
    """更新STATUS.md中的Demo统计"""
    updater = ReadmeUpdater(output_dir, status_path.parent / "README.md")
    stats = updater.collect_stats()
    totals = updater.calculate_totals(stats)

    with open(status_path, "r", encoding="utf-8") as f:
        content = f.read()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = re.sub(
        r"\*\*检查时间\*\*: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", f"**检查时间**: {now}", content
    )

    lang_map = {"python": "Python", "go": "Go", "nodejs": "Node.js", "kubernetes": "Kubernetes"}
    for lang, name in lang_map.items():
        data = stats.get(lang, {"base": 0, "libraries": {}, "tools": {}})
        total = (
            data.get("base", 0)
            + sum(data.get("libraries", {}).values())
            + sum(data.get("tools", {}).values())
        )
        pattern = rf"\| {name} \| \d+ \|"
        replacement = f"| {name} | {total} |"
        content = re.sub(pattern, replacement, content)

    content = re.sub(
        r"\| \*\*总计\*\* \| \*\*\d+\*\* \|", f"| **总计** | **{totals['grand_total']}** |", content
    )
