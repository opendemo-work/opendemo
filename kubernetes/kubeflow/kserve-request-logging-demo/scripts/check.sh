#!/usr/bin/env bash
# 检查 kserve-request-logging-demo 资源状态
set -euo pipefail

kubectl get all -n kserve-request-logging-demo
