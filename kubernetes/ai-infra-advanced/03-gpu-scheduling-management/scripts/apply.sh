#!/usr/bin/env bash
# 应用 03-gpu-scheduling-management 的 Kubernetes 资源
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/deployment.yaml

echo "✅ 03-gpu-scheduling-management 资源已应用到命名空间 03-gpu-scheduling-management"
