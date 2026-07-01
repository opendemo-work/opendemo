#!/usr/bin/env bash
# 检查 kserve-explainer-integration-demo 资源状态
set -euo pipefail

kubectl get all -n kserve-explainer-integration-demo
