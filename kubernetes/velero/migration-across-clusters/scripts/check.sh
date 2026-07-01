#!/usr/bin/env bash
# 检查 migration-across-clusters 资源状态
set -euo pipefail

kubectl get all -n migration-across-clusters
