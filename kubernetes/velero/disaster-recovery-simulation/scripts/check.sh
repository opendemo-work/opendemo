#!/usr/bin/env bash
# 检查 disaster-recovery-simulation 资源状态
set -euo pipefail

kubectl get all -n disaster-recovery-simulation
