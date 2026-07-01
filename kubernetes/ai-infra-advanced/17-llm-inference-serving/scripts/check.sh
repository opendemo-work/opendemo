#!/usr/bin/env bash
# 检查 17-llm-inference-serving 资源状态
set -euo pipefail

kubectl get all -n 17-llm-inference-serving
