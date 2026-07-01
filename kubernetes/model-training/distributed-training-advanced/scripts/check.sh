#!/usr/bin/env bash
# 检查 distributed-training-advanced 资源状态
set -euo pipefail

kubectl get all -n distributed-training-advanced
