#!/usr/bin/env bash
# 检查 katib-hyperparameter-tuning 资源状态
set -euo pipefail

kubectl get all -n katib-hyperparameter-tuning
