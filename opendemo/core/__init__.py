"""Core business logic modules"""

from opendemo.core.demo_repository import DemoRepository, Demo
from opendemo.core.demo_search import DemoSearch
from opendemo.core.demo_generator import DemoGenerator
from opendemo.core.demo_verifier import DemoVerifier

# Backward compatibility aliases
DemoManager = DemoRepository
SearchEngine = DemoSearch

__all__ = [
    'DemoRepository',
    'Demo',
    'DemoSearch',
    'DemoGenerator',
    'DemoVerifier',
    'DemoManager',  # Alias
    'SearchEngine',  # Alias
]
