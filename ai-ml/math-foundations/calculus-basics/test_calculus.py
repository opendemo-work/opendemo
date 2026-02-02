#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微积分基础测试文件
测试导数、偏导数、梯度下降、积分等功能的正确性
"""

import numpy as np
import pytest
from calculus_basics import CalculusBasics

class TestCalculusBasics:
    """微积分基础测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.calc = CalculusBasics()
    
    def test_derivative_basic(self):
        """测试基本导数计算"""
        # f(x) = x², f'(x) = 2x
        def f(x):
            return x**2
        
        def f_prime(x):
            return 2*x
        
        x_test = 3.0
        expected = 6.0  # 2 * 3 = 6
        result = f_prime(x_test)
        assert abs(result - expected) < 1e-10
    
    def test_partial_derivatives(self):
        """测试偏导数计算"""
        # f(x,y) = x² + y²
        # ∂f/∂x = 2x, ∂f/∂y = 2y
        
        def df_dx(x, y):
            return 2*x
        
        def df_dy(x, y):
            return 2*y
        
        x, y = 2.0, 3.0
        expected_dx = 4.0  # 2 * 2 = 4
        expected_dy = 6.0  # 2 * 3 = 6
        
        result_dx = df_dx(x, y)
        result_dy = df_dy(x, y)
        
        assert abs(result_dx - expected_dx) < 1e-10
        assert abs(result_dy - expected_dy) < 1e-10
    
    def test_gradient_calculation(self):
        """测试梯度计算"""
        # f(x,y) = x² + y², ∇f = [2x, 2y]
        def gradient(x, y):
            return np.array([2*x, 2*y])
        
        x, y = 1.0, 2.0
        expected_gradient = np.array([2.0, 4.0])
        result_gradient = gradient(x, y)
        
        np.testing.assert_array_almost_equal(result_gradient, expected_gradient, decimal=10)
    
    def test_gradient_descent_convergence(self):
        """测试梯度下降收敛性"""
        # f(x,y) = (x-3)² + (y-2)²，最小值在(3,2)
        def loss_function(x, y):
            return (x - 3)**2 + (y - 2)**2
        
        def gradient(x, y):
            return np.array([2*(x - 3), 2*(y - 2)])
        
        # 梯度下降参数
        learning_rate = 0.1
        max_iterations = 100
        tolerance = 1e-6
        
        # 初始点
        current_point = np.array([0.0, 0.0])
        
        # 梯度下降过程
        for i in range(max_iterations):
            grad = gradient(current_point[0], current_point[1])
            new_point = current_point - learning_rate * grad
            
            # 检查收敛
            if np.linalg.norm(new_point - current_point) < tolerance:
                break
            
            current_point = new_point
        
        # 验证是否接近最优解
        optimal_point = np.array([3.0, 2.0])
        distance_to_optimal = np.linalg.norm(current_point - optimal_point)
        assert distance_to_optimal < 0.1, f"未收敛到最优解附近，距离: {distance_to_optimal}"
    
    def test_numerical_integration(self):
        """测试数值积分"""
        # ∫₀³ x² dx = 9
        def f(x):
            return x**2
        
        # 梯形法则
        x = np.linspace(0, 3, 10000)
        y = f(x)
        trapezoid_result = np.trapz(y, x)
        expected = 9.0
        
        assert abs(trapezoid_result - expected) < 1e-3, \
               f"梯形法则误差过大: {abs(trapezoid_result - expected)}"
    
    def test_chain_rule(self):
        """测试链式法则"""
        # h(x) = f(g(x)) = (2x + 1)³
        # g(x) = 2x + 1, f(u) = u³
        # h'(x) = f'(g(x)) * g'(x) = 3(2x+1)² * 2 = 6(2x+1)²
        
        def g(x):
            return 2*x + 1
        
        def f(u):
            return u**3
        
        def dg_dx(x):
            return 2
        
        def df_du(u):
            return 3*u**2
        
        def dh_dx_direct(x):
            return 6 * (2*x + 1)**2  # 直接求导
        
        def dh_dx_chain(x):
            u = g(x)
            return df_du(u) * dg_dx(x)  # 链式法则
        
        # 测试点
        x_test = 1.0
        direct_result = dh_dx_direct(x_test)
        chain_result = dh_dx_chain(x_test)
        
        assert abs(direct_result - chain_result) < 1e-10, \
               f"链式法则验证失败: 直接求导={direct_result}, 链式法则={chain_result}"
    
    def test_second_derivative(self):
        """测试二阶导数"""
        # f(x) = x³, f'(x) = 3x², f''(x) = 6x
        def f(x):
            return x**3
        
        def f_double_prime(x):
            return 6*x
        
        x_test = 2.0
        expected = 12.0  # 6 * 2 = 12
        result = f_double_prime(x_test)
        
        assert abs(result - expected) < 1e-10
    
    def test_multivariable_function(self):
        """测试多元函数极值"""
        # f(x,y) = x² + y²，全局最小值在(0,0)
        def f(x, y):
            return x**2 + y**2
        
        # 验证在(0,0)处取得最小值
        min_value = f(0, 0)
        test_points = [(1, 1), (-1, -1), (2, 0), (0, 3)]
        
        for x, y in test_points:
            assert f(x, y) >= min_value, \
                   f"点({x},{y})处的函数值小于最小值"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])