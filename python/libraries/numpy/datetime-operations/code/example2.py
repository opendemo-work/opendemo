"""
文件: example2.py
功能: 演示字符串与datetime对象之间的转换——解析和格式化
"""

from datetime import datetime


def main():
    # 示例1：将字符串解析为datetime对象（Parsing）
    date_str = "2025-04-05 10:30:15"
    # strptime: string parse time，根据指定格式解析字符串
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    print(f"原始字符串: {date_str}")
    print(f"解析后的日期对象: {dt}")

    # 示例2：将datetime对象格式化为字符串（Formatting）
    # strftime: string format time，将时间对象转为可读字符串
    formatted_chinese = dt.strftime("%Y年%m月%d日 %H时%M分%S秒")
    print(f"格式化为中文显示: {formatted_chinese}")

    # ISO 8601 标准格式（常用于API和日志）
    iso_format = dt.isoformat()
    print(f"ISO格式输出: {iso_format}")

    # 自定义格式：模拟Apache日志风格
    custom_format = dt.strftime("[%d/%b/%Y:%H:%M:%S]")
    print(f"自定义格式: {custom_format}")

    # 示例3：从不同格式的字符串解析
    log_time_str = "05/Apr/2025:10:30:15"
    log_dt = datetime.strptime(log_time_str, "%d/%b/%Y:%H:%M:%S")
    print(f"从日志格式解析: {log_dt}")


if __name__ == "__main__":
    main()