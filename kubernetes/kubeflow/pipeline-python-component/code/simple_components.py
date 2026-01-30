"""
Kubeflow Pipeline Python组件示例

定义两个简单的Python函数组件
"""

from kfp import dsl


@dsl.component
def add_numbers(a: float, b: float) -> float:
    """
    简单的加法组件
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两个数字的和
    """
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    return result


@dsl.component
def multiply_numbers(a: float, b: float) -> float:
    """
    简单的乘法组件
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两个数字的乘积
    """
    result = a * b
    print(f"Multiplying {a} * {b} = {result}")
    return result


@dsl.component(
    packages_to_install=['numpy==1.24.0']
)
def calculate_mean(numbers: list) -> float:
    """
    计算平均值组件（使用外部依赖）
    
    Args:
        numbers: 数字列表
    
    Returns:
        平均值
    """
    import numpy as np
    
    arr = np.array(numbers)
    mean_value = np.mean(arr)
    print(f"Mean of {numbers} = {mean_value}")
    return float(mean_value)
