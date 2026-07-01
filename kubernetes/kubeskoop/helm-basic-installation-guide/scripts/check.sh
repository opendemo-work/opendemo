#!/usr/bin/env bash
# 检查 helm-basic-installation-guide 资源状态
set -euo pipefail

kubectl get all -n helm-basic-installation-guide
