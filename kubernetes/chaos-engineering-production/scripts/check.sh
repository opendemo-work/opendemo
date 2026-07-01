#!/usr/bin/env bash
# 检查 chaos-engineering-production 资源状态
set -euo pipefail

kubectl get all -n chaos-engineering-production
