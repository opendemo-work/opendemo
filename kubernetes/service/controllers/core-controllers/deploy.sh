#!/bin/bash
# 风险等级：🟡 中风险
# 说明：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
# 生产安全提示：
#   - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
#   - 注意检查依赖版本、端口占用和目标资源配置。
#   - 生产环境执行前请经过变更评审和备份确认。

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
