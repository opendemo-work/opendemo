"""
测试配置和共享Fixtures
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir():
    """创建临时测试目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config():
    """Mock配置服务"""
    config = Mock()
    config.get.side_effect = lambda key, default=None: {
        "output_directory": "opendemo_output",
        "user_demo_library": str(Path.home() / ".opendemo" / "demos"),
        "ai.api_key": "test-key",
        "ai.api_endpoint": "https://api.openai.com/v1/chat/completions",
        "ai.model": "gpt-4",
        "ai.temperature": 0.7,
        "ai.max_tokens": 4000,
        "ai.timeout": 60,
        "ai.retry_times": 3,
        "ai.retry_interval": 5,
        "enable_verification": False,
        "verification_method": "venv",
        "verification_timeout": 300,
    }.get(key, default)
    return config


@pytest.fixture(scope="session")
def sample_demo_data():
    """示例demo数据"""
    return {
        "metadata": {
            "name": "test-demo",
            "language": "python",
            "keywords": ["test", "demo"],
            "description": "A test demo",
            "difficulty": "beginner",
            "author": "test",
            "version": "1.0.0",
            "dependencies": {},
            "verified": False,
        },
        "files": [
            {
                "path": "README.md",
                "content": "# Test Demo\n\nThis is a test demo.",
            },
            {
                "path": "code/main.py",
                "content": 'print("Hello, World!")\n',
            },
            {
                "path": "metadata.json",
                "content": json.dumps({
                    "name": "test-demo",
                    "language": "python",
                    "keywords": ["test"],
                }),
            },
        ],
    }


@pytest.fixture(scope="session")
def sample_metadata():
    """示例元数据"""
    return {
        "name": "example-demo",
        "language": "python",
        "keywords": ["example", "test"],
        "description": "An example demo for testing",
        "difficulty": "beginner",
        "author": "Test Author",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
        "version": "1.0.0",
        "dependencies": {},
        "verified": True,
    }


@pytest.fixture
def mock_ai_response():
    """Mock AI API响应"""
    return {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "metadata": {
                        "name": "ai-generated-demo",
                        "folder_name": "generated-demo",
                        "language": "python",
                        "keywords": ["ai", "test"],
                        "description": "AI generated test demo",
                        "difficulty": "beginner",
                        "dependencies": {},
                    },
                    "files": [
                        {
                            "path": "README.md",
                            "content": "# AI Generated Demo",
                        },
                        {
                            "path": "code/main.py",
                            "content": "print('AI generated')",
                        },
                    ],
                })
            }
        }]
    }


@pytest.fixture
def mock_storage(temp_dir, mock_config):
    """Mock存储服务"""
    from opendemo.services.storage_service import StorageService
    
    storage = Mock(spec=StorageService)
    storage.builtin_library_path = temp_dir / "builtin"
    storage.user_library_path = temp_dir / "user"
    storage.builtin_library_path.mkdir(parents=True, exist_ok=True)
    storage.user_library_path.mkdir(parents=True, exist_ok=True)
    
    storage.get_output_directory.return_value = temp_dir / "output"
    storage.list_demos.return_value = []
    storage.load_demo_metadata.return_value = None
    storage.save_demo.return_value = True
    storage.copy_demo.return_value = True
    storage.delete_demo.return_value = True
    
    return storage
"""
测试配置和共享Fixtures
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir():
    """创建临时测试目录"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config():
    """Mock配置服务"""
    config = Mock()
    config.get.side_effect = lambda key, default=None: {
        "output_directory": "opendemo_output",
        "user_demo_library": str(Path.home() / ".opendemo" / "demos"),
        "ai.api_key": "test-key",
        "ai.api_endpoint": "https://api.openai.com/v1/chat/completions",
        "ai.model": "gpt-4",
        "ai.temperature": 0.7,
        "ai.max_tokens": 4000,
        "ai.timeout": 60,
        "ai.retry_times": 3,
        "ai.retry_interval": 5,
        "enable_verification": False,
        "verification_method": "venv",
        "verification_timeout": 300,
    }.get(key, default)
    return config


@pytest.fixture(scope="session")
def sample_demo_data():
    """示例demo数据"""
    return {
        "metadata": {
            "name": "test-demo",
            "language": "python",
            "keywords": ["test", "demo"],
            "description": "A test demo",
            "difficulty": "beginner",
            "author": "test",
            "version": "1.0.0",
            "dependencies": {},
            "verified": False,
        },
        "files": [
            {
                "path": "README.md",
                "content": "# Test Demo\n\nThis is a test demo.",
            },
            {
                "path": "code/main.py",
                "content": 'print("Hello, World!")\n',
            },
            {
                "path": "metadata.json",
                "content": json.dumps({
                    "name": "test-demo",
                    "language": "python",
                    "keywords": ["test"],
                }),
            },
        ],
    }


@pytest.fixture(scope="session")
def sample_metadata():
    """示例元数据"""
    return {
        "name": "example-demo",
        "language": "python",
        "keywords": ["example", "test"],
        "description": "An example demo for testing",
        "difficulty": "beginner",
        "author": "Test Author",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
        "version": "1.0.0",
        "dependencies": {},
        "verified": True,
    }


@pytest.fixture
def mock_ai_response():
    """Mock AI API响应"""
    return {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "metadata": {
                        "name": "ai-generated-demo",
                        "folder_name": "generated-demo",
                        "language": "python",
                        "keywords": ["ai", "test"],
                        "description": "AI generated test demo",
                        "difficulty": "beginner",
                        "dependencies": {},
                    },
                    "files": [
                        {
                            "path": "README.md",
                            "content": "# AI Generated Demo",
                        },
                        {
                            "path": "code/main.py",
                            "content": "print('AI generated')",
                        },
                    ],
                })
            }
        }]
    }


@pytest.fixture
def mock_storage(temp_dir, mock_config):
    """Mock存储服务"""
    from opendemo.services.storage_service import StorageService
    
    storage = Mock(spec=StorageService)
    storage.builtin_library_path = temp_dir / "builtin"
    storage.user_library_path = temp_dir / "user"
    storage.builtin_library_path.mkdir(parents=True, exist_ok=True)
    storage.user_library_path.mkdir(parents=True, exist_ok=True)
    
    storage.get_output_directory.return_value = temp_dir / "output"
    storage.list_demos.return_value = []
    storage.load_demo_metadata.return_value = None
    storage.save_demo.return_value = True
    storage.copy_demo.return_value = True
    storage.delete_demo.return_value = True
    
    return storage
