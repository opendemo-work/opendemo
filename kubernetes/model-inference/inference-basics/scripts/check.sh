#!/usr/bin/env bash
# 检查 inference-basics 资源状态
set -euo pipefail

kubectl get all -n inference-basics
