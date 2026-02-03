#!/bin/bash
# Ingress Production Environment Setup Script

set -e

NAMESPACE="ingress-prod"
INGRESS_NAMESPACE="ingress-nginx"

echo "🚀 Setting up Kubernetes Ingress Production Environment..."

# Create namespaces
echo "📁 Creating namespaces..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace $INGRESS_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Install NGINX Ingress Controller
echo "📥 Installing NGINX Ingress Controller..."
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace $INGRESS_NAMESPACE \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"="nlb" \
  --set controller.config.use-forwarded-headers=true \
  --set controller.metrics.enabled=true \
  --set controller.resources.requests.cpu=100m \
  --set controller.resources.requests.memory=90Mi \
  --set controller.resources.limits.cpu=1000m \
  --set controller.resources.limits.memory=512Mi \
  --wait --timeout 300s

# Deploy production applications
echo "📦 Deploying production applications..."
kubectl apply -f production-apps.yaml -n $NAMESPACE

# Apply ingress rules
echo "サービ Applying ingress rules..."
kubectl apply -f ingress-rules.yaml -n $NAMESPACE

# Wait for resources to be ready
echo "⏳ Waiting for resources to be ready..."
kubectl wait --for=condition=available deployment/api-v1-app -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=available deployment/web-app -n $NAMESPACE --timeout=300s

# Verify deployment
echo "✅ Verifying deployment..."
echo "Ingress Controller Pods:"
kubectl get pods -n $INGRESS_NAMESPACE
echo ""
echo "Application Pods:"
kubectl get pods -n $NAMESPACE
echo ""
echo "Services:"
kubectl get services -n $NAMESPACE
echo ""
echo "Ingress Resources:"
kubectl get ingress -n $NAMESPACE

# Get ingress controller external IP
echo ""
echo "🌐 Ingress Controller External Access:"
kubectl get svc ingress-nginx-controller -n $INGRESS_NAMESPACE -o wide

echo ""
echo "🎉 Ingress production environment setup complete!"
echo "Use 'kubectl get ingress -n $NAMESPACE' to view ingress rules"
echo "Configure your DNS to point to the external IP above"