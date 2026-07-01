#!/usr/bin/env bash
# 检查 basic-grafana 资源状态
set -euo pipefail

kubectl get all -n basic-grafana
