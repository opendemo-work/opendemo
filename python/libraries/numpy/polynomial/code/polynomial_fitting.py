"""
多项式数据拟合示例
使用NumPy的polyfit对模拟数据进行二次拟合
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    # 生成带有噪声的实验数据（模拟真实测量）
    np.random.seed(42)  # 保证结果可复现
    x_data = np.linspace(0, 8, 15)
    y_true = -0.5 * x_data ** 2 + 4 * x_data + 1  # 真实关系
    y_data = y_true + np.random.normal(0, 0.5, size=x_data.shape)  # 添加噪声
    
    # 使用二次多项式进行最小二乘拟合
    fitted_coeffs = np.polyfit(x_data, y_data, deg=2)
    fitted_poly = np.poly1d(fitted_coeffs)
    
    # 计算R²得分评估拟合质量
    y_pred = fitted_poly(x_data)
    ss_res = np.sum((y_data - y_pred) ** 2)
    ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
    r2_score = 1 - (ss_res / ss_tot)
    
    print(f"拟合的二次多项式: {fitted_coeffs[0]:.1f}x^2 + {fitted_coeffs[1]:.1f}x + {fitted_coeffs[2]:.1f}")
    print(f"R²得分: {r2_score:.2f}")
    
    # 绘制原始数据与拟合曲线
    x_smooth = np.linspace(0, 8, 200)
    plt.figure(figsize=(8, 5))
    plt.scatter(x_data, y_data, color='blue', label='原始数据', alpha=0.7)
    plt.plot(x_smooth, fitted_poly(x_smooth), color='red', label='拟合曲线')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('多项式数据拟合')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('fitted_curve.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("拟合图像已保存为 'fitted_curve.png'")

if __name__ == "__main__":
    main()