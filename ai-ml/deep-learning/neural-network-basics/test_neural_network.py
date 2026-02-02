#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神经网络基础测试文件
测试感知机、MLP、激活函数、反向传播等功能的正确性
"""

import numpy as np
import torch
import pytest
from neural_network_basics import NeuralNetworkBasics

class TestNeuralNetworkBasics:
    """神经网络基础测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.nn = NeuralNetworkBasics()
    
    def test_step_activation(self):
        """测试阶跃激活函数"""
        assert self.nn.step_activation(1.0) == 1
        assert self.nn.step_activation(0.0) == 1  # >= 0 为1
        assert self.nn.step_activation(-1.0) == 0
    
    def test_sigmoid_function(self):
        """测试Sigmoid激活函数"""
        x = np.array([0, 1, -1, 10, -10])
        result = self.nn.sigmoid(x)
        
        # 验证范围在(0,1)之间
        assert np.all(result > 0) and np.all(result < 1)
        
        # 验证特定值
        assert abs(result[0] - 0.5) < 1e-10  # sigmoid(0) = 0.5
        assert result[3] > 0.999  # sigmoid(10) ≈ 1
        assert result[4] < 0.001  # sigmoid(-10) ≈ 0
    
    def test_relu_function(self):
        """测试ReLU激活函数"""
        x = np.array([-2, -1, 0, 1, 2])
        result = self.nn.relu(x)
        
        # ReLU应该将负值变为0
        expected = np.array([0, 0, 0, 1, 2])
        np.testing.assert_array_equal(result, expected)
    
    def test_tanh_function(self):
        """测试Tanh激活函数"""
        x = np.array([0, 1, -1])
        result = self.nn.tanh(x)
        
        # 验证范围在(-1,1)之间
        assert np.all(result >= -1) and np.all(result <= 1)
        
        # 验证特定值
        assert abs(result[0]) < 1e-10  # tanh(0) = 0
        assert result[1] > 0  # tanh(1) > 0
        assert result[2] < 0  # tanh(-1) < 0
    
    def test_perceptron_and_gate(self):
        """测试感知机实现AND门"""
        # AND门真值表
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
        y = np.array([0, 0, 0, 1], dtype=float)
        
        # 手动设置合适的权重和偏置
        weights = np.array([1.0, 1.0])
        bias = -1.5
        
        # 测试所有输入
        correct_predictions = 0
        for i in range(len(X)):
            z = np.dot(weights, X[i]) + bias
            prediction = self.nn.step_activation(z)
            if abs(prediction - y[i]) < 1e-10:
                correct_predictions += 1
        
        # AND门应该能够被线性分离
        assert correct_predictions >= 3, f"AND门实现不正确，正确预测: {correct_predictions}/4"
    
    def test_softmax_normalization(self):
        """测试Softmax归一化"""
        x = np.array([1, 2, 3, 4, 5])
        result = self.nn.softmax_1d(x)
        
        # 验证和为1
        assert abs(np.sum(result) - 1.0) < 1e-10
        
        # 验证所有值为正
        assert np.all(result > 0)
        
        # 验证单调性（较大的输入对应较大的输出）
        assert result[0] < result[1] < result[2] < result[3] < result[4]
    
    def test_matrix_operations_shapes(self):
        """测试矩阵运算的形状兼容性"""
        # 测试前向传播中的矩阵乘法
        X = np.random.randn(4, 2)  # 4个样本，2个特征
        W = np.random.randn(2, 3)  # 2个输入，3个隐藏单元
        b = np.random.randn(1, 3)  # 偏置
        
        # 前向传播
        z = np.dot(X, W) + b
        assert z.shape == (4, 3)  # 应该得到4个样本，3个隐藏单元的输出
        
        # 激活函数
        a = self.nn.sigmoid(z)
        assert a.shape == z.shape
    
    def test_pytorch_mlp_structure(self):
        """测试PyTorch MLP网络结构"""
        import torch.nn as nn
        
        class SimpleMLP(nn.Module):
            def __init__(self):
                super(SimpleMLP, self).__init__()
                self.hidden = nn.Linear(2, 8)
                self.output = nn.Linear(8, 1)
                self.activation = nn.ReLU()
                self.sigmoid = nn.Sigmoid()
            
            def forward(self, x):
                x = self.activation(self.hidden(x))
                x = self.sigmoid(self.output(x))
                return x
        
        model = SimpleMLP()
        
        # 测试输入输出维度
        test_input = torch.randn(10, 2)  # 10个样本，2个特征
        output = model(test_input)
        
        assert output.shape == (10, 1)  # 10个样本，1个输出
        assert torch.all(output >= 0) and torch.all(output <= 1)  # Sigmoid输出范围
    
    def test_gradient_computation(self):
        """测试梯度计算的正确性"""
        # 使用PyTorch验证手动梯度计算
        import torch.nn.functional as F
        
        # 简单的损失函数和梯度计算
        x = torch.tensor([2.0], requires_grad=True)
        y = x**2  # y = x²
        y.backward()  # dy/dx = 2x
        
        expected_gradient = 2 * x.item()  # 2 * 2 = 4
        actual_gradient = x.grad.item()
        
        assert abs(actual_gradient - expected_gradient) < 1e-10
    
    def test_xor_problem_impossible_linear(self):
        """测试XOR问题无法线性分离"""
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
        y = np.array([0, 1, 1, 0], dtype=float)  # XOR输出
        
        # 尝试用线性分类器解决XOR
        weights = np.array([1.0, 1.0])
        bias = -0.5
        
        correct_linear = 0
        for i in range(len(X)):
            z = np.dot(weights, X[i]) + bias
            prediction = self.nn.step_activation(z)
            if abs(prediction - y[i]) < 1e-10:
                correct_linear += 1
        
        # 线性分类器无法正确解决XOR问题
        assert correct_linear < 4, f"线性分类器意外解决了XOR问题，正确率: {correct_linear}/4"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])