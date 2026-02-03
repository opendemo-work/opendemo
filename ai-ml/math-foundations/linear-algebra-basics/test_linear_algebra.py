#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
线性代数基础测试文件
测试向量运算、矩阵操作、特征值分解等功能的正确性
"""

import numpy as np
import pytest
from linear_algebra_basics import LinearAlgebraBasics

class TestLinearAlgebraBasics:
    """线性代数基础测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.la = LinearAlgebraBasics()
    
    def test_vector_addition(self):
        """测试向量加法"""
        v1 = np.array([1, 2, 3])
        v2 = np.array([4, 5, 6])
        expected = np.array([5, 7, 9])
        result = v1 + v2
        np.testing.assert_array_equal(result, expected)
    
    def test_vector_dot_product(self):
        """测试向量点积"""
        v1 = np.array([1, 2, 3])
        v2 = np.array([4, 5, 6])
        expected = 32  # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
        result = np.dot(v1, v2)
        assert result == expected
    
    def test_vector_norm(self):
        """测试向量模长"""
        v = np.array([3, 4])
        expected = 5.0  # sqrt(3² + 4²) = sqrt(25) = 5
        result = np.linalg.norm(v)
        assert abs(result - expected) < 1e-10
    
    def test_matrix_multiplication(self):
        """测试矩阵乘法"""
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        expected = np.array([[19, 22], [43, 50]])  # 手工计算结果
        result = np.dot(A, B)
        np.testing.assert_array_equal(result, expected)
    
    def test_matrix_determinant(self):
        """测试矩阵行列式"""
        A = np.array([[1, 2], [3, 4]])
        expected = -2  # 1*4 - 2*3 = 4 - 6 = -2
        result = np.linalg.det(A)
        assert abs(result - expected) < 1e-10
    
    def test_matrix_inverse(self):
        """测试矩阵逆"""
        A = np.array([[4, 7], [2, 6]])
        expected_det = 10  # 4*6 - 7*2 = 24 - 14 = 10
        det = np.linalg.det(A)
        assert abs(det - expected_det) < 1e-10
        
        # 测试逆矩阵存在
        A_inv = np.linalg.inv(A)
        # 验证 A * A^(-1) = I
        identity = np.dot(A, A_inv)
        expected_identity = np.eye(2)
        np.testing.assert_array_almost_equal(identity, expected_identity, decimal=10)
    
    def test_eigen_decomposition(self):
        """测试特征值分解"""
        # 创建对称矩阵
        A = np.array([[4, 2], [2, 3]])
        
        # 计算特征值和特征向量
        eigenvalues, eigenvectors = np.linalg.eig(A)
        
        # 验证特征值分解的正确性
        # A * v = λ * v 对每个特征值和特征向量都应该成立
        for i in range(len(eigenvalues)):
            lambda_i = eigenvalues[i]
            v_i = eigenvectors[:, i]
            Av = np.dot(A, v_i)
            lambda_v = lambda_i * v_i
            
            # 验证误差在可接受范围内
            error = np.linalg.norm(Av - lambda_v)
            assert error < 1e-10, f"特征值分解验证失败，误差: {error}"
    
    def test_singular_value_decomposition(self):
        """测试奇异值分解"""
        # 创建矩阵
        A = np.array([[1, 2, 3], [4, 5, 6]])
        
        # 进行SVD分解
        U, singular_values, Vt = np.linalg.svd(A, full_matrices=True)
        
        # 重构矩阵
        Sigma = np.zeros((U.shape[1], Vt.shape[0]))
        np.fill_diagonal(Sigma, singular_values)
        A_reconstructed = np.dot(U, np.dot(Sigma, Vt))
        
        # 验证重构误差很小
        reconstruction_error = np.linalg.norm(A - A_reconstructed)
        assert reconstruction_error < 1e-10, f"SVD重构误差过大: {reconstruction_error}"
    
    def test_matrix_rank(self):
        """测试矩阵秩"""
        # 满秩矩阵
        A_full_rank = np.array([[1, 2], [3, 4]])
        rank_full = np.linalg.matrix_rank(A_full_rank)
        assert rank_full == 2
        
        # 秩亏矩阵
        A_rank_deficient = np.array([[1, 2], [2, 4]])  # 第二行是第一行的2倍
        rank_deficient = np.linalg.matrix_rank(A_rank_deficient)
        assert rank_deficient == 1
    
    def test_orthogonal_vectors(self):
        """测试正交向量"""
        # 创建正交向量
        v1 = np.array([1, 0])
        v2 = np.array([0, 1])
        
        # 正交向量的点积应该为0
        dot_product = np.dot(v1, v2)
        assert abs(dot_product) < 1e-10
        
        # 验证都是单位向量
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        assert abs(norm_v1 - 1.0) < 1e-10
        assert abs(norm_v2 - 1.0) < 1e-10

if __name__ == "__main__":
    pytest.main([__file__, "-v"])