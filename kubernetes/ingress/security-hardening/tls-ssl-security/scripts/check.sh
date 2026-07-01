#!/usr/bin/env bash
# 检查 tls-ssl-security 资源状态
set -euo pipefail

kubectl get all -n tls-ssl-security
