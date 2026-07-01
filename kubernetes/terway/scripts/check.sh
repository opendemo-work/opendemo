#!/usr/bin/env bash
# 检查 terway 资源状态
set -euo pipefail

kubectl get all -n terway
