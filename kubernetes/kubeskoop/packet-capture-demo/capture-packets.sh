#!/bin/bash
# 自动化抓包脚本 - 从 Sidecar 容器执行 tcpdump

set -e

# 检查 Pod 是否就绪
echo "waiting for pod to be ready..."
kubectl wait --for=condition=ready pod/packet-capture-demo --timeout=60s

# 执行抓包命令
echo "capturing packets on eth0..."
kubectl exec packet-capture-demo -c tcpdump-sidecar -- \n  tcpdump -i eth0 -c 10 -w /captures/capture.pcap

echo "Saved to capture.pcap"

# 复制文件到本地
kubectl cp packet-capture-demo:/captures/capture.pcap ./capture.pcap