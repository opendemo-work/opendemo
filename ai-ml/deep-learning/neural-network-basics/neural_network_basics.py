#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神经网络基础演示程序
展示感知机、多层感知机、激活函数、反向传播等深度学习核心概念
"""

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, List
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NeuralNetworkBasics:
    """神经网络基础类 - 演示核心概念和实现"""
    
    def __init__(self):
        """初始化神经网络演示环境"""
        logger.info("初始化神经网络基础演示")
        self.setup_plot_style()
    
    def setup_plot_style(self):
        """设置绘图样式"""
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
        plt.rcParams['axes.unicode_minus'] = False    # 支持负号显示
        plt.style.use('seaborn-v0_8')                 # 使用seaborn样式
    
    def perceptron_demo(self) -> None:
        """感知机演示"""
        logger.info("=== 感知机演示 ===")
        
        # AND逻辑门训练数据
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
        y = np.array([0, 0, 0, 1], dtype=float)  # AND门输出
        
        # 初始化权重和偏置
        weights = np.random.randn(2) * 0.1
        bias = np.random.randn() * 0.1
        learning_rate = 0.1
        epochs = 100
        
        logger.info(f"初始权重: {weights}")
        logger.info(f"初始偏置: {bias}")
        
        # 感知机训练
        losses = []
        for epoch in range(epochs):
            total_loss = 0
            for i in range(len(X)):
                # 前向传播
                z = np.dot(weights, X[i]) + bias
                prediction = self.step_activation(z)
                
                # 计算损失
                loss = y[i] - prediction
                total_loss += abs(loss)
                
                # 更新权重和偏置
                weights += learning_rate * loss * X[i]
                bias += learning_rate * loss
            
            avg_loss = total_loss / len(X)
            losses.append(avg_loss)
            
            if epoch % 20 == 0:
                logger.info(f"Epoch {epoch}: 平均损失 = {avg_loss:.4f}")
        
        logger.info(f"训练完成!")
        logger.info(f"最终权重: {weights}")
        logger.info(f"最终偏置: {bias}")
        
        # 测试训练结果
        logger.info("测试结果:")
        for i in range(len(X)):
            z = np.dot(weights, X[i]) + bias
            prediction = self.step_activation(z)
            logger.info(f"输入 {X[i]} -> 输出 {prediction} (期望: {y[i]})")
        
        # 可视化
        self.visualize_perceptron(X, y, weights, bias)
    
    def mlp_classification_demo(self) -> None:
        """多层感知机分类演示"""
        logger.info("=== 多层感知机分类演示 ===")
        
        # 生成非线性可分数据
        np.random.seed(42)
        X = np.random.randn(200, 2)
        # 创建环形数据集
        y = ((X[:, 0]**2 + X[:, 1]**2) > 1).astype(float)
        
        logger.info(f"数据集大小: {X.shape}")
        logger.info(f"类别分布: 类别0有{np.sum(y==0)}个样本, 类别1有{np.sum(y==1)}个样本")
        
        # 转换为PyTorch张量
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y).unsqueeze(1)
        
        # 定义简单的MLP模型
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
        criterion = nn.BCELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        
        # 训练模型
        epochs = 1000
        losses = []
        
        for epoch in range(epochs):
            # 前向传播
            outputs = model(X_tensor)
            loss = criterion(outputs, y_tensor)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            losses.append(loss.item())
            
            if epoch % 200 == 0:
                logger.info(f"Epoch {epoch}: 损失 = {loss.item():.4f}")
        
        # 评估模型
        with torch.no_grad():
            predictions = model(X_tensor)
            predicted_classes = (predictions > 0.5).float()
            accuracy = (predicted_classes == y_tensor).float().mean()
            logger.info(f"训练准确率: {accuracy.item()*100:.2f}%")
        
        # 可视化结果
        self.visualize_mlp_results(X, y, model)
        self.visualize_training_loss(losses)
    
    def activation_functions_demo(self) -> None:
        """激活函数演示"""
        logger.info("=== 激活函数演示 ===")
        
        # 生成输入数据
        x = np.linspace(-5, 5, 1000)
        
        # 常用激活函数
        activations = {
            'Sigmoid': self.sigmoid(x),
            'Tanh': self.tanh(x),
            'ReLU': self.relu(x),
            'Leaky ReLU': self.leaky_relu(x),
            'Softmax': self.softmax_1d(x)  # 简化版softmax
        }
        
        # 可视化激活函数
        self.visualize_activation_functions(x, activations)
        
        # 显示函数特性
        logger.info("激活函数特性对比:")
        for name, func_values in activations.items():
            logger.info(f"{name}:")
            logger.info(f"  范围: [{np.min(func_values):.3f}, {np.max(func_values):.3f}]")
            logger.info(f"  在x=0处的值: {func_values[len(func_values)//2]:.3f}")
    
    def backpropagation_demo(self) -> None:
        """反向传播演示"""
        logger.info("=== 反向传播演示 ===")
        
        # 简单的2层网络: 输入(2) -> 隐藏(3) -> 输出(1)
        # 手动实现反向传播过程
        
        # 训练数据 (XOR问题)
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
        y = np.array([[0], [1], [1], [0]], dtype=float)
        
        # 初始化权重 (随机小值)
        np.random.seed(42)
        W1 = np.random.randn(2, 3) * 0.5  # 输入到隐藏层
        b1 = np.zeros((1, 3))
        W2 = np.random.randn(3, 1) * 0.5  # 隐藏到输出层
        b2 = np.zeros((1, 1))
        
        learning_rate = 1.0
        epochs = 10000
        
        logger.info("手动实现反向传播训练XOR问题")
        logger.info(f"网络结构: 2 -> 3 -> 1")
        logger.info(f"学习率: {learning_rate}")
        
        losses = []
        for epoch in range(epochs):
            total_loss = 0
            
            for i in range(len(X)):
                # 前向传播
                # 隐藏层
                z1 = np.dot(X[i:i+1], W1) + b1
                a1 = self.sigmoid(z1)
                
                # 输出层
                z2 = np.dot(a1, W2) + b2
                a2 = self.sigmoid(z2)
                
                # 计算损失
                loss = 0.5 * (y[i] - a2[0, 0])**2
                total_loss += loss
                
                # 反向传播
                # 输出层梯度
                dL_da2 = -(y[i] - a2[0, 0])
                da2_dz2 = a2[0, 0] * (1 - a2[0, 0])  # sigmoid导数
                dz2_dW2 = a1
                dz2_da1 = W2.T
                dz2_db2 = 1
                
                # 隐藏层梯度
                dL_dz2 = dL_da2 * da2_dz2
                dL_dW2 = np.outer(a1, dL_dz2)
                dL_db2 = dL_dz2
                dL_da1 = np.dot(dL_dz2, dz2_da1)
                da1_dz1 = a1 * (1 - a1)  # sigmoid导数
                dL_dz1 = dL_da1 * da1_dz1
                dL_dW1 = np.outer(X[i:i+1].T, dL_dz1)
                dL_db1 = dL_dz1
                
                # 更新权重
                W2 -= learning_rate * dL_dW2
                b2 -= learning_rate * dL_db2
                W1 -= learning_rate * dL_dW1
                b1 -= learning_rate * dL_db1
            
            avg_loss = total_loss / len(X)
            losses.append(avg_loss)
            
            if epoch % 2000 == 0:
                logger.info(f"Epoch {epoch}: 平均损失 = {avg_loss:.6f}")
        
        # 测试最终结果
        logger.info("训练完成，测试结果:")
        for i in range(len(X)):
            # 前向传播
            z1 = np.dot(X[i:i+1], W1) + b1
            a1 = self.sigmoid(z1)
            z2 = np.dot(a1, W2) + b2
            a2 = self.sigmoid(z2)
            logger.info(f"输入 {X[i]} -> 输出 {a2[0,0]:.4f} (期望: {y[i][0]})")
        
        # 可视化训练过程
        self.visualize_backpropagation(losses)
    
    # 激活函数定义
    def step_activation(self, x: float) -> int:
        """阶跃激活函数"""
        return 1 if x >= 0 else 0
    
    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid激活函数"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def tanh(self, x: np.ndarray) -> np.ndarray:
        """Tanh激活函数"""
        return np.tanh(x)
    
    def relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU激活函数"""
        return np.maximum(0, x)
    
    def leaky_relu(self, x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
        """Leaky ReLU激活函数"""
        return np.where(x > 0, x, alpha * x)
    
    def softmax_1d(self, x: np.ndarray) -> np.ndarray:
        """简化版Softmax（用于1D数组可视化）"""
        exp_x = np.exp(x - np.max(x))  # 数值稳定
        return exp_x / np.sum(exp_x)
    
    # 可视化方法
    def visualize_perceptron(self, X: np.ndarray, y: np.ndarray, 
                           weights: np.ndarray, bias: float) -> None:
        """可视化感知机决策边界"""
        plt.figure(figsize=(10, 8))
        
        # 绘制数据点
        colors = ['red' if label == 0 else 'blue' for label in y]
        plt.scatter(X[:, 0], X[:, 1], c=colors, s=100, alpha=0.7)
        
        # 绘制决策边界
        if abs(weights[1]) > 1e-10:  # 避免除零
            x_boundary = np.linspace(-0.5, 1.5, 100)
            y_boundary = -(weights[0] * x_boundary + bias) / weights[1]
            plt.plot(x_boundary, y_boundary, 'k-', linewidth=2, 
                    label=f'决策边界: {weights[0]:.2f}x₁ + {weights[1]:.2f}x₂ + {bias:.2f} = 0')
        
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.title('感知机决策边界 (AND门)')
        plt.xlabel('输入 x₁')
        plt.ylabel('输入 x₂')
        plt.xlim(-0.5, 1.5)
        plt.ylim(-0.5, 1.5)
        
        plt.savefig('perceptron_boundary.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("感知机决策边界图已保存为 perceptron_boundary.png")
    
    def visualize_mlp_results(self, X: np.ndarray, y: np.ndarray, model: nn.Module) -> None:
        """可视化MLP分类结果"""
        plt.figure(figsize=(12, 5))
        
        # 左图：原始数据
        plt.subplot(1, 2, 1)
        colors = ['red' if label == 0 else 'blue' for label in y]
        plt.scatter(X[:, 0], X[:, 1], c=colors, alpha=0.6)
        plt.title('原始数据分布')
        plt.xlabel('x₁')
        plt.ylabel('x₂')
        plt.grid(True, alpha=0.3)
        
        # 右图：模型预测结果
        plt.subplot(1, 2, 2)
        # 创建网格点进行预测
        xx, yy = np.meshgrid(np.linspace(X[:, 0].min()-0.5, X[:, 0].max()+0.5, 100),
                            np.linspace(X[:, 1].min()-0.5, X[:, 1].max()+0.5, 100))
        grid_points = np.c_[xx.ravel(), yy.ravel()]
        
        with torch.no_grad():
            grid_tensor = torch.FloatTensor(grid_points)
            predictions = model(grid_tensor).numpy().reshape(xx.shape)
        
        # 绘制决策边界
        contour = plt.contour(xx, yy, predictions, levels=[0.5], colors='black', linewidths=2)
        plt.clabel(contour, inline=True, fontsize=8)
        
        # 填充颜色表示概率
        plt.contourf(xx, yy, predictions, levels=50, alpha=0.6, cmap='RdYlBu')
        plt.colorbar(label='预测概率')
        
        # 绘制原始数据点
        plt.scatter(X[:, 0], X[:, 1], c=colors, s=30, edgecolors='black')
        plt.title('MLP分类结果')
        plt.xlabel('x₁')
        plt.ylabel('x₂')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('mlp_classification.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("MLP分类结果图已保存为 mlp_classification.png")
    
    def visualize_training_loss(self, losses: List[float]) -> None:
        """可视化训练损失曲线"""
        plt.figure(figsize=(10, 6))
        plt.plot(losses, 'b-', linewidth=2)
        plt.xlabel('训练轮次')
        plt.ylabel('损失值')
        plt.title('MLP训练损失曲线')
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        
        plt.savefig('training_loss.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("训练损失曲线图已保存为 training_loss.png")
    
    def visualize_activation_functions(self, x: np.ndarray, 
                                     activations: dict) -> None:
        """可视化激活函数"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.ravel()
        
        for idx, (name, values) in enumerate(activations.items()):
            if idx < len(axes):
                axes[idx].plot(x, values, linewidth=2)
                axes[idx].set_title(f'{name} 激活函数')
                axes[idx].grid(True, alpha=0.3)
                axes[idx].set_xlabel('输入')
                axes[idx].set_ylabel('输出')
        
        # 隐藏多余的子图
        for idx in range(len(activations), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('activation_functions.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("激活函数图已保存为 activation_functions.png")
    
    def visualize_backpropagation(self, losses: List[float]) -> None:
        """可视化反向传播训练过程"""
        plt.figure(figsize=(12, 5))
        
        # 损失曲线
        plt.subplot(1, 2, 1)
        plt.plot(losses, 'r-', linewidth=1, alpha=0.7)
        plt.xlabel('训练轮次')
        plt.ylabel('损失值')
        plt.title('反向传播训练损失')
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        
        # 最终损失的移动平均
        window_size = 1000
        if len(losses) >= window_size:
            moving_avg = [np.mean(losses[i:i+window_size]) 
                         for i in range(len(losses)-window_size+1)]
            plt.subplot(1, 2, 2)
            plt.plot(range(window_size-1, len(losses)), [losses[window_size-1]] + moving_avg, 
                    'b-', linewidth=2)
            plt.xlabel('训练轮次')
            plt.ylabel('平均损失')
            plt.title(f'移动平均损失 (窗口={window_size})')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('backpropagation_training.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info("反向传播训练图已保存为 backpropagation_training.png")

def main():
    """主函数 - 运行所有神经网络演示"""
    logger.info("开始神经网络基础演示")
    
    nn_demo = NeuralNetworkBasics()
    
    # 执行各项演示
    nn_demo.perceptron_demo()
    nn_demo.mlp_classification_demo()
    nn_demo.activation_functions_demo()
    nn_demo.backpropagation_demo()
    
    logger.info("神经网络基础演示完成")

if __name__ == "__main__":
    main()