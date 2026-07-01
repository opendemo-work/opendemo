#!/usr/bin/env bash
# 检查 path-based-routing 资源状态
set -euo pipefail

kubectl get all -n path-based-routing
