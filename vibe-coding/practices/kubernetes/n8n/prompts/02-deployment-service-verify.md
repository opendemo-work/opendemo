# Prompt 02: Deployment + Service + 验证

创建：

n8n-deployment.yaml：
- 1 副本，镜像 n8nio/n8n:latest
- 环境变量从 Secret 引用
- 挂载 ConfigMap → /etc/config，Secret → /etc/secrets (readOnly)，PVC → /home/node/.n8n
- 资源：requests 1CPU/2Gi，limits 2CPU/4Gi
- 健康检查：/healthz:5678
- serviceAccountName: n8n-sa

n8n-service.yaml：
- LoadBalancer，selector app=n8n，port 5678

验证：
kubectl apply -f manifests/
kubectl get pods,svc -n n8n-system

---
## 背景
- 工具：Claude Code
- 阶段：第 3-5 轮
- 结果：volumeMounts 顺序调整后正确
