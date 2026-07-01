#!/usr/bin/env bash
# 检查 model-training-basics 资源状态
set -euo pipefail

kubectl get all -n model-training-basics
