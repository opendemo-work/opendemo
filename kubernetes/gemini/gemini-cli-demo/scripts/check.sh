#!/usr/bin/env bash
# 检查 gemini-cli-demo 资源状态
set -euo pipefail

kubectl get all -n gemini-cli-demo
