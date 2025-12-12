"""Core business logic modules"""

from opendemo.core.demo_repository import DemoRepository, Demo
from opendemo.core.demo_search import DemoSearch
from opendemo.core.demo_generator import DemoGenerator
from opendemo.core.demo_verifier import DemoVerifier
from opendemo.core.readme_updater import ReadmeUpdater

# Backward compatibility aliases
DemoManager = DemoRepository
SearchEngine = DemoSearch

__all__ = [
    'DemoRepository',
    'Demo',
    'DemoSearch',
    'DemoGenerator',
    'DemoVerifier',
    'ReadmeUpdater',
    'DemoManager',  # Alias
    'SearchEngine',  # Alias
]
