#!/usr/bin/env bash
# 检查 packet-capture-demo 资源状态
set -euo pipefail

kubectl get all -n packet-capture-demo
