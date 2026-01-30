import numpy as np
import numpy.ma as ma


def main():
    """
    示例2：使用掩码数组处理传感器数据中的异常值
    场景：温度传感器记录中使用 -999.0 表示数据丢失
    """
    # 模拟一组温度读数，其中 -999.0 表示无效数据
    raw_temperatures = np.array([23.5, 24.1, -999.0, 25.3, 26.0])

    # 使用 masked_equal 自动将所有等于 -999.0 的值标记为无效
    temp_masked = ma.masked_equal(raw_temperatures, -999.0)

    print(f"原始传感器数据: {raw_temperatures}")
    print(f"掩码后数组: {temp_masked}")

    # 计算有效数据的平均温度
    avg_temp = temp_masked.mean()
    print(f"有效数据平均温度: {avg_temp:.3f}")

    # 可视化掩码状态
    print("各位置是否被屏蔽:", temp_masked.mask)


if __name__ == "__main__":
    main()