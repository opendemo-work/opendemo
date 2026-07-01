#!/usr/bin/env bash
# 检查 dashboard-rbac-configuration 资源状态
set -euo pipefail

kubectl get all -n dashboard-rbac-configuration
