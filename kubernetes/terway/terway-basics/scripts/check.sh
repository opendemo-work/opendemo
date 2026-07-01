#!/usr/bin/env bash
# 检查 terway-basics 资源状态
set -euo pipefail

kubectl get all -n terway-basics
