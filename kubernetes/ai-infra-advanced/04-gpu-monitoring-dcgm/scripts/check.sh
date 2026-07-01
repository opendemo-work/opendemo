#!/usr/bin/env bash
# 检查 04-gpu-monitoring-dcgm 资源状态
set -euo pipefail

kubectl get all -n 04-gpu-monitoring-dcgm
