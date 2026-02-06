# MLOps流水线实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 端到端MLOps流水线的设计和实现
- 模型训练、验证、部署的自动化流程
- 模型版本管理和实验跟踪
- CI/CD在机器学习项目中的应用

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- Docker环境
- Git版本控制系统

### 依赖安装
```bash
pip install mlflow prefect dvc kubernetes
pip install torch transformers scikit-learn pandas numpy
pip install pytest pytest-cov  # 测试工具
pip install evidently  # 数据和模型监控
```

## 📁 项目结构

```
mlops-pipeline-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── dvc.yaml                           # DVC管道定义
├── mlflow/                            # MLflow配置
│   ├── mlruns/                        # MLflow运行记录
│   └── experiments/                   # 实验定义
├── prefect/                           # Prefect工作流
│   ├── flows/                         # 工作流定义
│   ├── deployments/                   # 部署配置
│   └── infrastructure/                # 基础设施配置
├── data/                              # 数据文件
│   ├── raw/                           # 原始数据
│   ├── processed/                     # 处理后数据
│   └── validation/                    # 验证数据
├── models/                            # 模型文件
│   ├── artifacts/                     # 模型制品
│   ├── registry/                      # 模型注册表
│   └── versions/                      # 版本控制
├── src/                               # 源代码
│   ├── train.py                       # 训练脚本
│   ├── evaluate.py                    # 评估脚本
│   ├── predict.py                     # 预测脚本
│   └── utils/                         # 工具函数
├── tests/                             # 测试文件
│   ├── unit_tests/                    # 单元测试
│   ├── integration_tests/             # 集成测试
│   └── model_tests/                   # 模型测试
├── docker/                            # Docker配置
│   ├── Dockerfile                     # 训练容器
│   ├── Dockerfile.serve               # 服务容器
│   └── docker-compose.yml             # Compose配置
├── cicd/                              # CI/CD配置
│   ├── github_actions/                # GitHub Actions
│   ├── jenkins/                       # Jenkins配置
│   └── argo_workflows/                # Argo工作流
└── notebooks/                         # Jupyter笔记本
    ├── 01_data_exploration.ipynb      # 数据探索
    ├── 02_model_training.ipynb        # 模型训练
    └── 03_pipeline_implementation.ipynb # 流水线实现
```

## 🚀 快速开始

### 步骤1：初始化MLOps环境

```bash
# 初始化DVC仓库
dvc init

# 初始化MLflow跟踪
mlflow server --backend-store-uri ./mlflow/mlruns --default-artifact-root ./mlflow/artifacts &

# 设置Prefect云或本地API
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
```

### 步骤2：运行MLOps流水线

```bash
# 使用Prefect运行流水线
prefect deployment run mlops-pipeline/training-deployment

# 或者直接运行Python脚本
python src/train.py --config configs/training_config.yaml
```

### 步骤3：模型部署

```bash
# 部署模型到Kubernetes
kubectl apply -f k8s/model-deployment.yaml

# 或使用MLflow模型服务器
mlflow models serve -m models/registry/best_model -p 1234
```

## 🔍 代码详解

### 核心概念解析

#### 1. Prefect工作流定义
```python
# prefect/flows/training_pipeline.py
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import mlflow
import joblib

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def load_data(data_path: str):
    """加载数据任务"""
    import pandas as pd
    df = pd.read_csv(data_path)
    return df

@task
def preprocess_data(df):
    """数据预处理任务"""
    # 数据清洗和特征工程
    processed_df = df.dropna()
    return processed_df

@task
def train_model(X_train, y_train):
    """模型训练任务"""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    return model

@flow(name="mlops-training-pipeline")
def training_pipeline(data_path: str, model_output_path: str):
    """MLOps训练流水线"""
    # 启动MLflow运行
    with mlflow.start_run():
        # 执行流水线步骤
        raw_data = load_data(data_path)
        processed_data = preprocess_data(raw_data)
        
        # 分割数据
        from sklearn.model_selection import train_test_split
        X = processed_data.drop('target', axis=1)
        y = processed_data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # 训练模型
        model = train_model(X_train, y_train)
        
        # 评估模型
        from sklearn.metrics import accuracy_score
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # 记录参数和指标
        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_metric("accuracy", accuracy)
        
        # 保存模型
        joblib.dump(model, model_output_path)
        mlflow.log_artifact(model_output_path)
    
    return model_output_path
```

#### 2. 实际应用示例

##### 场景1：CI/CD流水线配置
```yaml
# cicd/github_actions/train-model.yaml
name: Train Model
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run DVC pipeline
      run: |
        dvc repro
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Upload model artifacts
      uses: actions/upload-artifact@v3
      with:
        name: trained-model
        path: models/artifacts/
```

##### 场景2：模型监控和告警
```python
# src/monitoring.py
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import *
import pandas as pd

def create_model_monitoring_report(reference_data, current_data):
    """创建模型监控报告"""
    column_mapping = ColumnMapping()
    column_mapping.target = 'target'
    column_mapping.prediction = 'prediction'
    
    report = Report(metrics=[
        DatasetMissingValuesMetric(),
        DatasetDriftMetric(),
        ClassificationQualityMetric(),
        ColumnQuantileMetric(column_name='feature_1', quantile=0.5),
    ])
    
    report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    
    return report
```

## 🧪 验证测试

### 测试1：流水线功能验证
```python
#!/usr/bin/env python
# 验证MLOps流水线功能
import tempfile
import os
import pandas as pd
from prefect.testing.utilities import prefect_test_harness
from prefect import flow

def test_mlops_pipeline():
    print("=== MLOps流水线功能验证 ===")
    
    # 创建临时数据
    with tempfile.TemporaryDirectory() as temp_dir:
        # 生成模拟数据
        data = pd.DataFrame({
            'feature_1': [1, 2, 3, 4, 5],
            'feature_2': [0.1, 0.2, 0.3, 0.4, 0.5],
            'target': [0, 1, 0, 1, 0]
        })
        
        data_path = os.path.join(temp_dir, 'sample_data.csv')
        data.to_csv(data_path, index=False)
        
        model_path = os.path.join(temp_dir, 'model.pkl')
        
        # 在测试模式下运行流水线
        with prefect_test_harness():
            from prefect.client import get_client
            result = training_pipeline(data_path, model_path)
            
            print(f"✅ 流水线执行成功")
            print(f"模型保存路径: {result}")
    
    print("✅ MLOps流水线验证通过")

if __name__ == "__main__":
    test_mlops_pipeline()
```

### 测试2：模型注册和部署验证
```python
#!/usr/bin/env python
# 验证模型注册和部署
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import tempfile
import os

def test_model_registration():
    print("=== 模型注册和部署验证 ===")
    
    # 创建示例模型
    X, y = make_classification(n_samples=100, n_features=4, n_classes=2)
    model = RandomForestClassifier()
    model.fit(X, y)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 使用MLflow跟踪模型
        with mlflow.start_run():
            # 记录模型
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                conda_env="./environment.yml",
                registered_model_name="example-model"
            )
            
            # 记录参数和指标
            mlflow.log_param("n_estimators", 100)
            mlflow.log_metric("accuracy", 0.95)
            
            print("✅ 模型注册成功")
            print(f"运行ID: {mlflow.active_run().info.run_id}")
    
    # 加载注册的模型
    logged_model = f"runs:/{mlflow.active_run().info.run_id}/model"
    loaded_model = mlflow.sklearn.load_model(logged_model)
    
    # 测试预测
    sample_prediction = loaded_model.predict(X[:1])
    print(f"✅ 模型加载和预测成功，预测结果: {sample_prediction[0]}")
    print("✅ 模型注册和部署验证通过")

if __name__ == "__main__":
    test_model_registration()
```

## ❓ 常见问题

### Q1: 如何处理流水线中的依赖关系？
**解决方案**：
```python
# 依赖管理最佳实践
"""
1. 使用Prefect或Airflow管理任务依赖
2. 通过DVC管理数据依赖
3. 使用MLflow跟踪实验依赖
4. 通过容器化确保环境一致性
"""
```

### Q2: 如何确保模型的可重现性？
**解决方案**：
```python
# 可重现性保证
"""
1. 固定随机种子
2. 版本控制数据和代码
3. 记录所有参数和环境
4. 使用容器化环境
"""
```

## 📚 扩展学习

### 相关技术
- **MLflow**: 实验跟踪和模型管理
- **DVC**: 数据版本控制
- **Prefect/Airflow**: 工作流编排
- **Kubeflow**: Kubernetes上的MLOps平台

### 进阶学习路径
1. 掌握端到端MLOps流水线设计
2. 学习模型监控和数据漂移检测
3. 理解A/B测试和在线评估
4. 掌握模型安全和合规性

### 企业级应用场景
- 自动化模型训练和部署
- 模型性能监控和告警
- 实验管理和版本控制
- 团队协作和模型共享

---
> **💡 提示**: MLOps流水线是现代AI工程的核心实践，通过自动化和标准化确保模型从开发到生产的可靠性和可维护性。