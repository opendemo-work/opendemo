# Kubeflow ML Platform

Kubeflow机器学习平台部署与使用演示。

## 什么是Kubeflow

Kubeflow是Kubernetes上的机器学习工作流平台：

```
Kubeflow组件:
┌─────────────────────────────────────────────────────────┐
│                   Kubeflow UI                           │
│              (中央仪表盘)                                │
├─────────────────────────────────────────────────────────┤
│  Notebooks │ Pipelines │ Katib │ KServe │ Training     │
│  (Jupyter) │ (工作流)  │ (AutoML)│ (推理)│ (分布式训练) │
├─────────────────────────────────────────────────────────┤
│              Kubernetes Cluster                         │
└─────────────────────────────────────────────────────────┘
```

## 安装部署

```bash
# 安装kfctl
wget https://github.com/kubeflow/kfctl/releases/latest/download/kfctl_linux.tar.gz
tar -xvf kfctl_linux.tar.gz
sudo mv kfctl /usr/local/bin/

# 部署Kubeflow
export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v1.8-branch/kfdef/kfctl_k8s_istio.v1.8.0.yaml"
kfctl apply -V -f ${CONFIG_URI}
```

## 核心组件

### 1. Notebooks
```bash
# 创建Jupyter Notebook
kubectl apply -f - <<EOF
apiVersion: kubeflow.org/v1
kind: Notebook
metadata:
  name: jupyter-notebook
spec:
  template:
    spec:
      containers:
      - name: jupyter
        image: jupyter/tensorflow-notebook:latest
        resources:
          requests:
            memory: 1Gi
            cpu: "1"
EOF
```

### 2. Pipelines
```python
import kfp
from kfp import dsl

@dsl.component
def preprocess_op():
    return dsl.ContainerOp(
        name='Preprocess Data',
        image='python:3.9',
        command=['python', '-c', 'print("Preprocessing...")']
    )

@dsl.pipeline(name='ML Pipeline')
def ml_pipeline():
    preprocess = preprocess_op()

kfp.compiler.Compiler().compile(ml_pipeline, 'pipeline.yaml')
```

## 学习要点

1. ML工作流编排
2. 分布式训练配置
3. 模型服务部署
4. 超参数调优
5. 实验追踪管理
