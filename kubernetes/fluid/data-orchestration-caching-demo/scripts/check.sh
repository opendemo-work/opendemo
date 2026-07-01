#!/usr/bin/env bash
# 检查 data-orchestration-caching-demo 资源状态
set -euo pipefail

kubectl get all -n data-orchestration-caching-demo
