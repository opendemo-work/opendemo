#!/usr/bin/env bash
# 检查 topic-presentations 资源状态
set -euo pipefail

kubectl get all -n topic-presentations
