#!/usr/bin/env bash
# 检查 ai-infra 资源状态
set -euo pipefail

kubectl get all -n ai-infra
