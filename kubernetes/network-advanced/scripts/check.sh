#!/usr/bin/env bash
# 检查 network-advanced 资源状态
set -euo pipefail

kubectl get all -n network-advanced
