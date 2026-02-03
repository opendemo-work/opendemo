#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python日期时间处理演示
展示datetime模块的常用功能
"""
from datetime import datetime, date, time, timedelta
from datetime import timezone
import calendar


def demo_datetime_basics():
    """日期时间基础"""
    print("=" * 50)
    print("1. 日期时间基础")
    print("=" * 50)
    
    # 当前日期时间
    now = datetime.now()
    print(f"当前时间: {now}")
    print(f"  年: {now.year}, 月: {now.month}, 日: {now.day}")
    print(f"  时: {now.hour}, 分: {now.minute}, 秒: {now.second}")
    print(f"  微秒: {now.microsecond}")
    print(f"  星期几: {now.weekday()} (0=周一)")
    
    # 仅日期
    today = date.today()
    print(f"\n仅日期: {today}")
    
    # 仅时间
    t = time(14, 30, 45)
    print(f"仅时间: {t}")
    
    # 创建指定日期时间
    dt = datetime(2024, 1, 15, 10, 30, 0)
    print(f"\n指定日期时间: {dt}")


def demo_datetime_formatting():
    """日期时间格式化"""
    print("\n" + "=" * 50)
    print("2. 日期时间格式化")
    print("=" * 50)
    
    now = datetime.now()
    
    # strftime - 格式化输出
    formats = [
        ("%Y-%m-%d", "年-月-日"),
        ("%Y/%m/%d %H:%M:%S", "年/月/日 时:分:秒"),
        ("%Y年%m月%d日", "中文格式"),
        ("%A, %B %d, %Y", "英文完整格式"),
        ("%y%m%d", "短日期"),
        ("%H:%M:%S", "时间"),
        ("%I:%M %p", "12小时制"),
    ]
    
    print("strftime格式化:")
    for fmt, desc in formats:
        print(f"  {fmt:25} ({desc}): {now.strftime(fmt)}")
    
    # strptime - 解析字符串
    print("\nstrptime解析:")
    date_str = "2024-01-15 14:30:00"
    parsed = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    print(f"  '{date_str}' -> {parsed}")


def demo_timedelta():
    """时间差"""
    print("\n" + "=" * 50)
    print("3. 时间差 timedelta")
    print("=" * 50)
    
    now = datetime.now()
    print(f"当前时间: {now}")
    
    # 创建时间差
    delta = timedelta(days=7, hours=3, minutes=30)
    print(f"\n时间差: {delta}")
    print(f"  总秒数: {delta.total_seconds()}")
    
    # 日期计算
    future = now + delta
    print(f"\n7天3小时30分钟后: {future}")
    
    past = now - timedelta(days=30)
    print(f"30天前: {past}")
    
    # 两个日期的差
    date1 = datetime(2024, 1, 1)
    date2 = datetime(2024, 12, 31)
    diff = date2 - date1
    print(f"\n{date2.date()} - {date1.date()} = {diff.days}天")


def demo_timezone():
    """时区处理"""
    print("\n" + "=" * 50)
    print("4. 时区处理")
    print("=" * 50)
    
    # UTC时间
    utc_now = datetime.now(timezone.utc)
    print(f"UTC时间: {utc_now}")
    
    # 本地时间(带时区)
    local_now = datetime.now().astimezone()
    print(f"本地时间: {local_now}")
    
    # 创建指定时区
    tz_east8 = timezone(timedelta(hours=8))
    beijing_time = datetime.now(tz_east8)
    print(f"北京时间(UTC+8): {beijing_time}")
    
    # 时区转换
    utc_time = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
    local_time = utc_time.astimezone(tz_east8)
    print(f"\nUTC {utc_time} -> 北京 {local_time}")


def demo_calendar():
    """日历操作"""
    print("\n" + "=" * 50)
    print("5. 日历操作")
    print("=" * 50)
    
    # 月历
    print("2024年1月:")
    cal = calendar.month(2024, 1)
    for line in cal.split('\n')[:4]:  # 只显示前几行
        print(f"  {line}")
    print("  ...")
    
    # 判断闰年
    years = [2020, 2021, 2024, 2100]
    print("\n闰年判断:")
    for year in years:
        is_leap = calendar.isleap(year)
        print(f"  {year}: {'是' if is_leap else '否'}闰年")
    
    # 获取月份天数
    print("\n月份天数:")
    for month in [1, 2, 4, 6]:
        days = calendar.monthrange(2024, month)[1]
        print(f"  2024年{month}月: {days}天")


def demo_practical_examples():
    """实用示例"""
    print("\n" + "=" * 50)
    print("6. 实用示例")
    print("=" * 50)
    
    # 计算年龄
    def calculate_age(birth_date):
        today = date.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    
    birth = date(1990, 6, 15)
    print(f"出生日期: {birth}, 年龄: {calculate_age(birth)}岁")
    
    # 工作日计算
    def add_business_days(start_date, days):
        current = start_date
        added = 0
        while added < days:
            current += timedelta(days=1)
            if current.weekday() < 5:  # 0-4是工作日
                added += 1
        return current
    
    start = date(2024, 1, 15)  # 假设是周一
    end = add_business_days(start, 5)
    print(f"\n{start}后5个工作日: {end}")
    
    # 本月第一天和最后一天
    today = date.today()
    first_day = today.replace(day=1)
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    last_day = next_month - timedelta(days=1)
    print(f"\n本月第一天: {first_day}")
    print(f"本月最后一天: {last_day}")
    
    # 时间戳转换
    now = datetime.now()
    timestamp = now.timestamp()
    print(f"\n当前时间戳: {timestamp}")
    print(f"时间戳转回: {datetime.fromtimestamp(timestamp)}")


def demo_date_comparison():
    """日期比较"""
    print("\n" + "=" * 50)
    print("7. 日期比较和排序")
    print("=" * 50)
    
    dates = [
        datetime(2024, 3, 15),
        datetime(2024, 1, 1),
        datetime(2024, 6, 30),
        datetime(2024, 2, 28),
    ]
    
    print("原始日期列表:")
    for d in dates:
        print(f"  {d.date()}")
    
    print("\n排序后:")
    for d in sorted(dates):
        print(f"  {d.date()}")
    
    # 日期比较
    d1 = datetime(2024, 1, 15)
    d2 = datetime(2024, 6, 15)
    print(f"\n{d1.date()} < {d2.date()}: {d1 < d2}")
    print(f"日期相差: {(d2 - d1).days}天")


if __name__ == "__main__":
    demo_datetime_basics()
    demo_datetime_formatting()
    demo_timedelta()
    demo_timezone()
    demo_calendar()
    demo_practical_examples()
    demo_date_comparison()
    print("\n[OK] 日期时间处理演示完成!")
