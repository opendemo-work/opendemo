"""
质量检查器测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from core.quality_checker import QualityChecker


class TestQualityChecker:
    """质量检查器测试类"""

    def setup_method(self):
        """设置测试环境"""
        self.checker = QualityChecker()

    def test_init(self):
        """测试初始化"""
        assert self.checker.project_root is not None
        assert self.checker.check_dir is not None

    def test_run_all_checks(self):
        """测试完整检查流程"""
        with patch('core.quality_checker.QualityChecker.run_unit_tests') as mock_unit:
            mock_unit.return_value = {'status': 'PASS', 'passed': 10, 'total': 10, 'tests': []}
        with patch('core.quality_checker.QualityChecker.run_cli_tests') as mock_cli:
            mock_cli.return_value = {'status': 'PASS', 'passed': 5, 'total': 5, 'tests': []}

        result = self.checker.run_all_checks()
        assert result['summary']['overall_status'] == 'PASS'
        assert result['unit_tests']['status'] == 'PASS'
        assert result['cli_tests']['status'] == 'PASS'

    def test_run_unit_tests_success(self):
        """测试单元测试成功"""
        mock_output = """============================= test session starts ==============================
collected 10 items

 tests/test_example.py ...........                                   [100%]

============================== 10 passed in 0.12s ==============================
"""

        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = mock_output
            mock_result.stderr = ''
            mock_run.return_value = mock_result

        result = self.checker.run_unit_tests()
        assert result['status'] == 'PASS'
        assert result['passed'] == 10
        assert result['total'] == 10

    def test_run_unit_tests_timeout(self):
        """测试单元测试超时"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired('pytest', 10)

        result = self.checker.run_unit_tests()
        assert result['status'] == 'FAIL'
        assert 'timeout' in result['error'].lower()

    def test_run_unit_tests_error(self):
        """测试单元测试异常"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception('Test error')

        result = self.checker.run_unit_tests()
        assert result['status'] == 'FAIL'
        assert 'test error' in result['error'].lower()

    def test_run_cli_tests(self):
        """测试CLI测试执行"""
        with patch('core.quality_checker.QualityChecker.run_cli_command') as mock_run:
            mock_run.return_value = {'status': 'PASS', 'output': 'Test output'}

        result = self.checker.run_cli_tests()
        assert result['status'] == 'PASS'
        assert len(result['tests']) > 0

    def test_run_cli_command(self):
        """测试CLI命令执行"""
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = 'Test output'
            mock_result.stderr = ''
            mock_run.return_value = mock_result

        result = self.checker.run_cli_command('opendemo --version')
        assert result['status'] == 'PASS'
        assert result['output'] == 'Test output'

    def test_generate_summary(self):
        """测试生成摘要"""
        unit_result = {'status': 'PASS', 'passed': 10, 'total': 10}
        cli_result = {'status': 'PASS', 'passed': 5, 'total': 5}

        summary = self.checker._generate_summary(unit_result, cli_result)
        assert summary['overall_status'] == 'PASS'
        assert summary['unit_tests_status'] == 'PASS'
        assert summary['cli_tests_status'] == 'PASS'

    def test_save_report(self):
        """测试保存报告"""
        # 先运行检查获取结果
        with patch('core.quality_checker.QualityChecker.run_all_checks') as mock_run:
            mock_run.return_value = {
                'summary': {'overall_status': 'PASS'},
                'unit_tests': {'status': 'PASS'},
                'cli_tests': {'status': 'PASS'}
            }

        # 运行检查
        self.checker.run_all_checks()

        # 测试保存报告
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.return_value = None
        with patch('builtins.open', new_callable=Mock) as mock_open:
            mock_file = Mock()
            mock_file.__enter__.return_value.write.return_value = None
            mock_open.return_value = mock_file

        report_path = self.checker.save_report()
        assert report_path is not None

    def test_generate_markdown_report(self):
        """测试生成Markdown报告"""
        test_result = {
            'summary': {
                'overall_status': 'PASS',
                'unit_tests_status': 'PASS',
                'cli_tests_status': 'PASS',
                'execution_time': 1.23
            },
            'unit_tests': {
                'status': 'PASS',
                'passed': 10,
                'total': 10,
                'tests': []
            },
            'cli_tests': {
                'status': 'PASS',
                'passed': 5,
                'total': 5,
                'tests': []
            }
        }

        report = self.checker._generate_markdown_report(test_result)
        assert '质量检查报告' in report
        assert 'PASS' in report
