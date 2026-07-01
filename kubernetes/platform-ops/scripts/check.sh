#!/usr/bin/env bash
# 检查 platform-ops 资源状态
set -euo pipefail

kubectl get all -n platform-ops
