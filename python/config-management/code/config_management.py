#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python配置管理演示
展示环境变量、配置文件、配置类等
"""
import os
import json
import tempfile
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


def demo_environment_variables():
    """环境变量"""
    print("=" * 50)
    print("1. 环境变量")
    print("=" * 50)
    
    # 获取环境变量
    path = os.environ.get('PATH', '')
    print(f"PATH: {path[:80]}...")
    
    # 获取带默认值
    debug = os.environ.get('DEBUG', 'false')
    print(f"DEBUG (默认值): {debug}")
    
    # 设置环境变量(仅当前进程)
    os.environ['MY_APP_MODE'] = 'development'
    print(f"MY_APP_MODE: {os.environ['MY_APP_MODE']}")
    
    # 使用getenv
    user = os.getenv('USERNAME') or os.getenv('USER', 'unknown')
    print(f"当前用户: {user}")
    
    # 所有环境变量
    print(f"\n环境变量总数: {len(os.environ)}")


def demo_dotenv():
    """dotenv配置"""
    print("\n" + "=" * 50)
    print("2. dotenv配置")
    print("=" * 50)
    
    # 创建示例.env文件
    temp_dir = tempfile.mkdtemp()
    env_file = Path(temp_dir) / '.env'
    
    env_content = """
# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=myapp

# API配置
API_KEY=os.getenv("API_KEY", "")
API_SECRET=os.getenv("API_SECRET", "")

# 应用配置
DEBUG=true
LOG_LEVEL=INFO
"""
    env_file.write_text(env_content.strip())
    
    print(f".env文件内容:")
    print(env_content)
    
    # 手动解析.env (不依赖python-dotenv)
    def load_dotenv(path):
        """简单的dotenv解析器"""
        config = {}
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    
    config = load_dotenv(env_file)
    print("解析结果:")
    for key, value in config.items():
        # 隐藏敏感信息
        if 'KEY' in key or 'SECRET' in key:
            print(f"  {key}: {'*' * len(value)}")
        else:
            print(f"  {key}: {value}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    
    print("\n使用python-dotenv库:")
    print("  pip install python-dotenv")
    print("  from dotenv import load_dotenv")
    print("  load_dotenv()  # 自动加载.env文件")


def demo_config_class():
    """配置类"""
    print("\n" + "=" * 50)
    print("3. 配置类")
    print("=" * 50)
    
    @dataclass
    class DatabaseConfig:
        host: str = 'localhost'
        port: int = 5432
        name: str = 'myapp'
        user: str = 'postgres'
        password: str = os.getenv("DB_PASSWORD", "")
        
        @property
        def connection_string(self):
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
    @dataclass
    class AppConfig:
        debug: bool = False
        log_level: str = 'INFO'
        secret_key: str = ''
        database: DatabaseConfig = field(default_factory=DatabaseConfig)
        
        @classmethod
        def from_env(cls):
            """从环境变量加载配置"""
            return cls(
                debug=os.getenv('DEBUG', 'false').lower() == 'true',
                log_level=os.getenv('LOG_LEVEL', 'INFO'),
                secret_key=os.getenv('SECRET_KEY', ''),
                database=DatabaseConfig(
                    host=os.getenv('DB_HOST', 'localhost'),
                    port=int(os.getenv('DB_PORT', '5432')),
                    name=os.getenv('DB_NAME', 'myapp'),
                    user=os.getenv('DB_USER', 'postgres'),
                    password=os.getenv('DB_PASSWORD', ''),
                )
            )
    
    # 使用配置
    config = AppConfig(
        debug=True,
        log_level='DEBUG',
        SECRET_KEY = os.getenv("JWT_SECRET", "default-secret"),
        database=DatabaseConfig(
            host='db.example.com',
            password: "${GENERIC_PASSWORD}"
        )
    )
    
    print(f"AppConfig:")
    print(f"  debug: {config.debug}")
    print(f"  log_level: {config.log_level}")
    print(f"  database.host: {config.database.host}")
    print(f"  connection_string: {config.database.connection_string}")


def demo_json_config():
    """JSON配置文件"""
    print("\n" + "=" * 50)
    print("4. JSON配置文件")
    print("=" * 50)
    
    config_data = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "debug": False
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "workers": 4
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp"
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(message)s"
        }
    }
    
    # 创建临时配置文件
    temp_dir = tempfile.mkdtemp()
    config_file = Path(temp_dir) / 'config.json'
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print(f"配置文件内容:")
    print(json.dumps(config_data, indent=2))
    
    # 加载配置
    def load_config(path):
        with open(path) as f:
            return json.load(f)
    
    config = load_config(config_file)
    print(f"\n加载配置:")
    print(f"  app.name: {config['app']['name']}")
    print(f"  server.port: {config['server']['port']}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)


def demo_config_hierarchy():
    """配置层级"""
    print("\n" + "=" * 50)
    print("5. 配置层级(优先级)")
    print("=" * 50)
    
    class Config:
        """支持多层配置的配置管理器"""
        
        def __init__(self):
            self._config = {}
        
        def load_defaults(self, defaults: dict):
            """加载默认配置(最低优先级)"""
            self._merge(defaults, 'defaults')
        
        def load_file(self, path: str):
            """加载配置文件"""
            with open(path) as f:
                data = json.load(f)
            self._merge(data, f'file:{path}')
        
        def load_env(self, prefix: str = 'APP_'):
            """加载环境变量配置(最高优先级)"""
            for key, value in os.environ.items():
                if key.startswith(prefix):
                    config_key = key[len(prefix):].lower()
                    self._config[config_key] = value
        
        def _merge(self, data: dict, source: str):
            """合并配置"""
            for key, value in data.items():
                if isinstance(value, dict) and key in self._config:
                    self._config[key].update(value)
                else:
                    self._config[key] = value
        
        def get(self, key: str, default=None):
            """获取配置值,支持点分隔的键"""
            keys = key.split('.')
            value = self._config
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
    
    # 使用示例
    config = Config()
    
    # 1. 默认配置
    config.load_defaults({
        'debug': False,
        'server': {'host': '127.0.0.1', 'port': 8080}
    })
    
    print("配置层级优先级:")
    print("  1. 默认配置 (最低)")
    print("  2. 配置文件")
    print("  3. 环境变量 (最高)")
    
    print(f"\n当前配置:")
    print(f"  debug: {config.get('debug')}")
    print(f"  server.host: {config.get('server.host')}")
    print(f"  server.port: {config.get('server.port')}")


def demo_config_validation():
    """配置验证"""
    print("\n" + "=" * 50)
    print("6. 配置验证")
    print("=" * 50)
    
    from dataclasses import dataclass
    
    class ConfigError(Exception):
        pass
    
    @dataclass
    class ValidatedConfig:
        host: str
        port: int
        database_url: str
        secret_key: str
        debug: bool = False
        
        def __post_init__(self):
            """构造后验证"""
            errors = []
            
            if not self.host:
                errors.append("host不能为空")
            
            if not (1 <= self.port <= 65535):
                errors.append(f"port必须在1-65535范围内: {self.port}")
            
            if not self.database_url.startswith(('postgresql://', 'mysql://')):
                errors.append(f"database_url格式无效: {self.database_url}")
            
            if len(self.secret_key) < 16:
                errors.append("secret_key长度至少16位")
            
            if errors:
                raise ConfigError("配置验证失败:\n" + "\n".join(f"  - {e}" for e in errors))
    
    # 有效配置
    print("有效配置:")
    try:
        config = ValidatedConfig(
            host='localhost',
            port=8080,
            database_url='postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}',
            SECRET_KEY = os.getenv("JWT_SECRET", "default-secret")
        )
        print(f"  验证通过: {config.host}:{config.port}")
    except ConfigError as e:
        print(f"  验证失败: {e}")
    
    # 无效配置
    print("\n无效配置:")
    try:
        config = ValidatedConfig(
            host='',
            port=99999,
            database_url='invalid-url',
            SECRET_KEY = os.getenv("JWT_SECRET", "default-secret")
        )
    except ConfigError as e:
        print(f"{e}")


if __name__ == "__main__":
    demo_environment_variables()
    demo_dotenv()
    demo_config_class()
    demo_json_config()
    demo_config_hierarchy()
    demo_config_validation()
    print("\n[OK] 配置管理演示完成!")
