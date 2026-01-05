"""
CLI模块单元测试
"""

import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from click.testing import CliRunner
import tempfile

from opendemo.cli import (
    cli,
    _scan_output_demos,
    _match_demo_in_output,
    _display_output_demo,
)


class TestCLIBasic:
    """CLI基础测试"""

    def test_cli_help(self):
        """测试--help选项"""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        
        assert result.exit_code == 0
        assert "Open Demo" in result.output
        assert "search" in result.output
        assert "get" in result.output
        assert "new" in result.output

    def test_cli_version(self):
        """测试--version选项"""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestScanOutputDemos:
    """_scan_output_demos函数测试"""

    def test_scan_output_demos_empty(self):
        """测试扫描空目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            result = _scan_output_demos(output_dir, "python")
            
            assert result == []

    def test_scan_output_demos_with_metadata(self):
        """测试扫描带metadata的demo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lang_dir = output_dir / "python"
            demo_dir = lang_dir / "test-demo"
            demo_dir.mkdir(parents=True)
            
            # 创建metadata.json
            metadata = {
                "name": "test-demo",
                "language": "python",
                "keywords": ["test", "demo"],
                "description": "Test demo",
                "difficulty": "beginner"
            }
            metadata_file = demo_dir / "metadata.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f)
            
            result = _scan_output_demos(output_dir, "python")
            
            assert len(result) == 1
            assert result[0]["name"] == "test-demo"
            assert result[0]["language"] == "python"
            assert result[0]["keywords"] == ["test", "demo"]

    def test_scan_output_demos_without_metadata(self):
        """测试扫描没有metadata的demo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lang_dir = output_dir / "python"
            demo_dir = lang_dir / "test-demo"
            demo_dir.mkdir(parents=True)
            
            result = _scan_output_demos(output_dir, "python")
            
            assert len(result) == 1
            assert result[0]["name"] == "test-demo"
            assert result[0]["difficulty"] == "unknown"

    def test_scan_output_demos_invalid_metadata(self):
        """测试扫描metadata无效的demo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lang_dir = output_dir / "python"
            demo_dir = lang_dir / "test-demo"
            demo_dir.mkdir(parents=True)
            
            # 创建无效的metadata.json
            metadata_file = demo_dir / "metadata.json"
            with open(metadata_file, "w") as f:
                f.write("invalid json{")
            
            result = _scan_output_demos(output_dir, "python")
            
            assert len(result) == 1
            assert result[0]["name"] == "test-demo"


class TestMatchDemoInOutput:
    """_match_demo_in_output函数测试"""

    def test_match_demo_exact_name(self):
        """测试精确匹配demo名称"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lang_dir = output_dir / "python"
            demo_dir = lang_dir / "logging"
            demo_dir.mkdir(parents=True)
            
            result = _match_demo_in_output(output_dir, "python", ["logging"])
            
            assert result is not None
            assert result["name"] == "logging"

    def test_match_demo_partial_name(self):
        """测试部分匹配demo名称"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lang_dir = output_dir / "python"
            demo_dir = lang_dir / "python-logging-demo"
            demo_dir.mkdir(parents=True)
            
            result = _match_demo_in_output(output_dir, "python", ["logging"])
            
            assert result is not None
            assert "logging" in result["name"]

    def test_match_demo_by_keywords(self):
        """测试通过关键字匹配demo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            lang_dir = output_dir / "python"
            demo_dir = lang_dir / "my-demo"
            demo_dir.mkdir(parents=True)
            
            # 创建metadata.json with keywords
            metadata = {
                "name": "my-demo",
                "keywords": ["logging", "file"]
            }
            metadata_file = demo_dir / "metadata.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f)
            
            result = _match_demo_in_output(output_dir, "python", ["logging"])
            
            assert result is not None
            assert result["name"] == "my-demo"

    def test_match_demo_not_found(self):
        """测试未找到匹配的demo"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            
            result = _match_demo_in_output(output_dir, "python", ["nonexistent"])
            
            assert result is None


class TestDisplayOutputDemo:
    """_display_output_demo函数测试"""

    def test_display_output_demo_with_metadata(self):
        """测试显示带metadata的demo信息"""
        with tempfile.TemporaryDirectory() as tmpdir:
            demo_path = Path(tmpdir) / "test-demo"
            demo_path.mkdir()
            
            demo_info = {
                "name": "test-demo",
                "keywords": ["test"],
                "description": "Test demo"
            }
            
            # 应该不会抛出异常
            with patch("opendemo.cli.print_success"):
                _display_output_demo(demo_info, demo_path, "python")

    def test_display_output_demo_with_code_dir(self):
        """测试显示带code目录的demo信息"""
        with tempfile.TemporaryDirectory() as tmpdir:
            demo_path = Path(tmpdir) / "test-demo"
            code_dir = demo_path / "code"
            code_dir.mkdir(parents=True)
            
            # 创建一些文件
            (code_dir / "main.py").write_text("print('hello')")
            
            demo_info = {
                "name": "test-demo",
                "keywords": [],
                "description": ""
            }
            
            with patch("opendemo.cli.print_success"):
                _display_output_demo(demo_info, demo_path, "python")


class TestSearchCommand:
    """search命令测试"""

    def test_search_command_help(self):
        """测试search命令帮助"""
        runner = CliRunner()
        result = runner.invoke(cli, ["search", "--help"])
        
        assert result.exit_code == 0
        assert "search" in result.output.lower()


class TestGetCommand:
    """get命令测试"""

    def test_get_unsupported_language(self):
        """测试不支持的语言"""
        runner = CliRunner()
        result = runner.invoke(cli, ["get", "rust", "test"])
        
        assert result.exit_code != 0
        assert "不支持的语言" in result.output

    def test_get_missing_keyword(self):
        """测试缺少关键字参数"""
        runner = CliRunner()
        result = runner.invoke(cli, ["get", "python"])
        
        assert result.exit_code != 0


class TestNewCommand:
    """new命令测试"""

    def test_new_unsupported_language(self):
        """测试不支持的语言"""
        runner = CliRunner()
        result = runner.invoke(cli, ["new", "rust", "test"])
        
        assert result.exit_code != 0
        assert "不支持的语言" in result.output

    def test_new_missing_topic(self):
        """测试缺少主题参数"""
        runner = CliRunner()
        result = runner.invoke(cli, ["new", "python"])
        
        assert result.exit_code != 0


class TestConfigCommand:
    """config命令测试"""

    def test_config_list(self):
        """测试config list命令"""
        runner = CliRunner()
        
        with patch("opendemo.cli.ConfigService") as mock_config_cls:
            mock_config = Mock()
            mock_config.get_all.return_value = {
                "output_directory": "opendemo_output",
                "ai": {"model": "gpt-4"}
            }
            mock_config_cls.return_value = mock_config
            
            result = runner.invoke(cli, ["config", "list"])
            
            assert result.exit_code == 0

    def test_config_get(self):
        """测试config get命令"""
        runner = CliRunner()
        
        with patch("opendemo.cli.ConfigService") as mock_config_cls:
            mock_config = Mock()
            mock_config.get.return_value = "opendemo_output"
            mock_config_cls.return_value = mock_config
            
            result = runner.invoke(cli, ["config", "get", "output_directory"])
            
            assert result.exit_code == 0
            assert "opendemo_output" in result.output

    def test_config_set(self):
        """测试config set命令"""
        runner = CliRunner()
        
        with patch("opendemo.cli.ConfigService") as mock_config_cls:
            mock_config = Mock()
            mock_config_cls.return_value = mock_config
            
            result = runner.invoke(cli, ["config", "set", "ai.model", "gpt-3.5-turbo"])
            
            assert result.exit_code == 0
