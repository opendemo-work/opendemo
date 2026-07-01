#!/usr/bin/env bash
# 检查 docker-advanced 资源状态
set -euo pipefail

kubectl get all -n docker-advanced
