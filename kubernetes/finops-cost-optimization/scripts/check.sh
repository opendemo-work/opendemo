#!/usr/bin/env bash
# 检查 finops-cost-optimization 资源状态
set -euo pipefail

kubectl get all -n finops-cost-optimization
