"""
存储服务测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from services.storage_service import StorageService
from services.config_service import ConfigService


class TestStorageService:
    """存储服务测试类"""

    def setup_method(self):
        """设置测试环境"""
        self.config = Mock(spec=ConfigService)
        self.config.get.side_effect = lambda key, default=None: {
            'output_directory': 'test_output',
            'builtin_library_path': 'builtin_demos',
            'user_library_path': 'user_demos'
        }.get(key, default)
        self.storage = StorageService(self.config)

    def test_init(self):
        """测试初始化"""
        assert self.storage.config == self.config

    def test_builtin_library_path(self):
        """测试获取内置库路径"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            path = self.storage.builtin_library_path
            assert 'builtin_demos' in str(path)

    def test_user_library_path(self):
        """测试获取用户库路径"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            path = self.storage.user_library_path
            assert 'user_demos' in str(path)

    def test_list_demos(self):
        """测试列出所有demo"""
        # 模拟文件系统结构
        mock_lang_dir = Mock()
        mock_demo_dir = Mock()
        mock_demo_dir.name = 'test-demo'
        mock_lang_dir.iterdir.return_value = [mock_demo_dir]
        
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
        with patch('pathlib.Path.iterdir') as mock_iterdir:
            mock_iterdir.return_value = [mock_lang_dir]
        with patch('services.storage_service.StorageService._load_demo_metadata') as mock_load:
            mock_load.return_value = {'name': 'test-demo', 'language': 'python'}

        demos = self.storage.list_demos()
        assert len(demos) == 1
        assert demos[0].name == 'test-demo'

    def test_load_demo_metadata(self):
        """测试加载元数据"""
        mock_metadata = {'name': 'test', 'language': 'python'}
        
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
        with patch('builtins.open', new_callable=Mock) as mock_open:
            mock_file = Mock()
            mock_file.__enter__.return_value.read.return_value = '{"name": "test", "language": "python"}'
            mock_open.return_value = mock_file
        with patch('json.load') as mock_load:
            mock_load.return_value = mock_metadata

        metadata = self.storage._load_demo_metadata(Path('test'))
        assert metadata == mock_metadata

    def test_save_demo(self):
        """测试保存demo"""
        mock_demo = Mock()
        mock_demo.name = 'test-demo'
        mock_demo.language = 'python'
        mock_demo.code = 'print("Hello")'
        mock_demo.readme = '# Test'
        mock_demo.metadata = {'verified': False}

        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.return_value = None
        with patch('builtins.open', new_callable=Mock) as mock_open:
            mock_file = Mock()
            mock_file.__enter__.return_value.write.return_value = None
            mock_open.return_value = mock_file

        result = self.storage.save_demo(mock_demo)
        assert result is True

    def test_copy_demo(self):
        """测试复制demo"""
        with patch('shutil.copytree') as mock_copytree:
            mock_copytree.return_value = None
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True

        result = self.storage.copy_demo(Path('source'), Path('destination'))
        assert result is True

    def test_delete_demo(self):
        """测试删除demo"""
        with patch('shutil.rmtree') as mock_rmtree:
            mock_rmtree.return_value = None
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True

        result = self.storage.delete_demo(Path('test-demo'))
        assert result is True

    def test_get_output_directory(self):
        """测试获取输出目录"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True

        path = self.storage.get_output_directory()
        assert 'test_output' in str(path)

    def test_ensure_directory(self):
        """测试确保目录存在"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.side_effect = [False, True]
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.return_value = None

        result = self.storage._ensure_directory(Path('test-dir'))
        assert result is True
