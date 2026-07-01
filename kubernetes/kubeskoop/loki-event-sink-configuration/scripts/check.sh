#!/usr/bin/env bash
# 检查 loki-event-sink-configuration 资源状态
set -euo pipefail

kubectl get all -n loki-event-sink-configuration
