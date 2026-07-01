#!/usr/bin/env bash
# 检查 microsoft 资源状态
set -euo pipefail

kubectl get all -n microsoft
