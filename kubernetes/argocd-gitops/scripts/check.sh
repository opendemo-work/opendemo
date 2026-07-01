#!/usr/bin/env bash
# 检查 argocd-gitops 资源状态
set -euo pipefail

kubectl get all -n argocd-gitops
