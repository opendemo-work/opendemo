#!/usr/bin/env bash
# 检查 registry-harbor 资源状态
set -euo pipefail

kubectl get all -n registry-harbor
