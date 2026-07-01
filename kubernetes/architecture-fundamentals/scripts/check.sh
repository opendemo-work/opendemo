#!/usr/bin/env bash
# 检查 architecture-fundamentals 资源状态
set -euo pipefail

kubectl get all -n architecture-fundamentals
