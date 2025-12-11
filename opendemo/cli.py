"""
CLI主程序

命令行接口实现。
"""

import sys
import json
import click
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from opendemo.services.config_service import ConfigService
from opendemo.services.storage_service import StorageService
from opendemo.services.ai_service import AIService
from opendemo.core.demo_manager import DemoManager
from opendemo.core.search_engine import SearchEngine
from opendemo.core.generator import DemoGenerator
from opendemo.core.verifier import DemoVerifier
from opendemo.core.contribution import ContributionManager
from opendemo.utils.formatters import (
    print_success, print_error, print_warning, print_info,
    print_demo_result, print_search_results, print_config_list,
    print_progress
)
from opendemo.utils.logger import setup_logger, get_logger

# 支持的语言列表
SUPPORTED_LANGUAGES = ['python', 'java']


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Open Demo - 智能化的编程学习辅助CLI工具"""
    # 初始化日志
    log_file = Path.home() / '.opendemo' / 'logs' / 'opendemo.log'
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
            metadata_file = item / 'metadata.json'
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    demos.append({
                        'path': item,
                        'name': item.name,
                        'language': metadata.get('language', language),
                        'keywords': metadata.get('keywords', []),
                        'description': metadata.get('description', ''),
                        'difficulty': metadata.get('difficulty', 'beginner'),
                        'verified': metadata.get('verified', False),
                        'metadata': metadata
                    })
                except Exception:
                    # 即使没有metadata，也列出目录
                    demos.append({
                        'path': item,
                        'name': item.name,
                        'language': language,
                        'keywords': [],
                        'description': '',
                        'difficulty': 'unknown',
                        'verified': False,
                        'metadata': {}
                    })
            else:
                # 目录存在但没有metadata，也列出
                demos.append({
                    'path': item,
                    'name': item.name,
                    'language': language,
                    'keywords': [],
                    'description': '',
                    'difficulty': 'unknown',
                    'verified': False,
                    'metadata': {}
                })
    
    return demos


def _match_demo_in_output(output_dir: Path, language: str, keywords: List[str]) -> Optional[Dict[str, Any]]:
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
    search_term = '-'.join(kw.lower() for kw in keywords)
    search_term_single = keywords[0].lower() if keywords else ''
    
    # 1. 精确匹配文件夹名称
    for demo in demos:
        folder_name = demo['name'].lower()
        if folder_name == search_term or folder_name == search_term_single:
            return demo
    
    # 2. 文件夹名称包含任一关键字
    best_match = None
    best_score = 0
    
    for demo in demos:
        folder_name = demo['name'].lower()
        score = 0
        
        for keyword in keywords:
            kw_lower = keyword.lower()
            if kw_lower in folder_name:
                score += 10
            # 检查metadata中的keywords
            if any(kw_lower in mk.lower() for mk in demo.get('keywords', [])):
                score += 5
        
        if score > best_score:
            best_score = score
            best_match = demo
    
    if best_score > 0:
        return best_match
    
    return None


def _display_output_demo(demo_info: Dict[str, Any], demo_path: Path, language: str):
    """显示输出目录中的demo信息"""
    from rich.console import Console
    console = Console()
    
    print_success("Demo已存在!")
    console.print(f"\n[bold]名称:[/bold] {demo_info['name']}")
    console.print(f"[bold]语言:[/bold] {language}")
    console.print(f"[bold]路径:[/bold] {demo_path}")
    
    if demo_info.get('keywords'):
        console.print(f"[bold]关键字:[/bold] {', '.join(demo_info['keywords'])}")
    
    if demo_info.get('description'):
        console.print(f"[bold]描述:[/bold] {demo_info['description']}")
    
    # 列出文件
    console.print("\n[bold]包含文件:[/bold]")
    code_dir = demo_path / 'code'
    if code_dir.exists():
        for f in code_dir.iterdir():
            if f.is_file():
                console.print(f"  - code/{f.name}")
    
    # 快速开始
    console.print("\n[bold]快速开始:[/bold]")
    console.print(f"  1. cd {demo_path}")
    if language.lower() == 'python':
        code_files = list(code_dir.glob('*.py')) if code_dir.exists() else []
        if code_files:
            console.print(f"  2. python code/{code_files[0].name}")
    
    console.print(f"\n[bold]如需重新生成:[/bold] opendemo get {language} {demo_info['name']} new")


@cli.command()
@click.argument('language')
@click.argument('keywords', nargs=-1, required=True)
@click.option('--verify', is_flag=True, help='启用自动验证')
def get(language, keywords, verify):
    """获取demo代码
    
    示例:
        opendemo get python logging       # 匹配已有demo
        opendemo get python logging new   # 强制重新生成
        opendemo get python 列表 操作
        opendemo get java 继承 --verify
    """
    logger = get_logger(__name__)
    
    # 验证语言
    if language.lower() not in SUPPORTED_LANGUAGES:
        print_error(f"不支持的语言: {language}")
        print_info(f"当前支持的语言: {', '.join(SUPPORTED_LANGUAGES)}")
        sys.exit(1)
    
    # 初始化服务
    config = ConfigService()
    storage = StorageService(config)
    demo_manager = DemoManager(storage)
    search_engine = SearchEngine(demo_manager)
    ai_service = AIService(config)
    generator = DemoGenerator(ai_service, demo_manager, config)
    verifier = DemoVerifier(config)
    
    # 检查是否有 'new' 参数，表示强制重新生成
    keywords_list = list(keywords)
    force_new = False
    if keywords_list and keywords_list[-1].lower() == 'new':
        force_new = True
        keywords_list = keywords_list[:-1]  # 移除 'new'
    
    if not keywords_list:
        print_error("请提供关键字")
        sys.exit(1)
    
    # 合并关键字
    topic = ' '.join(keywords_list)
    
    # 获取输出目录
    output_dir = storage.get_output_directory()
    
    # 如果不是强制生成，先在输出目录中查找
    if not force_new:
        print_progress(f"搜索 {language} - {topic} 的demo")
        
        # 首先在 opendemo_output/<language>/ 目录中匹配
        matched_demo = _match_demo_in_output(output_dir, language, keywords_list)
        
        if matched_demo:
            demo_path = matched_demo['path']
            print_success(f"在输出目录中找到匹配的demo: {matched_demo['name']}")
            
            # 显示demo信息
            _display_output_demo(matched_demo, demo_path, language)
            return
        
        # 在内置库和用户库中搜索
        results = search_engine.search(language=language, keywords=keywords_list)
        
        if results:
            demo = results[0]
            print_success(f"在本地库中找到匹配的demo: {demo.name}")
            
            # 复制到输出目录
            output_path = demo_manager.copy_demo_to_output(demo)
            
            if output_path:
                _display_demo_result(demo, output_path, demo_manager, verify, verifier, language)
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
    if not config.get('ai.api_key'):
        print_error("AI API密钥未配置")
        print_info("请运行: opendemo config set ai.api_key YOUR_KEY")
        sys.exit(1)
    
    # 如果是强制生成，生成新的文件夹名（带-new后缀）
    custom_name = None
    if force_new:
        base_name = '-'.join(kw.lower() for kw in keywords_list)
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
        language, 
        topic, 
        difficulty='beginner',
        custom_folder_name=custom_name
    )
    
    if not result:
        print_error("生成demo失败")
        sys.exit(1)
    
    demo = result['demo']
    output_path = Path(result['path'])
    
    print_success("成功生成demo")
    
    # 验证(如果启用)
    if verify or config.get('enable_verification', False):
        _verify_demo(demo, verifier, language, demo_manager)
    
    _display_demo_result(demo, output_path, demo_manager, verify, verifier, language)


@cli.command()
@click.argument('language', required=False)
@click.argument('keywords', nargs=-1)
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
    demo_manager = DemoManager(storage)
    search_engine = SearchEngine(demo_manager)
    
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
            folder_name = demo['name'].lower()
            # 检查文件夹名或keywords中是否包含搜索关键字
            match = any(kw in folder_name for kw in keyword_list)
            if not match:
                match = any(kw in mk.lower() for kw in keyword_list for mk in demo.get('keywords', []))
            if match:
                filtered_demos.append(demo)
        output_demos = filtered_demos
    
    # 按名称排序
    output_demos.sort(key=lambda x: x['name'])
    
    # 显示结果
    print_search_results(output_demos)


@cli.command()
@click.argument('language')
@click.argument('topic', nargs=-1, required=True)
@click.option('--difficulty', type=click.Choice(['beginner', 'intermediate', 'advanced']), 
              default='beginner', help='难度级别')
@click.option('--verify', is_flag=True, help='启用自动验证')
def new(language, topic, difficulty, verify):
    """创建新demo
    
    示例:
        opendemo new python 异步HTTP请求处理
        opendemo new java 设计模式工厂模式 --difficulty intermediate
    """
    logger = get_logger(__name__)
    
    # 验证语言
    if language.lower() not in SUPPORTED_LANGUAGES:
        print_error(f"不支持的语言: {language}")
        print_info(f"当前支持的语言: {', '.join(SUPPORTED_LANGUAGES)}")
        sys.exit(1)
    
    # 初始化服务
    config = ConfigService()
    
    # 检查API密钥
    if not config.get('ai.api_key'):
        print_error("AI API密钥未配置")
        print_info("请运行: opendemo config set ai.api_key YOUR_KEY")
        sys.exit(1)
    
    storage = StorageService(config)
    demo_manager = DemoManager(storage)
    ai_service = AIService(config)
    generator = DemoGenerator(ai_service, demo_manager, config)
    verifier = DemoVerifier(config)
    contribution_manager = ContributionManager(config, storage)
    
    # 合并主题
    topic_str = ' '.join(topic)
    
    print_progress(f"生成 {language} - {topic_str} 的demo (难度: {difficulty})")
    
    # 生成demo
    result = generator.generate(
        language, 
        topic_str, 
        difficulty=difficulty,
        save_to_user_library=False
    )
    
    if not result:
        print_error("生成demo失败")
        sys.exit(1)
    
    demo = result['demo']
    output_path = Path(result['path'])
    
    print_success("成功生成demo")
    
    # 验证(如果启用)
    if verify or config.get('enable_verification', False):
        _verify_demo(demo, verifier, language, demo_manager)
    
    _display_demo_result(demo, output_path, demo_manager, verify, verifier, language)
    
    # 询问是否贡献
    if contribution_manager.prompt_contribution(output_path):
        # 复制到用户库
        user_lib_path = contribution_manager.copy_to_user_library(output_path)
        
        if user_lib_path:
            print_success(f"已将demo保存到用户库: {user_lib_path}")
            
            # 准备贡献信息
            contrib_info = contribution_manager.prepare_contribution(user_lib_path)
            
            if contrib_info:
                print_info("\n贡献信息:")
                message = contribution_manager.generate_contribution_message(contrib_info)
                print(message)
                print_info(f"\n请手动将demo提交到仓库: {contrib_info['repository_url']}")
            else:
                print_warning("准备贡献信息失败")
        else:
            print_error("保存到用户库失败")


@cli.group()
def config():
    """配置管理"""
    pass


@config.command('init')
@click.option('--api-key', prompt='AI API密钥', help='AI服务API密钥')
def config_init(api_key):
    """初始化配置"""
    config_service = ConfigService()
    config_service.init_config(api_key=api_key)
    print_success(f"配置文件已创建: {config_service.global_config_path}")


@config.command('set')
@click.argument('key')
@click.argument('value')
@click.option('--global', 'is_global', is_flag=True, default=True, help='设置全局配置')
def config_set(key, value, is_global):
    """设置配置项
    
    示例:
        opendemo config set ai.api_key sk-xxx
        opendemo config set enable_verification true
    """
    config_service = ConfigService()
    
    # 转换值类型
    if value.lower() in ('true', 'false'):
        value = value.lower() == 'true'
    elif value.isdigit():
        value = int(value)
    
    config_service.set(key, value, global_scope=is_global)
    print_success(f"已设置 {key} = {value}")


@config.command('get')
@click.argument('key')
def config_get(key):
    """获取配置项
    
    示例:
        opendemo config get ai.model
    """
    config_service = ConfigService()
    value = config_service.get(key)
    
    if value is not None:
        # 隐藏敏感信息
        if 'key' in key.lower() or 'password' in key.lower():
            if value:
                value = "*" * 8
        print(f"{key} = {value}")
    else:
        print_warning(f"配置项不存在: {key}")


@config.command('list')
def config_list():
    """列出所有配置"""
    config_service = ConfigService()
    all_config = config_service.get_all()
    print_config_list(all_config)


def _verify_demo(demo, verifier, language, demo_manager):
    """验证demo"""
    print_progress("验证demo可执行性")
    verification_result = verifier.verify(demo.path, language)
    
    if verification_result.get('verified'):
        print_success("验证通过")
        # 更新元数据
        demo_manager.update_demo_metadata(demo, {'verified': True})
    elif verification_result.get('skipped'):
        print_warning(verification_result.get('message', '验证已跳过'))
    else:
        print_warning("验证未通过")
        errors = verification_result.get('errors', [])
        for error in errors:
            print_error(f"  - {error}")


def _display_demo_result(demo, output_path, demo_manager, verify, verifier, language):
    """显示demo结果"""
    files = demo_manager.get_demo_files(demo)
    
    # 生成快速开始步骤
    quick_start = [
        f"cd {output_path}",
    ]
    
    # 根据语言添加特定步骤
    if language.lower() == 'python':
        if (output_path / 'requirements.txt').exists():
            quick_start.append("pip install -r requirements.txt")
        
        # 找到第一个Python文件
        code_files = list((output_path / 'code').glob('*.py')) if (output_path / 'code').exists() else []
        if code_files:
            quick_start.append(f"python code/{code_files[0].name}")
    elif language.lower() == 'java':
        quick_start.append("# 根据项目类型使用Maven或Gradle构建")
    
    # 准备显示信息
    demo_info = {
        'language': demo.language,
        'topic': demo.name,
        'path': str(output_path),
        'files': files,
        'verified': demo.verified,
        'execution_time': 'N/A',
        'quick_start': quick_start,
        'readme_path': str(output_path / 'README.md')
    }
    
    print_demo_result(demo_info)


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


if __name__ == '__main__':
    main()
