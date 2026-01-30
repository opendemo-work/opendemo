"""
配置服务模块

负责加载、合并和管理配置文件。
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from opendemo.utils.logger import get_logger

logger = get_logger(__name__)


class ConfigService:
    """配置服务类"""

    # 默认配置
    DEFAULT_CONFIG = {
        "output_directory": "./opendemo_output",
        "user_demo_library": None,  # 将在初始化时设置为 ~/.opendemo/demos
        "default_language": "python",
        "enable_verification": False,
        "verification_method": "venv",
        "verification_timeout": 300,
        "ai": {
            "provider": "openai",
            "api_key": "",
            "api_endpoint": "",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 4000,
            "timeout": 60,
            "retry_times": 3,
            "retry_interval": 5,
        },
        "contribution": {
            "auto_prompt": True,
            "author_name": "",
            "author_email": "",
            "repository_url": "https://github.com/opendemo/demos",
        },
        "display": {
            "color_output": True,
            "page_size": 10,
            "verbose": False,
        },
    }

    def __init__(self):
        """初始化配置服务"""
        self.global_config_path = self._get_global_config_path()
        self.project_config_path = Path(".opendemo.yaml")
        self._config = None
        self._ensure_user_dirs()

    def _get_global_config_path(self) -> Path:
        """获取全局配置文件路径"""
        home = Path.home()
        return home / ".opendemo" / "config.yaml"

    def _ensure_user_dirs(self):
        """确保用户目录存在"""
        user_dir = Path.home() / ".opendemo"
        user_dir.mkdir(parents=True, exist_ok=True)

        # 创建demos目录
        demos_dir = user_dir / "demos"
        demos_dir.mkdir(exist_ok=True)

        # 创建logs目录
        logs_dir = user_dir / "logs"
        logs_dir.mkdir(exist_ok=True)

    def load(self) -> Dict[str, Any]:
        """
        加载配置,合并全局配置和项目配置

        Returns:
            合并后的配置字典
        """
        if self._config is not None:
            return self._config

        # 从默认配置开始
        config = self.DEFAULT_CONFIG.copy()

        # 设置user_demo_library默认值
        if config["user_demo_library"] is None:
            config["user_demo_library"] = str(Path.home() / ".opendemo" / "demos")

        # 加载全局配置
        if self.global_config_path.exists():
            global_config = self._load_yaml(self.global_config_path)
            config = self._merge_config(config, global_config)
            logger.debug(f"Loaded global config from {self.global_config_path}")

        # 加载项目配置(优先级更高)
        if self.project_config_path.exists():
            project_config = self._load_yaml(self.project_config_path)
            config = self._merge_config(config, project_config)
            logger.debug(f"Loaded project config from {self.project_config_path}")

        self._config = config
        return config

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """
        从YAML文件加载配置

        Args:
            path: YAML文件路径

        Returns:
            配置字典
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                return config
        except Exception as e:
            logger.error(f"Failed to load config from {path}: {e}")
            return {}

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并配置,override中的值会覆盖base中的值

        Args:
            base: 基础配置
            override: 覆盖配置

        Returns:
            合并后的配置
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项

        Args:
            key: 配置键,支持点分隔的嵌套键,如 'ai.api_key'
            default: 默认值

        Returns:
            配置值
        """
        config = self.load()
        keys = key.split(".")
        value = config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any, global_scope: bool = True):
        """
        设置配置项并保存到文件

        Args:
            key: 配置键,支持点分隔的嵌套键
            value: 配置值
            global_scope: 是否设置到全局配置,False则设置到项目配置
        """
        config_path = self.global_config_path if global_scope else self.project_config_path

        # 加载现有配置
        if config_path.exists():
            config = self._load_yaml(config_path)
        else:
            config = {}

        # 设置值
        keys = key.split(".")
        current = config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

        # 保存配置
        self._save_yaml(config_path, config)

        # 重置缓存
        self._config = None

        logger.info(f"Set {key} = {value} in {config_path}")

    def _save_yaml(self, path: Path, config: Dict[str, Any]):
        """
        保存配置到YAML文件

        Args:
            path: 文件路径
            config: 配置字典
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            logger.error(f"Failed to save config to {path}: {e}")
            raise

    def init_config(self, api_key: str = None):
        """
        初始化配置文件

        Args:
            api_key: AI API密钥
        """
        if self.global_config_path.exists():
            logger.warning(f"Config file already exists at {self.global_config_path}")
            return

        config = self.DEFAULT_CONFIG.copy()

        # 设置user_demo_library
        if config["user_demo_library"] is None:
            config["user_demo_library"] = str(Path.home() / ".opendemo" / "demos")

        if api_key:
            config["ai"]["api_key"] = api_key

        self._save_yaml(self.global_config_path, config)
        logger.info(f"Initialized config at {self.global_config_path}")

    def validate(self) -> tuple[bool, list]:
        """
        验证配置的有效性

        Returns:
            (是否有效, 错误信息列表)
        """
        config = self.load()
        errors = []

        # 检查AI配置
        if not config["ai"].get("api_key"):
            errors.append(
                "AI API key is not configured. Run 'opendemo config set ai.api_key YOUR_KEY'"
            )

        # 检查输出目录
        output_dir = config.get("output_directory")
        if output_dir:
            try:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Invalid output_directory: {e}")

        # 检查验证超时
        timeout = config.get("verification_timeout")
        if timeout is not None and (not isinstance(timeout, int) or timeout <= 0):
            errors.append("verification_timeout must be a positive integer")

        return len(errors) == 0, errors

    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置

        Returns:
            完整配置字典
        """
        return self.load().copy()
