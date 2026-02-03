#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卷积神经网络基础演示程序
展示卷积操作、池化操作、CNN架构等计算机视觉核心概念
"""

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from typing import Tuple, List
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CNNBasics:
    """卷积神经网络基础类 - 演示核心概念和实现"""
    
    def __init__(self):
        """初始化CNN演示环境"""
        logger.info("初始化卷积神经网络基础演示")
        self.setup_plot_style()
    
    def setup_plot_style(self):
        """设置绘图样式"""
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('seaborn-v0_8')
    
    def convolution_operation_demo(self) -> None:
        """卷积操作演示"""
        logger.info("=== 卷积操作演示 ===")
        
        # 创建示例图像 (7x7)
        image = np.array([
            [1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ], dtype=float)
        
        # 定义边缘检测滤波器
        edge_filter = np.array([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ], dtype=float)
        
        logger.info("原始图像:")
        logger.info(image)
        logger.info("边缘检测滤波器:")
        logger.info(edge_filter)
        
        # 执行卷积操作
        convolved = self.manual_conv2d(image, edge_filter, padding=1)
        logger.info("卷积结果:")
        logger.info(convolved)
        
        # 可视化
        self.visualize_convolution(image, edge_filter, convolved)
    
    def pooling_operation_demo(self) -> None:
        """池化操作演示"""
        logger.info("=== 池化操作演示 ===")
        
        # 创建示例特征图
        feature_map = np.random.rand(6, 6) * 10
        logger.info("原始特征图:")
        logger.info(feature_map)
        
        # 最大池化
        max_pooled = self.manual_max_pool2d(feature_map, pool_size=2)
        logger.info("最大池化结果 (2x2):")
        logger.info(max_pooled)
        
        # 平均池化
        avg_pooled = self.manual_avg_pool2d(feature_map, pool_size=2)
        logger.info("平均池化结果 (2x2):")
        logger.info(avg_pooled)
        
        # 可视化
        self.visualize_pooling(feature_map, max_pooled, avg_pooled)
    
    def simple_cnn_architecture_demo(self) -> None:
        """简单CNN架构演示"""
        logger.info("=== 简单CNN架构演示 ===")
        
        # 定义简单CNN模型
        class SimpleCNN(nn.Module):
            def __init__(self):
                super(SimpleCNN, self).__init__()
                # 卷积层1: 1->16通道, 3x3卷积核
                self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
                # 卷积层2: 16->32通道, 3x3卷积核
                self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
                # 最大池化层
                self.pool = nn.MaxPool2d(2, 2)
                # 全连接层
                self.fc1 = nn.Linear(32 * 7 * 7, 128)
                self.fc2 = nn.Linear(128, 10)  # 10个类别
                
            def forward(self, x):
                # 第一个卷积块
                x = self.pool(F.relu(self.conv1(x)))  # 28x28 -> 14x14
                # 第二个卷积块
                x = self.pool(F.relu(self.conv2(x)))  # 14x14 -> 7x7
                # 展平
                x = x.view(-1, 32 * 7 * 7)
                # 全连接层
                x = F.relu(self.fc1(x))
                x = self.fc2(x)
                return x
        
        model = SimpleCNN()
        logger.info("CNN模型架构:")
        logger.info(model)
        
        # 计算参数数量
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        logger.info(f"总参数数量: {total_params:,}")
        logger.info(f"可训练参数: {trainable_params:,}")
        
        # 演示前向传播
        dummy_input = torch.randn(1, 1, 28, 28)  # 模拟MNIST图像
        with torch.no_grad():
            output = model(dummy_input)
            logger.info(f"输入形状: {dummy_input.shape}")
            logger.info(f"输出形状: {output.shape}")
            logger.info(f"输出值范围: [{output.min():.3f}, {output.max():.3f}]")
    
    def manual_conv2d(self, image: np.ndarray, kernel: np.ndarray, 
                     padding: int = 0) -> np.ndarray:
        """手动实现2D卷积操作"""
        if padding > 0:
            padded_image = np.pad(image, padding, mode='constant')
        else:
            padded_image = image
        
        kernel_height, kernel_width = kernel.shape
        image_height, image_width = padded_image.shape
        
        # 输出尺寸计算
        out_height = image_height - kernel_height + 1
        out_width = image_width - kernel_width + 1
        
        result = np.zeros((out_height, out_width))
        
        # 执行卷积
        for i in range(out_height):
            for j in range(out_width):
                # 提取图像块
                image_patch = padded_image[i:i+kernel_height, j:j+kernel_width]
                # 计算卷积
                result[i, j] = np.sum(image_patch * kernel)
        
        return result
    
    def manual_max_pool2d(self, feature_map: np.ndarray, 
                         pool_size: int = 2) -> np.ndarray:
        """手动实现最大池化"""
        height, width = feature_map.shape
        out_height = height // pool_size
        out_width = width // pool_size
        
        result = np.zeros((out_height, out_width))
        
        for i in range(out_height):
            for j in range(out_width):
                # 提取池化区域
                region = feature_map[i*pool_size:(i+1)*pool_size, 
                                   j*pool_size:(j+1)*pool_size]
                # 取最大值
                result[i, j] = np.max(region)
        
        return result
    
    def manual_avg_pool2d(self, feature_map: np.ndarray, 
                         pool_size: int = 2) -> np.ndarray:
        """手动实现平均池化"""
        height, width = feature_map.shape
        out_height = height // pool_size
        out_width = width // pool_size
        
        result = np.zeros((out_height, out_width))
        
        for i in range(out_height):
            for j in range(out_width):
                # 提取池化区域
                region = feature_map[i*pool_size:(i+1)*pool_size, 
                                   j*pool_size:(j+1)*pool_size]
                # 取平均值
                result[i, j] = np.mean(region)
        
        return result
    
    def visualize_convolution(self, image: np.ndarray, kernel: np.ndarray, 
                            result: np.ndarray) -> None:
        """可视化卷积操作"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 原始图像
        axes[0].imshow(image, cmap='gray')
        axes[0].set_title('原始图像')
        axes[0].axis('off')
        
        # 卷积核
        im1 = axes[1].imshow(kernel, cmap='RdBu', vmin=-1, vmax=1)
        axes[1].set_title('卷积核 (边缘检测)')
        axes[1].axis('off')
        plt.colorbar(im1, ax=axes[1])
        
        # 卷积结果
        im2 = axes[2].imshow(result, cmap='gray')
        axes[2].set_title('卷积结果')
        axes[2].axis('off')
        plt.colorbar(im2, ax=axes[2])
        
        plt.tight_layout()
        plt.savefig('cnn_convolution.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("卷积操作图已保存为 cnn_convolution.png")
    
    def visualize_pooling(self, original: np.ndarray, max_pooled: np.ndarray, 
                         avg_pooled: np.ndarray) -> None:
        """可视化池化操作"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 原始特征图
        im0 = axes[0].imshow(original, cmap='viridis')
        axes[0].set_title('原始特征图')
        axes[0].axis('off')
        plt.colorbar(im0, ax=axes[0])
        
        # 最大池化
        im1 = axes[1].imshow(max_pooled, cmap='viridis')
        axes[1].set_title('最大池化')
        axes[1].axis('off')
        plt.colorbar(im1, ax=axes[1])
        
        # 平均池化
        im2 = axes[2].imshow(avg_pooled, cmap='viridis')
        axes[2].set_title('平均池化')
        axes[2].axis('off')
        plt.colorbar(im2, ax=axes[2])
        
        plt.tight_layout()
        plt.savefig('cnn_pooling.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("池化操作图已保存为 cnn_pooling.png")

def main():
    """主函数 - 运行所有CNN演示"""
    logger.info("开始卷积神经网络基础演示")
    
    cnn_demo = CNNBasics()
    
    # 执行各项演示
    cnn_demo.convolution_operation_demo()
    cnn_demo.pooling_operation_demo()
    cnn_demo.simple_cnn_architecture_demo()
    
    logger.info("卷积神经网络基础演示完成")

if __name__ == "__main__":
    main()