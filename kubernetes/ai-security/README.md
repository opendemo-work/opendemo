# AI Security on Kubernetes

Kubernetes AI安全实践演示。

## AI安全威胁

```
AI安全威胁模型:
┌─────────────────────────────────────────────────────────┐
│                  Model Inference                        │
│         (Prompt Injection / Model Theft)                │
├─────────────────────────────────────────────────────────┤
│                  Model Training                         │
│         (Data Poisoning / Backdoor)                     │
├─────────────────────────────────────────────────────────┤
│                  Infrastructure                         │
│         (Container Escape / Privilege)                  │
├─────────────────────────────────────────────────────────┤
│                  Supply Chain                           │
│         (Malicious Model / Dependency)                  │
└─────────────────────────────────────────────────────────┘
```

## 安全措施

```yaml
# 模型服务安全加固
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-llm
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: llm
        image: llm-service:latest
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop: ["ALL"]
          readOnlyRootFilesystem: true
        resources:
          limits:
            memory: "8Gi"
```

## 学习要点

1. 提示词注入防护
2. 模型访问控制
3. 容器安全加固
4. 供应链安全
