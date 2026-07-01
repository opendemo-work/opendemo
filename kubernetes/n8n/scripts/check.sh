#!/usr/bin/env bash
# 检查 n8n 资源状态
set -euo pipefail

kubectl get all -n n8n
