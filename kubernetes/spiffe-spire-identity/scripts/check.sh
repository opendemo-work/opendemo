#!/usr/bin/env bash
# 检查 spiffe-spire-identity 资源状态
set -euo pipefail

kubectl get all -n spiffe-spire-identity
