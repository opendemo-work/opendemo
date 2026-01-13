"""
CLI主程序

命令行接口实现。
"""

import sys
import json
import click
from pathlib import Path
from typing import List, Dict, Any, Optional

from opendemo.services.config_service import ConfigService
from opendemo.services.storage_service import StorageService
from opendemo.services.ai_service import AIService
from opendemo.core.demo_repository import DemoRepository
from opendemo.core.demo_search import DemoSearch
from opendemo.core.demo_generator import DemoGenerator
from opendemo.core.demo_verifier import DemoVerifier
from opendemo.core.readme_updater import ReadmeUpdater
from opendemo.core.quality_checker import QualityChecker
from opendemo.core.demo_list_updater import DemoListUpdater
from opendemo.utils.formatters import (
    print_success,
    print_error,
    print_warning,
    print_info,
    print_demo_result,
    print_search_results,
    print_config_list,
    print_progress,
    print_library_info,
)
from opendemo.utils.logger import setup_logger, get_logger

# 支持的语言列表
SUPPORTED_LANGUAGES = ["python", "java", "go", "nodejs", "kubernetes"]

# README.md路径
README_PATH = Path(__file__).parent.parent / "README.md"

# Demo列表文件路径
DEMO_LIST_PATH = Path(__file__).parent.parent / "demo-list.md"


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Open Demo - 智能化的编程学习辅助CLI工具"""
    # 初始化日志
    log_file = Path.home() / ".opendemo" / "logs" / "opendemo.log"
    setup_logger(log_file=str(log_file))


def _scan_output_demos(output_dir: Path, language: str) -> List[Dict[str, Any]]:
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


def _match_demo_in_output(
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
    demos = _scan_output_demos(output_dir, language)
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


def _update_demo_list(storage):
    """
    更新 demo-list.md 文件

    Args:
        storage: 存储服务
    """
    logger = get_logger(__name__)

    try:
        output_dir = storage.get_output_directory()
        updater = DemoListUpdater(output_dir, DEMO_LIST_PATH)
        success = updater.update()

        if success:
            summary = updater.get_summary()
            print_info(f"demo-list.md 已更新 ({summary})")
        else:
            print_warning("更新 demo-list.md 失败")

    except Exception as e:
        logger.error(f"Failed to update demo-list.md: {e}")
        print_warning(f"更新 demo-list.md 失败: {e}")


def _display_output_demo(demo_info: Dict[str, Any], demo_path: Path, language: str):
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


def _handle_library_command(
    library_command: Dict[str, Any],
    repository,
    search,
    storage,
    verify: bool,
    verifier,
    language: str,
):
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
            _display_demo_result(feature_demo, output_path, repository, verify, verifier, language)
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
                    _display_demo_result(
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


@cli.command()
@click.argument("language")
@click.argument("keywords", nargs=-1, required=True)
@click.option("--verify", is_flag=True, help="启用自动验证")
def get(language, keywords, verify):
    """获取demo代码

    示例:
        opendemo get python logging       # 匹配已有demo
        opendemo get python logging new   # 强制重新生成
        opendemo get python 列表 操作
        opendemo get java 继承 --verify
        opendemo get python numpy         # 显示numpy库的功能列表
        opendemo get python numpy array-creation  # 获取numpy库的array-creation功能demo
    """

    # 验证语言
    if language.lower() not in SUPPORTED_LANGUAGES:
        print_error(f"不支持的语言: {language}")
        print_info(f"当前支持的语言: {', '.join(SUPPORTED_LANGUAGES)}")
        sys.exit(1)

    # 初始化服务
    config = ConfigService()
    storage = StorageService(config)
    repository = DemoRepository(storage, config)
    search = DemoSearch(repository)
    ai_service = AIService(config)
    generator = DemoGenerator(ai_service, repository, config)
    verifier = DemoVerifier(config)

    # 检查是否为库命令
    keywords_list = list(keywords)
    library_command = repository.detect_library_command(language, keywords_list)

    if library_command:
        # 处理库命令
        _handle_library_command(
            library_command, repository, search, storage, verify, verifier, language
        )
        return

    # 原有的 demo 获取逻辑
    # 检查是否有 'new' 参数，表示强制重新生成
    force_new = False
    if keywords_list and keywords_list[-1].lower() == "new":
        force_new = True
        keywords_list = keywords_list[:-1]  # 移除 'new'

    if not keywords_list:
        print_error("请提供关键字")
        sys.exit(1)

    # 合并关键字
    topic = " ".join(keywords_list)

    # 获取输出目录
    output_dir = storage.get_output_directory()

    # 如果不是强制生成，先在输出目录中查找
    if not force_new:
        print_progress(f"搜索 {language} - {topic} 的demo")

        # 首先在 opendemo_output/<language>/ 目录中匹配
        matched_demo = _match_demo_in_output(output_dir, language, keywords_list)

        if matched_demo:
            demo_path = matched_demo["path"]
            print_success(f"在输出目录中找到匹配的demo: {matched_demo['name']}")

            # 显示demo信息
            _display_output_demo(matched_demo, demo_path, language)
            return

        # 在内置库和用户库中搜索
        results = search.search_demos(language=language, keywords=keywords_list)

        if results:
            demo = results[0]
            print_success(f"在本地库中找到匹配的demo: {demo.name}")

            # 复制到输出目录
            output_path = repository.copy_to_output(demo)

            if output_path:
                _display_demo_result(demo, output_path, repository, verify, verifier, language)
            else:
                print_error("复制demo失败")
                sys.exit(1)
            return

    # 未找到或强制生成,使用AI生成
    if force_new:
        print_info(f"强制重新生成: {topic}")
    else:
        print_warning("未找到匹配的demo")

    print_progress("使用AI生成demo")

    # 检查API密钥
    if not config.get("ai.api_key"):
        print_error("AI API密钥未配置")
        print_info("请运行: opendemo config set ai.api_key YOUR_KEY")
        sys.exit(1)

    # 如果是强制生成，生成新的文件夹名（带-new后缀）
    custom_name = None
    if force_new:
        base_name = "-".join(kw.lower() for kw in keywords_list)
        custom_name = f"{base_name}-new"
        # 检查是否已存在，如果存在则添加数字后缀
        lang_dir = output_dir / language.lower()
        if lang_dir.exists():
            suffix = 1
            while (lang_dir / custom_name).exists():
                custom_name = f"{base_name}-new{suffix}"
                suffix += 1

    # 生成demo
    result = generator.generate(
        language, topic, difficulty="beginner", custom_folder_name=custom_name
    )

    if not result:
        print_error("生成demo失败")
        sys.exit(1)

    demo = result["demo"]
    output_path = Path(result["path"])

    print_success("成功生成demo")

    # 验证(如果启用)
    if verify or config.get("enable_verification", False):
        _verify_demo(demo, verifier, language, repository)

    _display_demo_result(demo, output_path, repository, verify, verifier, language)

    # 更新 demo-list.md
    _update_demo_list(storage)


@cli.command()
@click.argument("language", required=False)
@click.argument("keywords", nargs=-1)
def search(language, keywords):
    """搜索demo

    示例:
        opendemo search python          # 列出所有python demo
        opendemo search python 数据结构  # 按关键字搜索
        opendemo search                 # 列出所有语言
    """
    # 初始化服务
    config = ConfigService()
    storage = StorageService(config)
    repository = DemoRepository(storage, config)

    # 获取输出目录
    output_dir = storage.get_output_directory()

    # 如果没有指定语言,列出所有语言
    if not language:
        print_info("可用的语言:")
        for lang in SUPPORTED_LANGUAGES:
            output_demos = _scan_output_demos(output_dir, lang)
            print(f"  - {lang}: {len(output_demos)} 个demo")

        print_info("\n使用 'opendemo search <语言>' 查看特定语言的demo")
        return

    # 验证语言
    if language.lower() not in SUPPORTED_LANGUAGES:
        print_error(f"不支持的语言: {language}")
        print_info(f"当前支持的语言: {', '.join(SUPPORTED_LANGUAGES)}")
        sys.exit(1)

    # 扫描输出目录中的demo
    output_demos = _scan_output_demos(output_dir, language)

    # 如果有关键字，进行过滤
    if keywords:
        keyword_list = [kw.lower() for kw in keywords]
        filtered_demos = []
        for demo in output_demos:
            folder_name = demo["name"].lower()
            # 检查文件夹名或keywords中是否包含搜索关键字
            match = any(kw in folder_name for kw in keyword_list)
            if not match:
                match = any(
                    kw in mk.lower() for kw in keyword_list for mk in demo.get("keywords", [])
                )
            if match:
                filtered_demos.append(demo)
        output_demos = filtered_demos

    # 按名称排序
    output_demos.sort(key=lambda x: x["name"])

    # 显示结果
    print_search_results(output_demos)


@cli.command()
@click.argument("language")
@click.argument("topic", nargs=-1, required=True)
@click.option(
    "--difficulty",
    type=click.Choice(["beginner", "intermediate", "advanced"]),
    default="beginner",
    help="难度级别",
)
@click.option("--verify", is_flag=True, help="启用自动验证")
def new(language, topic, difficulty, verify):
    """创建新demo

    示例:
        opendemo new python 异步HTTP请求处理
        opendemo new java 设计模式工厂模式 --difficulty intermediate
    """

    # 验证语言
    if language.lower() not in SUPPORTED_LANGUAGES:
        print_error(f"不支持的语言: {language}")
        print_info(f"当前支持的语言: {', '.join(SUPPORTED_LANGUAGES)}")
        sys.exit(1)

    # 初始化服务
    config = ConfigService()

    # 检查API密钥
    if not config.get("ai.api_key"):
        print_error("AI API密钥未配置")
        print_info("请运行: opendemo config set ai.api_key YOUR_KEY")
        sys.exit(1)

    storage = StorageService(config)
    repository = DemoRepository(storage, config)
    ai_service = AIService(config)
    generator = DemoGenerator(ai_service, repository, config)
    verifier = DemoVerifier(config)

    # 初始化库相关服务（传入AI服务用于智能判断库名）

    # 合并主题
    topic_str = " ".join(topic)

    # 检查是否为库demo请求（使用新的检测方法，支持未注册的库）
    topic_keywords = list(topic)
    library_name = repository.detect_library_for_new_command(language, topic_keywords, use_ai=True)

    if library_name:
        # 识别为库demo
        feature_keywords = topic_keywords[1:] if len(topic_keywords) > 1 else []
        if feature_keywords:
            # 使用功能关键字作为主题
            topic_str = " ".join(feature_keywords)
        else:
            # 没有功能关键字，使用库名作为主题
            topic_str = library_name
        print_info(f"识别为库demo: {library_name}")

    print_progress(f"生成 {language} - {topic_str} 的demo (难度: {difficulty})")

    # 生成demo
    result = generator.generate(
        language,
        topic_str,
        difficulty=difficulty,
        save_to_user_library=False,
        library_name=library_name,
    )

    if not result:
        print_error("生成demo失败")
        sys.exit(1)

    demo = result["demo"]
    output_path = Path(result["path"])

    print_success("成功生成demo")

    # 验证(如果启用)
    if verify or config.get("enable_verification", False):
        _verify_demo(demo, verifier, language, repository)

    _display_demo_result(demo, output_path, repository, verify, verifier, language)

    # 更新README.md
    _update_readme_after_new(storage, language, demo.name, library_name)

    # 更新 demo-list.md
    _update_demo_list(storage)


@cli.group()
def config():
    """配置管理"""
    pass


@config.command("init")
@click.option("--api-key", prompt="AI API密钥", help="AI服务API密钥")
def config_init(api_key):
    """初始化配置"""
    config_service = ConfigService()
    config_service.init_config(api_key=api_key)
    print_success(f"配置文件已创建: {config_service.global_config_path}")


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.option("--global", "is_global", is_flag=True, default=True, help="设置全局配置")
def config_set(key, value, is_global):
    """设置配置项

    示例:
        opendemo config set ai.api_key sk-xxx
        opendemo config set enable_verification true
    """
    config_service = ConfigService()

    # 转换值类型
    if value.lower() in ("true", "false"):
        value = value.lower() == "true"
    elif value.isdigit():
        value = int(value)

    config_service.set(key, value, global_scope=is_global)
    print_success(f"已设置 {key} = {value}")


@config.command("get")
@click.argument("key")
def config_get(key):
    """获取配置项

    示例:
        opendemo config get ai.model
    """
    config_service = ConfigService()
    value = config_service.get(key)

    if value is not None:
        # 隐藏敏感信息
        if "key" in key.lower() or "password" in key.lower():
            if value:
                value = "*" * 8
        print(f"{key} = {value}")
    else:
        print_warning(f"配置项不存在: {key}")


@config.command("list")
def config_list():
    """列出所有配置"""
    config_service = ConfigService()
    all_config = config_service.get_all()
    print_config_list(all_config)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="显示详细输出")
def check(verbose):
    """运行质量检查

    执行单元测试和CLI功能测试，生成检查报告。
    报告保存在项目根目录的 check 目录下。

    示例:
        opendemo check           # 运行检查并生成报告
        opendemo check -v        # 显示详细输出
    """
    from rich.console import Console
    from rich.table import Table
    from rich import box

    console = Console()

    print_info("开始质量检查...")

    # 创建检查器并运行
    checker = QualityChecker()

    with console.status("[bold blue]运行单元测试..."):
        results = checker.run_all_checks()

    # 保存报告
    report_path = checker.save_report()

    # 显示结果
    summary = results["summary"]

    if summary["overall_status"] == "PASS":
        print_success("质量检查通过!")
    else:
        print_warning("质量检查发现问题")

    # 显示摘要表格
    table = Table(title="检查结果摘要", box=box.ROUNDED)
    table.add_column("检查项", style="cyan")
    table.add_column("状态", justify="center")
    table.add_column("通过/总计", justify="center")

    unit_status = results["unit_tests"].get("status", "N/A")
    unit_style = "green" if unit_status == "PASS" else "red"
    table.add_row(
        "单元测试",
        f"[{unit_style}]{unit_status}[/{unit_style}]",
        f"{results['unit_tests'].get('passed', 0)}/{results['unit_tests'].get('total', 0)}",
    )

    cli_status = results["cli_tests"].get("status", "N/A")
    cli_style = "green" if cli_status == "PASS" else "red"
    table.add_row(
        "CLI功能测试",
        f"[{cli_style}]{cli_status}[/{cli_style}]",
        f"{results['cli_tests'].get('passed', 0)}/{results['cli_tests'].get('total', 0)}",
    )

    console.print(table)

    # 详细输出
    if verbose:
        console.print("\n[bold]CLI测试详情:[/bold]")
        for test in results["cli_tests"].get("tests", []):
            status_icon = "✅" if test["status"] == "PASS" else "❌"
            console.print(f"  {status_icon} {test['name']}: {test['command']}")

    # 显示报告路径
    console.print(f"\n[bold]报告已保存:[/bold] {report_path}")
    console.print(f"[dim]查看完整报告: cat {report_path.with_suffix('.md')}[/dim]")

    # 如果检查失败，返回非零退出码
    if summary["overall_status"] != "PASS":
        sys.exit(1)


def _verify_demo(demo, verifier, language, repository):
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


def _display_demo_result(demo, output_path, repository, verify, verifier, language):
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


def _update_readme_after_new(
    storage, language: str, demo_name: str, library_name: Optional[str] = None
):
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
            _update_status_md(output_dir, status_path)
            print_info("STATUS.md 已更新")
        except Exception as e:
            logger.error(f"Failed to update STATUS.md: {e}")
            print_warning(f"更新STATUS.md失败: {e}")


def _update_status_md(output_dir: Path, status_path: Path):
    """更新STATUS.md中的Demo统计"""
    import re
    from datetime import datetime

    updater = ReadmeUpdater(output_dir, status_path.parent / "README.md")
    stats = updater.collect_stats()
    totals = updater.calculate_totals(stats)

    with open(status_path, "r", encoding="utf-8") as f:
        content = f.read()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = re.sub(
        r"\*\*检查时间\*\*: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        f"**检查时间**: {now}", content
    )

    lang_map = {"python": "Python", "go": "Go", "nodejs": "Node.js", "kubernetes": "Kubernetes"}
    for lang, name in lang_map.items():
        data = stats.get(lang, {"base": 0, "libraries": {}, "tools": {}})
        total = data.get("base", 0) + sum(data.get("libraries", {}).values()) + sum(data.get("tools", {}).values())
        content = re.sub(rf"\| {name} \| \d+ \|", f"| {name} | {total} |", content)

    content = re.sub(
        r"\| \*\*总计\*\* \| \*\*\d+\*\* \|",
        f"| **总计** | **{totals['grand_total']}** |", content
    )

    with open(status_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    """主入口"""
    try:
        cli()
    except KeyboardInterrupt:
        print_warning("\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print_error(f"发生错误: {e}")
        logger = get_logger(__name__)
        logger.exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()
    main()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

    lang_map = {"python": "Python", "go": "Go", "nodejs": "Node.js", "kubernetes": "Kubernetes"}
    for lang, name in lang_map.items():
        data = stats.get(lang, {"base": 0, "libraries": {}, "tools": {}})
        total = data.get("base", 0) + sum(data.get("libraries", {}).values()) + sum(data.get("tools", {}).values())
        content = re.sub(rf"\| {name} \| \d+ \|", f"| {name} | {total} |", content)

    content = re.sub(
        r"\| \*\*总计\*\* \| \*\*\d+\*\* \|",
        f"| **总计** | **{totals['grand_total']}** |", content
    )

    with open(status_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    """主入口"""
    try:
        cli()
    except KeyboardInterrupt:
        print_warning("\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print_error(f"发生错误: {e}")
        logger = get_logger(__name__)
        logger.exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()
