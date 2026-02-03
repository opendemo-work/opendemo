#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 环境变量管理完整示例
演示如何安全地读取、设置和管理环境变量
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


# ============ 1. 读取环境变量 ============
print("=" * 50)
print("1. 读取环境变量")
print("=" * 50)

# 方式1: os.environ (KeyError if not found)
try:
    path = os.environ["PATH"]
    print(f"PATH (前100字符): {path[:100]}...")
except KeyError:
    print("PATH not found")

# 方式2: os.environ.get (返回默认值)
home = os.environ.get("HOME") or os.environ.get("USERPROFILE")
print(f"HOME/USERPROFILE: {home}")

# 方式3: os.getenv (推荐)
debug = os.getenv("DEBUG", "false")
port = os.getenv("PORT", "8080")
print(f"DEBUG: {debug}")
print(f"PORT: {port}")


# ============ 2. 设置环境变量 ============
print("\n" + "=" * 50)
print("2. 设置环境变量")
print("=" * 50)

# 设置环境变量 (只影响当前进程和子进程)
os.environ["MY_APP_NAME"] = "DemoApp"
os.environ["MY_APP_VERSION"] = "1.0.0"

print(f"MY_APP_NAME: {os.getenv('MY_APP_NAME')}")
print(f"MY_APP_VERSION: {os.getenv('MY_APP_VERSION')}")

# 删除环境变量
if "MY_APP_NAME" in os.environ:
    del os.environ["MY_APP_NAME"]
    print("已删除 MY_APP_NAME")

# 使用 pop 删除并获取值
version = os.environ.pop("MY_APP_VERSION", None)
print(f"删除并获取 MY_APP_VERSION: {version}")


# ============ 3. 常用环境变量 ============
print("\n" + "=" * 50)
print("3. 常用环境变量")
print("=" * 50)

common_vars = {
    "PATH": "可执行文件搜索路径",
    "HOME": "用户主目录 (Unix)",
    "USERPROFILE": "用户主目录 (Windows)",
    "TEMP": "临时文件目录",
    "TMP": "临时文件目录",
    "LANG": "语言设置",
    "USER": "当前用户名 (Unix)",
    "USERNAME": "当前用户名 (Windows)",
    "PYTHONPATH": "Python模块搜索路径",
    "VIRTUAL_ENV": "虚拟环境路径",
}

print("常用环境变量:")
for var, desc in common_vars.items():
    value = os.getenv(var)
    if value:
        display = value[:50] + "..." if len(value) > 50 else value
        print(f"  {var}: {display}")


# ============ 4. 类型转换 ============
print("\n" + "=" * 50)
print("4. 环境变量类型转换")
print("=" * 50)

def get_bool(key: str, default: bool = False) -> bool:
    """获取布尔值环境变量"""
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")

def get_int(key: str, default: int = 0) -> int:
    """获取整数环境变量"""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default

def get_float(key: str, default: float = 0.0) -> float:
    """获取浮点数环境变量"""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        return default

def get_list(key: str, separator: str = ",", default: list = None) -> list:
    """获取列表环境变量"""
    value = os.getenv(key)
    if not value:
        return default or []
    return [item.strip() for item in value.split(separator)]

# 设置测试值
os.environ["DEBUG"] = "true"
os.environ["MAX_CONNECTIONS"] = "100"
os.environ["TIMEOUT"] = "30.5"
os.environ["ALLOWED_HOSTS"] = "localhost,127.0.0.1,example.com"

print(f"DEBUG (bool): {get_bool('DEBUG')}")
print(f"MAX_CONNECTIONS (int): {get_int('MAX_CONNECTIONS')}")
print(f"TIMEOUT (float): {get_float('TIMEOUT')}")
print(f"ALLOWED_HOSTS (list): {get_list('ALLOWED_HOSTS')}")


# ============ 5. 环境配置类 ============
print("\n" + "=" * 50)
print("5. 环境配置类")
print("=" * 50)

@dataclass
class AppConfig:
    """应用配置类 - 从环境变量加载"""
    # 基本配置
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "MyApp"))
    debug: bool = field(default_factory=lambda: get_bool("DEBUG"))
    
    # 服务器配置
    host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: get_int("PORT", 8080))
    
    # 数据库配置
    db_host: str = field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    db_port: int = field(default_factory=lambda: get_int("DB_PORT", 5432))
    db_name: str = field(default_factory=lambda: os.getenv("DB_NAME", "app_db"))
    db_user: str = field(default_factory=lambda: os.getenv("DB_USER", "postgres"))
    db_password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", ""))
    
    @property
    def db_url(self) -> str:
        """构建数据库连接URL"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    def __post_init__(self):
        """验证配置"""
        if not self.db_password and not self.debug:
            print("警告: 生产环境未设置数据库密码")

# 设置环境变量
os.environ["APP_NAME"] = "ProductionApp"
os.environ["DEBUG"] = "false"
os.environ["DB_HOST"] = "db.example.com"
os.environ["DB_PASSWORD"] = os.getenv("DB_PASSWORD", "default-password")

config = AppConfig()
print(f"应用名称: {config.app_name}")
print(f"调试模式: {config.debug}")
print(f"服务地址: {config.host}:{config.port}")
print(f"数据库URL: {config.db_url}")


# ============ 6. .env 文件模拟 ============
print("\n" + "=" * 50)
print("6. .env 文件解析")
print("=" * 50)

def load_env_file(filepath: str) -> Dict[str, str]:
    """
    解析.env文件
    支持:
    - KEY=value
    - KEY="quoted value"
    - # 注释
    - 空行
    """
    env_vars = {}
    path = Path(filepath)
    
    if not path.exists():
        return env_vars
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            
            # 解析 KEY=value
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 移除引号
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                env_vars[key] = value
    
    return env_vars

def load_dotenv(filepath: str = ".env", override: bool = False):
    """加载.env文件到环境变量"""
    env_vars = load_env_file(filepath)
    for key, value in env_vars.items():
        if override or key not in os.environ:
            os.environ[key] = value
    return env_vars

# 创建示例.env文件
env_content = """
# 应用配置
APP_ENV=development
SECRET_KEY = os.getenv("JWT_SECRET", "default-secret")

# 数据库
DATABASE_URL='postgres://user:pass@localhost/db'

# 功能开关
FEATURE_FLAG=true
"""

# 写入临时.env文件
env_file = Path("temp_demo.env")
env_file.write_text(env_content, encoding='utf-8')

# 加载
loaded = load_env_file(str(env_file))
print("解析的.env内容:")
for key, value in loaded.items():
    print(f"  {key}: {value}")

# 清理
env_file.unlink()


# ============ 7. 敏感信息处理 ============
print("\n" + "=" * 50)
print("7. 敏感信息安全处理")
print("=" * 50)

class SecretString:
    """敏感字符串包装器 - 防止意外打印"""
    
    def __init__(self, value: str):
        self._value = value
    
    def get_secret_value(self) -> str:
        """获取实际值"""
        return self._value
    
    def __repr__(self) -> str:
        return "SecretString('**********')"
    
    def __str__(self) -> str:
        return "**********"
    
    def __eq__(self, other):
        if isinstance(other, SecretString):
            return self._value == other._value
        return False

# 使用示例
api_key = SecretString(os.getenv("API_KEY", ""))
db_password = SecretString(os.getenv("DB_PASSWORD", ""))

print(f"API Key: {api_key}")  # 不会泄露
print(f"DB Password: {db_password}")  # 不会泄露
print(f"实际API Key: {api_key.get_secret_value()}")  # 需要明确获取


# ============ 8. 多环境配置 ============
print("\n" + "=" * 50)
print("8. 多环境配置")
print("=" * 50)

class Environment:
    """环境配置管理"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    
    @classmethod
    def current(cls) -> str:
        return os.getenv("APP_ENV", cls.DEVELOPMENT)
    
    @classmethod
    def is_development(cls) -> bool:
        return cls.current() == cls.DEVELOPMENT
    
    @classmethod
    def is_production(cls) -> bool:
        return cls.current() == cls.PRODUCTION

# 根据环境加载不同配置
def get_config_for_env() -> dict:
    env = Environment.current()
    
    base_config = {
        "app_name": "MyApp",
        "log_level": "INFO",
    }
    
    env_configs = {
        Environment.DEVELOPMENT: {
            "debug": True,
            "db_host": "localhost",
            "log_level": "DEBUG",
        },
        Environment.STAGING: {
            "debug": True,
            "db_host": "staging-db.example.com",
        },
        Environment.PRODUCTION: {
            "debug": False,
            "db_host": "prod-db.example.com",
            "log_level": "WARNING",
        },
    }
    
    config = {**base_config, **env_configs.get(env, {})}
    return config

os.environ["APP_ENV"] = "development"
print(f"当前环境: {Environment.current()}")
print(f"是否开发环境: {Environment.is_development()}")
print(f"环境配置: {get_config_for_env()}")


# ============ 9. 子进程环境 ============
print("\n" + "=" * 50)
print("9. 子进程环境变量")
print("=" * 50)

import subprocess

# 子进程继承父进程环境变量
os.environ["PARENT_VAR"] = "inherited"

# 运行子进程并传递额外环境变量
result = subprocess.run(
    [sys.executable, "-c", "import os; print('PARENT_VAR:', os.getenv('PARENT_VAR')); print('CHILD_VAR:', os.getenv('CHILD_VAR'))"],
    env={**os.environ, "CHILD_VAR": "child_only"},
    capture_output=True,
    text=True
)
print("子进程输出:")
print(result.stdout)


# ============ 10. 最佳实践 ============
print("\n" + "=" * 50)
print("10. 环境变量最佳实践")
print("=" * 50)
print("""
1. 安全性:
   - 永远不要在代码中硬编码敏感信息
   - 使用 .env 文件并加入 .gitignore
   - 使用 SecretString 包装敏感数据

2. 命名规范:
   - 使用大写字母和下划线
   - 添加应用前缀 (如 MYAPP_DB_HOST)
   - 保持一致性

3. 默认值:
   - 总是提供合理的默认值
   - 开发环境默认值应该安全
   - 生产环境必须显式设置

4. 验证:
   - 启动时验证必需的环境变量
   - 验证值的类型和范围
   - 失败时提供清晰的错误信息

5. 推荐工具:
   - python-dotenv: 加载.env文件
   - pydantic-settings: 类型安全的配置
   - environs: 环境变量解析
""")
