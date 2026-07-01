#!/usr/bin/env bash
# 检查 extensions 资源状态
set -euo pipefail

kubectl get all -n extensions
