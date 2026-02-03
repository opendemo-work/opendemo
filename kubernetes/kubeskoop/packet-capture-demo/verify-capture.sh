#!/bin/bash
# 验证抓包结果脚本

if [ ! -f "capture.pcap" ]; then
  echo "Error: capture.pcap not found. Run capture-packets.sh first."
  exit 1
fi

echo "Reading from capture.pcap"
tcpdump -r capture.pcap -c 5