#!/usr/bin/env bash
# 检查 32-mlops-pipeline 资源状态
set -euo pipefail

kubectl get all -n 32-mlops-pipeline
