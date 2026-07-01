#!/usr/bin/env bash
# 检查 custom-annotations 资源状态
set -euo pipefail

kubectl get all -n custom-annotations
