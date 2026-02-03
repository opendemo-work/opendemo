"""
质量检查模块

执行单元测试和CLI功能测试，生成检查报告。
"""

import subprocess
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from opendemo.utils.logger import get_logger


class QualityChecker:
    """质量检查器"""

    def __init__(self, project_root: Path = None):
        """
        初始化质量检查器

        Args:
            project_root: 项目根目录路径
        """
        self.logger = get_logger(__name__)
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.check_dir = self.project_root / "check"
        self.results: Dict[str, Any] = {
            "timestamp": "",
            "summary": {},
            "unit_tests": {},
            "cli_tests": {},
            "errors": [],
        }

    def run_all_checks(self) -> Dict[str, Any]:
        """
        运行所有检查

        Returns:
            检查结果字典
        """
        self.results["timestamp"] = datetime.now().isoformat()

        # 1. 运行单元测试
        self.logger.info("Running unit tests...")
        self._run_unit_tests()

        # 2. 运行CLI功能测试
        self.logger.info("Running CLI tests...")
        self._run_cli_tests()

        # 3. 生成摘要
        self._generate_summary()

        return self.results

    def _run_unit_tests(self):
        """运行单元测试"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-q"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=120,
            )

            output = result.stdout + result.stderr

            # 解析测试结果
            passed = 0
            failed = 0
            errors = 0

            # 匹配结果行 "X passed" 或 "X passed, Y failed"
            match = re.search(r"(\d+) passed", output)
            if match:
                passed = int(match.group(1))

            match = re.search(r"(\d+) failed", output)
            if match:
                failed = int(match.group(1))

            match = re.search(r"(\d+) error", output)
            if match:
                errors = int(match.group(1))

            self.results["unit_tests"] = {
                "status": "PASS" if result.returncode == 0 else "FAIL",
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "total": passed + failed + errors,
                "output": output[-2000:] if len(output) > 2000 else output,  # 限制输出长度
            }

        except subprocess.TimeoutExpired:
            self.results["unit_tests"] = {
                "status": "TIMEOUT",
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "total": 0,
                "output": "Unit tests timed out after 120 seconds",
            }
            self.results["errors"].append("Unit tests timed out")
        except Exception as e:
            self.results["unit_tests"] = {
                "status": "ERROR",
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "total": 0,
                "output": str(e),
            }
            self.results["errors"].append(f"Unit test error: {e}")

    def _run_cli_tests(self):
        """运行CLI功能测试"""
        cli_tests = []

        # 测试用例列表
        test_cases = [
            {
                "name": "version",
                "command": ["--version"],
                "expected_in_output": ["0.1.0"],
                "should_succeed": True,
            },
            {
                "name": "help",
                "command": ["--help"],
                "expected_in_output": ["search", "get", "new", "config"],
                "should_succeed": True,
            },
            {
                "name": "search_all_languages",
                "command": ["search"],
                "expected_in_output": ["python", "go", "nodejs"],
                "should_succeed": True,
            },
            {
                "name": "search_python",
                "command": ["search", "python"],
                "expected_in_output": ["demo"],
                "should_succeed": True,
            },
            {
                "name": "search_with_keyword",
                "command": ["search", "python", "logging"],
                "expected_in_output": ["logging"],
                "should_succeed": True,
            },
            {
                "name": "get_existing_demo",
                "command": ["get", "python", "logging"],
                "expected_in_output": ["logging"],
                "should_succeed": True,
            },
            {
                "name": "get_unsupported_language",
                "command": ["get", "rust", "test"],
                "expected_in_output": ["不支持的语言"],
                "should_succeed": False,
            },
            {
                "name": "config_list",
                "command": ["config", "list"],
                "expected_in_output": ["output_directory", "ai.model"],
                "should_succeed": True,
            },
            {
                "name": "new_unsupported_language",
                "command": ["new", "ruby", "test"],
                "expected_in_output": ["不支持的语言"],
                "should_succeed": False,
            },
        ]

        for test in test_cases:
            result = self._run_cli_command(test["command"])

            # 检查输出是否包含预期内容
            output_match = all(
                exp.lower() in result["output"].lower() for exp in test["expected_in_output"]
            )

            # 检查退出码
            exit_code_match = (result["exit_code"] == 0) == test["should_succeed"]

            test_result = {
                "name": test["name"],
                "command": " ".join(test["command"]),
                "status": "PASS" if (output_match and exit_code_match) else "FAIL",
                "exit_code": result["exit_code"],
                "output_match": output_match,
                "exit_code_match": exit_code_match,
            }

            cli_tests.append(test_result)

        passed = sum(1 for t in cli_tests if t["status"] == "PASS")
        failed = len(cli_tests) - passed

        self.results["cli_tests"] = {
            "status": "PASS" if failed == 0 else "FAIL",
            "passed": passed,
            "failed": failed,
            "total": len(cli_tests),
            "tests": cli_tests,
        }

    def _run_cli_command(self, args: List[str]) -> Dict[str, Any]:
        """
        运行CLI命令

        Args:
            args: 命令参数列表

        Returns:
            包含输出和退出码的字典
        """
        try:
            cmd = [sys.executable, "-c", "from opendemo import main; main()"] + args
            result = subprocess.run(
                cmd, cwd=str(self.project_root), capture_output=True, text=True, timeout=60
            )
            return {"output": result.stdout + result.stderr, "exit_code": result.returncode}
        except subprocess.TimeoutExpired:
            return {"output": "Command timed out", "exit_code": -1}
        except Exception as e:
            return {"output": str(e), "exit_code": -1}

    def _generate_summary(self):
        """生成检查摘要"""
        unit_status = self.results["unit_tests"].get("status", "UNKNOWN")
        cli_status = self.results["cli_tests"].get("status", "UNKNOWN")

        overall_status = "PASS" if (unit_status == "PASS" and cli_status == "PASS") else "FAIL"

        self.results["summary"] = {
            "overall_status": overall_status,
            "unit_tests_status": unit_status,
            "cli_tests_status": cli_status,
            "unit_tests_passed": self.results["unit_tests"].get("passed", 0),
            "unit_tests_total": self.results["unit_tests"].get("total", 0),
            "cli_tests_passed": self.results["cli_tests"].get("passed", 0),
            "cli_tests_total": self.results["cli_tests"].get("total", 0),
            "errors_count": len(self.results["errors"]),
        }

    def save_report(self) -> Path:
        """
        保存检查报告

        Returns:
            报告文件路径
        """
        # 确保 check 目录存在
        self.check_dir.mkdir(exist_ok=True)

        # 生成报告文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.check_dir / f"check_report_{timestamp}.json"

        # 保存 JSON 报告
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        # 同时生成可读的 Markdown 报告
        md_report = self._generate_markdown_report()
        md_file = self.check_dir / f"check_report_{timestamp}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_report)

        # 更新最新报告链接
        latest_file = self.check_dir / "latest_report.json"
        with open(latest_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Report saved to {report_file}")
        return report_file

    def _generate_markdown_report(self) -> str:
        """生成 Markdown 格式报告"""
        summary = self.results["summary"]
        unit = self.results["unit_tests"]
        cli = self.results["cli_tests"]

        status_emoji = "✅" if summary["overall_status"] == "PASS" else "❌"

        report = f"""# OpenDemo CLI 质量检查报告

**检查时间**: {self.results['timestamp']}

## 总体状态: {status_emoji} {summary['overall_status']}

---

## 单元测试

| 指标 | 结果 |
|------|------|
| 状态 | {unit.get('status', 'N/A')} |
| 通过 | {unit.get('passed', 0)} |
| 失败 | {unit.get('failed', 0)} |
| 错误 | {unit.get('errors', 0)} |
| 总计 | {unit.get('total', 0)} |

---

## CLI 功能测试

| 指标 | 结果 |
|------|------|
| 状态 | {cli.get('status', 'N/A')} |
| 通过 | {cli.get('passed', 0)} |
| 失败 | {cli.get('failed', 0)} |
| 总计 | {cli.get('total', 0)} |

### 测试详情

| 测试名称 | 命令 | 状态 |
|----------|------|------|
"""

        for test in cli.get("tests", []):
            status_icon = "✅" if test["status"] == "PASS" else "❌"
            report += f"| {test['name']} | `{test['command']}` | {status_icon} {test['status']} |\n"

        if self.results["errors"]:
            report += "\n---\n\n## 错误信息\n\n"
            for error in self.results["errors"]:
                report += f"- {error}\n"

        report += f"""
---

## 摘要

- 单元测试: **{summary['unit_tests_passed']}/{summary['unit_tests_total']}** 通过
- CLI测试: **{summary['cli_tests_passed']}/{summary['cli_tests_total']}** 通过
- 错误数量: **{summary['errors_count']}**
"""

        return report

    def get_report_summary(self) -> str:
        """
        获取简短的报告摘要

        Returns:
            摘要字符串
        """
        summary = self.results.get("summary", {})
        return (
            f"单元测试: {summary.get('unit_tests_passed', 0)}/{summary.get('unit_tests_total', 0)} 通过, "
            f"CLI测试: {summary.get('cli_tests_passed', 0)}/{summary.get('cli_tests_total', 0)} 通过"
        )
