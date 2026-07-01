#!/usr/bin/env bash
# 检查 20-vector-database-rag 资源状态
set -euo pipefail

kubectl get all -n 20-vector-database-rag
