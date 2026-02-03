#!/bin/bash
# NGINX Ingress Controller 生产环境部署脚本

set -e

NAMESPACE="ingress-system"
CONTROLLER_NAME="ingress-nginx"

echo "🚀 开始部署 NGINX Ingress Controller 生产环境..."

# 1. 创建命名空间
echo "📁 创建命名空间: $NAMESPACE"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# 2. 添加Helm仓库
echo "📥 添加 Helm 仓库..."
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# 3. 生产级部署
echo "サービ 执行生产级部署..."
helm install $CONTROLLER_NAME ingress-nginx/ingress-nginx \
  --namespace $NAMESPACE \
  --version 4.8.3 \
  --set controller.replicaCount=3 \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"="nlb" \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-cross-zone-load-balancing-enabled"="true" \
  --set controller.config.use-forwarded-headers=true \
  --set controller.config.compute-full-forwarded-for=true \
  --set controller.metrics.enabled=true \
  --set controller.metrics.serviceMonitor.enabled=true \
  --set controller.resources.requests.cpu=200m \
  --set controller.resources.requests.memory=256Mi \
  --set controller.resources.limits.cpu=1000m \
  --set controller.resources.limits.memory=1Gi \
  --set controller.autoscaling.enabled=true \
  --set controller.autoscaling.minReplicas=3 \
  --set controller.autoscaling.maxReplicas=10 \
  --set controller.autoscaling.targetCPUUtilizationPercentage=80 \
  --set controller.podAnnotations."prometheus\.io/scrape"="true" \
  --set controller.podAnnotations."prometheus\.io/port"="10254" \
  --wait --timeout 600s

# 4. 应用生产配置
echo "🔧 应用生产配置..."
kubectl apply -f production-config.yaml -n $NAMESPACE

# 5. 等待资源就绪
echo "⏳ 等待资源就绪..."
kubectl wait --for=condition=available deployment/${CONTROLLER_NAME}-controller -n $NAMESPACE --timeout=300s

# 6. 验证部署
echo "✅ 验证部署状态..."
echo "控制器Pod状态:"
kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=ingress-nginx
echo ""
echo "服务状态:"
kubectl get svc -n $NAMESPACE
echo ""
echo "IngressClass:"
kubectl get ingressclasses

# 7. 获取外部访问信息
echo ""
echo "🌐 外部访问信息:"
kubectl get svc ${CONTROLLER_NAME}-controller -n $NAMESPACE -o wide

echo ""
echo "🎉 NGINX Ingress Controller 生产环境部署完成！"
echo "使用 'kubectl get svc -n $NAMESPACE' 查看外部IP地址"