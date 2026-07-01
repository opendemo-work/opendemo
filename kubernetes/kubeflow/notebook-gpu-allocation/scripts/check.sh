#!/usr/bin/env bash
# 检查 notebook-gpu-allocation 资源状态
set -euo pipefail

kubectl get all -n notebook-gpu-allocation
