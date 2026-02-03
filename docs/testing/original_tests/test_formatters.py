"""
Formatters单元测试
"""

from unittest.mock import Mock, patch, MagicMock
from opendemo.utils.formatters import (
    print_success,
    print_error,
    print_warning,
    print_info,
    print_demo_result,
    print_search_results,
)


class TestFormatters:
    """Formatters测试类"""

    def test_print_success(self):
        """测试成功消息输出"""
        with patch("opendemo.utils.formatters.console") as mock_console:
            print_success("Test success message")
            mock_console.print.assert_called_once()

    def test_print_error(self):
        """测试错误消息输出"""
        with patch("opendemo.utils.formatters.console") as mock_console:
            print_error("Test error message")
            mock_console.print.assert_called_once()

    def test_print_warning(self):
        """测试警告消息输出"""
        with patch("opendemo.utils.formatters.console") as mock_console:
            print_warning("Test warning message")
            mock_console.print.assert_called_once()

    def test_print_info(self):
        """测试信息消息输出"""
        with patch("opendemo.utils.formatters.console") as mock_console:
            print_info("Test info message")
            mock_console.print.assert_called_once()

    def test_print_demo_result(self):
        """测试Demo结果输出"""
        with patch("opendemo.utils.formatters.console") as mock_console:
            demo_result = {
                "path": "/test/path",
                "language": "python",
                "topic": "test topic",
                "files": [{" name": "main.py"}, {"name": "README.md"}],
            }
            print_demo_result(demo_result)
            assert mock_console.print.called

    def test_print_search_results(self):
        """测试搜索结果输出"""
        with patch("opendemo.utils.formatters.console") as mock_console:
            results = [
                {
                    "name": "test-demo",
                    "language": "python",
                    "keywords": ["test"],
                    "description": "Test demo",
                }
            ]
            print_search_results(results, "python")
            assert mock_console.print.called

    def test_print_search_results_empty(self):
        """测试空搜索结果输出"""
        with patch("opendemo.utils.formatters.console") as mock_console:
            print_search_results([], "python")
            assert mock_console.print.called
