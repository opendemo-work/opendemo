#!/usr/bin/env bash
# 检查 storage-fundamentals 资源状态
set -euo pipefail

kubectl get all -n storage-fundamentals
