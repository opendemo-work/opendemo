#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
线性代数基础演示程序
展示向量运算、矩阵操作、特征值分解等AI/ML核心数学概念
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LinearAlgebraBasics:
    """线性代数基础类 - 演示核心概念和运算"""
    
    def __init__(self):
        """初始化线性代数演示环境"""
        logger.info("初始化线性代数基础演示")
        self.setup_plot_style()
    
    def setup_plot_style(self):
        """设置绘图样式"""
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
        plt.rcParams['axes.unicode_minus'] = False    # 支持负号显示
        plt.style.use('seaborn-v0_8')                 # 使用seaborn样式
    
    def vector_operations(self) -> None:
        """向量运算演示"""
        logger.info("=== 向量运算演示 ===")
        
        # 创建向量
        v1 = np.array([3, 4])
        v2 = np.array([1, 2])
        
        logger.info(f"向量 v1: {v1}")
        logger.info(f"向量 v2: {v2}")
        
        # 向量加法
        v_sum = v1 + v2
        logger.info(f"向量加法 v1 + v2 = {v_sum}")
        
        # 向量减法
        v_diff = v1 - v2
        logger.info(f"向量减法 v1 - v2 = {v_diff}")
        
        # 标量乘法
        scalar = 2
        v_scaled = scalar * v1
        logger.info(f"标量乘法 {scalar} * v1 = {v_scaled}")
        
        # 点积（内积）
        dot_product = np.dot(v1, v2)
        logger.info(f"点积 v1 · v2 = {dot_product}")
        
        # 向量模长
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        logger.info(f"向量v1模长: {norm_v1:.2f}")
        logger.info(f"向量v2模长: {norm_v2:.2f}")
        
        # 向量夹角
        cos_angle = dot_product / (norm_v1 * norm_v2)
        angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        angle_deg = np.degrees(angle_rad)
        logger.info(f"向量夹角: {angle_deg:.2f}°")
        
        # 可视化向量
        self.visualize_vectors(v1, v2, v_sum)
    
    def matrix_operations(self) -> None:
        """矩阵运算演示"""
        logger.info("=== 矩阵运算演示 ===")
        
        # 创建矩阵
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        
        logger.info(f"矩阵 A:\n{A}")
        logger.info(f"矩阵 B:\n{B}")
        
        # 矩阵加法
        C = A + B
        logger.info(f"矩阵加法 A + B =\n{C}")
        
        # 矩阵乘法
        D = np.dot(A, B)
        logger.info(f"矩阵乘法 A × B =\n{D}")
        
        # 矩阵转置
        A_T = A.T
        logger.info(f"矩阵A的转置 A^T =\n{A_T}")
        
        # 矩阵行列式
        det_A = np.linalg.det(A)
        logger.info(f"矩阵A的行列式 det(A) = {det_A:.2f}")
        
        # 矩阵逆
        if det_A != 0:
            A_inv = np.linalg.inv(A)
            logger.info(f"矩阵A的逆 A^(-1) =\n{A_inv}")
            
            # 验证逆矩阵
            identity = np.dot(A, A_inv)
            logger.info(f"A × A^(-1) =\n{identity}")
        else:
            logger.warning("矩阵A不可逆（行列式为0）")
        
        # 矩阵秩
        rank_A = np.linalg.matrix_rank(A)
        logger.info(f"矩阵A的秩: {rank_A}")
    
    def eigen_decomposition(self) -> None:
        """特征值分解演示"""
        logger.info("=== 特征值分解演示 ===")
        
        # 创建对称矩阵（便于特征值分解）
        A = np.array([[4, 2], [2, 3]])
        logger.info(f"对称矩阵 A:\n{A}")
        
        # 计算特征值和特征向量
        eigenvalues, eigenvectors = np.linalg.eig(A)
        
        logger.info(f"特征值: {eigenvalues}")
        logger.info(f"特征向量:\n{eigenvectors}")
        
        # 验证特征值分解
        # A * v = λ * v
        for i in range(len(eigenvalues)):
            lambda_i = eigenvalues[i]
            v_i = eigenvectors[:, i]
            Av = np.dot(A, v_i)
            lambda_v = lambda_i * v_i
            
            logger.info(f"验证第{i+1}个特征值:")
            logger.info(f"  A * v_{i+1} = {Av}")
            logger.info(f"  λ_{i+1} * v_{i+1} = {lambda_v}")
            logger.info(f"  误差: {np.linalg.norm(Av - lambda_v):.2e}")
        
        # 可视化特征向量
        self.visualize_eigenvectors(A, eigenvalues, eigenvectors)
    
    def singular_value_decomposition(self) -> None:
        """奇异值分解演示"""
        logger.info("=== 奇异值分解演示 ===")
        
        # 创建矩形矩阵
        A = np.array([[1, 2, 3], [4, 5, 6]])
        logger.info(f"矩阵 A:\n{A}")
        
        # 进行奇异值分解: A = U * Σ * V^T
        U, singular_values, Vt = np.linalg.svd(A, full_matrices=True)
        
        logger.info(f"U矩阵:\n{U}")
        logger.info(f"奇异值: {singular_values}")
        logger.info(f"V^T矩阵:\n{Vt}")
        
        # 重构矩阵
        # 创建对角矩阵Σ
        Sigma = np.zeros((U.shape[1], Vt.shape[0]))
        np.fill_diagonal(Sigma, singular_values)
        
        # 验证分解
        A_reconstructed = np.dot(U, np.dot(Sigma, Vt))
        reconstruction_error = np.linalg.norm(A - A_reconstructed)
        
        logger.info(f"重构矩阵:\n{A_reconstructed}")
        logger.info(f"重构误差: {reconstruction_error:.2e}")
    
    def visualize_vectors(self, v1: np.ndarray, v2: np.ndarray, v_sum: np.ndarray) -> None:
        """可视化向量运算"""
        plt.figure(figsize=(10, 8))
        
        # 绘制向量
        plt.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, 
                  color='blue', width=0.005, label=f'v1 = {v1}')
        plt.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, 
                  color='red', width=0.005, label=f'v2 = {v2}')
        plt.quiver(0, 0, v_sum[0], v_sum[1], angles='xy', scale_units='xy', scale=1, 
                  color='green', width=0.005, label=f'v1+v2 = {v_sum}')
        
        # 设置图形属性
        max_val = max(np.abs([v1, v2, v_sum]).max()) + 1
        plt.xlim(-max_val, max_val)
        plt.ylim(-max_val, max_val)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)
        plt.legend()
        plt.title('向量运算可视化')
        plt.xlabel('X轴')
        plt.ylabel('Y轴')
        plt.axis('equal')
        
        # 保存图像
        plt.savefig('vector_operations.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("向量运算图已保存为 vector_operations.png")
    
    def visualize_eigenvectors(self, A: np.ndarray, eigenvalues: np.ndarray, 
                              eigenvectors: np.ndarray) -> None:
        """可视化特征向量"""
        plt.figure(figsize=(10, 8))
        
        # 绘制单位圆
        theta = np.linspace(0, 2*np.pi, 100)
        circle_x = np.cos(theta)
        circle_y = np.sin(theta)
        plt.plot(circle_x, circle_y, 'b--', alpha=0.5, label='单位圆')
        
        # 绘制变换后的椭圆
        transformed_points = []
        for i in range(len(theta)):
            point = np.array([circle_x[i], circle_y[i]])
            transformed_point = np.dot(A, point)
            transformed_points.append(transformed_point)
        
        transformed_points = np.array(transformed_points)
        plt.plot(transformed_points[:, 0], transformed_points[:, 1], 'r-', 
                alpha=0.7, label='变换后')
        
        # 绘制特征向量
        for i in range(len(eigenvalues)):
            v = eigenvectors[:, i]
            scale = np.sqrt(eigenvalues[i])  # 特征值的平方根表示伸缩比例
            plt.quiver(0, 0, v[0]*scale, v[1]*scale, angles='xy', 
                      scale_units='xy', scale=1, color=['orange', 'purple'][i],
                      width=0.008, label=f'特征向量 {i+1} (λ={eigenvalues[i]:.2f})')
        
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)
        plt.legend()
        plt.title('矩阵变换与特征向量可视化')
        plt.xlabel('X轴')
        plt.ylabel('Y轴')
        plt.axis('equal')
        
        # 保存图像
        plt.savefig('eigenvectors.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("特征向量图已保存为 eigenvectors.png")

def main():
    """主函数 - 运行所有线性代数演示"""
    logger.info("开始线性代数基础演示")
    
    la = LinearAlgebraBasics()
    
    # 执行各项演示
    la.vector_operations()
    la.matrix_operations()
    la.eigen_decomposition()
    la.singular_value_decomposition()
    
    logger.info("线性代数基础演示完成")

if __name__ == "__main__":
    main()