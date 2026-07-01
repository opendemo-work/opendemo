#!/usr/bin/env bash
# 检查 persistent-storage 资源状态
set -euo pipefail

kubectl get all -n persistent-storage
