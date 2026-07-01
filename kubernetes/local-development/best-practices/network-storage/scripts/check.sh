#!/usr/bin/env bash
# 检查 network-storage 资源状态
set -euo pipefail

kubectl get all -n network-storage
