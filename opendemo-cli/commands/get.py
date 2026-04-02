"""
get 命令模块

获取demo代码的命令实现。
"""

import sys
from pathlib import Path

import click

from services.config_service import ConfigService
from services.storage_service import StorageService
from services.ai_service import AIService
from core.demo_repository import DemoRepository
from core.demo_search import DemoSearch
from core.demo_generator import DemoGenerator
from core.demo_verifier import DemoVerifier
from utils.formatters import (
    print_success,
    print_error,
    print_info,
    print_progress,
    print_warning,
)
from .base import (
    SUPPORTED_LANGUAGES,
    match_demo_in_output,
    display_output_demo,
    display_demo_result,
    handle_library_command,
    verify_demo,
    update_demo_list,
)


@click.command()
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
        handle_library_command(
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
        matched_demo = match_demo_in_output(output_dir, language, keywords_list)

        if matched_demo:
            demo_path = matched_demo["path"]
            print_success(f"在输出目录中找到匹配的demo: {matched_demo['name']}")

            # 显示demo信息
            display_output_demo(matched_demo, demo_path, language)
            return

        # 在内置库和用户库中搜索
        results = search.search_demos(language=language, keywords=keywords_list)

        if results:
            demo = results[0]
            print_success(f"在本地库中找到匹配的demo: {demo.name}")

            # 复制到输出目录
            output_path = repository.copy_to_output(demo)

            if output_path:
                display_demo_result(demo, output_path, repository, verify, verifier, language)
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
        verify_demo(demo, verifier, language, repository)

    display_demo_result(demo, output_path, repository, verify, verifier, language)

    # 更新 demo-list.md
    update_demo_list(storage)
