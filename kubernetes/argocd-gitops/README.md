# ArgoCD GitOps 实践演示 - 声明式持续交付

> 在本地 Kubernetes 集群中部署 ArgoCD，并通过 Application 资源将 Git 仓库中的 Guestbook 示例应用自动同步到集群，体验 GitOps 工作流。

---

## 📋 目录

- [🎯 学习目标](#-学习目标)
- [📐 架构图](#-架构图)
- [🚀 快速开始](#-快速开始)
- [📖 核心概念](#-核心概念)
- [💻 代码示例](#-代码示例)
- [🔧 配置说明](#-配置说明)
- [🧪 验证测试](#-验证测试)
- [📊 运行结果](#-运行结果)
- [🐛 常见问题](#-常见问题)
- [📚 扩展学习](#-扩展学习)

---

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 解释 GitOps 的核心思想：Git 作为单一事实来源
- ✅ 在本地 K8s 集群中安装并访问 ArgoCD
- ✅ 使用 ArgoCD Application CRD 声明式管理应用生命周期
- ✅ 配置自动同步（auto-sync）、自修复（self-heal）和自动清理（prune）
- ✅ 检查应用同步状态和健康状态

---

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         GitOps 工作流                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐         ┌─────────────┐         ┌─────────┐  │
│   │   Git 仓库   │────────▶│   ArgoCD    │────────▶│   K8s   │  │
│   │ (期望状态)   │         │  (控制器)    │         │ (实际)  │  │
│   └─────────────┘         └──────┬──────┘         └────┬────┘  │
│           ▲                      │                     │       │
│           │              ┌───────┴───────┐             │       │
│           │              │   Diff/Compare  │◀──────────┘       │
│           │              └───────────────┘                     │
│           │                                                     │
│           └─────────────────────────────────────────────────────┘
│                              自动/手动同步                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ArgoCD 内部组件:
┌─────────────────────────────────────────┐
│           ArgoCD Server                 │
│      (Web UI / CLI / API)               │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐  ┌────────┐  ┌────────────┐
│  Repo  │  │  App   │  │   App      │
│ Server │  │ Server │  │ Controller │
└────────┘  └────────┘  └────────────┘
```

---

## 🚀 快速开始

### 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Kubernetes 集群 | v1.25+ | 可使用 kind、minikube 或 Docker Desktop |
| kubectl | v1.25+ | 集群管理 CLI |
| 可选：argocd CLI | v2.10+ | 用于命令行管理 |

### 安装步骤

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 进入案例目录
cd kubernetes/argocd-gitops

# 2. 确保已连接本地集群
kubectl cluster-info

# 3. 一键安装 ArgoCD 并部署示例应用
./scripts/install_argocd.sh

# 4. 检查状态
./scripts/check_status.sh
```

### 访问 ArgoCD UI

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 端口转发
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 在浏览器中访问 https://localhost:8080
# 用户名: admin
# 密码通过以下命令获取:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

---

## 📖 核心概念

### 1. GitOps

GitOps 是一种以 Git 仓库为唯一事实来源（Single Source of Truth）的运维模式。所有基础设施和应用配置都存储在 Git 中，控制器持续监听 Git 变更并将其同步到目标环境。

### 2. ArgoCD Application

Application 是 ArgoCD 的核心自定义资源（CRD），用于定义：
- **source**：Git 仓库地址、分支、路径
- **destination**：目标集群和命名空间
- **syncPolicy**：自动同步、自修复、自动清理策略

### 3. 同步策略

| 策略 | 说明 |
|------|------|
| `automated` | 检测到 Git 变更后自动触发同步 |
| `selfHeal` | 当集群内资源被手动修改时，自动恢复到 Git 定义的状态 |
| `prune` | 删除 Git 中已移除但在集群中仍然存在的资源 |

### 4. ApplicationSet

ApplicationSet 用于在多个环境/集群中批量生成 Application，适合多租户或多区域场景。

---

## 💻 代码示例

### 示例 1：Application 资源定义

**文件**：`manifests/guestbook-application.yaml`

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### 示例 2：手动应用和同步

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建应用
kubectl apply -f manifests/guestbook-application.yaml

# 查看应用状态
kubectl get application guestbook -n argocd

# 查看同步详情
kubectl describe application guestbook -n argocd
```

### 示例 3：使用 argocd CLI

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 登录
argocd login localhost:8080 --username admin --password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

# 列出应用
argocd app list

# 手动同步
argocd app sync guestbook
```

---

## 🔧 配置说明

### Application 关键字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `spec.source.repoURL` | Git 仓库地址 | `https://github.com/argoproj/argocd-example-apps.git` |
| `spec.source.targetRevision` | 分支或 commit | `HEAD` |
| `spec.source.path` | 仓库内路径 | `guestbook` |
| `spec.destination.server` | 目标集群地址 | `https://kubernetes.default.svc` |
| `spec.destination.namespace` | 目标命名空间 | `guestbook` |
| `spec.syncPolicy.automated` | 自动同步策略 | `{prune: true, selfHeal: true}` |

---

## 🧪 验证测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 1. 检查 ArgoCD Pod 是否全部 Running
kubectl get pods -n argocd

# 2. 检查 Application 状态是否为 Synced
kubectl get application guestbook -n argocd

# 3. 检查 Guestbook 应用资源是否已部署
kubectl get all -n guestbook

# 4. 测试自修复：手动修改 Deployment 副本数，观察是否被恢复
kubectl scale deployment guestbook-ui -n guestbook --replicas=2
# 等待约 5 秒后再次检查，ArgoCD 应将其恢复为 1 副本
kubectl get deployment guestbook-ui -n guestbook
```

---

## 📊 运行结果

### 预期输出

```
$ kubectl get application guestbook -n argocd
NAME        SYNC STATUS   HEALTH STATUS
guestbook   Synced        Healthy

$ kubectl get pods -n argocd
NAME                                  READY   STATUS
guestbook-ui-7d4d9c5b-abc12           1/1     Running
argocd-server-xxx                     1/1     Running
argocd-application-controller-xxx     1/1     Running
```

---

## 🐛 常见问题

### Q1：ArgoCD Pod 一直 Pending 怎么办？

**A**：检查集群资源是否充足，或者镜像拉取是否失败：

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
kubectl describe pod -n argocd -l app.kubernetes.io/name=argocd-server
```

### Q2：Application 状态显示 OutOfSync？

**A**：OutOfSync 表示 Git 定义与集群实际状态不一致。可以等待自动同步，或手动执行：

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
argocd app sync guestbook
```

### Q3：无法通过 port-forward 访问 UI？

**A**：确认使用的是 HTTPS，并且没有证书信任问题。首次访问时浏览器会提示证书不安全，选择继续访问即可。

### Q4：如何卸载 ArgoCD？

**A**：运行卸载脚本：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/uninstall.sh
```

---

## 📚 扩展学习

### 相关案例

- [Istio Service Mesh 基础](../istio-service-mesh-basics/) - 学习服务网格与 GitOps 结合
- [Prometheus 监控基础](../prometheus/basic-prometheus/) - 为 ArgoCD 配置可观测性

### 推荐资源

- 📖 [ArgoCD 官方文档](https://argo-cd.readthedocs.io/)
- 📖 [GitOps 实践指南](https://www.gitops.tech/)
- 🎥 [ArgoCD Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)

### 进阶主题

- [ ] ApplicationSet 多环境部署
- [ ] ArgoCD Projects 与 RBAC
- [ ] Sealed Secrets / External Secrets 集成
- [ ] ArgoCD Image Updater 自动更新镜像
- [ ] Argo Rollouts 渐进式发布

---

*最后更新：2026-06-26*  
*版本：1.1.0*  
*维护者：OpenDemo Team*
