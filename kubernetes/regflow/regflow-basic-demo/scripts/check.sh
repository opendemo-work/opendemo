#!/usr/bin/env bash
# 检查 regflow-basic-demo 资源状态
set -euo pipefail

kubectl get all -n regflow-basic-demo
