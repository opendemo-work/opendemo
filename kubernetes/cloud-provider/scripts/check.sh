#!/usr/bin/env bash
# 检查 cloud-provider 资源状态
set -euo pipefail

kubectl get all -n cloud-provider
