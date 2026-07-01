#!/usr/bin/env bash
# 检查 topic-structural-trouble-shooting 资源状态
set -euo pipefail

kubectl get all -n topic-structural-trouble-shooting
