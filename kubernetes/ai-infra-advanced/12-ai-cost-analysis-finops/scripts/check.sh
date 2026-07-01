#!/usr/bin/env bash
# 检查 12-ai-cost-analysis-finops 资源状态
set -euo pipefail

kubectl get all -n 12-ai-cost-analysis-finops
