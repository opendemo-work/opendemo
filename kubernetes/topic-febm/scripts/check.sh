#!/usr/bin/env bash
# 检查 topic-febm 资源状态
set -euo pipefail

kubectl get all -n topic-febm
