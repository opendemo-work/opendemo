#!/usr/bin/env bash
# 检查 local-demo 资源状态
set -euo pipefail

kubectl get all -n local-demo
