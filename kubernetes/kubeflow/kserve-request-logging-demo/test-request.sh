#!/bin/bash
# 发送测试推理请求到 KServe 服务

SERVICE_HOST="simple-model.default.example.com"
INGRESS_GATEWAY="istio-ingressgateway.istio-system.nip.io"

# 自动获取入口网关 IP（兼容 Minikube / Kind / 外部集群）
if [[ $(kubectl config current-context) == "minikube" ]]; then
  INGRESS_IP=$(minikube ip)
else
  INGRESS_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
fi

# 构造请求头和数据
REQUEST_DATA='{"instances": [[1.0, 2.0, 3.0, 4.0]]}'

echo "Sending request to http://$INGRESS_IP (Host: $SERVICE_HOST)"

curl -H "Host: $SERVICE_HOST" \
     -H "Content-Type: application/json" \
     -d "$REQUEST_DATA" \
     "http://$INGRESS_IP/v1/models/simple-model:predict"

echo "\n\nRequest sent. Check logs using: kubectl logs <pod-name> -c kserve-container"