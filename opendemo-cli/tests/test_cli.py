"""
CLI 入口测试
"""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# 添加包路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli import cli
from services.config_service import ConfigService
from services.storage_service import StorageService
from core.demo_repository import DemoRepository
from core.demo_search import DemoSearch
from core.demo_generator import DemoGenerator
from core.demo_verifier import DemoVerifier


class TestCLI:
    """CLI测试类"""

    def setup_method(self):
        """设置测试环境"""
        self.runner = CliRunner()

    def test_cli_version(self):
        """测试版本命令"""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert 'version' in result.output.lower()

    def test_cli_help(self):
        """测试帮助命令"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Open Demo' in result.output

    def test_cli_no_args(self):
        """测试无参数默认行为"""
        result = self.runner.invoke(cli)
        assert result.exit_code == 0
        assert 'Usage' in result.output

    def test_search_all_languages(self):
        """测试搜索所有语言"""
        with patch('cli._scan_output_demos') as mock_scan:
            mock_scan.return_value = []
            result = self.runner.invoke(cli, ['search'])
            assert result.exit_code == 0
            assert '可用的语言:' in result.output

    def test_search_specific_language(self):
        """测试搜索特定语言"""
        mock_demo = {
            'name': 'test-demo',
            'language': 'python',
            'keywords': ['test'],
            'description': 'Test demo',
            'difficulty': 'beginner',
            'verified': False
        }
        
        with patch('cli._scan_output_demos') as mock_scan:
            mock_scan.return_value = [mock_demo]
            result = self.runner.invoke(cli, ['search', 'python'])
            assert result.exit_code == 0
            assert 'test-demo' in result.output

    def test_search_with_keyword(self):
        """测试关键字搜索"""
        mock_demo = {
            'name': 'test-demo',
            'language': 'python',
            'keywords': ['test'],
            'description': 'Test demo',
            'difficulty': 'beginner',
            'verified': False
        }
        
        with patch('cli._scan_output_demos') as mock_scan:
            mock_scan.return_value = [mock_demo]
            result = self.runner.invoke(cli, ['search', 'python', 'test'])
            assert result.exit_code == 0
            assert 'test-demo' in result.output

    def test_get_existing_demo(self):
        """测试获取已存在的demo"""
        mock_demo = {
            'path': Path('test/path'),
            'name': 'test-demo',
            'language': 'python',
            'keywords': ['test'],
            'description': 'Test demo',
            'difficulty': 'beginner',
            'verified': False
        }
        
        with patch('cli._match_demo_in_output') as mock_match:
            mock_match.return_value = mock_demo
            result = self.runner.invoke(cli, ['get', 'python', 'test'])
            assert result.exit_code == 0
            assert 'Demo已存在!' in result.output

    def test_get_unsupported_language(self):
        """测试不支持的语言"""
        result = self.runner.invoke(cli, ['get', 'unsupported', 'test'])
        assert result.exit_code == 1
        assert '不支持的语言' in result.output

    def test_new_with_description(self):
        """测试使用描述生成demo"""
        mock_result = {
            'demo': Mock(),
            'path': 'test/path'
        }
        mock_result['demo'].name = 'test-demo'
        mock_result['demo'].language = 'python'
        mock_result['demo'].verified = False
        
        with patch('cli.ConfigService') as mock_config:
            mock_config_instance = Mock()
            mock_config_instance.get.side_effect = lambda key, default=None: {
                'ai.api_key': 'test-key',
                'enable_verification': False
            }.get(key, default)
            mock_config.return_value = mock_config_instance
        
        with patch('cli.StorageService') as mock_storage:
            mock_storage_instance = Mock()
            mock_storage_instance.get_output_directory.return_value = Path('test/output')
            mock_storage.return_value = mock_storage_instance
        
        with patch('cli.DemoRepository') as mock_repo:
            mock_repo_instance = Mock()
            mock_repo_instance.detect_library_for_new_command.return_value = None
            mock_repo.return_value = mock_repo_instance
        
        with patch('cli.AIService') as mock_ai:
            mock_ai_instance = Mock()
            mock_ai.return_value = mock_ai_instance
        
        with patch('cli.DemoGenerator') as mock_generator:
            mock_generator_instance = Mock()
            mock_generator_instance.generate.return_value = mock_result
            mock_generator.return_value = mock_generator_instance
        
        with patch('cli.DemoVerifier') as mock_verifier:
            mock_verifier_instance = Mock()
            mock_verifier.return_value = mock_verifier_instance
        
        with patch('cli._update_readme_after_new') as mock_update_readme:
            mock_update_readme.return_value = None
        
        with patch('cli._update_demo_list') as mock_update_list:
            mock_update_list.return_value = None

        result = self.runner.invoke(cli, ['new', 'python', 'test', 'demo'])
        assert result.exit_code == 0
        assert '成功生成demo' in result.output

    def test_config_list(self):
        """测试配置列表命令"""
        mock_config = {
            'ai.api_key': 'test-key',
            'output_directory': 'test/output'
        }
        
        with patch('cli.ConfigService') as mock_config_service:
            mock_config_instance = Mock()
            mock_config_instance.get_all.return_value = mock_config
            mock_config_service.return_value = mock_config_instance

        result = self.runner.invoke(cli, ['config', 'list'])
        assert result.exit_code == 0
        assert 'ai.api_key' in result.output

    def test_config_get(self):
        """测试获取配置命令"""
        with patch('cli.ConfigService') as mock_config_service:
            mock_config_instance = Mock()
            mock_config_instance.get.return_value = 'test-key'
            mock_config_service.return_value = mock_config_instance

        result = self.runner.invoke(cli, ['config', 'get', 'ai.api_key'])
        assert result.exit_code == 0
        assert 'ai.api_key = test-key' in result.output

    def test_config_set(self):
        """测试设置配置命令"""
        with patch('cli.ConfigService') as mock_config_service:
            mock_config_instance = Mock()
            mock_config_instance.set.return_value = None
            mock_config_service.return_value = mock_config_instance

        result = self.runner.invoke(cli, ['config', 'set', 'test.key', 'test-value'])
        assert result.exit_code == 0
        assert '已设置 test.key = test-value' in result.output

    def test_check_run(self):
        """测试质量检查命令"""
        mock_result = {
            'summary': {'overall_status': 'PASS'},
            'unit_tests': {'status': 'PASS', 'passed': 10, 'total': 10},
            'cli_tests': {'status': 'PASS', 'passed': 5, 'total': 5}
        }
        
        with patch('cli.QualityChecker') as mock_checker:
            mock_checker_instance = Mock()
            mock_checker_instance.run_all_checks.return_value = mock_result
            mock_checker_instance.save_report.return_value = Path('test/report.json')
            mock_checker.return_value = mock_checker_instance

        result = self.runner.invoke(cli, ['check'])
        assert result.exit_code == 0
        assert '质量检查通过!' in result.output
