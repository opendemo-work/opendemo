#!/usr/bin/env bash
# 应用 opa-gatekeeper-policy 的 Kubernetes 资源
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/deployment.yaml

echo "✅ opa-gatekeeper-policy 资源已应用到命名空间 opa-gatekeeper-policy"
