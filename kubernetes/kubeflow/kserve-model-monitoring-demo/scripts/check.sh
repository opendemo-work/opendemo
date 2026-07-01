#!/usr/bin/env bash
# 检查 kserve-model-monitoring-demo 资源状态
set -euo pipefail

kubectl get all -n kserve-model-monitoring-demo
