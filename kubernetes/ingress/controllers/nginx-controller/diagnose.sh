#!/bin/bash
# NGINX Ingress Controller 诊断脚本

NAMESPACE="ingress-system"

echo "🔧 NGINX Ingress Controller 诊断工具"
echo "======================================"

# 1. 基础状态检查
echo "📋 1. 基础状态检查"
echo "命名空间状态:"
kubectl get namespace $NAMESPACE 2>/dev/null || echo "命名空间不存在"
echo ""
echo "控制器Pod状态:"
kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=ingress-nginx -o wide
echo ""
echo "服务状态:"
kubectl get svc -n $NAMESPACE -o wide

# 2. 配置验证
echo ""
echo "⚙️ 2. 配置验证"
echo "ConfigMap配置:"
kubectl get configmap nginx-configuration -n $NAMESPACE -o yaml | head -20
echo ""
echo "IngressClasses:"
kubectl get ingressclasses -o wide

# 3. 日志检查
echo ""
echo "📝 3. 控制器日志检查"
echo "最近50行日志:"
kubectl logs -n $NAMESPACE -l app.kubernetes.io/name=ingress-nginx --tail=50 2>/dev/null || echo "无法获取日志"

# 4. 性能指标
echo ""
echo "📊 4. 性能指标检查"
echo "控制器资源使用:"
kubectl top pods -n $NAMESPACE -l app.kubernetes.io/name=ingress-nginx 2>/dev/null || echo "Metrics server不可用"

# 5. 网络连通性测试
echo ""
echo "🌐 5. 网络连通性测试"
SVC_IP=$(kubectl get svc ingress-nginx-controller -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
if [ ! -z "$SVC_IP" ]; then
    echo "测试外部访问 ($SVC_IP):"
    curl -s -w "HTTP状态: %{http_code}\n响应时间: %{time_total}s\n" http://$SVC_IP/healthz 2>/dev/null || echo "无法访问外部IP"
else
    echo "⚠️ 未找到外部IP地址"
fi

# 6. 配置文件检查
echo ""
echo "📄 6. NGINX配置检查"
kubectl exec -n $NAMESPACE deploy/ingress-nginx-controller -- cat /etc/nginx/nginx.conf 2>/dev/null | head -30 || echo "无法获取配置文件"

# 7. 版本信息
echo ""
echo "🏷️ 7. 版本信息"
kubectl exec -n $NAMESPACE deploy/ingress-nginx-controller -- /nginx-ingress-controller --version 2>/dev/null || echo "无法获取版本信息"

echo ""
echo "✅ 诊断完成，请根据以上输出检查问题"