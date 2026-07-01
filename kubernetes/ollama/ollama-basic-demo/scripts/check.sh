#!/usr/bin/env bash
# 检查 ollama-basic-demo 资源状态
set -euo pipefail

kubectl get all -n ollama-basic-demo
