#!/bin/bash
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