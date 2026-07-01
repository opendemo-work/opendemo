#!/bin/bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

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
