# Kubeflow Pipeline工作流编排

## 概述

本Demo演示如何定义和执行完整的机器学习工作流Pipeline，包括数据预处理、模型训练、模型评估和模型部署等典型步骤。展示了Pipeline的编排能力和组件间的数据传递。

**所属组件**: Kubeflow Pipelines  
**难度级别**: intermediate  
**核心功能**: 工作流编排、数据传递、条件执行

## 前置条件

### 环境要求
- Python 3.8或更高版本
- Kubeflow Pipelines SDK (kfp) 2.0+
- Kubernetes集群：v1.26+
- Kubeflow平台：v1.8+

### Python环境
```bash
pip install kfp==2.0.0
```

## 代码文件说明

### code/ml_pipeline.py
完整的机器学习Pipeline定义，包含：
- 数据加载组件
- 数据预处理组件
- 模型训练组件
- 模型评估组件
- 条件部署逻辑

## 实操步骤

### 1. 查看Pipeline定义

Pipeline包含以下步骤：

```python
@dsl.pipeline(
    name='ml-training-pipeline',
    description='Complete ML workflow with data processing and model training'
)
def ml_training_pipeline(
    data_path: str,
    model_name: str = 'iris-model',
    accuracy_threshold: float = 0.85
):
    # 步骤1: 加载数据
    load_task = load_data(data_path=data_path)
    
    # 步骤2: 预处理
    preprocess_task = preprocess_data(
        input_data=load_task.outputs['dataset']
    )
    
    # 步骤3: 训练模型
    train_task = train_model(
        train_data=preprocess_task.outputs['train_data'],
        test_data=preprocess_task.outputs['test_data']
    )
    
    # 步骤4: 评估模型
    eval_task = evaluate_model(
        model=train_task.outputs['model'],
        test_data=preprocess_task.outputs['test_data']
    )
    
    # 条件部署: 只有准确率达标才部署
    with dsl.Condition(eval_task.outputs['accuracy'] >= accuracy_threshold):
        deploy_model(
            model=train_task.outputs['model'],
            model_name=model_name
        )
```

### 2. 编译Pipeline

```bash
cd code
python ml_pipeline.py
```

生成`ml_training_pipeline.yaml`文件。

### 3. 上传并运行

#### 使用Dashboard
1. 登录Kubeflow Dashboard
2. 上传编译后的YAML
3. 创建Run并配置参数
4. 监控执行过程

#### 使用Python SDK
```python
import kfp

client = kfp.Client(host='<KUBEFLOW_ENDPOINT>')

# 创建实验
experiment = client.create_experiment(name='ml-workflow-demo')

# 运行Pipeline
run = client.run_pipeline(
    experiment_id=experiment.id,
    job_name='ml-training-run-1',
    pipeline_package_path='ml_training_pipeline.yaml',
    params={
        'data_path': 's3://my-bucket/iris-data.csv',
        'model_name': 'iris-classifier',
        'accuracy_threshold': 0.90
    }
)
```

## 验证和测试

### 1. 监控Pipeline执行

在Dashboard中查看：
- 各步骤执行状态
- 组件间数据流转
- 条件分支执行情况

### 2. 查看组件输出

每个组件的输出可在Dashboard中查看：
- 数据预处理结果
- 模型训练指标
- 评估结果（准确率、F1分数等）

### 3. 检查模型部署

如果准确率达标，检查模型是否成功部署：

```bash
kubectl get inferenceservice -n kubeflow
```

## 高级特性

### 1. 并行执行

```python
with dsl.ParallelFor(items=['model_a', 'model_b', 'model_c']) as item:
    train_model(model_type=item)
```

### 2. 条件执行

```python
with dsl.Condition(metric > threshold):
    deploy_model()
with dsl.Else():
    retrain_model()
```

### 3. 循环执行

```python
with dsl.ParallelFor(range(5)) as i:
    cross_validation_fold(fold_number=i)
```

## 监控和日志

### Pipeline级别监控

```python
# 获取运行状态
run_detail = client.get_run(run_id=run.id)
print(f"Status: {run_detail.run.status}")

# 等待完成
client.wait_for_run_completion(run_id=run.id, timeout=3600)
```

### 组件级别日志

```bash
# 查看特定组件的日志
kubectl logs -n kubeflow <pod-name> -c main
```

## 故障排查

### 问题1：组件执行失败

**排查步骤**：
1. 查看组件日志
2. 检查输入参数
3. 验证依赖包安装
4. 检查资源限制

### 问题2：数据传递错误

**排查步骤**：
1. 验证输出路径配置
2. 检查存储权限
3. 确认数据格式正确

### 问题3：条件分支未执行

**排查步骤**：
1. 检查条件表达式
2. 验证输入值类型
3. 查看评估结果

## 清理步骤

```python
# 删除运行记录
client.runs.delete_run(run_id=run.id)

# 删除实验
client.experiments.delete_experiment(experiment_id=experiment.id)
```

## 扩展参考

### 官方文档
- [Kubeflow Pipelines工作流指南](https://www.kubeflow.org/docs/components/pipelines/)

### 进阶主题
- 缓存和重用组件输出
- 递归工作流
- 动态生成Pipeline
- 跨集群执行

### 关联Demo
- [Pipeline Python组件开发]
- [Pipeline实验管理]
- [Pipeline工件追踪]

## 最佳实践

1. **模块化设计** - 每个组件功能单一
2. **错误处理** - 添加重试和降级逻辑
3. **资源优化** - 合理配置CPU和内存
4. **日志记录** - 记录关键执行信息
5. **参数化** - 使用参数提高复用性

## 版本说明

本Demo基于：
- Kubeflow Pipelines: 2.0+
- Kubernetes: v1.26+
- Python: 3.8+
