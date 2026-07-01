#!/usr/bin/env bash
# 检查 backup-hooks 资源状态
set -euo pipefail

kubectl get all -n backup-hooks
