#!/usr/bin/env bash
# 检查 operator-framework 资源状态
set -euo pipefail

kubectl get all -n operator-framework
