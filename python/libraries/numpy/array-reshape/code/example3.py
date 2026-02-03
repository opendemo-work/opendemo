import numpy as np


def main():
    """
    示例3：实际应用场景模拟
    图像数据预处理中的reshape操作
    """
    # 模拟一张28x28像素、3通道（RGB）的图像
    image_data = np.random.rand(28, 28, 3)
    print(f"原始图像数据形状 (高度, 宽度, 通道): {image_data.shape}")
    
    # 在机器学习中，常需将图像展平为一维向量，并增加批量维度
    # 方法：reshape(批量大小, 特征总数)
    flattened = image_data.reshape(1, -1)  # 1表示批量大小为1，-1自动计算特征数
    print(f"转换为批量输入形状 (批量大小, 特征数): {flattened.shape}")
    
    # 输出特征数量
    print(f"每个样本有 {flattened.shape[1]} 个特征")
    print("模型输入准备完成。")


if __name__ == "__main__":
    main()