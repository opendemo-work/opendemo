#!/usr/bin/env bash
# 检查 basic-jaeger 资源状态
set -euo pipefail

kubectl get all -n basic-jaeger
