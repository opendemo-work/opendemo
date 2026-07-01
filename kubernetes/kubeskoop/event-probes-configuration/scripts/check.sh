#!/usr/bin/env bash
# 检查 event-probes-configuration 资源状态
set -euo pipefail

kubectl get all -n event-probes-configuration
