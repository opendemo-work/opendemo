#!/usr/bin/env bash
# 检查 rbac-auth 资源状态
set -euo pipefail

kubectl get all -n rbac-auth
