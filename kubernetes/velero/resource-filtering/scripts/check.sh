#!/usr/bin/env bash
# 检查 resource-filtering 资源状态
set -euo pipefail

kubectl get all -n resource-filtering
