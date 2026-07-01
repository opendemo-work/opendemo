#!/usr/bin/env bash
# 检查 monitoring-logging 资源状态
set -euo pipefail

kubectl get all -n monitoring-logging
