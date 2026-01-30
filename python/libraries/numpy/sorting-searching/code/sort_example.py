import numpy as np


def main():
    """
    演示基本的数组排序功能
    使用 np.sort() 对一组浮点数进行升序排序
    """
    # 创建一个包含学生成绩的NumPy数组（未排序）
    scores = np.array([3.5, 1.2, 4.8, 2.1, 3.9])
    
    print("原始数组:", scores)
    
    # 使用np.sort()进行排序，返回一个新的排序后数组
    sorted_scores = np.sort(scores)
    
    print("排序后数组:", sorted_scores)


if __name__ == "__main__":
    main()