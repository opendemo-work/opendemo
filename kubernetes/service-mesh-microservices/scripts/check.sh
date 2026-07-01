#!/usr/bin/env bash
# 检查 service-mesh-microservices 资源状态
set -euo pipefail

kubectl get all -n service-mesh-microservices
