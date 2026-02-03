"""
DemoGenerator单元测试
"""

from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from opendemo.core.demo_generator import DemoGenerator
from opendemo.core.demo_repository import Demo


class TestDemoGenerator:
    """DemoGenerator测试类"""

    def test_init(self):
        """测试初始化"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        generator = DemoGenerator(ai_service, repository, config)

        assert generator.ai_service == ai_service
        assert generator.repository == repository
        assert generator.config == config

    def test_generate_success(self):
        """测试成功生成demo"""
        # 准备mock对象
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        # 配置mock返回值
        config.get.return_value = "TestAuthor"

        demo_data = {
            "metadata": {
                "name": "test-demo",
                "keywords": ["test", "demo"],
                "description": "Test description",
                "folder_name": "test-folder",
            },
            "files": [{"name": "main.py", "content": "print('hello')"}],
        }
        ai_service.generate_demo.return_value = demo_data

        mock_demo = Mock(spec=Demo)
        mock_demo.path = Path("/test/path")
        mock_demo.name = "test-demo"
        repository.create_demo.return_value = mock_demo
        repository.get_demo_files.return_value = ["main.py"]

        generator = DemoGenerator(ai_service, repository, config)

        # 执行生成
        result = generator.generate("python", "test topic", "beginner")

        # 验证结果
        assert result is not None
        assert result["demo"] == mock_demo
        assert result["language"] == "python"
        assert result["topic"] == "test topic"
        assert result["verified"] is False

        # 验证调用
        ai_service.generate_demo.assert_called_once_with("python", "test topic", "beginner")
        repository.create_demo.assert_called_once()

    def test_generate_with_library(self):
        """测试包含第三方库的demo生成"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        config.get.return_value = "TestAuthor"

        demo_data = {
            "metadata": {
                "name": "numpy-demo",
                "keywords": ["numpy", "array"],
                "description": "Numpy demo",
            },
            "files": [{"name": "main.py", "content": "import numpy"}],
        }
        ai_service.generate_demo.return_value = demo_data

        mock_demo = Mock(spec=Demo)
        mock_demo.path = Path("/test/numpy-demo")
        repository.create_demo.return_value = mock_demo
        repository.get_demo_files.return_value = ["main.py"]

        generator = DemoGenerator(ai_service, repository, config)

        # 生成库demo
        result = generator.generate(
            "python", "array operations", "beginner", library_name="numpy"
        )

        assert result is not None
        # 验证create_demo被调用时包含library_name
        call_args = repository.create_demo.call_args
        assert call_args[1]["library_name"] == "numpy"

    def test_generate_ai_failure(self):
        """测试AI服务失败的处理"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        # AI返回None表示失败
        ai_service.generate_demo.return_value = None

        generator = DemoGenerator(ai_service, repository, config)

        result = generator.generate("python", "test", "beginner")

        assert result is None

    def test_generate_parse_error(self):
        """测试解析AI响应失败"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        # AI返回空数据（空字典视为失败）
        ai_service.generate_demo.return_value = {}
        config.get.return_value = "TestAuthor"

        generator = DemoGenerator(ai_service, repository, config)

        result = generator.generate("python", "test", "beginner")

        # 空数据应该返回None表示失败
        assert result is None

    def test_generate_save_error(self):
        """测试保存demo失败"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        config.get.return_value = "TestAuthor"

        demo_data = {
            "metadata": {"name": "test"},
            "files": [{"name": "main.py", "content": ""}],
        }
        ai_service.generate_demo.return_value = demo_data

        # repository创建失败
        repository.create_demo.return_value = None

        generator = DemoGenerator(ai_service, repository, config)

        result = generator.generate("python", "test", "beginner")

        assert result is None

    def test_generate_custom_folder_name(self):
        """测试自定义文件夹名"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        config.get.return_value = "TestAuthor"

        demo_data = {
            "metadata": {"name": "test"},
            "files": [],
        }
        ai_service.generate_demo.return_value = demo_data

        mock_demo = Mock(spec=Demo)
        mock_demo.path = Path("/test/custom-name")
        repository.create_demo.return_value = mock_demo
        repository.get_demo_files.return_value = []

        generator = DemoGenerator(ai_service, repository, config)

        result = generator.generate(
            "python", "test", "beginner", custom_folder_name="custom-name"
        )

        assert result is not None
        # 验证custom_folder_name被传递
        call_args = repository.create_demo.call_args
        assert call_args[1]["custom_folder_name"] == "custom-name"

    def test_regenerate_success(self):
        """测试成功重新生成"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()
        storage = Mock()

        config.get.return_value = "TestAuthor"
        repository.storage = storage

        # 模拟已存在的demo
        existing_demo = Mock(spec=Demo)
        existing_demo.language = "python"
        existing_demo.name = "old-demo"
        existing_demo.difficulty = "beginner"
        repository.load_demo.return_value = existing_demo

        # 模拟生成新demo
        demo_data = {
            "metadata": {"name": "new-demo"},
            "files": [],
        }
        ai_service.generate_demo.return_value = demo_data

        new_demo = Mock(spec=Demo)
        new_demo.path = Path("/test/new-demo")
        repository.create_demo.return_value = new_demo
        repository.get_demo_files.return_value = []

        generator = DemoGenerator(ai_service, repository, config)

        demo_path = Path("/test/old-demo")
        result = generator.regenerate(demo_path, "intermediate")

        assert result is not None
        # 验证删除旧demo
        storage.delete_demo.assert_called_once_with(demo_path)
        # 验证生成新demo
        ai_service.generate_demo.assert_called_once_with(
            "python", "old-demo", "intermediate"
        )

    def test_regenerate_metadata_not_found(self):
        """测试metadata.json不存在"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        # load_demo返回None表示未找到
        repository.load_demo.return_value = None

        generator = DemoGenerator(ai_service, repository, config)

        result = generator.regenerate(Path("/nonexistent"), "beginner")

        assert result is None

    def test_regenerate_keep_difficulty(self):
        """测试重新生成时保持难度"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()
        storage = Mock()

        config.get.return_value = "TestAuthor"
        repository.storage = storage

        existing_demo = Mock(spec=Demo)
        existing_demo.language = "go"
        existing_demo.name = "test-demo"
        existing_demo.difficulty = "advanced"
        repository.load_demo.return_value = existing_demo

        demo_data = {"metadata": {"name": "test"}, "files": []}
        ai_service.generate_demo.return_value = demo_data

        new_demo = Mock(spec=Demo)
        new_demo.path = Path("/test/new")
        repository.create_demo.return_value = new_demo
        repository.get_demo_files.return_value = []

        generator = DemoGenerator(ai_service, repository, config)

        # 不指定新难度
        result = generator.regenerate(Path("/test/old"), None)

        assert result is not None
        # 验证使用原有难度
        ai_service.generate_demo.assert_called_once_with("go", "test-demo", "advanced")

    def test_generate_metadata_enrichment(self):
        """测试元数据补充"""
        ai_service = Mock()
        repository = Mock()
        config = Mock()

        # 配置作者信息
        config.get.return_value = "John Doe"

        demo_data = {
            "metadata": {"name": "test"},
            "files": [],
        }
        ai_service.generate_demo.return_value = demo_data

        mock_demo = Mock(spec=Demo)
        mock_demo.path = Path("/test/path")
        repository.create_demo.return_value = mock_demo
        repository.get_demo_files.return_value = []

        generator = DemoGenerator(ai_service, repository, config)

        with patch("opendemo.core.demo_generator.datetime") as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = "2024-01-01T00:00:00"
            result = generator.generate("python", "test", "beginner")

        assert result is not None
        # 验证create_demo调用时的作者参数
        call_args = repository.create_demo.call_args
        assert call_args[1]["author"] == "John Doe"
