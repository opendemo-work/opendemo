#!/usr/bin/env bash
# 检查 falco-runtime-security 资源状态
set -euo pipefail

kubectl get all -n falco-runtime-security
