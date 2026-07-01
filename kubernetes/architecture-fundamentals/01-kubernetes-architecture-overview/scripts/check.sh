#!/usr/bin/env bash
# 检查 01-kubernetes-architecture-overview 资源状态
set -euo pipefail

kubectl get all -n 01-kubernetes-architecture-overview
