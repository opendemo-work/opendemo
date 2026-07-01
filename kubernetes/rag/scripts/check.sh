#!/usr/bin/env bash
# 检查 rag 资源状态
set -euo pipefail

kubectl get all -n rag
