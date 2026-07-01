#!/usr/bin/env bash
# 检查 pipeline-python-component 资源状态
set -euo pipefail

kubectl get all -n pipeline-python-component
