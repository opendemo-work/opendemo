#!/usr/bin/env bash
# 检查 modelscope 资源状态
set -euo pipefail

kubectl get all -n modelscope
