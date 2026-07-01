#!/usr/bin/env bash
# 检查 rook-storage-orchestration 资源状态
set -euo pipefail

kubectl get all -n rook-storage-orchestration
