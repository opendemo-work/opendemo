#!/usr/bin/env bash
# 检查 custom-resources 资源状态
set -euo pipefail

kubectl get all -n custom-resources
