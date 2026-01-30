"""
多项式基础操作示例
展示如何使用NumPy进行多项式求值、求导和积分
"""

import numpy as np


def main():
    # 定义多项式系数 [2, 3, 1] 表示 2x^2 + 3x + 1
    coeffs = [2, 3, 1]
    
    print(f"多项式 P(x) = 2x^2 + 3x + 1")
    
    # 计算多项式在 x=2 处的值
    x_value = 2
    result = np.polyval(coeffs, x_value)
    print(f"P({x_value}) = {result}")
    
    # 计算多项式的导数
    derivative_coeffs = np.polyder(coeffs)
    print(f"导数: {derivative_coeffs[0]:.0f}x + {derivative_coeffs[1]}" if len(derivative_coeffs) == 2 else f"导数: {derivative_coeffs[0]:.0f}x")
    
    # 计算多项式的不定积分（常数项设为0）
    integral_coeffs = np.polyint(coeffs)
    integral_str = " + ".join([
        f"{coef:.4f}x^{len(integral_coeffs)-i-1}" 
        for i, coef in enumerate(integral_coeffs)
    ]).replace("x^1", "x").replace("x^0", "")
    print(f"积分: {integral_str}")

if __name__ == "__main__":
    main()