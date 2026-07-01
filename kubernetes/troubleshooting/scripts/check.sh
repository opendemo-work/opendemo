#!/usr/bin/env bash
# 检查 troubleshooting 资源状态
set -euo pipefail

kubectl get all -n troubleshooting
