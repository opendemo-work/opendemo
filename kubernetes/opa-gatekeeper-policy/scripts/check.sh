#!/usr/bin/env bash
# 检查 opa-gatekeeper-policy 资源状态
set -euo pipefail

kubectl get all -n opa-gatekeeper-policy
