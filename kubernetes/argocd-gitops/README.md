# ArgoCD GitOps

ArgoCD GitOps演示，展示声明式持续交付和应用程序生命周期管理。

## 什么是GitOps

GitOps是一种使用Git作为声明式基础设施和应用程序的单一事实来源的实践。

```
GitOps工作流:
┌──────────┐     ┌──────────┐     ┌──────────┐
│   Git    │────▶│  ArgoCD  │────▶│  K8s     │
│ (Source) │     │ (Sync)   │     │ (Target) │
└──────────┘     └──────────┘     └──────────┘
      │                                 │
      │         ┌──────────┐            │
      │         │   Diff   │◀───────────┘
      │         └──────────┘  (Monitor)
      │                                 │
      └─────────────────────────────────┘
            (Auto/ Manual Sync)
```

## ArgoCD架构

```
ArgoCD组件:
┌─────────────────────────────────────────┐
│           ArgoCD Server                 │
│         (API / Web UI)                  │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Repo    │ │  App     │ │  App     │
│  Server  │ │  Server  │ │  Controller
└──────────┘ └──────────┘ └──────────┘
        │           │           │
        └───────────┴───────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   Git Repo   │        │  Kubernetes  │
└──────────────┘        └──────────────┘
```

## 快速开始

### 1. 安装ArgoCD

```bash
# 创建命名空间
kubectl create namespace argocd

# 安装ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 查看Pod状态
kubectl get pods -n argocd -w
```

### 2. 访问ArgoCD UI

```bash
# 端口转发
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 访问 https://localhost:8080

# 获取初始密码
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# 默认用户名: admin
```

### 3. 配置Git仓库

```bash
# 添加仓库 (CLI)
argocd repo add https://github.com/yourusername/your-repo.git \
  --username your-username \
  --password your-token

# 或使用SSH
argocd repo add git@github.com:yourusername/your-repo.git \
  --ssh-private-key-path ~/.ssh/id_rsa
```

### 4. 创建应用

```bash
# 通过CLI创建应用
argocd app create my-app \
  --repo https://github.com/yourusername/your-repo.git \
  --path k8s/overlays/dev \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default \
  --sync-policy automated \
  --auto-prune \
  --self-heal
```

### 5. 同步应用

```bash
# 手动同步
argocd app sync my-app

# 查看状态
argocd app get my-app

# 查看日志
argocd app logs my-app
```

## 应用定义 (Application)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourusername/your-repo.git
    targetRevision: HEAD
    path: k8s/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true        # 自动删除资源
      selfHeal: true     # 自动修复漂移
    syncOptions:
    - CreateNamespace=true
```

## 应用集 (ApplicationSet)

多环境部署:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-appset
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - cluster: dev
        url: https://dev-cluster.com
      - cluster: staging
        url: https://staging-cluster.com
      - cluster: prod
        url: https://prod-cluster.com
  template:
    metadata:
      name: '{{cluster}}-my-app'
    spec:
      project: default
      source:
        repoURL: https://github.com/yourusername/your-repo.git
        targetRevision: HEAD
        path: k8s/overlays/{{cluster}}
      destination:
        server: '{{url}}'
        namespace: my-app
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## 同步策略

### 自动同步
```yaml
syncPolicy:
  automated:
    prune: true      # 删除Git中不存在的资源
    selfHeal: true   # 自动修复手动修改
```

### 钩子 (Hooks)
```yaml
metadata:
  annotations:
    argocd.argoproj.io/hook: PreSync    # 同步前执行
    argocd.argoproj.io/hook: PostSync   # 同步后执行
    argocd.argoproj.io/hook: SyncFail   # 同步失败时执行
```

## Kustomize集成

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

images:
- name: my-app
  newTag: v1.2.3

patchesStrategicMerge:
- replica-patch.yaml
```

## Helm集成

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-helm-app
spec:
  source:
    repoURL: https://charts.bitnami.com/bitnami
    chart: nginx
    targetRevision: 13.2.0
    helm:
      values: |
        service:
          type: LoadBalancer
        replicaCount: 3
```

## 多集群管理

```bash
# 添加集群
argocd cluster add <context-name>

# 列出集群
argocd cluster list

# 为特定集群创建应用
argocd app create my-app \
  --repo https://github.com/org/repo.git \
  --path apps/my-app \
  --dest-server https://prod-cluster.example.com \
  --dest-namespace production
```

## 监控和告警

### Prometheus指标
```yaml
# ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: argocd-metrics
  endpoints:
  - port: metrics
```

## 最佳实践

1. **单仓库vs多仓库**: 根据团队规模选择
2. **应用分层**: 基础设施层、平台层、应用层
3. ** secrets管理**: 使用Sealed Secrets或External Secrets
4. **权限控制**: 使用Projects进行RBAC
5. **回滚策略**: 利用Git历史进行回滚

## 学习要点

1. 声明式配置管理
2. 配置漂移检测和修复
3. 多环境部署策略
4. GitOps安全实践
5. CI/CD与GitOps集成

## 参考

- [ArgoCD官方文档](https://argo-cd.readthedocs.io/)
- [GitOps实践指南](https://www.gitops.tech/)
