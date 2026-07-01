#!/usr/bin/env bash
# 检查 ingress-security 资源状态
set -euo pipefail

kubectl get all -n ingress-security
