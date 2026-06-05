# Prompt 01: RBAC + Secret + ConfigMap

创建 Kubernetes 清单：

rbac.yaml：
- Namespace: n8n-system
- ServiceAccount: n8n-sa
- ClusterRole: n8n-cluster-role（只读权限：get, list, watch 对核心资源）
- ClusterRoleBinding

secret.yaml：
- n8n-secrets (Opaque)
- 值用 ${SECRET_PLACEHOLDER} 占位

configmap.yaml：
- n8n-config
- 包含 config.yaml（n8n 配置指向 postgres）
- start.sh（加载 secret 后启动 n8n）
- prometheus.yaml（监控配置）

---
## 背景
- 工具：Claude Code（终端模式）
- 阶段：第 1-2 轮
- 结果：正确
