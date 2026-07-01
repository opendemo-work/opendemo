#!/bin/bash
# 风险等级：🟢 低风险
# 说明：只读查询或无害信息展示，不会修改系统状态。
# 生产安全提示：
#   - 通常为只读操作，不会修改系统状态。
#   - 可安全地在学习环境中执行。

# 验证抓包结果脚本

if [ ! -f "capture.pcap" ]; then
  echo "Error: capture.pcap not found. Run capture-packets.sh first."
  exit 1
fi

echo "Reading from capture.pcap"
tcpdump -r capture.pcap -c 5
