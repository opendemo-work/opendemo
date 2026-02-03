"""
多项式函数绘图示例
绘制指定多项式在区间上的图像
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    # 定义多项式系数: 0.3x^3 - x^2 - 2x + 5
    coeffs = [0.3, -1, -2, 5]
    poly = np.poly1d(coeffs)
    
    # 生成x轴数据
    x = np.linspace(-2, 5, 400)
    y = poly(x)
    
    print("正在绘制区间 [-2, 5] 上的多项式图像...")
    
    # 创建图像
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label=str(poly).replace('\n', ''))
    plt.xlabel('x', fontsize=12)
    plt.ylabel('P(x)', fontsize=12)
    plt.title('多项式函数图像', fontsize=14)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 标记根（近似）
    roots = np.roots(coeffs)
    real_roots = roots[np.isreal(roots)].real
    plt.scatter(real_roots, [0]*len(real_roots), color='red', zorder=5, label='实数根')
    
    plt.legend()
    plt.savefig('polynomial_plot.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"图像已保存为 'polynomial_plot.png'")
    print(f"实数根: {[f'{r:.3f}' for r in real_roots]}")

if __name__ == "__main__":
    main()