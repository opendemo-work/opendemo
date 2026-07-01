#!/usr/bin/env bash
# 检查 job-cronjob-basics 资源状态
set -euo pipefail

kubectl get all -n job-cronjob-basics
