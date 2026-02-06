"""Core business logic modules"""

# 修复导入路径
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.demo_repository import DemoRepository, Demo
from core.demo_search import DemoSearch
from core.demo_generator import DemoGenerator
from core.demo_verifier import DemoVerifier
from core.readme_updater import ReadmeUpdater
from core.quality_checker import QualityChecker

# Backward compatibility aliases
DemoManager = DemoRepository
SearchEngine = DemoSearch

__all__ = [
    "DemoRepository",
    "Demo",
    "DemoSearch",
    "DemoGenerator",
    "DemoVerifier",
    "ReadmeUpdater",
    "QualityChecker",
    "DemoManager",  # Alias
    "SearchEngine",  # Alias
]
