#!/usr/bin/env bash
# 检查 05-distributed-training-frameworks 资源状态
set -euo pipefail

kubectl get all -n 05-distributed-training-frameworks
