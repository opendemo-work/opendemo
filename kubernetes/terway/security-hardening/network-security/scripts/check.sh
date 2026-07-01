#!/usr/bin/env bash
# 检查 network-security 资源状态
set -euo pipefail

kubectl get all -n network-security
