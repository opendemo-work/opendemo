#!/usr/bin/env bash
# 检查 kserve-autoscaling-config-demo 资源状态
set -euo pipefail

kubectl get all -n kserve-autoscaling-config-demo
