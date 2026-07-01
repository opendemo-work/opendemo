#!/usr/bin/env bash
# 检查 docker-cli-integration 资源状态
set -euo pipefail

kubectl get all -n docker-cli-integration
