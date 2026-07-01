#!/usr/bin/env bash
# 检查 scheduled-backup 资源状态
set -euo pipefail

kubectl get all -n scheduled-backup
