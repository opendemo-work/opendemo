#!/usr/bin/env bash
# 检查 notebook-persistent-storage 资源状态
set -euo pipefail

kubectl get all -n notebook-persistent-storage
