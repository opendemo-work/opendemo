#!/usr/bin/env bash
# 检查 pv-pvc-troubleshooting 资源状态
set -euo pipefail

kubectl get all -n pv-pvc-troubleshooting
