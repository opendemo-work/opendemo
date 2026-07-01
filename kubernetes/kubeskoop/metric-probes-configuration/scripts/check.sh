#!/usr/bin/env bash
# 检查 metric-probes-configuration 资源状态
set -euo pipefail

kubectl get all -n metric-probes-configuration
