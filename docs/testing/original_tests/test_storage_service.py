"""
StorageService 单元测试
"""

import pytest
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from opendemo.services.storage_service import StorageService


class TestStorageServiceInit:
    """StorageService 初始化测试"""

    def test_init(self, mock_config):
        """测试初始化"""
        storage = StorageService(mock_config)
        assert storage.config == mock_config
        assert storage._builtin_library_path is None
        assert storage._user_library_path is None


class TestStorageServicePaths:
    """路径管理测试"""

    def test_builtin_library_path(self, mock_config):
        """测试获取内置库路径"""
        storage = StorageService(mock_config)
        path = storage.builtin_library_path
        
        assert path is not None
        assert isinstance(path, Path)
        # 缓存测试
        assert storage.builtin_library_path is path

    def test_user_library_path(self, mock_config, temp_dir):
        """测试获取用户库路径"""
        mock_config.get.side_effect = lambda key, default=None: {
            "user_demo_library": str(temp_dir / "user_demos")
        }.get(key, default)
        
        storage = StorageService(mock_config)
        path = storage.user_library_path
        
        assert path == temp_dir / "user_demos"
        assert path.exists()  # 应该自动创建

    def test_get_output_directory(self, mock_config, temp_dir):
        """测试获取输出目录"""
        mock_config.get.side_effect = lambda key, default=None: {
            "output_directory": str(temp_dir / "output")
        }.get(key, default)
        
        storage = StorageService(mock_config)
        output_dir = storage.get_output_directory()
        
        assert output_dir == temp_dir / "output"
        assert output_dir.exists()


class TestStorageServiceList:
    """Demo列表测试"""

    def test_list_demos_empty(self, mock_config, temp_dir):
        """测试空demo库"""
        mock_config.get.side_effect = lambda key, default=None: {
            "user_demo_library": str(temp_dir / "user")
        }.get(key, default)
        
        with patch.object(StorageService, 'builtin_library_path', temp_dir / "builtin"):
            storage = StorageService(mock_config)
            demos = storage.list_demos()
            assert demos == []

    def test_list_demos_with_demos(self, mock_config, temp_dir, sample_metadata):
        """测试列出demo"""
        # 创建测试demo
        demo_path = temp_dir / "user" / "python" / "test-demo"
        demo_path.mkdir(parents=True)
        
        metadata_file = demo_path / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(sample_metadata, f)
        
        mock_config.get.side_effect = lambda key, default=None: {
            "user_demo_library": str(temp_dir / "user")
        }.get(key, default)
        
        with patch.object(StorageService, 'builtin_library_path', temp_dir / "builtin"):
            storage = StorageService(mock_config)
            demos = storage.list_demos(library="user")
            
            assert len(demos) == 1
            assert demos[0] == demo_path

    def test_list_demos_by_language(self, mock_config, temp_dir, sample_metadata):
        """测试按语言过滤"""
        # 创建Python demo
        py_demo = temp_dir / "user" / "python" / "py-demo"
        py_demo.mkdir(parents=True)
        (py_demo / "metadata.json").write_text(json.dumps(sample_metadata))
        
        # 创建Go demo
        go_demo = temp_dir / "user" / "go" / "go-demo"
        go_demo.mkdir(parents=True)
        (go_demo / "metadata.json").write_text(json.dumps({**sample_metadata, "language": "go"}))
        
        mock_config.get.side_effect = lambda key, default=None: {
            "user_demo_library": str(temp_dir / "user")
        }.get(key, default)
        
        with patch.object(StorageService, 'builtin_library_path', temp_dir / "builtin"):
            storage = StorageService(mock_config)
            
            # 只查询Python
            py_demos = storage.list_demos(library="user", language="python")
            assert len(py_demos) == 1
            assert py_demos[0] == py_demo

    def test_find_demos_in_path_nonexistent(self, mock_config):
        """测试不存在的路径"""
        storage = StorageService(mock_config)
        demos = storage._find_demos_in_path(Path("/nonexistent"))
        assert demos == []


class TestStorageServiceMetadata:
    """元数据操作测试"""

    def test_load_demo_metadata_success(self, mock_config, temp_dir, sample_metadata):
        """测试加载元数据成功"""
        demo_path = temp_dir / "demo"
        demo_path.mkdir()
        
        metadata_file = demo_path / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(sample_metadata, f)
        
        storage = StorageService(mock_config)
        metadata = storage.load_demo_metadata(demo_path)
        
        assert metadata is not None
        assert metadata["name"] == sample_metadata["name"]

    def test_load_demo_metadata_not_found(self, mock_config, temp_dir):
        """测试元数据文件不存在"""
        demo_path = temp_dir / "demo"
        demo_path.mkdir()
        
        storage = StorageService(mock_config)
        metadata = storage.load_demo_metadata(demo_path)
        
        assert metadata is None

    def test_load_demo_metadata_invalid_json(self, mock_config, temp_dir):
        """测试无效的JSON"""
        demo_path = temp_dir / "demo"
        demo_path.mkdir()
        
        metadata_file = demo_path / "metadata.json"
        metadata_file.write_text("invalid json{")
        
        storage = StorageService(mock_config)
        metadata = storage.load_demo_metadata(demo_path)
        
        assert metadata is None


class TestStorageServiceSave:
    """保存Demo测试"""

    def test_save_demo_success(self, mock_config, temp_dir, sample_demo_data):
        """测试保存demo成功"""
        target_path = temp_dir / "saved_demo"
        
        storage = StorageService(mock_config)
        result = storage.save_demo(sample_demo_data, target_path)
        
        assert result is True
        assert target_path.exists()
        assert (target_path / "metadata.json").exists()
        assert (target_path / "README.md").exists()
        assert (target_path / "code" / "main.py").exists()

    def test_save_demo_creates_nested_dirs(self, mock_config, temp_dir):
        """测试保存demo创建嵌套目录"""
        target_path = temp_dir / "a" / "b" / "c" / "demo"
        demo_data = {
            "metadata": {"name": "test"},
            "files": [{"path": "deep/nested/file.txt", "content": "test"}]
        }
        
        storage = StorageService(mock_config)
        result = storage.save_demo(demo_data, target_path)
        
        assert result is True
        assert (target_path / "deep" / "nested" / "file.txt").exists()

    def test_save_demo_failure(self, mock_config, temp_dir):
        """测试保存失败"""
        # 使用只读路径模拟失败
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            storage = StorageService(mock_config)
            result = storage.save_demo({"metadata": {}, "files": []}, temp_dir / "demo")
            assert result is False


class TestStorageServiceCopy:
    """复制Demo测试"""

    def test_copy_demo_success(self, mock_config, temp_dir):
        """测试复制demo成功"""
        # 创建源demo
        source_path = temp_dir / "source"
        source_path.mkdir()
        (source_path / "file.txt").write_text("content")
        
        target_path = temp_dir / "target"
        
        storage = StorageService(mock_config)
        result = storage.copy_demo(source_path, target_path)
        
        assert result is True
        assert target_path.exists()
        assert (target_path / "file.txt").read_text() == "content"

    def test_copy_demo_overwrites_existing(self, mock_config, temp_dir):
        """测试复制覆盖已存在的demo"""
        source_path = temp_dir / "source"
        source_path.mkdir()
        (source_path / "new.txt").write_text("new content")
        
        target_path = temp_dir / "target"
        target_path.mkdir()
        (target_path / "old.txt").write_text("old content")
        
        storage = StorageService(mock_config)
        result = storage.copy_demo(source_path, target_path)
        
        assert result is True
        assert (target_path / "new.txt").exists()
        assert not (target_path / "old.txt").exists()

    def test_copy_demo_failure(self, mock_config, temp_dir):
        """测试复制失败"""
        source_path = temp_dir / "source"
        target_path = temp_dir / "target"
        
        storage = StorageService(mock_config)
        result = storage.copy_demo(source_path, target_path)
        
        assert result is False


class TestStorageServiceDelete:
    """删除Demo测试"""

    def test_delete_demo_success(self, mock_config, temp_dir):
        """测试删除demo成功"""
        demo_path = temp_dir / "demo"
        demo_path.mkdir()
        (demo_path / "file.txt").write_text("content")
        
        storage = StorageService(mock_config)
        result = storage.delete_demo(demo_path)
        
        assert result is True
        assert not demo_path.exists()

    def test_delete_demo_not_found(self, mock_config, temp_dir):
        """测试删除不存在的demo"""
        demo_path = temp_dir / "nonexistent"
        
        storage = StorageService(mock_config)
        result = storage.delete_demo(demo_path)
        
        assert result is False

    def test_delete_demo_failure(self, mock_config, temp_dir):
        """测试删除失败"""
        demo_path = temp_dir / "demo"
        demo_path.mkdir()
        
        with patch("shutil.rmtree", side_effect=PermissionError("Access denied")):
            storage = StorageService(mock_config)
            result = storage.delete_demo(demo_path)
            assert result is False


class TestStorageServiceFileOperations:
    """文件操作测试"""

    def test_read_file_success(self, mock_config, temp_dir):
        """测试读取文件成功"""
        file_path = temp_dir / "test.txt"
        file_path.write_text("test content", encoding="utf-8")
        
        storage = StorageService(mock_config)
        content = storage.read_file(file_path)
        
        assert content == "test content"

    def test_read_file_not_found(self, mock_config, temp_dir):
        """测试读取不存在的文件"""
        file_path = temp_dir / "nonexistent.txt"
        
        storage = StorageService(mock_config)
        content = storage.read_file(file_path)
        
        assert content is None

    def test_write_file_success(self, mock_config, temp_dir):
        """测试写入文件成功"""
        file_path = temp_dir / "output.txt"
        
        storage = StorageService(mock_config)
        result = storage.write_file(file_path, "new content")
        
        assert result is True
        assert file_path.read_text() == "new content"

    def test_write_file_creates_parent_dirs(self, mock_config, temp_dir):
        """测试写入文件创建父目录"""
        file_path = temp_dir / "a" / "b" / "c" / "file.txt"
        
        storage = StorageService(mock_config)
        result = storage.write_file(file_path, "content")
        
        assert result is True
        assert file_path.exists()

    def test_write_file_failure(self, mock_config, temp_dir):
        """测试写入文件失败"""
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            storage = StorageService(mock_config)
            result = storage.write_file(temp_dir / "file.txt", "content")
            assert result is False

    def test_ensure_directory_success(self, mock_config, temp_dir):
        """测试确保目录存在"""
        dir_path = temp_dir / "a" / "b" / "c"
        
        storage = StorageService(mock_config)
        result = storage.ensure_directory(dir_path)
        
        assert result is True
        assert dir_path.exists()
        assert dir_path.is_dir()

    def test_ensure_directory_failure(self, mock_config, temp_dir):
        """测试创建目录失败"""
        with patch.object(Path, "mkdir", side_effect=PermissionError("Access denied")):
            storage = StorageService(mock_config)
            result = storage.ensure_directory(temp_dir / "test")
            assert result is False


class TestStorageServiceMigration:
    """迁移功能测试"""

    def test_check_migration_status_not_migrated(self, mock_config, temp_dir):
        """测试检查迁移状态-未迁移"""
        mock_config.get.side_effect = lambda key, default=None: {
            "output_directory": str(temp_dir / "output")
        }.get(key, default)
        
        storage = StorageService(mock_config)
        status = storage.check_migration_status()
        
        assert status is False

    def test_check_migration_status_migrated(self, mock_config, temp_dir):
        """测试检查迁移状态-已迁移"""
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        (output_dir / ".migration_completed").write_text("{}")
        
        mock_config.get.side_effect = lambda key, default=None: {
            "output_directory": str(output_dir)
        }.get(key, default)
        
        storage = StorageService(mock_config)
        status = storage.check_migration_status()
        
        assert status is True

    def test_migrate_builtin_libraries_already_migrated(self, mock_config, temp_dir):
        """测试已迁移的情况"""
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        (output_dir / ".migration_completed").write_text("{}")
        
        mock_config.get.side_effect = lambda key, default=None: {
            "output_directory": str(output_dir)
        }.get(key, default)
        
        storage = StorageService(mock_config)
        result = storage.migrate_builtin_libraries()
        
        assert result is True

    def test_migrate_builtin_libraries_success(self, mock_config, temp_dir):
        """测试迁移内置库成功"""
        # 创建内置库结构
        builtin_path = temp_dir / "builtin"
        python_lib = builtin_path / "python" / "libraries" / "numpy" / "array-creation"
        python_lib.mkdir(parents=True)
        (python_lib / "metadata.json").write_text(json.dumps({"name": "array-creation"}))
        
        output_dir = temp_dir / "output"
        
        mock_config.get.side_effect = lambda key, default=None: {
            "output_directory": str(output_dir)
        }.get(key, default)
        
        with patch.object(StorageService, 'builtin_library_path', builtin_path):
            storage = StorageService(mock_config)
            result = storage.migrate_builtin_libraries()
            
            assert result is True
            assert (output_dir / ".migration_completed").exists()
            assert (output_dir / "python" / "libraries" / "numpy" / "array-creation").exists()

    def test_migrate_builtin_libraries_failure(self, mock_config, temp_dir):
        """测试迁移失败"""
        builtin_path = temp_dir / "builtin"
        builtin_path.mkdir()
        
        mock_config.get.side_effect = lambda key, default=None: {
            "output_directory": str(temp_dir / "output")
        }.get(key, default)
        
        with patch.object(StorageService, 'builtin_library_path', builtin_path):
            with patch.object(Path, "iterdir", side_effect=PermissionError("Access denied")):
                storage = StorageService(mock_config)
                result = storage.migrate_builtin_libraries()
                assert result is False
