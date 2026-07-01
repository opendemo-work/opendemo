#!/usr/bin/env bash
# 检查 notebook-server-creation 资源状态
set -euo pipefail

kubectl get all -n notebook-server-creation
