#!/usr/bin/env bash
# 检查 pipeline-experiment-management 资源状态
set -euo pipefail

kubectl get all -n pipeline-experiment-management
