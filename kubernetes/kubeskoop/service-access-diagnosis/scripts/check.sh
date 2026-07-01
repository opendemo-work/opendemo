#!/usr/bin/env bash
# 检查 service-access-diagnosis 资源状态
set -euo pipefail

kubectl get all -n service-access-diagnosis
