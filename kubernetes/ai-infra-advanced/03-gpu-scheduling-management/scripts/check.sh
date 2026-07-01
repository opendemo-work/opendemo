#!/usr/bin/env bash
# 检查 03-gpu-scheduling-management 资源状态
set -euo pipefail

kubectl get all -n 03-gpu-scheduling-management
