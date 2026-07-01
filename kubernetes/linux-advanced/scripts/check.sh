#!/usr/bin/env bash
# 检查 linux-advanced 资源状态
set -euo pipefail

kubectl get all -n linux-advanced
