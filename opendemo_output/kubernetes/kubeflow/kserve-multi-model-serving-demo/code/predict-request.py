#!/usr/bin/env python3
# predict-request.py
# 向 KServe 多模型服务发送预测请求的客户端脚本

import requests
import json

# 设置推理服务的入口网关地址（通常由 Istio IngressGateway 提供）
# 在本地测试时可通过端口转发访问：kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
INGRESS_HOST = "localhost"
INGRESS_PORT = "8080"

# 构建每个模型的完整 URL
SKLEARN_URL = f"http://{INGRESS_HOST}:{INGRESS_PORT}/v2/models/sklearn-model/versions/v1/infer"
XGBOOST_URL = f"http://{INGRESS_HOST}:{INGRESS_PORT}/v2/models/xgboost-model/versions/v1/infer"

# 标准化的 KServe v2 推理协议请求体
# 参考：https://github.com/kserve/kserve/blob/master/docs/predict-api/v2/required_api.md
request_data = {
    "inputs": [
        {
            "name": "input-0",
            "shape": [2, 4],
            "datatype": "FP32",
            "data": [
                [6.8, 2.8, 4.8, 1.4],
                [6.0, 3.4, 4.5, 1.6]
            ]
        }
    ]
}

# 设置请求头，标明内容类型
headers = {"Content-Type": "application/json"}

if __name__ == "__main__":
    try:
        # 发送请求到 Sklearn 模型
        response = requests.post(SKLEARN_URL, data=json.dumps(request_data), headers=headers)
        print(f"Sklearn 模型响应: {response.json()}")
        
        # 发送请求到 XGBoost 模型
        response = requests.post(XGBOOST_URL, data=json.dumps(request_data), headers=headers)
        print(f"XGBoost 模型响应: {response.json()}")
        
    except requests.exceptions.ConnectionError:
        print("连接失败，请确保：\n1. KServe 服务已正确部署\n2. Istio IngressGateway 正在运行\n3. 已执行端口转发或配置了 DNS")
    except Exception as e:
        print(f"请求出错: {str(e)}")