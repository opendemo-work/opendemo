"""
new 命令模块

创建新demo的命令实现。
"""

import sys
from pathlib import Path

import click

from services.config_service import ConfigService
from services.storage_service import StorageService
from services.ai_service import AIService
from core.demo_repository import DemoRepository
from core.demo_generator import DemoGenerator
from core.demo_verifier import DemoVerifier
from utils.formatters import (
    print_success,
    print_error,
    print_info,
    print_progress,
)
from .base import (
    SUPPORTED_LANGUAGES,
    display_demo_result,
    verify_demo,
    update_demo_list,
    update_readme_after_new,
)


@click.command()
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
        verify_demo(demo, verifier, language, repository)

    display_demo_result(demo, output_path, repository, verify, verifier, language)

    # 更新README.md
    update_readme_after_new(storage, language, demo.name, library_name)

    # 更新 demo-list.md
    update_demo_list(storage)
