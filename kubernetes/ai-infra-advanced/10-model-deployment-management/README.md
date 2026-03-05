# 模型部署管理

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **工具**: KServe, Seldon, BentoML

---

## 概述

模型部署管理涵盖模型服务化、版本管理、流量控制、自动扩缩容等核心能力，实现AI模型的高效部署和运维。

---

## KServe部署

### InferenceService基础部署

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sklearn-model
  namespace: ml-serving
spec:
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "s3://models/sklearn/iris"
      resources:
        requests:
          cpu: "1"
          memory: "2Gi"
        limits:
          cpu: "2"
          memory: "4Gi"
```

### GPU推理服务

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: pytorch-gpu
  namespace: ml-serving
  annotations:
    serving.kserve.io/autoscalerClass: hpa
    serving.kserve.io/metric: concurrency
    serving.kserve.io/target: "4"
spec:
  predictor:
    model:
      modelFormat:
        name: pytorch
      storageUri: "s3://models/pytorch/resnet50"
      resources:
        requests:
          nvidia.com/gpu: 1
          memory: "8Gi"
        limits:
          nvidia.com/gpu: 1
          memory: "16Gi"
```

---

## Seldon Core部署

### SeldonDeployment

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: ml-model
  namespace: ml-serving
spec:
  predictors:
    - name: default
      replicas: 2
      graph:
        name: classifier
        implementation: SKLEARN_SERVER
        modelUri: s3://models/sklearn/iris
        envSecretRefName: s3-credentials
      componentSpecs:
        - spec:
            containers:
              - name: classifier
                resources:
                  requests:
                    cpu: "1"
                    memory: "2Gi"
                  limits:
                    cpu: "2"
                    memory: "4Gi"
```

### A/B测试部署

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: ab-test-model
  namespace: ml-serving
spec:
  predictors:
    - name: model-a
      traffic: 80
      graph:
        name: classifier-a
        implementation: SKLEARN_SERVER
        modelUri: s3://models/v1
    - name: model-b
      traffic: 20
      graph:
        name: classifier-b
        implementation: SKLEARN_SERVER
        modelUri: s3://models/v2
```

---

## BentoML部署

### BentoService定义

```python
import bentoml
from bentoml.io import NumpyNdarray, JSON
from sklearn.ensemble import RandomForestClassifier

@bentoml.service(
    resources={"gpu": 1, "memory": "8Gi"},
    traffic={"timeout": 30}
)
class IrisClassifier:
    def __init__(self):
        self.model = bentoml.sklearn.load_model("iris_classifier:latest")
    
    @bentoml.api
    def predict(self, input_array: NumpyNdarray) -> NumpyNdarray:
        return self.model.predict(input_array)
    
    @bentoml.api
    def predict_proba(self, input_array: NumpyNdarray) -> JSON:
        return {"probabilities": self.model.predict_proba(input_array).tolist()}
```

### Kubernetes部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bentoml-service
  namespace: ml-serving
spec:
  replicas: 2
  selector:
    matchLabels:
      app: bentoml-service
  template:
    metadata:
      labels:
        app: bentoml-service
    spec:
      containers:
        - name: bentoml
          image: bentoml/iris-classifier:latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: "1"
              memory: "2Gi"
            limits:
              cpu: "2"
              memory: "4Gi"
```

---

## 自动扩缩容

### HPA配置

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-hpa
  namespace: ml-serving
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bentoml-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
```

---

## 金丝雀发布

### Argo Rollouts配置

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: model-rollout
  namespace: ml-serving
spec:
  replicas: 4
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause: {duration: 10m}
        - setWeight: 40
        - pause: {duration: 10m}
        - setWeight: 60
        - pause: {duration: 10m}
        - setWeight: 80
        - pause: {duration: 10m}
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
        args:
          - name: service-name
            value: model-service
  selector:
    matchLabels:
      app: model-service
  template:
    metadata:
      labels:
        app: model-service
    spec:
      containers:
        - name: model
          image: model:v2
```

---

## 相关案例

- [模型注册中心](../09-model-registry/) - 模型版本管理
- [LLM推理服务](../17-llm-inference-serving/) - LLM推理
- [MLOps流水线](../32-mlops-pipeline/) - ML流水线

---

**维护者**: OpenDemo Team | **许可证**: MIT
