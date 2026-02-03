#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卷积神经网络基础测试文件
测试卷积操作、池化操作、CNN架构等功能的正确性
"""

import numpy as np
import torch
import torch.nn as nn
import pytest
from cnn_basics import CNNBasics

class TestCNNBasics:
    """卷积神经网络基础测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.cnn = CNNBasics()
    
    def test_manual_conv2d_basic(self):
        """测试手动卷积操作"""
        # 简单测试用例
        image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
        kernel = np.array([[1, 0], [0, 1]], dtype=float)
        
        result = self.cnn.manual_conv2d(image, kernel)
        
        # 验证输出尺寸
        assert result.shape == (2, 2)
        
        # 验证特定位置的计算结果
        expected_00 = 1*1 + 2*0 + 4*0 + 5*1  # 1*1 + 5*1 = 6
        assert abs(result[0, 0] - expected_00) < 1e-10
    
    def test_conv2d_with_padding(self):
        """测试带填充的卷积操作"""
        image = np.array([[1, 2], [3, 4]], dtype=float)
        kernel = np.array([[1, 1], [1, 1]], dtype=float)
        
        # 无填充
        result_no_pad = self.cnn.manual_conv2d(image, kernel, padding=0)
        assert result_no_pad.shape == (1, 1)
        
        # 有填充
        result_with_pad = self.cnn.manual_conv2d(image, kernel, padding=1)
        assert result_with_pad.shape == (2, 2)
    
    def test_max_pooling(self):
        """测试最大池化操作"""
        # 创建包含明显最大值的特征图
        feature_map = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ], dtype=float)
        
        pooled = self.cnn.manual_max_pool2d(feature_map, pool_size=2)
        
        # 验证输出尺寸
        assert pooled.shape == (2, 2)
        
        # 验证最大值提取正确
        expected = np.array([[6, 8], [14, 16]], dtype=float)
        np.testing.assert_array_equal(pooled, expected)
    
    def test_avg_pooling(self):
        """测试平均池化操作"""
        feature_map = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ], dtype=float)
        
        pooled = self.cnn.manual_avg_pool2d(feature_map, pool_size=2)
        
        # 验证输出尺寸
        assert pooled.shape == (2, 2)
        
        # 验证平均值计算正确
        expected = np.array([[3.5, 5.5], [11.5, 13.5]], dtype=float)
        np.testing.assert_array_almost_equal(pooled, expected, decimal=10)
    
    def test_pooling_size_consistency(self):
        """测试池化尺寸一致性"""
        feature_map = np.random.rand(8, 8)
        
        # 测试不同池化尺寸
        for pool_size in [2, 4]:
            pooled = self.cnn.manual_max_pool2d(feature_map, pool_size)
            expected_shape = (8 // pool_size, 8 // pool_size)
            assert pooled.shape == expected_shape
    
    def test_pytorch_cnn_layer(self):
        """测试PyTorch CNN层"""
        # 测试卷积层
        conv_layer = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        
        # 测试输入输出
        test_input = torch.randn(1, 1, 28, 28)
        output = conv_layer(test_input)
        
        assert output.shape == (1, 32, 28, 28)  # 保持空间尺寸不变(因为padding=1)
    
    def test_cnn_parameter_count(self):
        """测试CNN参数计数"""
        # 简单CNN层参数计算
        conv_layer = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3)
        
        # 计算期望参数数量: (3*3*3 + 1) * 16 = 448
        # 3*3*3 是权重参数，1是偏置参数
        expected_params = (3 * 3 * 3 + 1) * 16
        actual_params = sum(p.numel() for p in conv_layer.parameters())
        
        assert actual_params == expected_params
    
    def test_feature_map_dimensions(self):
        """测试特征图尺寸计算"""
        batch_size, channels, height, width = 4, 3, 32, 32
        
        # 卷积层测试
        conv = nn.Conv2d(channels, 64, kernel_size=3, padding=1)
        input_tensor = torch.randn(batch_size, channels, height, width)
        output = conv(input_tensor)
        
        # 验证输出尺寸
        assert output.shape == (batch_size, 64, height, width)  # padding=1保持尺寸
        
        # 池化层测试
        pool = nn.MaxPool2d(kernel_size=2, stride=2)
        pooled_output = pool(output)
        
        # 验证池化后尺寸减半
        assert pooled_output.shape == (batch_size, 64, height//2, width//2)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])