#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python日志记录演示
展示logging模块的常用功能
"""
import logging
import logging.handlers
import tempfile
import os
import sys


def demo_basic_logging():
    """基本日志"""
    print("=" * 50)
    print("1. 基本日志")
    print("=" * 50)
    
    # 配置基本日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s - %(message)s'
    )
    
    # 日志级别
    print("日志级别示例:")
    logging.debug("这是DEBUG级别")
    logging.info("这是INFO级别")
    logging.warning("这是WARNING级别")
    logging.error("这是ERROR级别")
    logging.critical("这是CRITICAL级别")


def demo_logger_config():
    """Logger配置"""
    print("\n" + "=" * 50)
    print("2. Logger配置")
    print("=" * 50)
    
    # 创建logger
    logger = logging.getLogger('my_app')
    logger.setLevel(logging.DEBUG)
    
    # 清除之前的handler
    logger.handlers.clear()
    
    # 创建控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # 添加handler到logger
    logger.addHandler(console_handler)
    
    print("自定义Logger输出:")
    logger.info("应用启动")
    logger.warning("配置文件未找到,使用默认配置")
    logger.error("数据库连接失败")
    
    return logger


def demo_file_logging():
    """文件日志"""
    print("\n" + "=" * 50)
    print("3. 文件日志")
    print("=" * 50)
    
    # 创建临时日志文件
    temp_dir = tempfile.mkdtemp()
    log_file = os.path.join(temp_dir, 'app.log')
    
    # 创建logger
    logger = logging.getLogger('file_logger')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # 文件handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(file_handler)
    
    # 写入日志
    logger.info("程序启动")
    logger.debug("调试信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    
    # 读取日志文件内容
    print(f"日志文件: {log_file}")
    with open(log_file, 'r', encoding='utf-8') as f:
        print(f.read())
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)


def demo_rotating_file():
    """轮转日志"""
    print("\n" + "=" * 50)
    print("4. 轮转日志")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    log_file = os.path.join(temp_dir, 'rotating.log')
    
    # 创建logger
    logger = logging.getLogger('rotating_logger')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # 按大小轮转 (每100字节轮转,保留3个备份)
    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=100,
        backupCount=3,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    
    # 写入多条日志触发轮转
    for i in range(10):
        logger.info(f"这是第{i+1}条日志消息")
    
    # 显示生成的文件
    print("生成的日志文件:")
    for f in sorted(os.listdir(temp_dir)):
        filepath = os.path.join(temp_dir, f)
        size = os.path.getsize(filepath)
        print(f"  {f} ({size} bytes)")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    
    print("\n按时间轮转示例 (TimedRotatingFileHandler):")
    print("  - when='D': 每天轮转")
    print("  - when='H': 每小时轮转")
    print("  - when='M': 每分钟轮转")


def demo_exception_logging():
    """异常日志"""
    print("\n" + "=" * 50)
    print("5. 异常日志")
    print("=" * 50)
    
    logger = logging.getLogger('exception_logger')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    print("记录异常信息:")
    try:
        result = 1 / 0
    except Exception as e:
        # 使用exc_info记录堆栈
        logger.error("发生异常", exc_info=True)
        
        # 或使用exception()方法
        # logger.exception("发生异常")


def demo_custom_levels():
    """自定义日志级别"""
    print("\n" + "=" * 50)
    print("6. 日志级别详解")
    print("=" * 50)
    
    levels = [
        (logging.DEBUG, 10, "DEBUG - 调试信息"),
        (logging.INFO, 20, "INFO - 一般信息"),
        (logging.WARNING, 30, "WARNING - 警告"),
        (logging.ERROR, 40, "ERROR - 错误"),
        (logging.CRITICAL, 50, "CRITICAL - 严重错误"),
    ]
    
    print("日志级别对照表:")
    for level, value, desc in levels:
        print(f"  {logging.getLevelName(level):10} = {value:3} | {desc}")


def demo_structured_logging():
    """结构化日志"""
    print("\n" + "=" * 50)
    print("7. 结构化日志(使用extra)")
    print("=" * 50)
    
    logger = logging.getLogger('structured_logger')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # 自定义格式包含extra字段
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | user=%(user)s | action=%(action)s | %(message)s',
        datefmt='%H:%M:%S'
    ))
    logger.addHandler(handler)
    
    print("结构化日志输出:")
    logger.info("用户登录", extra={'user': 'alice', 'action': 'login'})
    logger.info("访问页面", extra={'user': 'alice', 'action': 'page_view'})
    logger.warning("权限不足", extra={'user': 'alice', 'action': 'access_denied'})


def demo_filter():
    """日志过滤器"""
    print("\n" + "=" * 50)
    print("8. 日志过滤器")
    print("=" * 50)
    
    class LevelFilter(logging.Filter):
        """只允许特定级别的日志"""
        def __init__(self, level):
            super().__init__()
            self.level = level
        
        def filter(self, record):
            return record.levelno == self.level
    
    logger = logging.getLogger('filter_logger')
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    
    # 只记录WARNING级别
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    handler.addFilter(LevelFilter(logging.WARNING))
    logger.addHandler(handler)
    
    print("过滤只显示WARNING级别:")
    logger.debug("DEBUG消息")
    logger.info("INFO消息")
    logger.warning("WARNING消息")
    logger.error("ERROR消息")


def demo_production_config():
    """生产环境配置示例"""
    print("\n" + "=" * 50)
    print("9. 生产环境配置示例")
    print("=" * 50)
    
    config_example = '''
# 推荐的生产环境配置
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # 根logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )
    
    # 控制台handler (WARNING及以上)
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(formatter)
    
    # 文件handler (INFO及以上, 轮转)
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    
    return logger
'''
    print(config_example)


if __name__ == "__main__":
    # 重置logging配置
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    demo_basic_logging()
    demo_logger_config()
    demo_file_logging()
    demo_rotating_file()
    demo_exception_logging()
    demo_custom_levels()
    demo_structured_logging()
    demo_filter()
    demo_production_config()
    print("\n[OK] 日志记录演示完成!")
