#!/usr/bin/env bash
# 应用 notebook-gpu-allocation 的 Kubernetes 资源
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/deployment.yaml

echo "✅ notebook-gpu-allocation 资源已应用到命名空间 notebook-gpu-allocation"
