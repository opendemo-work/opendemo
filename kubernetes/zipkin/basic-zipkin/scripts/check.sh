#!/usr/bin/env bash
# 检查 basic-zipkin 资源状态
set -euo pipefail

kubectl get all -n basic-zipkin
