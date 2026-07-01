#!/usr/bin/env bash
# 检查 cloud-native-api-gateway 资源状态
set -euo pipefail

kubectl get all -n cloud-native-api-gateway
