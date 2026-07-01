#!/usr/bin/env bash
# 检查 13-ai-platform-observability 资源状态
set -euo pipefail

kubectl get all -n 13-ai-platform-observability
