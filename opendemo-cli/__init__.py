"""
Open Demo CLI - 智能化的编程学习辅助CLI工具

提供快速获取、搜索和创建高质量可执行demo代码的功能。
"""

__version__ = "0.1.0"
__author__ = "Open Demo Contributors"

from opendemo.core.demo_repository import DemoRepository, Demo
from opendemo.core.demo_search import DemoSearch
from opendemo.services.config_service import ConfigService

# Backward compatibility aliases
DemoManager = DemoRepository
SearchEngine = DemoSearch

__all__ = [
    "DemoRepository",
    "Demo",
    "DemoSearch",
    "ConfigService",
    "DemoManager",  # Alias
    "SearchEngine",  # Alias
]
