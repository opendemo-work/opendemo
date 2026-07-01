#!/usr/bin/env bash
# 风险等级：🔴 高风险
# 说明：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
# 生产安全提示：
#   - 会删除/格式化/停止关键资源，生产环境慎用。
#   - 执行前请确认目标范围，建议在隔离测试环境验证。
#   - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。

# 卸载 ArgoCD 和示例应用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "卸载 ArgoCD 和示例应用..."
kubectl delete -f manifests/guestbook-application.yaml --ignore-not-found=true
kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml --ignore-not-found=true
kubectl delete namespace argocd --ignore-not-found=true
kubectl delete namespace guestbook --ignore-not-found=true

echo "✅ 卸载完成"
