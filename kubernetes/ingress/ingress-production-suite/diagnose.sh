#!/bin/bash
# Ingress Diagnostic and Troubleshooting Script

NAMESPACE="ingress-prod"
INGRESS_NAMESPACE="ingress-nginx"

echo "🔧 Kubernetes Ingress Diagnostic Tool"
echo "====================================="

# Ingress status overview
echo "📋 Ingress Status Overview:"
kubectl get ingress -n $NAMESPACE -o wide

echo ""
echo "📊 Detailed Ingress Information:"
for ingress in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "--- Ingress: $ingress ---"
    kubectl describe ingress $ingress -n $NAMESPACE
    echo ""
done

# Ingress controller status
echo "⚙️ Ingress Controller Status:"
kubectl get pods -n $INGRESS_NAMESPACE
kubectl get svc -n $INGRESS_NAMESPACE

echo ""
echo "🔍 Ingress Controller Logs:"
kubectl logs -n $INGRESS_NAMESPACE -l app.kubernetes.io/name=ingress-nginx --tail=20

# Service and endpoint verification
echo ""
echo "🔗 Service and Endpoint Verification:"
kubectl get services -n $NAMESPACE
kubectl get endpoints -n $NAMESPACE

# DNS resolution tests
echo ""
echo "🌐 DNS Resolution Tests:"
for ingress in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].spec.rules[*].host}'); do
    echo "Testing DNS for $ingress:"
    nslookup $ingress 2>/dev/null || echo "DNS resolution failed for $ingress"
    echo ""
done

# HTTP connectivity tests
echo "🔌 HTTP Connectivity Tests:"
INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n $INGRESS_NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ ! -z "$INGRESS_IP" ]; then
    echo "Testing connectivity to Ingress Controller ($INGRESS_IP):"
    
    # Test each ingress host
    for host in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].spec.rules[*].host}'); do
        echo "Testing $host:"
        curl -H "Host: $host" -s -w "HTTP Code: %{http_code}\nResponse Time: %{time_total}s\n" http://$INGRESS_IP/ 2>/dev/null || echo "Connectivity test failed for $host"
        echo ""
    done
else
    echo "⚠️  No external IP found for Ingress Controller"
fi

# Certificate verification
echo "🔐 TLS Certificate Status:"
for secret in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].spec.tls[*].secretName}'); do
    if [ ! -z "$secret" ]; then
        echo "Certificate Secret: $secret"
        kubectl get secret $secret -n $NAMESPACE -o yaml | grep -E "tls.crt|tls.key" | head -2
        echo ""
    fi
done

# Rate limiting and security checks
echo "🛡️ Security Configuration:"
for ingress in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Security annotations for $ingress:"
    kubectl get ingress $ingress -n $NAMESPACE -o jsonpath='{.metadata.annotations}' | jq 'with_entries(select(.key | startswith("nginx.ingress.kubernetes.io")))'
    echo ""
done

# Performance metrics
echo "📈 Performance Metrics:"
echo "Active connections:"
kubectl exec -n $INGRESS_NAMESPACE -l app.kubernetes.io/name=ingress-nginx -- curl -s http://localhost:10254/metrics | grep nginx_ingress_controller_nginx_process_connections || echo "Metrics not available"

echo ""
echo "✅ Diagnostic completed. Review the output above for any issues."