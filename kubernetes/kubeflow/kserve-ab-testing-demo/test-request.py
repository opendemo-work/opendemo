#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
向 KServe A/B 测试服务发送推理请求，验证流量分配效果。
"""

import requests
import json

# 配置参数（需先在 shell 中导出环境变量）
INGRESS_HOST = "<YOUR_INGRESS_IP>"  # 替换为实际值或从环境读取
SERVICE_HOSTNAME = "ab-test-model.default.example.com"  # 与 InferenceService 名称匹配

# 示例输入数据（鸢尾花分类示例）
input_data = {
    "instances": [
        [6.7, 3.1, 4.7, 1.5],  # 特征向量
        [4.6, 3.1, 1.5, 0.2]
    ]
}

def send_request():
    """发送单次请求并解析返回的模型版本"""
    try:
        response = requests.post(
            f"http://{INGRESS_HOST}/v1/models/{SERVICE_HOSTNAME.split('.')[0]}:predict",
            headers={"Host": SERVICE_HOSTNAME},
            data=json.dumps(input_data),
            timeout=10
        )
        result = response.json()
        
        # 假设模型服务在响应中返回其版本信息（由镜像逻辑决定）
        model_version = result.get("version", "unknown")
        print(f"请求响应来自模型版本: {model_version}")
        
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    # 发送 10 次请求观察流量分布
    for _ in range(10):
        send_request()