#!/usr/bin/env bash
# 检查 karmada-multi-cluster 资源状态
set -euo pipefail

kubectl get all -n karmada-multi-cluster
