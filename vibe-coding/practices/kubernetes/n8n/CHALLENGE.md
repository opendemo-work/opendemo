# 挑战：Kubernetes n8n 自动化平台部署

## 难度：intermediate | 预计用时：35 分钟 | 推荐工具：Claude Code / Cursor

## 目标

在 Kubernetes 集群中部署 n8n 工作流自动化平台：

1. **Namespace + RBAC** — 创建 `n8n-system` 命名空间、ServiceAccount、ClusterRole（只读权限）、ClusterRoleBinding
2. **Secret** — 存放加密密钥和数据库密码（使用 `${SECRET_PLACEHOLDER}` 占位）
3. **ConfigMap** — n8n 配置文件 + 启动脚本 + Prometheus 监控配置
4. **Deployment** — 1 副本 n8n 容器，挂载 ConfigMap + Secret + PVC，配置健康检查
5. **Service** — LoadBalancer 类型，暴露 5678 端口

## 约束

- Kubernetes v1.23+
- n8n 镜像：`n8nio/n8n:latest`
- 资源：requests 1 CPU/2Gi，limits 2 CPU/4Gi
- 健康检查：`/healthz` 端口 5678，liveness 30s 延迟，readiness 10s 延迟
- 数据库配置指向 PostgreSQL（host: postgres, port: 5432）
- Secret 值使用 `${SECRET_PLACEHOLDER}` 占位符

## 验证

```bash
# 应用所有清单
kubectl apply -f manifests/

# 检查部署状态
kubectl get pods -n n8n-system
kubectl get svc -n n8n-system

# 检查 RBAC
kubectl get clusterrole n8n-cluster-role
kubectl get serviceaccount n8n-sa -n n8n-system

# 访问 n8n
# 获取 External IP 后访问 http://<IP>:5678
```

## 提示（卡住时再看）

<details>
<summary>提示 1：文件组织</summary>

每个资源类型一个 YAML 文件：rbac.yaml（Namespace + SA + ClusterRole + Binding）、secret.yaml、configmap.yaml、n8n-deployment.yaml、n8n-service.yaml。

</details>

<details>
<summary>提示 2：Deployment 关键配置</summary>

环境变量通过 `valueFrom.secretKeyRef` 引用 Secret，ConfigMap 通过 volume 挂载到 `/etc/config`，Secret 挂载到 `/etc/secrets`（readOnly）。

</details>

<details>
<summary>提示 3：关键 Prompt</summary>

"用 K8s YAML 部署 n8n 工作流平台。需要：Namespace n8n-system、RBAC 只读权限、Secret 存密钥、ConfigMap 含配置和启动脚本、Deployment 1 副本用 n8nio/n8n:latest 镜像配健康检查、Service LoadBalancer:5678。资源限制 1CPU/2Gi 到 2CPU/4Gi。"

</details>

## 对应原 Demo

完成后对比参考实现：`kubernetes/n8n/`
