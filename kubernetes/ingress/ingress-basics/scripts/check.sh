#!/usr/bin/env bash
# 检查 ingress-basics 资源状态
set -euo pipefail

kubectl get all -n ingress-basics
