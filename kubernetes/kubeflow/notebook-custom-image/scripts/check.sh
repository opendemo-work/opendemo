#!/usr/bin/env bash
# 检查 notebook-custom-image 资源状态
set -euo pipefail

kubectl get all -n notebook-custom-image
