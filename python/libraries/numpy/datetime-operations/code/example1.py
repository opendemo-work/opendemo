"""
文件: example1.py
功能: 演示datetime基本操作——时间创建、计算时间差和程序执行计时
"""

from datetime import datetime, timedelta
import time


def main():
    # 获取当前系统时间
    current_time = datetime.now()
    print(f"当前时间: {current_time}")

    # 创建具体的时间点（无时区信息，称为naive datetime）
    start = datetime(2025, 4, 5, 8, 0, 0)  # 早上8点
    end = datetime(2025, 4, 5, 18, 0, 0)  # 下午6点
    print(f"开始时间: {start}")
    print(f"结束时间: {end}")

    # 计算两个时间点之间的时间差（返回timedelta对象）
    duration = end - start
    print(f"工作时长: {duration}")

    # 演示程序执行耗时测量
    start_time = datetime.now()
    time.sleep(0.0001)  # 模拟短暂操作
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"程序执行耗时: {execution_time}")


if __name__ == "__main__":
    main()