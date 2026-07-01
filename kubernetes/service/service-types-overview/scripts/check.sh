#!/usr/bin/env bash
# 检查 service-types-overview 资源状态
set -euo pipefail

kubectl get all -n service-types-overview
