#!/usr/bin/env bash
# 检查 10-model-deployment-management 资源状态
set -euo pipefail

kubectl get all -n 10-model-deployment-management
