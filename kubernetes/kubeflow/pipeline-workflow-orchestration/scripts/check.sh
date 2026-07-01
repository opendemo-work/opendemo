#!/usr/bin/env bash
# 检查 pipeline-workflow-orchestration 资源状态
set -euo pipefail

kubectl get all -n pipeline-workflow-orchestration
