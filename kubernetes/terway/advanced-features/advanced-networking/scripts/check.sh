#!/usr/bin/env bash
# 检查 advanced-networking 资源状态
set -euo pipefail

kubectl get all -n advanced-networking
