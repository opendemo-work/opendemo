#!/usr/bin/env bash
# 检查 coredns-advanced-features 资源状态
set -euo pipefail

kubectl get all -n coredns-advanced-features
