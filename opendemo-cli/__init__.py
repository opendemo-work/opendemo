"""
Open Demo CLI - 智能化的编程学习辅助CLI工具

提供快速获取、搜索和创建高质量可执行demo代码的功能。
"""

__version__ = "0.1.0"
__author__ = "Open Demo Contributors"

# 设置正确的包导入路径
import sys
from pathlib import Path
_package_root = Path(__file__).parent
if str(_package_root) not in sys.path:
    sys.path.insert(0, str(_package_root))

# 延迟导入以避免循环依赖
def __getattr__(name):
    """延迟导入机制"""
    if name == "DemoRepository":
        from .core.demo_repository import DemoRepository
        return DemoRepository
    elif name == "Demo":
        from .core.demo_repository import Demo
        return Demo
    elif name == "DemoSearch":
        from .core.demo_search import DemoSearch
        return DemoSearch
    elif name == "ConfigService":
        from .services.config_service import ConfigService
        return ConfigService
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Backward compatibility aliases
@property
def DemoManager(self):
    from .core.demo_repository import DemoRepository
    return DemoRepository

@property
def SearchEngine(self):
    from .core.demo_search import DemoSearch
    return DemoSearch

__all__ = [
    "DemoRepository",
    "Demo",
    "DemoSearch",
    "ConfigService",
    "DemoManager",  # Alias
    "SearchEngine",  # Alias
]
