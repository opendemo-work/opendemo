#!/usr/bin/env bash
# 风险等级：🟡 中风险
# 说明：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
# 生产安全提示：
#   - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
#   - 注意检查依赖版本、端口占用和目标资源配置。
#   - 生产环境执行前请经过变更评审和备份确认。

# 在本地 Kubernetes 集群（kind/minikube）中安装 ArgoCD

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=========================================="
echo "ArgoCD 本地安装脚本"
echo "=========================================="

# 检查 kubectl
if ! command -v kubectl &>/dev/null; then
    echo "❌ kubectl 未找到，请先安装"
    exit 1
fi

# 检查集群连接
if ! kubectl cluster-info &>/dev/null; then
    echo "❌ 无法连接到 Kubernetes 集群"
    echo "请先创建集群，例如: kind create cluster 或 minikube start"
    exit 1
fi

# 创建命名空间
echo "[1/4] 创建 argocd 命名空间..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

# 安装 ArgoCD
echo "[2/4] 安装 ArgoCD..."
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 等待部署就绪
echo "[3/4] 等待 ArgoCD 组件就绪（约 1-2 分钟）..."
kubectl wait --for=condition=available --timeout=120s deployment/argocd-server -n argocd || true

# 部署示例应用
echo "[4/4] 部署示例 Guestbook 应用..."
kubectl apply -f manifests/guestbook-application.yaml

echo ""
echo "✅ ArgoCD 安装完成"
echo ""
echo "获取初始密码:"
echo "  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath=\"{.data.password}\" | base64 -d"
echo ""
echo "端口转发访问 UI:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo "  访问 https://localhost:8080 （用户名: admin）"
