#!/usr/bin/env bash
# 检查 kubeflow-dashboard-installation-demo 资源状态
set -euo pipefail

kubectl get all -n kubeflow-dashboard-installation-demo
