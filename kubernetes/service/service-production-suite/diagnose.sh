#!/bin/bash
# 风险等级：🟡 中风险
# 说明：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
# 生产安全提示：
#   - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
#   - 注意检查依赖版本、端口占用和目标资源配置。
#   - 生产环境执行前请经过变更评审和备份确认。

# Service Diagnostic and Troubleshooting Script

NAMESPACE="service-prod"

echo "🔧 Kubernetes Service Diagnostic Tool"
echo "====================================="

# Service status overview
echo "📋 Service Status Overview:"
kubectl get services -n $NAMESPACE -o wide

echo ""
echo "📊 Detailed Service Information:"
for svc in $(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "--- Service: $svc ---"
    kubectl describe service $svc -n $NAMESPACE
    echo ""
done

# Endpoint verification
echo "🔗 Endpoint Verification:"
kubectl get endpoints -n $NAMESPACE

echo ""
echo "🔍 DNS Resolution Tests:"
for svc in $(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Testing DNS for $svc.$NAMESPACE.svc.cluster.local:"
    kubectl run dns-test-$svc --image=busybox:1.28 --rm -it -n $NAMESPACE -- nslookup $svc.$NAMESPACE.svc.cluster.local || echo "DNS resolution failed"
    echo ""
done

# Network connectivity tests
echo "🌐 Network Connectivity Tests:"
APP_POD=$(kubectl get pods -n $NAMESPACE -l app=myapp -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ ! -z "$APP_POD" ]; then
    echo "Testing service connectivity from pod $APP_POD:"
    kubectl exec -it $APP_POD -n $NAMESPACE -- wget -qO- --timeout=10 http://app-clusterip.$NAMESPACE.svc.cluster.local || echo "Service connectivity test failed"
    echo ""
    
    # Port connectivity test
    echo "Testing port connectivity:"
    kubectl exec -it $APP_POD -n $NAMESPACE -- nc -zv app-clusterip.$NAMESPACE.svc.cluster.local 80 2>&1 || echo "Port 80 connectivity test failed"
fi

# Health check verification
echo ""
echo "🩺 Health Check Verification:"
for svc in $(kubectl get services -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
    echo "Checking endpoints for service $svc:"
    kubectl get endpoints $svc -n $NAMESPACE -o jsonpath='{.subsets[*].addresses[*].ip}' | tr ' ' '\n' | while read ip; do
        if [ ! -z "$ip" ]; then
            echo "  Endpoint IP: $ip"
            # Add specific health check logic here if needed
        fi
    done
    echo ""
done

# Network policy check
echo "🛡️ Network Policy Status:"
kubectl get networkpolicies -n $NAMESPACE 2>/dev/null || echo "No network policies found"

# Resource usage
echo ""
echo "📈 Resource Usage:"
kubectl top pods -n $NAMESPACE 2>/dev/null || echo "Metrics server not available"

echo ""
echo "✅ Diagnostic completed. Review the output above for any issues."
