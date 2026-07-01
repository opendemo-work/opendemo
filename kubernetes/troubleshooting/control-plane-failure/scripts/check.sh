#!/usr/bin/env bash
# 检查 control-plane-failure 资源状态
set -euo pipefail

kubectl get all -n control-plane-failure
