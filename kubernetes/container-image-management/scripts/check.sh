#!/usr/bin/env bash
# 检查 container-image-management 资源状态
set -euo pipefail

kubectl get all -n container-image-management
