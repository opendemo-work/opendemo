"""
Open Demo CLI - 智能化的编程学习辅助CLI工具

提供快速获取、搜索和创建高质量可执行demo代码的功能。
"""

__version__ = "0.1.0"
__author__ = "Open Demo Contributors"

from opendemo.core.demo_manager import DemoManager
from opendemo.core.search_engine import SearchEngine
from opendemo.services.config_service import ConfigService

__all__ = [
    "DemoManager",
    "SearchEngine",
    "ConfigService",
]
