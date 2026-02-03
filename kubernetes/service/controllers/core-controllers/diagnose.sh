#!/bin/bash
# Service Controllers 诊断脚本

echo "🔧 Service Controllers 诊断工具"
echo "=================================="

# 1. 基础控制器状态
echo "📋 1. 基础控制器状态"
echo "kube-proxy DaemonSet:"
kubectl get daemonsets -n kube-system kube-proxy -o wide
echo ""
echo "CoreDNS Deployment:"
kubectl get deployments -n kube-system coredns -o wide
echo ""
echo "控制器Pod状态:"
kubectl get pods -n kube-system -l k8s-app=kube-proxy
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 2. 配置验证
echo ""
echo "⚙️ 2. 配置验证"
echo "kube-proxy 配置:"
kubectl get configmap kube-proxy -n kube-system -o yaml | head -20
echo ""
echo "CoreDNS 配置:"
kubectl get configmap coredns -n kube-system -o yaml | head -20

# 3. 服务发现测试
echo ""
echo "🔍 3. 服务发现测试"
echo "测试集群内部服务发现:"
kubectl run debug --image=busybox --rm -it -- nslookup kubernetes.default 2>/dev/null || echo "服务发现测试完成"
echo ""
echo "测试自定义服务发现:"
for svc in $(kubectl get services --all-namespaces -o jsonpath='{.items[*].metadata.name}'); do
    ns=$(kubectl get service $svc --all-namespaces -o jsonpath='{.metadata.namespace}')
    echo "测试 $svc.$ns.svc.cluster.local"
    kubectl run debug-$svc --image=busybox --rm -it -- nslookup $svc.$ns.svc.cluster.local 2>/dev/null || echo "  无法解析"
done

# 4. 性能指标
echo ""
echo "📈 4. 性能指标"
echo "控制器资源使用:"
kubectl top pods -n kube-system -l k8s-app=kube-proxy 2>/dev/null || echo "Metrics server不可用"
kubectl top pods -n kube-system -l k8s-app=kube-dns 2>/dev/null || echo "Metrics server不可用"

# 5. 网络策略检查
echo ""
echo "🛡️ 5. 网络策略检查"
kubectl get networkpolicies --all-namespaces 2>/dev/null || echo "无网络策略配置"

echo ""
echo "✅ 诊断完成，请根据以上输出检查控制器状态"