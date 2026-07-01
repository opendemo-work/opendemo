#!/usr/bin/env bash
# 检查 rook-ceph-storage 资源状态
set -euo pipefail

kubectl get all -n rook-ceph-storage
