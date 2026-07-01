#!/usr/bin/env bash
# 检查 volume-snapshot-location 资源状态
set -euo pipefail

kubectl get all -n volume-snapshot-location
