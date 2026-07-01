#!/usr/bin/env bash
# 检查 gitops-ci-cd 资源状态
set -euo pipefail

kubectl get all -n gitops-ci-cd
