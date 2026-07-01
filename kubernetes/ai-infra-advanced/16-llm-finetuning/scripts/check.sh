#!/usr/bin/env bash
# 检查 16-llm-finetuning 资源状态
set -euo pipefail

kubectl get all -n 16-llm-finetuning
