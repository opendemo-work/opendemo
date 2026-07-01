#!/usr/bin/env bash
# 检查 efk 资源状态
set -euo pipefail

kubectl get all -n efk
