#!/usr/bin/env bash
# 检查 node-failure 资源状态
set -euo pipefail

kubectl get all -n node-failure
