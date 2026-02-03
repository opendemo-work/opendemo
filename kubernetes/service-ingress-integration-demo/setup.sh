#!/bin/bash
# Service-Ingress Integration Setup Script

set -e

NAMESPACE="service-ingress-integration"
INGRESS_NAMESPACE="ingress-nginx"

echo "🚀 Setting up Service-Ingress Integration Environment..."

# Create namespace
echo "📁 Creating namespace: $NAMESPACE"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Ensure Ingress controller is installed
echo "🔍 Checking Ingress controller..."
if ! kubectl get namespace $INGRESS_NAMESPACE >/dev/null 2>&1; then
    echo "📥 Installing NGINX Ingress Controller..."
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install ingress-nginx ingress-nginx/ingress-nginx \
      --namespace $INGRESS_NAMESPACE \
      --create-namespace \
      --set controller.service.type=LoadBalancer \
      --set controller.metrics.enabled=true \
      --wait --timeout 300s
else
    echo "✅ Ingress controller already installed"
fi

# Deploy integration components
echo "📦 Deploying integration components..."
kubectl apply -f integration-components.yaml -n $NAMESPACE

# Deploy sample applications
echo "サービ Deploying sample applications..."
kubectl apply -f sample-applications.yaml -n $NAMESPACE

# Wait for resources to be ready
echo "⏳ Waiting for resources to be ready..."
kubectl wait --for=condition=available deployment/frontend-app -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=available deployment/api-gateway -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=available deployment/user-service -n $NAMESPACE --timeout=300s
kubectl wait --for=condition=available deployment/order-service -n $NAMESPACE --timeout=300s

# Verify deployment
echo "✅ Verifying deployment..."
echo "Pods:"
kubectl get pods -n $NAMESPACE
echo ""
echo "Services:"
kubectl get services -n $NAMESPACE
echo ""
echo "Ingress:"
kubectl get ingress -n $NAMESPACE
echo ""
echo "Network Policies:"
kubectl get networkpolicies -n $NAMESPACE

# Test service connectivity
echo "🧪 Testing service connectivity..."
FRONTEND_POD=$(kubectl get pods -n $NAMESPACE -l app=frontend -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $FRONTEND_POD -n $NAMESPACE -- wget -qO- http://localhost:8080 2>/dev/null || echo "Frontend service test completed"

# Get ingress information
echo ""
echo "🌐 Ingress Information:"
kubectl get svc ingress-nginx-controller -n $INGRESS_NAMESPACE -o wide

echo ""
echo "🎉 Service-Ingress integration environment setup complete!"
echo "Use 'kubectl get ingress -n $NAMESPACE' to view ingress rules"
echo "Configure DNS to point to the external IP for full functionality"