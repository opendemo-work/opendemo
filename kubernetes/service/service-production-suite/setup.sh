#!/bin/bash
# 风险等级：🟡 中风险
# 说明：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
# 生产安全提示：
#   - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
#   - 注意检查依赖版本、端口占用和目标资源配置。
#   - 生产环境执行前请经过变更评审和备份确认。

# Service Production Environment Setup Script

set -e

NAMESPACE="service-prod"

echo "🚀 Setting up Kubernetes Service Production Environment..."

# Create namespace
echo "📁 Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply RBAC configuration
echo "🔒 Applying RBAC configuration..."
kubectl apply -f rbac-config.yaml -n $NAMESPACE

# Deploy production application
echo "📦 Deploying production application..."
kubectl apply -f production-app.yaml -n $NAMESPACE

# Apply service configurations
echo "サービ Applying service configurations..."
kubectl apply -f services.yaml -n $NAMESPACE

# Wait for resources to be ready
echo "⏳ Waiting for resources to be ready..."
kubectl wait --for=condition=available deployment/production-app -n $NAMESPACE --timeout=300s

# Verify deployment
echo "✅ Verifying deployment..."
echo "Pods:"
kubectl get pods -n $NAMESPACE
echo ""
echo "Services:"
kubectl get services -n $NAMESPACE
echo ""
echo "Deployments:"
kubectl get deployments -n $NAMESPACE

# Test service connectivity
echo "🧪 Testing service connectivity..."
APP_POD=$(kubectl get pods -n $NAMESPACE -l app=myapp -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $APP_POD -n $NAMESPACE -- wget -qO- http://localhost:8080/healthz || echo "Health check endpoint not available"

echo "🎉 Service production environment setup complete!"
echo "Use 'kubectl get services -n $NAMESPACE' to view service endpoints"
