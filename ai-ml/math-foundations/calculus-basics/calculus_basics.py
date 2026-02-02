#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微积分基础演示程序
展示导数、偏导数、梯度、积分等AI/ML核心数学概念
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from typing import Callable, Tuple
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CalculusBasics:
    """微积分基础类 - 演示核心概念和运算"""
    
    def __init__(self):
        """初始化微积分演示环境"""
        logger.info("初始化微积分基础演示")
        self.setup_plot_style()
    
    def setup_plot_style(self):
        """设置绘图样式"""
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
        plt.rcParams['axes.unicode_minus'] = False    # 支持负号显示
        plt.style.use('seaborn-v0_8')                 # 使用seaborn样式
    
    def derivative_concept(self) -> None:
        """导数概念演示"""
        logger.info("=== 导数概念演示 ===")
        
        # 定义函数 f(x) = x²
        def f(x):
            return x**2
        
        # 定义导数 f'(x) = 2x
        def f_prime(x):
            return 2*x
        
        # 计算特定点的导数
        x_point = 2.0
        derivative_at_point = f_prime(x_point)
        logger.info(f"函数 f(x) = x² 在 x = {x_point} 处的导数: {derivative_at_point}")
        
        # 几何意义：切线斜率
        tangent_line = lambda x: derivative_at_point * (x - x_point) + f(x_point)
        logger.info(f"在点 ({x_point}, {f(x_point)}) 处的切线方程: y = {derivative_at_point}(x - {x_point}) + {f(x_point)}")
        
        # 可视化
        self.visualize_derivative(f, f_prime, x_point)
    
    def partial_derivatives(self) -> None:
        """偏导数演示"""
        logger.info("=== 偏导数演示 ===")
        
        # 定义二元函数 f(x,y) = x² + y²
        def f(x, y):
            return x**2 + y**2
        
        # 偏导数 ∂f/∂x = 2x, ∂f/∂y = 2y
        def df_dx(x, y):
            return 2*x
        
        def df_dy(x, y):
            return 2*y
        
        # 计算特定点的偏导数
        x_point, y_point = 1.0, 2.0
        partial_x = df_dx(x_point, y_point)
        partial_y = df_dy(x_point, y_point)
        
        logger.info(f"函数 f(x,y) = x² + y²")
        logger.info(f"在点 ({x_point}, {y_point}) 处:")
        logger.info(f"  ∂f/∂x = {partial_x}")
        logger.info(f"  ∂f/∂y = {partial_y}")
        
        # 梯度向量
        gradient = np.array([partial_x, partial_y])
        logger.info(f"梯度向量: ∇f = [{partial_x}, {partial_y}]")
        logger.info(f"梯度模长: {np.linalg.norm(gradient):.2f}")
        
        # 可视化
        self.visualize_partial_derivatives(f, df_dx, df_dy, x_point, y_point)
    
    def gradient_descent_demo(self) -> None:
        """梯度下降演示"""
        logger.info("=== 梯度下降演示 ===")
        
        # 定义损失函数 f(x,y) = (x-3)² + (y-2)²
        def loss_function(x, y):
            return (x - 3)**2 + (y - 2)**2
        
        # 梯度 ∇f = [2(x-3), 2(y-2)]
        def gradient(x, y):
            return np.array([2*(x - 3), 2*(y - 2)])
        
        # 梯度下降参数
        learning_rate = 0.1
        max_iterations = 50
        tolerance = 1e-6
        
        # 初始点
        current_point = np.array([0.0, 0.0])
        logger.info(f"初始点: {current_point}")
        logger.info(f"学习率: {learning_rate}")
        
        # 梯度下降过程
        trajectory = [current_point.copy()]
        losses = [loss_function(current_point[0], current_point[1])]
        
        for i in range(max_iterations):
            grad = gradient(current_point[0], current_point[1])
            new_point = current_point - learning_rate * grad
            
            # 检查收敛
            if np.linalg.norm(new_point - current_point) < tolerance:
                logger.info(f"在第 {i+1} 次迭代后收敛")
                break
            
            current_point = new_point
            trajectory.append(current_point.copy())
            losses.append(loss_function(current_point[0], current_point[1]))
        
        trajectory = np.array(trajectory)
        logger.info(f"最终点: {current_point}")
        logger.info(f"最终损失值: {losses[-1]:.6f}")
        logger.info(f"最优解 (3, 2) 与当前解的距离: {np.linalg.norm(current_point - np.array([3, 2])):.6f}")
        
        # 可视化
        self.visualize_gradient_descent(loss_function, trajectory, losses)
    
    def numerical_integration(self) -> None:
        """数值积分演示"""
        logger.info("=== 数值积分演示 ===")
        
        # 定义被积函数 f(x) = x²
        def f(x):
            return x**2
        
        # 积分区间
        a, b = 0, 3
        
        # 解析解: ∫₀³ x² dx = [x³/3]₀³ = 27/3 = 9
        analytical_result = 9.0
        logger.info(f"函数 f(x) = x² 在区间 [{a}, {b}] 上的定积分")
        logger.info(f"解析解: {analytical_result}")
        
        # 数值积分方法
        # 1. 梯形法则
        x_trapezoid = np.linspace(a, b, 1000)
        y_trapezoid = f(x_trapezoid)
        trapezoid_result = np.trapz(y_trapezoid, x_trapezoid)
        logger.info(f"梯形法则结果: {trapezoid_result:.6f}")
        logger.info(f"梯形法则误差: {abs(trapezoid_result - analytical_result):.2e}")
        
        # 2. Simpson法则
        simpson_result, simpson_error = integrate.quad(f, a, b)
        logger.info(f"Simpson法则结果: {simpson_result:.6f}")
        logger.info(f"Simpson法则误差: {abs(simpson_result - analytical_result):.2e}")
        
        # 3. Monte Carlo方法
        n_samples = 100000
        x_mc = np.random.uniform(a, b, n_samples)
        y_mc = f(x_mc)
        mc_result = (b - a) * np.mean(y_mc)
        logger.info(f"Monte Carlo结果: {mc_result:.6f}")
        logger.info(f"Monte Carlo误差: {abs(mc_result - analytical_result):.2e}")
        
        # 可视化
        self.visualize_integration(f, a, b, analytical_result)
    
    def chain_rule_demo(self) -> None:
        """链式法则演示"""
        logger.info("=== 链式法则演示 ===")
        
        # 复合函数: h(x) = f(g(x)) = (2x + 1)³
        # 其中 g(x) = 2x + 1, f(u) = u³
        
        def g(x):
            return 2*x + 1
        
        def f(u):
            return u**3
        
        def h(x):
            return f(g(x))  # (2x + 1)³
        
        # 导数计算
        def dg_dx(x):
            return 2  # g'(x) = 2
        
        def df_du(u):
            return 3*u**2  # f'(u) = 3u²
        
        def dh_dx(x):
            u = g(x)
            return df_du(u) * dg_dx(x)  # 链式法则: h'(x) = f'(g(x)) * g'(x)
        
        # 验证链式法则
        test_x = 1.0
        u_val = g(test_x)
        direct_derivative = 3 * (2*test_x + 1)**2 * 2  # 直接求导
        chain_rule_derivative = dh_dx(test_x)  # 链式法则
        
        logger.info(f"复合函数 h(x) = (2x + 1)³")
        logger.info(f"在 x = {test_x} 处:")
        logger.info(f"  g({test_x}) = {u_val}")
        logger.info(f"  直接求导结果: {direct_derivative}")
        logger.info(f"  链式法则结果: {chain_rule_derivative}")
        logger.info(f"  误差: {abs(direct_derivative - chain_rule_derivative):.2e}")
        
        # 可视化
        self.visualize_chain_rule(h, dh_dx, test_x)
    
    def visualize_derivative(self, f: Callable, f_prime: Callable, x_point: float) -> None:
        """可视化导数概念"""
        plt.figure(figsize=(12, 8))
        
        # 绘制原函数
        x = np.linspace(-3, 3, 1000)
        y = f(x)
        plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
        
        # 绘制切线
        tangent_x = np.linspace(x_point - 1, x_point + 1, 100)
        tangent_y = f_prime(x_point) * (tangent_x - x_point) + f(x_point)
        plt.plot(tangent_x, tangent_y, 'r--', linewidth=2, 
                label=f'切线 (斜率 = {f_prime(x_point)})')
        
        # 标记切点
        plt.plot(x_point, f(x_point), 'ro', markersize=8, 
                label=f'切点 ({x_point}, {f(x_point)})')
        
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.title('导数的几何意义 - 切线斜率')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(-3, 3)
        plt.ylim(-1, 10)
        
        plt.savefig('derivative_concept.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("导数概念图已保存为 derivative_concept.png")
    
    def visualize_partial_derivatives(self, f: Callable, df_dx: Callable, 
                                    df_dy: Callable, x_point: float, y_point: float) -> None:
        """可视化偏导数"""
        fig = plt.figure(figsize=(15, 5))
        
        # 3D表面图
        ax1 = fig.add_subplot(131, projection='3d')
        x = np.linspace(-3, 3, 50)
        y = np.linspace(-3, 3, 50)
        X, Y = np.meshgrid(x, y)
        Z = f(X, Y)
        
        ax1.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')
        ax1.scatter([x_point], [y_point], [f(x_point, y_point)], 
                   color='red', s=100, label='考察点')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('f(x,y)')
        ax1.set_title('函数表面')
        
        # 等高线图
        ax2 = fig.add_subplot(132)
        contour = ax2.contour(X, Y, Z, levels=20)
        ax2.clabel(contour, inline=True, fontsize=8)
        ax2.plot(x_point, y_point, 'ro', markersize=8, label='考察点')
        
        # 绘制梯度方向
        grad_x = df_dx(x_point, y_point)
        grad_y = df_dy(x_point, y_point)
        ax2.arrow(x_point, y_point, 0.5*grad_x, 0.5*grad_y, 
                 head_width=0.2, head_length=0.3, fc='red', ec='red',
                 label=f'梯度方向 [{grad_x:.1f}, {grad_y:.1f}]')
        
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_title('等高线图与梯度')
        
        # 梯度向量图
        ax3 = fig.add_subplot(133)
        X_grid, Y_grid = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
        U = df_dx(X_grid, Y_grid)
        V = df_dy(X_grid, Y_grid)
        ax3.quiver(X_grid, Y_grid, U, V, np.sqrt(U**2 + V**2), 
                  cmap='viridis', scale=50)
        ax3.plot(x_point, y_point, 'ro', markersize=8, label='考察点')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.set_xlabel('x')
        ax3.set_ylabel('y')
        ax3.set_title('梯度场')
        
        plt.tight_layout()
        plt.savefig('partial_derivatives.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("偏导数图已保存为 partial_derivatives.png")
    
    def visualize_gradient_descent(self, loss_func: Callable, 
                                 trajectory: np.ndarray, losses: list) -> None:
        """可视化梯度下降过程"""
        fig = plt.figure(figsize=(15, 5))
        
        # 损失函数等高线图
        ax1 = fig.add_subplot(131)
        x_range = np.linspace(-1, 5, 100)
        y_range = np.linspace(-1, 5, 100)
        X, Y = np.meshgrid(x_range, y_range)
        Z = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = loss_func(X[i, j], Y[i, j])
        
        contour = ax1.contour(X, Y, Z, levels=20)
        ax1.clabel(contour, inline=True, fontsize=8)
        
        # 绘制轨迹
        ax1.plot(trajectory[:, 0], trajectory[:, 1], 'ro-', markersize=4, 
                linewidth=2, label='优化轨迹')
        ax1.plot(3, 2, 'g*', markersize=15, label='最优点 (3, 2)')
        ax1.plot(trajectory[0, 0], trajectory[0, 1], 'bs', markersize=8, 
                label='起始点')
        
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title('梯度下降轨迹')
        
        # 损失值变化
        ax2 = fig.add_subplot(132)
        iterations = range(len(losses))
        ax2.plot(iterations, losses, 'b-o', markersize=4)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('迭代次数')
        ax2.set_ylabel('损失值')
        ax2.set_title('损失函数收敛过程')
        
        # 对数尺度损失变化
        ax3 = fig.add_subplot(133)
        ax3.semilogy(iterations, losses, 'r-o', markersize=4)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlabel('迭代次数')
        ax3.set_ylabel('损失值 (对数尺度)')
        ax3.set_title('收敛速度分析')
        
        plt.tight_layout()
        plt.savefig('gradient_descent.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("梯度下降图已保存为 gradient_descent.png")
    
    def visualize_integration(self, f: Callable, a: float, b: float, 
                            analytical_result: float) -> None:
        """可视化积分概念"""
        plt.figure(figsize=(12, 8))
        
        # 绘制函数曲线
        x = np.linspace(a-0.5, b+0.5, 1000)
        y = f(x)
        plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
        
        # 填充积分区域
        x_fill = np.linspace(a, b, 1000)
        y_fill = f(x_fill)
        plt.fill_between(x_fill, 0, y_fill, alpha=0.3, color='green', 
                        label=f'积分区域 = {analytical_result}')
        
        # 绘制积分边界
        plt.axvline(x=a, color='red', linestyle='--', linewidth=2, 
                   label=f'下限 a = {a}')
        plt.axvline(x=b, color='red', linestyle='--', linewidth=2, 
                   label=f'上限 b = {b}')
        
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.title('定积分的几何意义 - 曲边梯形面积')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(a-0.5, b+0.5)
        plt.ylim(0, max(y)*1.1)
        
        plt.savefig('integration_concept.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("积分概念图已保存为 integration_concept.png")
    
    def visualize_chain_rule(self, h: Callable, dh_dx: Callable, x_point: float) -> None:
        """可视化链式法则"""
        plt.figure(figsize=(12, 8))
        
        # 绘制复合函数
        x = np.linspace(-1, 3, 1000)
        y = h(x)
        plt.plot(x, y, 'b-', linewidth=2, label='h(x) = (2x+1)³')
        
        # 绘制切线
        slope = dh_dx(x_point)
        tangent_y = slope * (x - x_point) + h(x_point)
        plt.plot(x, tangent_y, 'r--', linewidth=2, 
                label=f'切线 (斜率 = {slope:.1f})')
        
        # 标记考察点
        plt.plot(x_point, h(x_point), 'ro', markersize=8, 
                label=f'考察点 ({x_point}, {h(x_point):.1f})')
        
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.title('链式法则 - 复合函数的导数')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(-1, 3)
        plt.ylim(0, 50)
        
        plt.savefig('chain_rule.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("链式法则图已保存为 chain_rule.png")

def main():
    """主函数 - 运行所有微积分演示"""
    logger.info("开始微积分基础演示")
    
    calc = CalculusBasics()
    
    # 执行各项演示
    calc.derivative_concept()
    calc.partial_derivatives()
    calc.gradient_descent_demo()
    calc.numerical_integration()
    calc.chain_rule_demo()
    
    logger.info("微积分基础演示完成")

if __name__ == "__main__":
    main()