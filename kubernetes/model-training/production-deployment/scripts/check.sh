#!/usr/bin/env bash
# 检查 production-deployment 资源状态
set -euo pipefail

kubectl get all -n production-deployment
