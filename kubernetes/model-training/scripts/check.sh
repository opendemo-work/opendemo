#!/usr/bin/env bash
# 检查 model-training 资源状态
set -euo pipefail

kubectl get all -n model-training
