# Argo Workflows

Argo工作流引擎部署与使用演示。

## 什么是Argo Workflows

Kubernetes原生工作流引擎，支持DAG、步骤、循环等复杂流程：

```
工作流示例:
    ┌─────────┐
    │  Start  │
    └────┬────┘
         │
    ┌────┴────┐
    │  Step A │
    └────┬────┘
         │
    ┌────┴────┐
    │  Step B │────┐
    └────┬────┘    │
         │         │
    ┌────┴────┐    │
    │  Step C │◀───┘
    └────┬────┘
         │
    ┌────┴────┐
    │   End   │
    └─────────┘
```

## 安装部署

```bash
# 安装Argo Workflows
kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/latest/download/install.yaml

# 配置访问
kubectl patch svc argo-server -n argo -p '{"spec": {"type": "NodePort"}}'
```

## 工作流定义

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-world-
spec:
  entrypoint: whalesay
  templates:
  - name: whalesay
    container:
      image: docker/whalesay
      command: [cowsay]
      args: ["hello world"]
```

## DAG工作流

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: dag-diamond-
spec:
  entrypoint: diamond
  templates:
  - name: diamond
    dag:
      tasks:
      - name: A
        template: echo
        arguments:
          parameters: [{name: message, value: A}]
      - name: B
        dependencies: [A]
        template: echo
        arguments:
          parameters: [{name: message, value: B}]
      - name: C
        dependencies: [A]
        template: echo
        arguments:
          parameters: [{name: message, value: C}]
      - name: D
        dependencies: [B, C]
        template: echo
        arguments:
          parameters: [{name: message, value: D}]
  - name: echo
    inputs:
      parameters:
      - name: message
    container:
      image: alpine:3.7
      command: [echo, "{{inputs.parameters.message}}"]
```

## 学习要点

1. 工作流模板设计
2. DAG依赖管理
3. 参数与制品传递
4. 重试与超时策略
5. 事件驱动触发
