#!/usr/bin/env bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# 检查 ArgoCD 和示例应用状态

set -euo pipefail

echo "=========================================="
echo "ArgoCD 状态检查"
echo "=========================================="

if ! kubectl cluster-info &>/dev/null; then
    echo "❌ 无法连接到 Kubernetes 集群"
    exit 1
fi

echo ""
echo "--- ArgoCD 命名空间 Pod ---"
kubectl get pods -n argocd

echo ""
echo "--- ArgoCD Application 列表 ---"
kubectl get applications -n argocd

echo ""
echo "--- Guestbook 应用状态 ---"
kubectl get application guestbook -n argocd -o jsonpath='{.status.sync.status}' 2>/dev/null || echo "应用尚未创建"
echo ""

echo ""
echo "--- 已部署资源 ---"
kubectl get all -n guestbook 2>/dev/null || echo "guestbook 命名空间尚未创建"

echo ""
echo "✅ 检查完成"
