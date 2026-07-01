#!/usr/bin/env bash
# 检查 01-ai-infrastructure-overview 资源状态
set -euo pipefail

kubectl get all -n 01-ai-infrastructure-overview
