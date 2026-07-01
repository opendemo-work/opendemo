#!/usr/bin/env bash
# 检查 csi-plugin-advanced 资源状态
set -euo pipefail

kubectl get all -n csi-plugin-advanced
