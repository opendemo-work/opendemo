#!/usr/bin/env bash
# 检查 ingress-production-suite 资源状态
set -euo pipefail

kubectl get all -n ingress-production-suite
