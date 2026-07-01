#!/usr/bin/env bash
# 检查 resource-shortage 资源状态
set -euo pipefail

kubectl get all -n resource-shortage
