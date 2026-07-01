#!/usr/bin/env bash
# 检查 cilium-service-mesh 资源状态
set -euo pipefail

kubectl get all -n cilium-service-mesh
