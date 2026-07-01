#!/usr/bin/env bash
# 检查 dev-workflow 资源状态
set -euo pipefail

kubectl get all -n dev-workflow
