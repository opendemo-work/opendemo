"""
config 命令模块

配置管理的命令实现。
"""

import click

from services.config_service import ConfigService
from utils.formatters import print_success, print_warning, print_config_list


@click.group()
def config():
    """配置管理"""
    pass


@config.command("init")
@click.option("--api-key", prompt="AI API密钥", help="AI服务API密钥")
def init(api_key):
    """初始化配置"""
    config_service = ConfigService()
    config_service.init_config(api_key=api_key)
    print_success(f"配置文件已创建: {config_service.global_config_path}")


@config.command("set")
@click.argument("key")
@click.argument("value")
@click.option("--global", "is_global", is_flag=True, default=True, help="设置全局配置")
def set(key, value, is_global):
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
def get(key):
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
def list():
    """列出所有配置"""
    config_service = ConfigService()
    all_config = config_service.get_all()
    print_config_list(all_config)
