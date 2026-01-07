"""
Kubeflow Pipeline定义示例

使用Python函数组件构建简单的数学运算Pipeline
"""

from kfp import dsl
from simple_components import add_numbers, multiply_numbers, calculate_mean


@dsl.pipeline(
    name='simple-math-pipeline',
    description='A simple pipeline demonstrating Python function components'
)
def simple_math_pipeline(
    a: float = 5.0,
    b: float = 3.0,
    multiplier: float = 2.0
):
    """
    简单数学运算Pipeline
    
    Args:
        a: 第一个输入数字
        b: 第二个输入数字
        multiplier: 乘数
    """
    # 步骤1：加法运算
    add_task = add_numbers(a=a, b=b)
    
    # 步骤2：乘法运算，使用步骤1的输出
    multiply_task = multiply_numbers(
        a=add_task.output,
        b=multiplier
    )
    
    # 步骤3：计算平均值
    mean_task = calculate_mean(
        numbers=[a, b, add_task.output, multiply_task.output]
    )
    
    # 打印最终结果
    print(f"Pipeline completed!")
    print(f"Add result: {add_task.output}")
    print(f"Multiply result: {multiply_task.output}")
    print(f"Mean: {mean_task.output}")


if __name__ == '__main__':
    # 编译Pipeline
    from kfp import compiler
    
    compiler.Compiler().compile(
        pipeline_func=simple_math_pipeline,
        package_path='simple_math_pipeline.yaml'
    )
    
    print("Pipeline compiled successfully!")
    print("Generated file: simple_math_pipeline.yaml")
