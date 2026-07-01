#!/usr/bin/env bash
# 检查 latency-detection-configuration 资源状态
set -euo pipefail

kubectl get all -n latency-detection-configuration
