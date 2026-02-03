#!/bin/bash
# Service-Ingress Integration Diagnostic Script

NAMESPACE="service-ingress-integration"
INGRESS_NAMESPACE="ingress-nginx"

echo "🔧 Service-Ingress Integration Diagnostic Tool"
echo "=============================================="

# 1. Overall status check
echo "📋 1. Overall Resource Status"
echo "Namespaces:"
kubectl get namespaces | grep -E "(ingress|service-ingress)"
echo ""
echo "Pods in $NAMESPACE:"
kubectl get pods -n $NAMESPACE -o wide
echo ""
echo "Services in $NAMESPACE:"
kubectl get services -n $NAMESPACE -o wide
echo ""
echo "Ingress resources:"
kubectl get ingress -n $NAMESPACE -o wide

# 2. Service-Endpoint verification
echo ""
echo "🔗 2. Service-Endpoint Verification"
kubectl get endpoints -n $NAMESPACE
echo ""
for svc in $(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Service $svc endpoints:"
    kubectl describe endpoints $svc -n $NAMESPACE | grep -A 10 "Addresses:"
    echo ""
done

# 3. Ingress controller status
echo "⚙️ 3. Ingress Controller Status"
if kubectl get namespace $INGRESS_NAMESPACE >/dev/null 2>&1; then
    echo "Ingress controller pods:"
    kubectl get pods -n $INGRESS_NAMESPACE
    echo ""
    echo "Ingress controller service:"
    kubectl get svc -n $INGRESS_NAMESPACE
    echo ""
    echo "Recent controller logs:"
    kubectl logs -n $INGRESS_NAMESPACE -l app.kubernetes.io/name=ingress-nginx --tail=20 2>/dev/null || echo "No logs available"
else
    echo "⚠️  Ingress controller namespace not found"
fi

# 4. Network policy verification
echo ""
echo "🛡️ 4. Network Policy Status"
kubectl get networkpolicies -n $NAMESPACE 2>/dev/null || echo "No network policies found"
echo ""
for np in $(kubectl get networkpolicies -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
    echo "Policy $np:"
    kubectl describe networkpolicy $np -n $NAMESPACE
    echo ""
done

# 5. Internal service connectivity test
echo "🌐 5. Internal Service Connectivity Test"
for svc in $(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Testing connectivity to $svc:"
    kubectl run debug-$svc --image=busybox --rm -it -n $NAMESPACE -- \
        timeout 10 wget -qO- --timeout=5 http://$svc 2>&1 || echo "Failed to connect to $svc"
    echo ""
done

# 6. External access test
echo "🔌 6. External Access Test"
INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n $INGRESS_NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
if [ ! -z "$INGRESS_IP" ]; then
    echo "Ingress Controller IP: $INGRESS_IP"
    echo ""
    
    for host in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].spec.rules[*].host}'); do
        echo "Testing $host -> $INGRESS_IP:"
        curl -H "Host: $host" -s -w "HTTP Code: %{http_code}\nResponse Time: %{time_total}s\n" \
             http://$INGRESS_IP/ 2>/dev/null || echo "Connectivity test failed for $host"
        echo ""
    done
else
    echo "⚠️  No external IP found for Ingress Controller"
fi

# 7. Performance and metrics
echo "📈 7. Performance Metrics"
echo "Service request counts:"
for svc in $(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "$svc: $(kubectl get endpoints $svc -n $NAMESPACE -o jsonpath='{.subsets[*].addresses[*].ip}' | wc -w) endpoints"
done
echo ""

# 8. Configuration validation
echo "📋 8. Configuration Validation"
echo "Ingress annotations:"
for ingress in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Ingress $ingress annotations:"
    kubectl get ingress $ingress -n $NAMESPACE -o jsonpath='{.metadata.annotations}' | jq '.' 2>/dev/null || echo "No annotations found"
    echo ""
done

echo "✅ Diagnostic completed. Review output above for any issues."