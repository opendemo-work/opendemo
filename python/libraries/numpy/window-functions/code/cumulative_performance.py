import pandas as pd
import numpy as np


def create_performance_data():
    """
    创建员工业绩数据
    
    Returns:
        DataFrame: 包含员工销售额的数据
    """
    # 定义员工姓名和对应的销售额
    employees = ['员工A', '员工B', '员工C', '员工D', '员工E']
    sales = [5000, 7500, 6200, 8100, 6900]
    
    # 创建DataFrame
    performance_df = pd.DataFrame({
        '员工': employees,
        '销售额': sales
    })
    
    # 设置员工列为索引
    performance_df.set_index('员工', inplace=True)
    
    return performance_df


def calculate_cumulative_metrics(performance_df):
    """
    计算累计业绩指标
    
    Args:
        performance_df (DataFrame): 业绩数据
    
    Returns:
        DataFrame: 包含累计统计的分析结果
    """
    # 使用扩展窗口计算累计和
    # expanding()创建从第一行到当前行的窗口
    performance_df['累计销售额'] = performance_df['销售额'].expanding().sum()
    
    # 使用扩展窗口计算累计平均
    performance_df['累计平均销售额'] = performance_df['销售额'].expanding().mean()
    
    # 计算累计最大值
    performance_df['历史最高单人销售额'] = performance_df['销售额'].expanding().max()
    
    # 计算累计最小值
    performance_df['历史最低单人销售额'] = performance_df['销售额'].expanding().min()
    
    return performance_df


def main():
    """
    主函数：执行累计业绩分析
    """
    print("=== 员工业绩累计统计分析 ===")
    
    # 创建业绩数据
    performance_data = create_performance_data()
    
    # 计算累计指标
    analyzed_data = calculate_cumulative_metrics(performance_data)
    
    # 显示结果
    print(analyzed_data)
    
    # 显示团队整体表现
    print("\n=== 团队绩效总结 ===")
    total_sales = analyzed_data['累计销售额'].iloc[-1]
    avg_per_employee = analyzed_data['累计平均销售额'].iloc[-1]
    
    print(f"团队总销售额: ¥{total_sales:,}")
    print(f"人均累计销售额: ¥{avg_per_employee:,.2f}")
    print(f"业绩差距: ¥{analyzed_data['销售额'].max() - analyzed_data['销售额'].min():,}")


if __name__ == "__main__":
    main()