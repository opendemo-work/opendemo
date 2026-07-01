#!/usr/bin/env bash
# 检查 service-ingress-integration-demo 资源状态
set -euo pipefail

kubectl get all -n service-ingress-integration-demo
