#!/usr/bin/env bash
# 检查 yaml-manifests 资源状态
set -euo pipefail

kubectl get all -n yaml-manifests
