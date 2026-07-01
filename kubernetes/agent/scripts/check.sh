#!/usr/bin/env bash
# 检查 agent 资源状态
set -euo pipefail

kubectl get all -n agent
