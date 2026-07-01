#!/usr/bin/env bash
# 检查 basic-elk 资源状态
set -euo pipefail

kubectl get all -n basic-elk
