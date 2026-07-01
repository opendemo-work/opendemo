#!/usr/bin/env bash
# 检查 dashboard-basic-setup 资源状态
set -euo pipefail

kubectl get all -n dashboard-basic-setup
