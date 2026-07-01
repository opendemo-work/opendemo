#!/usr/bin/env bash
# 检查 model-finetuning-optimization 资源状态
set -euo pipefail

kubectl get all -n model-finetuning-optimization
