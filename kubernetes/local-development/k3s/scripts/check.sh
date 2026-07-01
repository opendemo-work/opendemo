#!/usr/bin/env bash
# 检查 k3s 资源状态
set -euo pipefail

kubectl get all -n k3s
