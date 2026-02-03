"""
文件: basic_stats.py
功能: 使用statistics模块计算基础统计量
作者: Python编程导师
日期: 2024
"""

import statistics


def main():
    """主函数：演示基础统计计算"""
    # 示例数据：一组学生的测试分数
    scores = [10, 15, 20, 25, 30, 35, 40]

    print("=== 基础统计数据 ===")
    print(f"数据: {scores}")

    # 计算平均值（均值）
    # 均值反映数据的集中趋势
    mean_value = statistics.mean(scores)
    print(f"平均值: {mean_value:.2f}")

    # 计算中位数
    # 中位数是排序后位于中间的值，对异常值不敏感
    median_value = statistics.median(scores)
    print(f"中位数: {median_value}")

    # 计算众数
    # 众数是出现频率最高的值
    try:
        mode_value = statistics.mode(scores)
        print(f"众数: {mode_value}")
    except statistics.StatisticsError:
        print("众数: 无（所有值唯一）")

    # 计算样本标准差
    # 标准差衡量数据的离散程度
    stdev_value = statistics.stdev(scores)
    print(f"标准差: {stdev_value:.2f}")

    # 计算样本方差
    # 方差是标准差的平方
    variance_value = statistics.variance(scores)
    print(f"方差: {variance_value:.1f}")


if __name__ == "__main__":
    main()
