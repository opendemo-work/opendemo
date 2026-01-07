# Kubeflow Pipeline Python组件开发

## 概述

本Demo演示如何使用Python函数创建轻量级Kubeflow Pipeline组件。Python函数组件是最简单的组件类型，适合快速原型开发和简单的数据处理任务。

**所属组件**: Kubeflow Pipelines  
**难度级别**: beginner  
**核心功能**: Python函数组件、组件定义、Pipeline编排

## 前置条件

### 环境要求
- Python 3.8或更高版本
- Kubeflow Pipelines SDK (kfp) 2.0+
- Kubernetes集群：v1.26或更高版本
- Kubeflow平台：v1.8或更高版本

### Python环境配置

安装Kubeflow Pipelines SDK：

```bash
pip install kfp==2.0.0
```

### 权限要求
- 有权限访问Kubeflow Pipelines API
- 有权限在目标命名空间运行Pipeline

## 代码文件说明

### code/simple_components.py
定义两个简单的Python函数组件：
- `add_numbers` - 数字加法组件
- `multiply_numbers` - 数字乘法组件

### code/simple_pipeline.py
定义一个使用上述组件的简单Pipeline

### code/requirements.txt
Python依赖包列表

## 实操步骤

### 1. 创建Python组件

查看示例组件代码 `code/simple_components.py`：

```python
from kfp import dsl

@dsl.component
def add_numbers(a: float, b: float) -> float:
    """简单的加法组件"""
    return a + b

@dsl.component
def multiply_numbers(a: float, b: float) -> float:
    """简单的乘法组件"""
    return a * b
```

**关键点**：
- 使用 `@dsl.component` 装饰器将Python函数转换为Pipeline组件
- 函数参数需要类型注解
- 函数返回值也需要类型注解

### 2. 创建Pipeline

查看Pipeline定义 `code/simple_pipeline.py`：

```python
from kfp import dsl
from simple_components import add_numbers, multiply_numbers

@dsl.pipeline(
    name='simple-math-pipeline',
    description='A simple pipeline that does math operations'
)
def simple_math_pipeline(a: float = 5.0, b: float = 3.0):
    # 第一步：加法
    add_task = add_numbers(a=a, b=b)
    
    # 第二步：乘法，使用第一步的结果
    multiply_task = multiply_numbers(
        a=add_task.output,
        b=2.0
    )
```

### 3. 编译Pipeline

编译Pipeline为YAML格式：

```bash
cd code
python -c "
from kfp import compiler
from simple_pipeline import simple_math_pipeline

compiler.Compiler().compile(
    pipeline_func=simple_math_pipeline,
    package_path='simple_math_pipeline.yaml'
)
print('Pipeline compiled successfully!')
"
```

编译后会生成 `simple_math_pipeline.yaml` 文件。

### 4. 上传并运行Pipeline

#### 方式一：使用Kubeflow Dashboard

1. 登录Kubeflow Dashboard
2. 进入Pipelines页面
3. 点击"Upload Pipeline"
4. 上传 `simple_math_pipeline.yaml`
5. 创建Run并执行

#### 方式二：使用Python SDK

```python
import kfp

# 连接到Kubeflow Pipelines
client = kfp.Client(host='<KUBEFLOW_ENDPOINT>')

# 创建实验
experiment = client.create_experiment(name='math-operations')

# 运行Pipeline
run = client.run_pipeline(
    experiment_id=experiment.id,
    job_name='simple-math-run',
    pipeline_package_path='simple_math_pipeline.yaml',
    params={'a': 10.0, 'b': 5.0}
)

print(f"Pipeline run created: {run.id}")
```

## 验证和测试

### 1. 检查Pipeline运行状态

在Dashboard中查看Pipeline运行状态，或使用SDK：

```python
import kfp

client = kfp.Client(host='<KUBEFLOW_ENDPOINT>')
run_detail = client.get_run(run_id='<RUN_ID>')
print(f"Status: {run_detail.run.status}")
```

### 2. 查看组件输出

在Dashboard的Run详情页面可以看到：
- 每个组件的执行状态
- 组件的输入参数
- 组件的输出结果

**预期输出**：
- add_numbers 组件输出：15.0 (10.0 + 5.0)
- multiply_numbers 组件输出：30.0 (15.0 * 2.0)

### 3. 查看日志

点击组件可以查看详细日志：

```bash
# 或使用kubectl查看Pod日志
kubectl logs -n kubeflow <pod-name>
```

## 高级用法

### 1. 带多个输出的组件

```python
from kfp import dsl
from typing import NamedTuple

@dsl.component
def divide_with_remainder(
    dividend: int,
    divisor: int
) -> NamedTuple('Outputs', [('quotient', int), ('remainder', int)]):
    """除法组件，返回商和余数"""
    from collections import namedtuple
    
    quotient = dividend // divisor
    remainder = dividend % divisor
    
    outputs = namedtuple('Outputs', ['quotient', 'remainder'])
    return outputs(quotient, remainder)
```

### 2. 使用外部依赖

```python
@dsl.component(
    packages_to_install=['numpy==1.24.0', 'pandas==2.0.0']
)
def process_data(input_path: str) -> str:
    """处理数据的组件"""
    import numpy as np
    import pandas as pd
    
    # 数据处理逻辑
    data = pd.read_csv(input_path)
    result = np.mean(data.values)
    
    return f"Mean value: {result}"
```

### 3. 条件执行

```python
@dsl.pipeline
def conditional_pipeline(threshold: float = 0.5):
    # 生成随机数
    random_task = generate_random()
    
    # 条件判断
    with dsl.Condition(random_task.output > threshold):
        process_high_value()
    
    with dsl.Condition(random_task.output <= threshold):
        process_low_value()
```

## 监控和日志

### Pipeline执行监控

在Kubeflow Dashboard中可以实时监控：
- Pipeline整体执行进度
- 每个组件的状态（Pending/Running/Succeeded/Failed）
- 组件之间的依赖关系
- 资源使用情况

### 日志查看

查看特定组件的日志：

```bash
# 获取Pipeline运行的Pod
kubectl get pods -n kubeflow -l pipeline/runid=<RUN_ID>

# 查看特定Pod日志
kubectl logs -n kubeflow <pod-name> -c main
```

## 故障排查

### 问题1：组件导入失败

**症状**：Pipeline编译时报错"cannot import component"

**解决方案**：
- 确保组件函数在同一个模块或正确导入
- 检查Python路径设置
- 使用绝对导入

### 问题2：类型注解错误

**症状**：Pipeline运行时参数类型不匹配

**解决方案**：
- 确保所有函数参数都有类型注解
- 使用支持的基础类型（int, float, str, bool）
- 复杂类型使用InputPath/OutputPath

### 问题3：依赖包安装失败

**症状**：组件运行时找不到依赖包

**解决方案**：
- 在@dsl.component中指定packages_to_install
- 或使用自定义基础镜像
- 检查包名和版本是否正确

## 清理步骤

### 删除Pipeline Run

在Dashboard中删除特定Run，或使用SDK：

```python
client = kfp.Client(host='<KUBEFLOW_ENDPOINT>')
client.runs.delete_run(run_id='<RUN_ID>')
```

### 删除Pipeline

```python
client.pipelines.delete_pipeline(pipeline_id='<PIPELINE_ID>')
```

## 扩展参考

### 官方文档
- [Kubeflow Pipelines SDK文档](https://kubeflow-pipelines.readthedocs.io/)
- [Python函数组件指南](https://www.kubeflow.org/docs/components/pipelines/user-guides/components/python-function-components/)

### 进阶主题
- 使用InputPath和OutputPath处理大文件
- 创建可复用的组件库
- 实现复杂的条件和循环逻辑
- 集成外部数据源
- 实现并行执行

### 关联Demo
- [Pipeline容器组件开发] - 使用容器化组件
- [Pipeline工作流编排] - 复杂工作流设计
- [Pipeline参数化执行] - 参数化Pipeline
- [Pipeline工件追踪] - 管理模型和数据工件

## 最佳实践

1. **组件设计原则**
   - 保持组件功能单一和简洁
   - 使用清晰的函数名和参数名
   - 添加详细的文档字符串
   - 进行充分的错误处理

2. **类型注解**
   - 所有参数和返回值都要有类型注解
   - 优先使用基础类型
   - 复杂数据使用Path传递

3. **依赖管理**
   - 明确指定所有外部依赖
   - 固定依赖包版本
   - 避免使用系统级依赖

4. **测试和调试**
   - 先在本地测试Python函数
   - 使用小数据集验证逻辑
   - 查看完整的日志输出

## 版本说明

本Demo基于以下版本测试：
- Kubeflow Pipelines SDK: 2.0.0
- Kubernetes: v1.26+
- Python: 3.8+
