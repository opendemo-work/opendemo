# MLOps流水线

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **工具**: Kubeflow, MLflow, Argo Workflows

---

## 概述

MLOps流水线实现机器学习全生命周期的自动化，涵盖数据处理、模型训练、模型部署、监控告警等环节。

---

## Kubeflow Pipelines

### Pipeline定义

```python
from kfp import dsl
from kfp.dsl import component, Output, Model, Dataset

@component(base_image="python:3.9")
def data_preprocessing(
    input_data: str,
    output_data: Output[Dataset]
):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    
    df = pd.read_csv(input_data)
    df = df.dropna()
    
    train_df, test_df = train_test_split(df, test_size=0.2)
    
    train_df.to_csv(output_data.path + "/train.csv", index=False)
    test_df.to_csv(output_data.path + "/test.csv", index=False)

@component(base_image="pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime")
def model_training(
    train_data: Input[Dataset],
    model_output: Output[Model],
    epochs: int = 10,
    learning_rate: float = 0.001
):
    import torch
    import torch.nn as nn
    import pandas as pd
    
    train_df = pd.read_csv(train_data.path + "/train.csv")
    
    model = nn.Sequential(
        nn.Linear(10, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 1)
    )
    
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(torch.randn(32, 10))
        loss = criterion(outputs, torch.randn(32, 1))
        loss.backward()
        optimizer.step()
    
    torch.save(model.state_dict(), model_output.path)

@component(base_image="python:3.9")
def model_evaluation(
    model_input: Input[Model],
    test_data: Input[Dataset],
    metrics_output: Output[Dataset]
):
    import torch
    import pandas as pd
    import json
    
    model = torch.load(model_input.path)
    test_df = pd.read_csv(test_data.path + "/test.csv")
    
    metrics = {
        "accuracy": 0.95,
        "precision": 0.94,
        "recall": 0.96,
        "f1_score": 0.95
    }
    
    with open(metrics_output.path, "w") as f:
        json.dump(metrics, f)

@dsl.pipeline(
    name="ML Training Pipeline",
    description="End-to-end ML training pipeline"
)
def ml_pipeline(
    input_data: str,
    epochs: int = 10,
    learning_rate: float = 0.001
):
    preprocess_task = data_preprocessing(
        input_data=input_data
    )
    
    training_task = model_training(
        train_data=preprocess_task.outputs["output_data"],
        epochs=epochs,
        learning_rate=learning_rate
    )
    training_task.set_gpu_limit(1)
    
    evaluation_task = model_evaluation(
        model_input=training_task.outputs["model_output"],
        test_data=preprocess_task.outputs["output_data"]
    )
```

### Pipeline部署

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: ml-training-workflow
  namespace: kubeflow
spec:
  entrypoint: ml-pipeline
  templates:
    - name: ml-pipeline
      dag:
        tasks:
          - name: data-preprocessing
            template: preprocessing-template
          - name: model-training
            template: training-template
            dependencies: [data-preprocessing]
          - name: model-evaluation
            template: evaluation-template
            dependencies: [model-training]
    
    - name: preprocessing-template
      container:
        image: python:3.9
        command: [python, preprocess.py]
    
    - name: training-template
      container:
        image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
        command: [python, train.py]
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 16Gi
    
    - name: evaluation-template
      container:
        image: python:3.9
        command: [python, evaluate.py]
```

---

## MLflow集成

### MLflow部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow
  namespace: mlops
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mlflow
  template:
    metadata:
      labels:
        app: mlflow
    spec:
      containers:
        - name: mlflow
          image: ghcr.io/mlflow/mlflow:v2.9.0
          args:
            - server
            - --backend-store-uri
            - postgresql://user:pass@postgres:5432/mlflow
            - --default-artifact-root
            - s3://mlflow-artifacts/
            - --host
            - "0.0.0.0"
            - --port
            - "5000"
          ports:
            - containerPort: 5000
          env:
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access-key
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret-key
```

### MLflow实验跟踪

```python
import mlflow
import mlflow.pytorch

mlflow.set_tracking_uri("http://mlflow.mlops.svc.cluster.local:5000")
mlflow.set_experiment("llm-finetuning")

with mlflow.start_run():
    mlflow.log_params({
        "learning_rate": 1e-4,
        "epochs": 10,
        "batch_size": 32,
        "model_name": "llama-2-7b"
    })
    
    for epoch in range(10):
        loss = train_epoch(model, dataloader)
        mlflow.log_metric("loss", loss, step=epoch)
    
    mlflow.pytorch.log_model(model, "model")
```

---

## 模型注册与部署

### 模型注册

```yaml
apiVersion: mlflow.org/v1alpha1
kind: RegisteredModel
metadata:
  name: llama-2-7b-finetuned
spec:
  description: "Fine-tuned LLaMA 2 7B model"
  tags:
    - key: framework
      value: pytorch
    - key: task
      value: text-generation
```

### 模型部署

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llama-2-7b-finetuned
spec:
  predictor:
    model:
      modelFormat:
        name: mlflow
      storageUri: "s3://mlflow-artifacts/1/models/llama-2-7b-finetuned"
      resources:
        requests:
          nvidia.com/gpu: 1
          memory: 24Gi
```

---

## 相关案例

- [模型注册中心](../09-model-registry/) - 模型版本管理
- [模型部署管理](../10-model-deployment-management/) - 模型部署
- [AI平台可观测性](../13-ai-platform-observability/) - 监控体系

---

**维护者**: OpenDemo Team | **许可证**: MIT
