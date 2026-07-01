#!/usr/bin/env bash
# 检查 kubeflow 资源状态
set -euo pipefail

kubectl get all -n kubeflow
