import numpy as np


def create_rotation_matrix(angle_degrees):
    """
    创建二维旋转矩阵
    
    参数:
        angle_degrees: 旋转角度（度）
    
    返回:
        2x2 旋转矩阵
    """
    # 将角度转换为弧度
    angle_radians = np.radians(angle_degrees)
    
    # 创建旋转矩阵
    # 形式为: [[cosθ, -sinθ],
    #         [sinθ, cosθ]]
    cos_a = np.cos(angle_radians)
    sin_a = np.sin(angle_radians)
    
    rotation_matrix = np.array([
        [cos_a, -sin_a],
        [sin_a, cos_a]
    ])
    
    return rotation_matrix


def main():
    """
    演示矩阵乘法在几何变换中的应用
    将一个正方形的四个顶点绕原点旋转45度
    """
    
    # 定义正方形的四个顶点坐标 (4x2 矩阵)
    points = np.array([
        [0, 0],  # 左下角
        [1, 0],  # 右下角
        [1, 1],  # 右上角
        [0, 1]   # 左上角
    ])
    
    # 创建45度旋转矩阵
    rotation_mat = create_rotation_matrix(45)
    
    # 对每个点应用旋转变换
    # 注意：我们需要对每个坐标点右乘旋转矩阵
    rotated_points = np.dot(points, rotation_mat.T)  # 转置以匹配维度
    
    # 输出结果
    print("原始坐标点:")
    print(points)
    print(f"旋转矩阵 (45度):\n{rotation_mat}")
    print("旋转后的坐标:")
    print(rotated_points)
    
    # 验证旋转后正方形的性质（边长应保持不变）
    original_side = np.linalg.norm(points[1] - points[0])  # 底边长度
    rotated_side = np.linalg.norm(rotated_points[1] - rotated_points[0])
    
    print(f"\n原始边长: {original_side:.6f}")
    print(f"旋转后边长: {rotated_side:.6f}")
    print(f"长度保持不变: {np.isclose(original_side, rotated_side)}")


if __name__ == "__main__":
    main()