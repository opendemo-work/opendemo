#!/usr/bin/env bash
# 检查 disaster-recovery-business-continuity 资源状态
set -euo pipefail

kubectl get all -n disaster-recovery-business-continuity
