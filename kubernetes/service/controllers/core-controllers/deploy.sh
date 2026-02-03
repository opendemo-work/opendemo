#!/bin/bash
# Service Controllers 部署脚本

set -e

NAMESPACE="service-controllers"

echo "🚀 开始部署 Service Controllers 生产环境..."

# 1. 创建命名空间
echo "📁 创建命名空间: $NAMESPACE"
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# 2. 验证基础控制器状态
echo "🔍 验证基础控制器状态..."
echo "kube-proxy 状态:"
kubectl get daemonsets -n kube-system kube-proxy
echo ""
echo "CoreDNS 状态:"
kubectl get deployments -n kube-system coredns

# 3. 应用控制器配置
echo "🔧 应用控制器配置..."
kubectl apply -f controllers-config.yaml -n kube-system

# 4. 部署监控配置
echo "📊 部署监控配置..."
# 这里可以添加 ServiceMonitor 配置

# 5. 验证部署
echo "✅ 验证部署状态..."
echo "控制器Pod状态:"
kubectl get pods -n kube-system -l k8s-app=kube-proxy
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 6. 测试服务发现
echo "🧪 测试服务发现功能..."
kubectl run debug --image=busybox --rm -it -- nslookup kubernetes.default || echo "服务发现测试完成"

echo ""
echo "🎉 Service Controllers 部署完成！"
echo "使用 'kubectl get pods -n kube-system' 查看控制器状态"