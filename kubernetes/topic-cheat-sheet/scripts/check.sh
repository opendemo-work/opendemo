#!/usr/bin/env bash
# 检查 topic-cheat-sheet 资源状态
set -euo pipefail

kubectl get all -n topic-cheat-sheet
