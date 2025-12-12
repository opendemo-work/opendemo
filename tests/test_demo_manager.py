"""
DemoRepository 和 Demo 类单元测试
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock

from opendemo.core.demo_repository import Demo, DemoRepository


class TestDemo:
    """Demo 类测试"""
    
    def test_demo_init(self):
        """测试 Demo 初始化"""
        path = Path("/test/demo")
        metadata = {
            'name': 'test-demo',
            'language': 'python',
            'keywords': ['test', 'demo'],
            'description': 'A test demo',
            'difficulty': 'beginner',
            'verified': True
        }
        
        demo = Demo(path, metadata)
        
        assert demo.path == path
        assert demo.metadata == metadata
    
    def test_demo_properties(self):
        """测试 Demo 属性"""
        path = Path("/test/demo")
        metadata = {
            'name': 'test-demo',
            'language': 'python',
            'keywords': ['test', 'demo'],
            'description': 'A test demo',
            'difficulty': 'intermediate',
            'verified': True
        }
        
        demo = Demo(path, metadata)
        
        assert demo.name == 'test-demo'
        assert demo.language == 'python'
        assert demo.keywords == ['test', 'demo']
        assert demo.description == 'A test demo'
        assert demo.difficulty == 'intermediate'
        assert demo.verified is True
    
    def test_demo_default_properties(self):
        """测试 Demo 默认属性"""
        path = Path("/test/demo")
        metadata = {}  # 空元数据
        
        demo = Demo(path, metadata)
        
        # 应使用默认值
        assert demo.name == 'demo'  # 使用路径名
        assert demo.language == 'unknown'
        assert demo.keywords == []
        assert demo.description == ''
        assert demo.difficulty == 'beginner'
        assert demo.verified is False
    
    def test_demo_to_dict(self):
        """测试 Demo 转字典"""
        path = Path("/test/demo")
        metadata = {
            'name': 'test-demo',
            'language': 'python',
            'keywords': ['test'],
            'description': 'Test',
            'difficulty': 'beginner',
            'verified': False
        }
        
        demo = Demo(path, metadata)
        result = demo.to_dict()
        
        assert isinstance(result, dict)
        assert result['name'] == 'test-demo'
        assert result['language'] == 'python'
        assert 'path' in result
        assert 'metadata' in result


class TestDemoRepository:
    """DemoRepository 类测试"""
    
    def test_init(self):
        """测试 DemoRepository 初始化"""
        mock_storage = Mock()
        repository = DemoRepository(mock_storage)
        
        assert repository.storage == mock_storage
        assert repository._demo_cache == {}
    
    def test_generate_safe_name(self):
        """测试生成 demo 目录名（纯ASCII英文）"""
        mock_storage = Mock()
        repository = DemoRepository(mock_storage)
        
        # 测试正常名称
        name = repository._generate_safe_name("Hello World", "python")
        assert name == "python-hello-world"
        
        # 测试带特殊字符
        name = repository._generate_safe_name("Test_Demo!", "java")
        assert name == "java-test-demo"
        
        # 测试中文名称（应该过滤掉中文）
        name = repository._generate_safe_name("并发编程goroutines", "go")
        assert name == "go-goroutines"
        
        # 测试纯中文（应该返回默认名称）
        name = repository._generate_safe_name("中文主题", "nodejs")
        assert name == "nodejs-demo"
    
    def test_get_file_description(self):
        """测试获取文件描述"""
        mock_storage = Mock()
        repository = DemoRepository(mock_storage)
        
        # 测试各种文件类型
        assert repository._get_file_description(Path("README.md")) == '实操指南'
        assert repository._get_file_description(Path("metadata.json")) == 'Demo元数据'
        assert repository._get_file_description(Path("requirements.txt")) == 'Python依赖'
        assert repository._get_file_description(Path("pom.xml")) == 'Java依赖'
        assert repository._get_file_description(Path("test.py")) == 'Python代码'
        assert repository._get_file_description(Path("Main.java")) == 'Java代码'
        assert repository._get_file_description(Path("other.txt")) == '其他文件'
    
    def test_load_demo_with_cache(self):
        """测试加载 demo 使用缓存"""
        mock_storage = Mock()
        mock_storage.load_demo_metadata.return_value = {'name': 'test'}
        
        repository = DemoRepository(mock_storage)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            demo_path = Path(temp_dir) / "test-demo"
            demo_path.mkdir()
            
            # 第一次加载
            demo1 = repository.load_demo(demo_path)
            assert demo1 is not None
            
            # 第二次加载应使用缓存
            demo2 = repository.load_demo(demo_path)
            assert demo2 is demo1
            
            # storage 只调用一次
            assert mock_storage.load_demo_metadata.call_count == 1
    
    def test_load_demo_not_found(self):
        """测试加载不存在的 demo"""
        mock_storage = Mock()
        mock_storage.load_demo_metadata.return_value = None
        
        repository = DemoRepository(mock_storage)
        
        demo = repository.load_demo(Path("/nonexistent/demo"))
        assert demo is None


class TestDemoRepositoryIntegration:
    """DemoRepository 集成测试"""
    
    def test_load_all_demos(self):
        """测试加载所有 demos"""
        mock_storage = Mock()
        mock_storage.list_demos.return_value = []
        
        repository = DemoRepository(mock_storage)
        demos = repository.load_all_demos()
        
        assert isinstance(demos, list)
        mock_storage.list_demos.assert_called_once()
