#!/usr/bin/env bash
# 检查 terway-advanced 资源状态
set -euo pipefail

kubectl get all -n terway-advanced
