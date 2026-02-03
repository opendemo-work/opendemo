"""
Logger单元测试
"""

import logging
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from opendemo.utils.logger import setup_logger, get_logger


class TestLogger:
    """Logger测试类"""

    def test_setup_logger_basic(self):
        """测试基本logger设置"""
        logger = setup_logger("test_logger")
        
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0

    def test_setup_logger_with_level(self):
        """测试设置不同日志级别"""
        logger = setup_logger("test_debug", level=logging.DEBUG)
        
        assert logger.level == logging.DEBUG

    def test_setup_logger_with_file(self):
        """测试日志文件输出"""
        with patch("opendemo.utils.logger.Path") as mock_path:
            with patch("opendemo.utils.logger.RotatingFileHandler") as mock_handler:
                mock_path_instance = MagicMock(spec=Path)
                mock_path.return_value = mock_path_instance
                mock_path_instance.parent = MagicMock()
                
                logger = setup_logger("test_file", log_file="/tmp/test.log")
                
                mock_handler.assert_called_once()
                assert logger.name == "test_file"

    def test_setup_logger_no_duplicate_handlers(self):
        """测试避免重复添加handlers"""
        logger1 = setup_logger("test_dup")
        handlers_count1 = len(logger1.handlers)
        
        logger2 = setup_logger("test_dup")
        handlers_count2 = len(logger2.handlers)
        
        assert handlers_count1 == handlers_count2

    def test_get_logger(self):
        """测试获取logger实例"""
        logger = get_logger("opendemo")
        
        assert logger.name == "opendemo"
        assert isinstance(logger, logging.Logger)

    def test_get_logger_custom_name(self):
        """测试获取自定义名称的logger"""
        logger = get_logger("custom_logger")
        
        assert logger.name == "custom_logger"
