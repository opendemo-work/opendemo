#!/usr/bin/env bash
# 检查 istio-service-mesh-basics 资源状态
set -euo pipefail

kubectl get all -n istio-service-mesh-basics
