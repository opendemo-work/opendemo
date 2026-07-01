#!/usr/bin/env bash
# 检查 backup-monitoring 资源状态
set -euo pipefail

kubectl get all -n backup-monitoring
