"""
QualityChecker 单元测试
"""

import pytest
import json
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from opendemo.core.quality_checker import QualityChecker


class TestQualityCheckerInit:
    """QualityChecker 初始化测试"""

    def test_init_default(self):
        """测试默认初始化"""
        checker = QualityChecker()
        
        assert checker.project_root is not None
        assert checker.check_dir == checker.project_root / "check"

    def test_init_custom_root(self, temp_dir):
        """测试自定义项目根目录"""
        checker = QualityChecker(project_root=temp_dir)
        
        assert checker.project_root == temp_dir
        assert checker.check_dir == temp_dir / "check"


class TestQualityCheckerUnitTests:
    """单元测试运行测试"""

    def test_run_unit_tests_success(self, temp_dir):
        """测试单元测试成功"""
        checker = QualityChecker(project_root=temp_dir)
        
        mock_result = Mock(
            returncode=0,
            stdout="10 passed",
            stderr=""
        )
        
        with patch("subprocess.run", return_value=mock_result):
            checker._run_unit_tests()
            
            assert checker.results["unit_tests"]["status"] == "PASS"
            assert checker.results["unit_tests"]["passed"] == 10
            assert checker.results["unit_tests"]["failed"] == 0

    def test_run_unit_tests_with_failures(self, temp_dir):
        """测试单元测试有失败"""
        checker = QualityChecker(project_root=temp_dir)
        
        mock_result = Mock(
            returncode=1,
            stdout="5 passed, 2 failed",
            stderr=""
        )
        
        with patch("subprocess.run", return_value=mock_result):
            checker._run_unit_tests()
            
            assert checker.results["unit_tests"]["status"] == "FAIL"
            assert checker.results["unit_tests"]["passed"] == 5
            assert checker.results["unit_tests"]["failed"] == 2

    def test_run_unit_tests_timeout(self, temp_dir):
        """测试单元测试超时"""
        checker = QualityChecker(project_root=temp_dir)
        
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("pytest", 120)):
            checker._run_unit_tests()
            
            assert checker.results["unit_tests"]["status"] == "TIMEOUT"
            assert len(checker.results["errors"]) > 0

    def test_run_unit_tests_error(self, temp_dir):
        """测试单元测试错误"""
        checker = QualityChecker(project_root=temp_dir)
        
        with patch("subprocess.run", side_effect=Exception("Test error")):
            checker._run_unit_tests()
            
            assert checker.results["unit_tests"]["status"] == "ERROR"
            assert len(checker.results["errors"]) > 0


class TestQualityCheckerCLITests:
    """CLI测试运行测试"""

    def test_run_cli_tests_all_pass(self, temp_dir):
        """测试所有CLI测试通过"""
        checker = QualityChecker(project_root=temp_dir)
        
        # Mock CLI命令执行 - 每个测试用例都返回预期输出
        def mock_cli_cmd(args):
            if "--version" in args:
                return {"output": "0.1.0", "exit_code": 0}
            elif "--help" in args:
                return {"output": "search get new config", "exit_code": 0}
            elif "search" in args:
                if len(args) == 1:
                    return {"output": "python go nodejs demo", "exit_code": 0}
                elif "python" in args and "logging" in args:
                    return {"output": "logging demo", "exit_code": 0}
                elif "python" in args:
                    return {"output": "demo", "exit_code": 0}
            elif "get" in args:
                if "rust" in args:
                    return {"output": "不支持的语言", "exit_code": 1}
                else:
                    return {"output": "logging demo", "exit_code": 0}
            elif "config" in args and "list" in args:
                return {"output": "output_directory ai.model", "exit_code": 0}
            elif "new" in args and "ruby" in args:
                return {"output": "不支持的语言", "exit_code": 1}
            return {"output": "ok", "exit_code": 0}
        
        with patch.object(checker, "_run_cli_command", side_effect=mock_cli_cmd):
            checker._run_cli_tests()
            
            assert checker.results["cli_tests"]["status"] == "PASS"
            assert checker.results["cli_tests"]["passed"] > 0

    def test_run_cli_command_success(self, temp_dir):
        """测试CLI命令执行成功"""
        checker = QualityChecker(project_root=temp_dir)
        
        mock_result = Mock(returncode=0, stdout="output", stderr="")
        
        with patch("subprocess.run", return_value=mock_result):
            result = checker._run_cli_command(["--version"])
            
            assert result["exit_code"] == 0
            assert result["output"] == "output"

    def test_run_cli_command_timeout(self, temp_dir):
        """测试CLI命令超时"""
        checker = QualityChecker(project_root=temp_dir)
        
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 60)):
            result = checker._run_cli_command(["test"])
            
            assert result["exit_code"] == -1
            assert "timed out" in result["output"].lower()

    def test_run_cli_command_error(self, temp_dir):
        """测试CLI命令错误"""
        checker = QualityChecker(project_root=temp_dir)
        
        with patch("subprocess.run", side_effect=Exception("Command error")):
            result = checker._run_cli_command(["test"])
            
            assert result["exit_code"] == -1


class TestQualityCheckerReporting:
    """报告生成测试"""

    def test_generate_summary_all_pass(self, temp_dir):
        """测试生成全通过摘要"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "unit_tests": {"status": "PASS", "passed": 10, "total": 10},
            "cli_tests": {"status": "PASS", "passed": 5, "total": 5},
            "errors": []
        }
        
        checker._generate_summary()
        
        assert checker.results["summary"]["overall_status"] == "PASS"
        assert checker.results["summary"]["unit_tests_passed"] == 10
        assert checker.results["summary"]["cli_tests_passed"] == 5

    def test_generate_summary_with_failures(self, temp_dir):
        """测试生成有失败的摘要"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "unit_tests": {"status": "FAIL", "passed": 8, "total": 10},
            "cli_tests": {"status": "PASS", "passed": 5, "total": 5},
            "errors": []
        }
        
        checker._generate_summary()
        
        assert checker.results["summary"]["overall_status"] == "FAIL"

    def test_save_report(self, temp_dir):
        """测试保存报告"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "timestamp": "2024-01-01T00:00:00",
            "summary": {
                "overall_status": "PASS",
                "unit_tests_passed": 10,
                "unit_tests_total": 10,
                "cli_tests_passed": 5,
                "cli_tests_total": 5,
                "errors_count": 0
            },
            "unit_tests": {"status": "PASS", "passed": 10, "failed": 0, "errors": 0, "total": 10},
            "cli_tests": {"status": "PASS", "passed": 5, "failed": 0, "total": 5, "tests": []},
            "errors": []
        }
        
        report_path = checker.save_report()
        
        assert report_path.exists()
        assert report_path.suffix == ".json"
        assert (temp_dir / "check" / "latest_report.json").exists()

    def test_generate_markdown_report(self, temp_dir):
        """测试生成Markdown报告"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "timestamp": "2024-01-01T00:00:00",
            "summary": {
                "overall_status": "PASS",
                "unit_tests_passed": 10,
                "unit_tests_total": 10,
                "cli_tests_passed": 5,
                "cli_tests_total": 5,
                "errors_count": 0
            },
            "unit_tests": {"status": "PASS", "passed": 10, "failed": 0, "errors": 0, "total": 10},
            "cli_tests": {
                "status": "PASS",
                "passed": 5,
                "failed": 0,
                "total": 5,
                "tests": [
                    {"name": "test1", "command": "cmd", "status": "PASS"}
                ]
            },
            "errors": []
        }
        
        report = checker._generate_markdown_report()
        
        assert "# OpenDemo CLI 质量检查报告" in report
        assert "✅" in report
        assert "10" in report

    def test_get_report_summary(self, temp_dir):
        """测试获取报告摘要"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "summary": {
                "unit_tests_passed": 10,
                "unit_tests_total": 10,
                "cli_tests_passed": 5,
                "cli_tests_total": 5
            }
        }
        
        summary = checker.get_report_summary()
        
        assert "10/10" in summary
        assert "5/5" in summary


class TestQualityCheckerIntegration:
    """集成测试"""

    def test_run_all_checks(self, temp_dir):
        """测试运行所有检查"""
        checker = QualityChecker(project_root=temp_dir)
        
        with patch.object(checker, "_run_unit_tests"):
            with patch.object(checker, "_run_cli_tests"):
                checker.results = {
                    "unit_tests": {"status": "PASS", "passed": 10, "total": 10},
                    "cli_tests": {"status": "PASS", "passed": 5, "total": 5},
                    "errors": []
                }
                
                results = checker.run_all_checks()
                
                assert "summary" in results
                assert results["summary"]["overall_status"] == "PASS"

    def test_end_to_end_with_mock(self, temp_dir):
        """测试端到端流程(Mock)"""
        checker = QualityChecker(project_root=temp_dir)
        
        # Mock pytest运行 - 返回完整的通过结果
        mock_pytest = Mock(returncode=0, stdout="10 passed", stderr="")
        
        # Mock CLI命令 - 确保所有命令都返回成功并包含预期输出
        def mock_cli_cmd(args):
            if "--version" in args:
                return {"output": "0.1.0", "exit_code": 0}
            elif "--help" in args:
                return {"output": "search get new config", "exit_code": 0}
            elif "search" in args:
                if len(args) == 1:
                    return {"output": "python go nodejs demo", "exit_code": 0}
                elif "python" in args and "logging" in args:
                    return {"output": "logging demo", "exit_code": 0}
                elif "python" in args:
                    return {"output": "demo", "exit_code": 0}
            elif "get" in args:
                if "rust" in args:
                    return {"output": "不支持的语言", "exit_code": 1}
                else:
                    return {"output": "logging demo", "exit_code": 0}
            elif "config" in args and "list" in args:
                return {"output": "output_directory ai.model", "exit_code": 0}
            elif "new" in args and "ruby" in args:
                return {"output": "不支持的语言", "exit_code": 1}
            return {"output": "ok", "exit_code": 0}
        
        with patch("subprocess.run", return_value=mock_pytest):
            with patch.object(checker, "_run_cli_command", side_effect=mock_cli_cmd):
                results = checker.run_all_checks()
                
                assert results["summary"]["overall_status"] == "PASS"
                
                # 保存报告
                report_path = checker.save_report()
                assert report_path.exists()


class TestQualityCheckerEdgeCases:
    """边界条件测试"""

    def test_empty_output(self, temp_dir):
        """测试空输出"""
        checker = QualityChecker(project_root=temp_dir)
        
        mock_result = Mock(returncode=0, stdout="", stderr="")
        
        with patch("subprocess.run", return_value=mock_result):
            checker._run_unit_tests()
            
            assert checker.results["unit_tests"]["passed"] == 0
            assert checker.results["unit_tests"]["total"] == 0

    def test_malformed_output(self, temp_dir):
        """测试格式错误的输出"""
        checker = QualityChecker(project_root=temp_dir)
        
        mock_result = Mock(returncode=0, stdout="random output", stderr="")
        
        with patch("subprocess.run", return_value=mock_result):
            checker._run_unit_tests()
            
            # 应该能处理而不崩溃
            assert "unit_tests" in checker.results

    def test_report_with_special_characters(self, temp_dir):
        """测试报告包含特殊字符"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "timestamp": "2024-01-01T00:00:00",
            "summary": {"overall_status": "PASS", "unit_tests_passed": 1, "unit_tests_total": 1, "cli_tests_passed": 1, "cli_tests_total": 1, "errors_count": 0},
            "unit_tests": {"status": "PASS", "passed": 1, "failed": 0, "errors": 0, "total": 1},
            "cli_tests": {"status": "PASS", "passed": 1, "failed": 0, "total": 1, "tests": []},
            "errors": ["测试错误：中文特殊字符 <>"]
        }
        
        report_path = checker.save_report()
        
        # 验证能够正确保存和读取
        assert report_path.exists()
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert "测试错误" in data["errors"][0]
        
        with patch("subprocess.run", return_value=mock_result):
            checker._run_unit_tests()
            
            # 应该能处理而不崩溃
            assert "unit_tests" in checker.results

    def test_report_with_special_characters(self, temp_dir):
        """测试报告包含特殊字符"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "timestamp": "2024-01-01T00:00:00",
            "summary": {"overall_status": "PASS", "unit_tests_passed": 1, "unit_tests_total": 1, "cli_tests_passed": 1, "cli_tests_total": 1, "errors_count": 0},
            "unit_tests": {"status": "PASS", "passed": 1, "failed": 0, "errors": 0, "total": 1},
            "cli_tests": {"status": "PASS", "passed": 1, "failed": 0, "total": 1, "tests": []},
            "errors": ["测试错误：中文特殊字符 <>"]
        }
        
        report_path = checker.save_report()
        
        # 验证能够正确保存和读取
        assert report_path.exists()
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert "测试错误" in data["errors"][0]
            
            # 应该能处理而不崩溃
            assert "unit_tests" in checker.results

    def test_report_with_special_characters(self, temp_dir):
        """测试报告包含特殊字符"""
        checker = QualityChecker(project_root=temp_dir)
        checker.results = {
            "timestamp": "2024-01-01T00:00:00",
            "summary": {"overall_status": "PASS", "unit_tests_passed": 1, "unit_tests_total": 1, "cli_tests_passed": 1, "cli_tests_total": 1, "errors_count": 0},
            "unit_tests": {"status": "PASS", "passed": 1, "failed": 0, "errors": 0, "total": 1},
            "cli_tests": {"status": "PASS", "passed": 1, "failed": 0, "total": 1, "tests": []},
            "errors": ["测试错误：中文特殊字符 <>"]
        }
        
        report_path = checker.save_report()
        
        # 验证能够正确保存和读取
        assert report_path.exists()
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert "测试错误" in data["errors"][0]
