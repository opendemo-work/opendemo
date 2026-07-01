#!/usr/bin/env bash
# 检查 infra-production 资源状态
set -euo pipefail

kubectl get all -n infra-production
