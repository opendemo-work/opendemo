#!/usr/bin/env bash
# 检查 knative-serverless 资源状态
set -euo pipefail

kubectl get all -n knative-serverless
