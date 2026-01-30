import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_sales_data():
    """
    创建模拟销售数据
    
    Returns:
        DataFrame: 包含日期和销售额的销售数据
    """
    # 设置随机种子以确保结果可重现
    np.random.seed(42)
    
    # 创建30天的日期范围
    start_date = datetime(2023, 1, 1)
    date_range = [start_date + timedelta(days=i) for i in range(30)]
    
    # 生成模拟销售数据（在80-200范围内波动）
    sales_values = np.random.randint(80, 200, size=30)
    
    # 创建DataFrame
    sales_data = pd.DataFrame({
        '日期': date_range,
        '销售额': sales_values
    })
    
    # 设置日期列为索引以便于时间序列分析
    sales_data.set_index('日期', inplace=True)
    
    return sales_data


def analyze_sales_trends(sales_data):
    """
    分析销售趋势，应用窗口函数
    
    Args:
        sales_data (DataFrame): 销售数据
    
    Returns:
        DataFrame: 包含移动平均的分析结果
    """
    # 创建7天滚动窗口并计算平均值
    # rolling()创建滑动窗口，window参数指定窗口大小
    sales_data['7天移动平均'] = sales_data['销售额'].rolling(window=7).mean()
    
    # 创建30天滚动窗口计算标准差（衡量销售波动性）
    sales_data['30天波动率'] = sales_data['销售额'].rolling(window=30).std()
    
    # 创建3天滚动窗口计算最大值
    sales_data['3天最高销售额'] = sales_data['销售额'].rolling(window=3).max()
    
    return sales_data


def main():
    """
    主函数：执行销售趋势分析
    """
    print("=== 销售数据与移动平均分析 ===")
    
    # 创建销售数据
    sales_data = create_sales_data()
    
    # 应用窗口函数进行趋势分析
    analyzed_data = analyze_sales_trends(sales_data)
    
    # 显示前10行结果
    print(analyzed_data.head(10))
    
    # 显示一些统计信息
    print("\n=== 统计摘要 ===")
    print(f"总销售额: {analyzed_data['销售额'].sum():,}")
    print(f"平均日销售额: {analyzed_data['销售额'].mean():.2f}")
    print(f"7天移动平均最新值: {analyzed_data['7天移动平均'].iloc[-1]:.2f}")
    

if __name__ == "__main__":
    main()