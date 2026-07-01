#!/usr/bin/env bash
# 检查 cluster-backup 资源状态
set -euo pipefail

kubectl get all -n cluster-backup
