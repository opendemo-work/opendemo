#!/usr/bin/env bash
# 检查 service-production-suite 资源状态
set -euo pipefail

kubectl get all -n service-production-suite
