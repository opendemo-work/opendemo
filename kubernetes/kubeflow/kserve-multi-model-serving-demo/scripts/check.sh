#!/usr/bin/env bash
# 检查 kserve-multi-model-serving-demo 资源状态
set -euo pipefail

kubectl get all -n kserve-multi-model-serving-demo
