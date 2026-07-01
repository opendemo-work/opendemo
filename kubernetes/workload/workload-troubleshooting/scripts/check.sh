#!/usr/bin/env bash
# 检查 workload-troubleshooting 资源状态
set -euo pipefail

kubectl get all -n workload-troubleshooting
