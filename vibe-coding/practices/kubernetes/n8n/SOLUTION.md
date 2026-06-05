# 解决过程：Kubernetes n8n 自动化平台部署

## 使用的工具：Claude Code（终端模式）

---

### 第 1 轮：RBAC + Namespace

**Prompt：**
> 创建 Kubernetes RBAC 清单（rbac.yaml）：
> - Namespace: n8n-system
> - ServiceAccount: n8n-sa (在 n8n-system 中)
> - ClusterRole: n8n-cluster-role，只读权限（get, list, watch）对 pods, services, configmaps, secrets, deployments, statefulsets, pv, pvc
> - ClusterRoleBinding: n8n-cluster-role-binding，绑定 SA 和 ClusterRole

**AI 生成：** 正确。RBAC 权限遵循最小权限原则。

---

### 第 2 轮：Secret + ConfigMap

**Prompt：**
> 创建两个清单：
> 1. secret.yaml — n8n-secrets (Opaque)，包含 n8n-encryption-key, postgres-password, postgres-user, postgres-database，值用 ${SECRET_PLACEHOLDER} 占位
> 2. configmap.yaml — n8n-config，包含三段：
>    - config.yaml：n8n 配置（host, port, webhook, database 指向 postgres）
>    - start.sh：启动脚本（加载 secret 环境变量后执行 n8n start）
>    - prometheus.yaml：监控配置（scrape n8n pod）

**AI 生成：** 正确。ConfigMap 多 key 设计合理。

---

### 第 3 轮：Deployment

**Prompt：**
> 创建 n8n-deployment.yaml：
> - 1 副本，镜像 n8nio/n8n:latest
> - 环境变量从 Secret 引用（N8N_ENCRYPTION_KEY, DB_POSTGRES_PASSWORD 等）
> - 挂载 ConfigMap 到 /etc/config，Secret 到 /etc/secrets (readOnly)
> - PVC n8n-data-pvc 挂载到 /home/node/.n8n
> - 资源：requests 1CPU/2Gi，limits 2CPU/4Gi
> - 健康检查：/healthz:5678，liveness 30s 延迟/30s 间隔，readiness 10s 延迟/10s 间隔
> - serviceAccountName: n8n-sa

**AI 生成：** 正确。

**问题：** AI 生成的 volumeMounts 顺序不一致。先挂载 config → secrets → data 更合理。

**修复：** 调整 volumeMounts 顺序。

---

### 第 4 轮：Service

**Prompt：**
> 创建 n8n-service.yaml：LoadBalancer 类型，selector app=n8n，port 5678

**AI 生成：** 正确。

---

### 第 5 轮：验证

```bash
kubectl apply -f manifests/
kubectl get pods -n n8n-system
kubectl get svc -n n8n-system
```

**结果：** 资源全部创建成功 ✅（需要集群环境才能验证 pod 运行状态）

---

## 总结

| 维度 | 值 |
|------|-----|
| 总轮次 | 5 轮 |
| 实际用时 | ~20 分钟 |
| AI 犯错次数 | 0（volumeMounts 顺序是风格问题） |
| 人工干预 | 调整挂载顺序 |

### 关键技巧
- **K8s YAML 分文件管理** — 按资源类型拆分：rbac、secret、configmap、deployment、service
- **Secret 占位符** — 教程中用 `${SECRET_PLACEHOLDER}`，生产环境用 `kubectl create secret` 或 Sealed Secrets
- **健康检查配置** — liveness 用较长延迟（30s）给应用启动时间，readiness 用较短延迟（10s）

### 常见坑
- Namespace 必须先创建 — 其他资源依赖 namespace 存在
- Secret 的值需要 base64 编码 — `data:` 字段下必须是 base64，`stringData:` 可以用明文
- PVC 需要 StorageClass — 集群必须有默认 StorageClass 或手动指定
- LoadBalancer 在 minikube 中需要 `minikube tunnel` — 否则 External-IP 永远是 pending
