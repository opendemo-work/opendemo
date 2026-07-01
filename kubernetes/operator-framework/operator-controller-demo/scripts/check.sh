#!/usr/bin/env bash
# 检查 operator-controller-demo 资源状态
set -euo pipefail

kubectl get all -n operator-controller-demo
