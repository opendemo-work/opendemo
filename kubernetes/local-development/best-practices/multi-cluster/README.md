# 🌐 Kubernetes 多集群管理最佳实践

> 本地开发环境中的多集群管理策略与最佳实践指南

## 🎯 场景概述

在本地开发环境中，有时需要同时管理多个Kubernetes集群，例如：
- 开发环境集群
- 测试环境集群  
- 演示环境集群
- 学习研究集群

### 📋 适用场景
- **开发测试分离**：将开发和测试环境分开
- **多项目管理**：同时处理多个项目
- **版本验证**：测试不同Kubernetes版本
- **学习研究**：对比不同部署方案

## 🛠️ 集群命名和组织策略

### 1. 命名规范

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 推荐的集群命名规范
# 格式：{项目}-{环境}-{标识}
# 示例：
kind create cluster --name dev-project-a
kind create cluster --name test-project-a  
kind create cluster --name demo-project-b
minikube start --profile=dev-project-c

# 更复杂的命名（包含版本信息）
kind create cluster --name dev-project-a-k8s128
kind create cluster --name test-project-a-k8s127
```

### 2. 上下文管理

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 查看所有kubectl上下文
kubectl config get-contexts

# 使用别名管理上下文
alias kctx='kubectl config get-contexts'
alias kuse='kubectl config use-context'

# 创建上下文切换函数
switch_dev_cluster() {
    kubectl config use-context kind-dev-project-a
    echo "切换到开发集群: $(kubectl config current-context)"
}

switch_test_cluster() {
    kubectl config use-context kind-test-project-a
    echo "切换到测试集群: $(kubectl config current-context)"
}

# 自动提示当前集群
export PS1='[$(kubectl config current-context 2>/dev/null | cut -d '\'' '\'' -f 1)] \w $ '
```

### 3. 配置管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 为不同集群创建不同的配置文件
# ~/.kube/config-dev
# ~/.kube/config-test
# ~/.kube/config-prod

# 使用环境变量切换配置
export KUBECONFIG=~/.kube/config-dev
kubectl config get-contexts

# 或者合并多个配置文件
export KUBECONFIG=~/.kube/config:~/.kube/config-dev:~/.kube/config-test
```

## 🚀 不同工具的多集群管理

### 1. minikube 多集群管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 创建多个minikube集群
minikube start --profile=dev-cluster --memory=4096 --cpus=2
minikube start --profile=test-cluster --memory=2048 --cpus=1
minikube start --profile=learn-cluster --kubernetes-version=v1.28.0

# 列出所有集群
minikube profile list

# 停止特定集群
minikube stop --profile=dev-cluster

# 删除特定集群
minikube delete --profile=test-cluster

# 快速切换集群
alias mkdev='minikube profile dev-cluster && kubectl config use-context minikube'
alias mktest='minikube profile test-cluster && kubectl config use-context minikube'
```

### 2. kind 多集群管理

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 创建命名的kind集群
kind create cluster --name dev-cluster
kind create cluster --name test-cluster --config=test-config.yaml
kind create cluster --name demo-cluster --image=kindest/node:v1.27.3

# 列出所有集群
kind get clusters

# 为特定集群设置kubectl上下文
kubectl config use-context kind-dev-cluster
kubectl config use-context kind-test-cluster

# 删除特定集群
kind delete cluster --name test-cluster

# 快速集群切换脚本
switch_kind_cluster() {
    local cluster_name=$1
    if kind get clusters | grep -q $cluster_name; then
        kubectl config use-context kind-$cluster_name
        echo "已切换到集群: kind-$cluster_name"
        kubectl cluster-info
    else
        echo "集群 kind-$cluster_name 不存在"
    fi
}
```

### 3. k3s 多集群管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用不同的配置文件运行多个k3s实例
# 注意：k3s在单机上运行多实例需要不同的端口和配置

# 创建不同配置的k3s集群
sudo k3s server --data-dir /var/lib/rancher/k3s/dev --https-listen-port 6444 --kube-apiserver-arg=advertise-address=127.0.0.1 --kube-apiserver-arg=bind-address=127.0.0.1 &

sudo k3s server --data-dir /var/lib/rancher/k3s/test --https-listen-port 6445 --kube-apiserver-arg=advertise-address=127.0.0.2 --kube-apiserver-arg=bind-address=127.0.0.2 &

# 为每个实例创建对应的kubeconfig
sudo cp /var/lib/rancher/k3s/dev/server/cred/admin.kubeconfig ~/.kube/config-dev
sudo cp /var/lib/rancher/k3s/test/server/cred/admin.kubeconfig ~/.kube/config-test
```

## 🔧 资源管理最佳实践

### 1. 资源隔离

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 使用命名空间进行资源隔离
kubectl create namespace development
kubectl create namespace testing
kubectl create namespace staging

# 为不同环境设置资源配额
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: development
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 4Gi
    limits.cpu: "4"
    limits.memory: 8Gi
    persistentvolumeclaims: "10"
    services.loadbalancers: "2"
EOF

# 设置LimitRange限制默认资源请求
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limit-range
  namespace: development
spec:
  limits:
  - default:
      cpu: 200m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 256Mi
    type: Container
EOF
```

### 2. 资源监控

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 监控多集群资源使用
monitor_clusters() {
    echo "=== 集群资源使用情况 ==="
    for context in $(kubectl config get-contexts -o name); do
        echo "--- $context ---"
        kubectl config use-context $context
        kubectl top nodes 2>/dev/null || echo "Metrics server not available in $context"
        echo ""
    done
}

# 创建资源使用报告
generate_cluster_report() {
    local report_file="cluster-report-$(date +%Y%m%d-%H%M%S).txt"
    echo "Kubernetes集群资源报告 - $(date)" > $report_file
    echo "" >> $report_file
    
    for context in $(kubectl config get-contexts -o name); do
        echo "=== 集群: $context ===" >> $report_file
        kubectl config use-context $context
        
        echo "节点信息:" >> $report_file
        kubectl get nodes -o wide >> $report_file
        echo "" >> $report_file
        
        echo "资源使用:" >> $report_file
        kubectl top nodes >> $report_file 2>/dev/null || echo "Metrics不可用" >> $report_file
        echo "" >> $report_file
        
        echo "Pod状态:" >> $report_file
        kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded >> $report_file
        echo "" >> $report_file
    done
    
    echo "报告已生成: $report_file"
}
```

## 🔄 环境切换脚本

### 1. 智能切换脚本

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
#!/bin/bash
# 多集群管理脚本 - cluster-manager.sh

CLUSTER_MANAGER_VERSION="1.0.0"

show_help() {
    echo "Kubernetes多集群管理工具 $CLUSTER_MANAGER_VERSION"
    echo "用法: $0 [command] [options]"
    echo ""
    echo "命令:"
    echo "  list          - 列出所有集群"
    echo "  switch NAME   - 切换到指定集群"
    echo "  info          - 显示当前集群信息"
    echo "  status        - 显示所有集群状态"
    echo "  cleanup       - 清理不活跃的资源"
    echo "  report        - 生成集群使用报告"
    echo ""
    echo "示例:"
    echo "  $0 list"
    echo "  $0 switch dev-cluster"
    echo "  $0 info"
}

list_clusters() {
    echo "=== 可用的Kubernetes集群 ==="
    kubectl config get-contexts
}

switch_cluster() {
    local target_cluster=$1
    if kubectl config get-contexts $target_cluster &>/dev/null; then
        kubectl config use-context $target_cluster
        echo "已切换到集群: $target_cluster"
        kubectl cluster-info
    else
        echo "错误: 集群 '$target_cluster' 不存在"
        echo "可用集群:"
        kubectl config get-contexts -o name
    fi
}

show_current_info() {
    local current_ctx=$(kubectl config current-context)
    echo "当前集群上下文: $current_ctx"
    echo "集群信息:"
    kubectl cluster-info
    echo "节点状态:"
    kubectl get nodes
    echo "命名空间:"
    kubectl get namespaces
}

show_all_status() {
    echo "=== 所有集群状态 ==="
    for ctx in $(kubectl config get-contexts -o name); do
        echo "--- $ctx ---"
        kubectl config use-context $ctx &>/dev/null
        if kubectl cluster-info &>/dev/null; then
            echo "状态: 运行中"
            node_count=$(kubectl get nodes --no-headers 2>/dev/null | wc -l)
            echo "节点数: $node_count"
            pod_count=$(kubectl get pods --all-namespaces --no-headers 2>/dev/null | wc -l)
            echo "Pod数: $pod_count"
        else
            echo "状态: 不可用"
        fi
        echo ""
    done
}

cleanup_resources() {
    echo "清理不活跃资源..."
    
    # 清理失败的Pod
    kubectl delete pods --field-selector=status.phase=Failed --all-namespaces
    
    # 清理已完成的Job
    kubectl delete jobs --field-selector=status.successful=1 --all-namespaces
    
    # 清理已完成的CronJob
    for ctx in $(kubectl config get-contexts -o name); do
        kubectl config use-context $ctx &>/dev/null
        if kubectl cluster-info &>/dev/null; then
            echo "清理集群: $ctx"
            kubectl delete jobs --field-selector=status.succeeded=1 --all-namespaces
        fi
    done
    
    echo "清理完成"
}

generate_report() {
    local report_file="/tmp/cluster-report-$(date +%Y%m%d-%H%M%S).txt"
    echo "生成集群报告到: $report_file"
    
    echo "Kubernetes多集群报告 - $(date)" > $report_file
    echo "========================" >> $report_file
    echo "" >> $report_file
    
    for ctx in $(kubectl config get-contexts -o name); do
        kubectl config use-context $ctx &>/dev/null
        if kubectl cluster-info &>/dev/null; then
            echo "集群: $ctx" >> $report_file
            echo "-------" >> $report_file
            echo "节点信息:" >> $report_file
            kubectl get nodes -o wide >> $report_file
            echo "" >> $report_file
            
            echo "资源使用:" >> $report_file
            kubectl top nodes >> $report_file 2>/dev/null || echo "Metrics server unavailable" >> $report_file
            echo "" >> $report_file
        else
            echo "集群: $ctx (不可用)" >> $report_file
        fi
        echo "" >> $report_file
    done
    
    echo "报告生成完成: $report_file"
}

# 主程序逻辑
case "${1:-help}" in
    "list")
        list_clusters
        ;;
    "switch")
        if [ -z "$2" ]; then
            echo "错误: 请指定要切换的集群名称"
            exit 1
        fi
        switch_cluster "$2"
        ;;
    "info")
        show_current_info
        ;;
    "status")
        show_all_status
        ;;
    "cleanup")
        cleanup_resources
        ;;
    "report")
        generate_report
        ;;
    "help"|*)
        show_help
        ;;
esac
```

### 2. 环境变量管理

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 集群环境变量管理
# ~/.bashrc 或 ~/.zshrc 中添加

# 集群别名
alias kdev='kubectl config use-context kind-dev-cluster'
alias ktest='kubectl config use-context kind-test-cluster'
alias kdemo='kubectl config use-context kind-demo-cluster'

# 集群状态检查函数
check_cluster_status() {
    local cluster_name=${1:-$(kubectl config current-context)}
    echo "检查集群: $cluster_name"
    kubectl config use-context $cluster_name
    kubectl cluster-info
    kubectl get nodes
}

# 集群快速部署函数
deploy_to_cluster() {
    local cluster_name=$1
    local manifest_file=$2
    
    if [ -z "$cluster_name" ] || [ -z "$manifest_file" ]; then
        echo "用法: deploy_to_cluster <cluster-name> <manifest-file>"
        return 1
    fi
    
    kubectl config use-context $cluster_name
    kubectl apply -f $manifest_file
}
```

## 📊 监控和维护

### 1. 集群健康检查

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 定期健康检查脚本
health_check() {
    echo "=== 集群健康检查报告 ==="
    for ctx in $(kubectl config get-contexts -o name); do
        echo "检查集群: $ctx"
        kubectl config use-context $ctx &>/dev/null
        
        if ! kubectl cluster-info &>/dev/null; then
            echo "  ❌ 集群不可达"
            continue
        fi
        
        # 检查节点状态
        local node_ready=$(kubectl get nodes --no-headers 2>/dev/null | grep -c " Ready")
        local node_total=$(kubectl get nodes --no-headers 2>/dev/null | wc -l)
        echo "  ✅ 节点状态: $node_ready/$node_total Ready"
        
        # 检查系统组件
        local system_pods=$(kubectl get pods -n kube-system --no-headers 2>/dev/null | wc -l)
        local running_pods=$(kubectl get pods -n kube-system --no-headers 2>/dev/null | grep -c " Running")
        echo "  ✅ 系统组件: $running_pods/$system_pods Running"
        
        # 检查API服务器延迟
        local start_time=$(date +%s%N)
        kubectl get nodes &>/dev/null
        local end_time=$(date +%s%N)
        local latency=$(( ($end_time - $start_time) / 1000000 ))
        echo "  ⏱️  API延迟: ${latency}ms"
        
        echo ""
    done
}
```

### 2. 资源优化

🟢 低风险：只读查询或无害信息展示，不会修改系统状态。
```bash
# 集群资源优化建议
optimize_cluster_resources() {
    echo "=== 集群资源优化建议 ==="
    for ctx in $(kubectl config get-contexts -o name); do
        echo "分析集群: $ctx"
        kubectl config use-context $ctx &>/dev/null
        
        if ! kubectl cluster-info &>/dev/null; then
            continue
        fi
        
        # 检查未使用的命名空间
        echo "  未使用的命名空间:"
        kubectl get namespaces --no-headers | while read ns status rest; do
            pod_count=$(kubectl get pods -n $ns --no-headers 2>/dev/null | wc -l)
            if [ "$pod_count" -eq 0 ] && [ "$ns" != "kube-system" ] && [ "$ns" != "default" ] && [ "$ns" != "kube-public" ]; then
                echo "    - $ns (空命名空间)"
            fi
        done
        
        # 检查资源请求未设置的Pod
        echo "  未设置资源请求的Pod:"
        kubectl get pods --all-namespaces --no-headers | while read namespace name rest; do
            resource_requests=$(kubectl get pod $name -n $namespace -o jsonpath='{.spec.containers[0].resources.requests}' 2>/dev/null)
            if [ -z "$resource_requests" ] || [ "$resource_requests" = "{}" ]; then
                echo "    - $namespace/$name"
            fi
        done
        
        echo ""
    done
}
```

## 🚀 高级技巧

### 1. 集群同步

🔴 高风险：可能造成数据丢失、服务中断、权限提升或不可逆破坏。
> ⚠️ 生产安全提示：
> - 会删除/格式化/停止关键资源，生产环境慎用。
> - 执行前请确认目标范围，建议在隔离测试环境验证。
> - 涉及数据操作前请备份，涉及服务操作前请通知相关人员。
```bash
# 在多个集群间同步配置
sync_configs_between_clusters() {
    local source_cluster=$1
    local target_clusters=("${@:2}")
    
    if [ -z "$source_cluster" ] || [ ${#target_clusters[@]} -eq 0 ]; then
        echo "用法: sync_configs_between_clusters <source-cluster> <target-cluster1> [target-cluster2...]"
        return 1
    fi
    
    # 从源集群导出现有配置
    kubectl config use-context $source_cluster
    local temp_dir="/tmp/cluster-sync-$(date +%s)"
    mkdir -p $temp_dir
    
    # 导出命名空间和配置
    kubectl get namespaces -o yaml > $temp_dir/namespaces.yaml
    kubectl get configmaps --all-namespaces -o yaml > $temp_dir/configmaps.yaml
    kubectl get secrets --all-namespaces -o yaml > $temp_dir/secrets.yaml
    
    # 同步到目标集群
    for target in "${target_clusters[@]}"; do
        echo "同步到集群: $target"
        kubectl config use-context $target
        kubectl apply -f $temp_dir/namespaces.yaml
        kubectl apply -f $temp_dir/configmaps.yaml
        kubectl apply -f $temp_dir/secrets.yaml
    done
    
    rm -rf $temp_dir
}
```

### 2. 集群备份

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 集群配置备份
backup_cluster_config() {
    local cluster_name=${1:-$(kubectl config current-context)}
    local backup_dir=${2:-"/tmp/backup-$cluster_name-$(date +%Y%m%d)"}
    
    mkdir -p $backup_dir
    
    echo "备份集群 $cluster_name 到 $backup_dir"
    
    # 备份命名空间
    kubectl get namespaces -o yaml > $backup_dir/namespaces.yaml
    
    # 备份所有资源（除了特定类型）
    for resource in deployments services configmaps secrets daemonsets statefulsets; do
        kubectl get $resource --all-namespaces -o yaml > $backup_dir/${resource}.yaml 2>/dev/null || echo "跳过 $resource (不存在)"
    done
    
    # 备份CRD
    kubectl get crd -o yaml > $backup_dir/crd.yaml 2>/dev/null || echo "跳过 CRD (不存在)"
    
    # 生成备份摘要
    echo "备份摘要 - $(date)" > $backup_dir/README.md
    echo "集群: $cluster_name" >> $backup_dir/README.md
    echo "备份时间: $(date)" >> $backup_dir/README.md
    echo "文件数量: $(ls $backup_dir | wc -l)" >> $backup_dir/README.md
    
    echo "备份完成: $backup_dir"
}
```

## 🎯 最佳实践总结

### 管理原则
1. **命名一致性**：使用统一的命名规范
2. **资源隔离**：通过命名空间和配额进行隔离
3. **监控可见**：定期检查集群状态和资源使用
4. **自动化运维**：使用脚本简化重复操作
5. **安全访问**：确保不同环境的访问权限分离

### 性能考虑
- 合理分配系统资源给各个集群
- 定期清理不再使用的资源
- 使用轻量级的集群方案（如k3s）用于测试环境
- 监控系统整体资源使用情况

### 故障排除
- 建立快速切换上下文的机制
- 准备环境检查和修复脚本
- 定期备份重要配置
- 维护环境文档和操作手册

---

> **💡 提示**: 多集群管理需要良好的组织和自动化工具支持。建议根据实际需求选择合适的管理策略和工具。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/apply.sh
```

### 检查状态

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
./scripts/check.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 Kubernetes 核心概念。

### 2. 适用场景

- 场景 1：开发与测试
- 场景 2：生产环境参考
- 场景 3：故障排查

## 💻 代码示例

### 基本命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
