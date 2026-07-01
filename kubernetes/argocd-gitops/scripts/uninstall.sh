#!/usr/bin/env bash
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
