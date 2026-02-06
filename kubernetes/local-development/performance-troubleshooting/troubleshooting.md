# 🛠️ Kubernetes本地环境故障排除指南

> 系统性的故障诊断和解决方案，帮助快速定位和解决常见问题

## 🎯 故障诊断流程

### 1. 问题分类和优先级

```
高优先级问题（立即处理）：
- 集群无法启动
- kubectl无法连接
- 核心组件异常

中优先级问题（尽快处理）：
- Pod调度失败
- 服务访问异常
- 资源不足

低优先级问题（可计划处理）：
- 性能优化
- 配置调整
- 功能增强
```

### 2. 系统性诊断方法

```bash
# 1. 环境检查清单
check_environment() {
    echo "=== 环境检查 ==="
    echo "macOS版本: $(sw_vers -productVersion)"
    echo "CPU核心数: $(sysctl -n hw.ncpu)"
    echo "内存大小: $(sysctl -n hw.memsize / 1024 / 1024 / 1024)GB"
    echo "Docker状态: $(docker info &>/dev/null && echo '运行中' || echo '未运行')"
    echo "kubectl版本: $(kubectl version --client 2>/dev/null | head -1)"
}

# 2. 集群状态检查
check_cluster_status() {
    echo "=== 集群状态检查 ==="
    kubectl cluster-info 2>/dev/null || echo "❌ 无法连接到集群"
    kubectl get nodes 2>/dev/null || echo "❌ 无法获取节点信息"
    kubectl get componentstatuses 2>/dev/null || echo "❌ 组件状态异常"
}

# 3. 资源使用检查
check_resources() {
    echo "=== 资源使用检查 ==="
    echo "系统内存使用:"
    top -l 1 -n 0 | grep PhysMem
    echo "Docker资源使用:"
    docker info 2>/dev/null | grep -E "(CPUs|Memory)"
    echo "Kubernetes节点资源:"
    kubectl top nodes 2>/dev/null || echo "❌ 无法获取资源信息"
}
```

## 🔧 常见问题分类解决

### 1. 启动和初始化问题

#### 集群启动失败

**问题现象**：
- minikube start 卡住或失败
- kind create cluster 超时
- k3s server 启动异常

**诊断步骤**：
```bash
# 1. 检查系统资源
./diagnostic.sh system-check

# 2. 检查端口占用
./diagnostic.sh port-check

# 3. 查看详细日志
./diagnostic.sh verbose-logs
```

**解决方案**：
```bash
# 通用解决步骤：

# 1. 清理环境
cleanup_environment() {
    echo "清理环境..."
    # 停止所有相关进程
    pkill -f "minikube|kind|k3s"
    
    # 清理Docker资源
    docker system prune -af
    
    # 清理Kubernetes配置
    rm -rf ~/.kube/config
    rm -rf ~/.minikube
}

# 2. 重新初始化
reinitialize_cluster() {
    local tool=$1
    case $tool in
        "minikube")
            minikube delete --all
            minikube start --driver=docker --memory=6144 --cpus=4
            ;;
        "kind")
            kind delete clusters --all
            kind create cluster --wait 5m
            ;;
        "k3s")
            sudo /usr/local/bin/k3s-uninstall.sh
            curl -sfL https://get.k3s.io | sh -
            ;;
    esac
}
```

#### kubectl连接问题

**问题现象**：
- kubectl命令超时
- "Unable to connect to the server"错误
- 上下文配置错误

**诊断命令**：
```bash
# 1. 检查kubectl配置
kubectl config view
kubectl config current-context

# 2. 测试API Server连接
kubectl cluster-info
curl -k https://localhost:6443/livez

# 3. 检查证书有效性
kubectl config view --raw | grep certificate-authority-data | wc -c
```

**解决方案**：
```bash
# 重置kubectl配置
reset_kubectl_config() {
    # 备份当前配置
    cp ~/.kube/config ~/.kube/config.backup.$(date +%s)
    
    # 根据不同工具重置配置
    case $(kubectl config current-context 2>/dev/null) in
        *minikube*)
            minikube update-context
            ;;
        *kind*)
            kind export kubeconfig --name $(kind get clusters | head -1)
            ;;
        *k3s*)
            sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
            chmod 600 ~/.kube/config
            ;;
    esac
    
    # 验证连接
    kubectl cluster-info
}
```

### 2. 资源调度问题

#### Pod Pending状态

**问题现象**：
- Pod长时间处于Pending状态
- 无法调度到节点
- 资源不足错误

**诊断命令**：
```bash
# 1. 查看Pod详细信息
kubectl describe pod <pod-name>

# 2. 检查节点资源
kubectl describe nodes
kubectl top nodes

# 3. 查看调度器日志
kubectl logs -n kube-system -l component=kube-scheduler
```

**解决方案**：
```bash
# Pod调度问题解决脚本
solve_pod_scheduling() {
    local pod_name=$1
    
    # 获取Pod调度失败原因
    local reason=$(kubectl describe pod $pod_name | grep -A 5 "Events:" | tail -5)
    
    case $reason in
        *"Insufficient memory"*)
            echo "内存不足，调整资源请求"
            kubectl patch deployment $pod_name -p '{"spec":{"template":{"spec":{"containers":[{"name":"'"$pod_name"'","resources":{"requests":{"memory":"64Mi"}}}]}}}}'
            ;;
        *"Insufficient cpu"*)
            echo "CPU不足，调整资源请求"
            kubectl patch deployment $pod_name -p '{"spec":{"template":{"spec":{"containers":[{"name":"'"$pod_name"'","resources":{"requests":{"cpu":"50m"}}}]}}}}'
            ;;
        *"NodeAffinity"*)
            echo "节点亲和性配置问题"
            kubectl patch deployment $pod_name --type=json -p='[{"op": "remove", "path": "/spec/template/spec/affinity"}]'
            ;;
        *)
            echo "其他调度问题，尝试重新调度"
            kubectl delete pod $pod_name
            ;;
    esac
}
```

#### 资源配额超限

**问题现象**：
- "exceeded quota"错误
- "Forbidden"权限错误
- 资源创建被拒绝

**诊断命令**：
```bash
# 1. 检查资源配额
kubectl get resourcequota --all-namespaces
kubectl describe resourcequota <quota-name> -n <namespace>

# 2. 检查限制范围
kubectl get limitrange --all-namespaces
kubectl describe limitrange <limitrange-name> -n <namespace>

# 3. 查看当前资源使用
kubectl describe namespace <namespace>
```

**解决方案**：
```bash
# 资源配额调整
adjust_resource_quota() {
    local namespace=$1
    local cpu_limit=$2
    local memory_limit=$3
    
    # 创建或更新资源配额
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: $namespace
spec:
  hard:
    requests.cpu: "$cpu_limit"
    requests.memory: "$memory_limit"
    limits.cpu: "$((cpu_limit * 2))"
    limits.memory: "$((memory_limit * 2))"
    persistentvolumeclaims: "10"
    services.loadbalancers: "2"
EOF
}
```

### 3. 网络连接问题

#### 服务访问失败

**问题现象**：
- Service无法访问
- ClusterIP连接超时
- NodePort端口不通

**诊断命令**：
```bash
# 1. 检查服务配置
kubectl get services
kubectl describe service <service-name>

# 2. 检查端点
kubectl get endpoints <service-name>

# 3. 网络连通性测试
kubectl run debug-pod --image=busybox --rm -it -- sh
# 在容器内测试：ping <service-cluster-ip>
```

**解决方案**：
```bash
# 服务访问问题解决
solve_service_access() {
    local service_name=$1
    
    # 检查服务类型和端口
    local service_type=$(kubectl get service $service_name -o jsonpath='{.spec.type}')
    local cluster_ip=$(kubectl get service $service_name -o jsonpath='{.spec.clusterIP}')
    local port=$(kubectl get service $service_name -o jsonpath='{.spec.ports[0].port}')
    
    case $service_type in
        "ClusterIP")
            echo "测试ClusterIP访问: curl http://$cluster_ip:$port"
            ;;
        "NodePort")
            local node_port=$(kubectl get service $service_name -o jsonpath='{.spec.ports[0].nodePort}')
            echo "测试NodePort访问: curl http://localhost:$node_port"
            ;;
        "LoadBalancer")
            echo "LoadBalancer服务需要外部负载均衡器支持"
            ;;
    esac
    
    # 检查网络策略
    kubectl get networkpolicies -n $(kubectl get service $service_name -o jsonpath='{.metadata.namespace}')
}
```

#### DNS解析失败

**问题现象**：
- Pod内无法解析域名
- "Could not resolve host"错误
- CoreDNS Pod异常

**诊断命令**：
```bash
# 1. 检查CoreDNS状态
kubectl get pods -n kube-system | grep coredns
kubectl logs -n kube-system -l k8s-app=kube-dns

# 2. 测试DNS解析
kubectl run dns-test --image=busybox --rm -it -- sh
# nslookup kubernetes.default
# nslookup google.com

# 3. 检查DNS配置
kubectl get configmap coredns -n kube-system -o yaml
```

**解决方案**：
```bash
# DNS问题解决
solve_dns_issue() {
    # 1. 重启CoreDNS
    echo "重启CoreDNS..."
    kubectl rollout restart deployment coredns -n kube-system
    
    # 2. 检查配置
    echo "检查CoreDNS配置..."
    kubectl get configmap coredns -n kube-system -o yaml | grep -A 10 Corefile
    
    # 3. 测试解析
    echo "测试DNS解析..."
    kubectl run dns-test --image=busybox --rm -it -- sh -c "nslookup kubernetes.default"
    
    # 4. 如果问题持续，重建CoreDNS
    if [ $? -ne 0 ]; then
        echo "重建CoreDNS..."
        kubectl delete pod -n kube-system -l k8s-app=kube-dns
    fi
}
```

### 4. 存储相关问题

#### 持久卷挂载失败

**问题现象**：
- "MountVolume.SetUp failed"错误
- PVC处于Pending状态
- 存储类不可用

**诊断命令**：
```bash
# 1. 检查存储资源状态
kubectl get pv
kubectl get pvc
kubectl get storageclass

# 2. 查看详细错误信息
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name>

# 3. 检查节点存储
kubectl describe nodes
```

**解决方案**：
```bash
# 存储问题解决
solve_storage_issue() {
    local pvc_name=$1
    
    # 检查PVC状态
    local pvc_status=$(kubectl get pvc $pvc_name -o jsonpath='{.status.phase}')
    
    case $pvc_status in
        "Pending")
            echo "PVC处于Pending状态，检查存储类..."
            local storage_class=$(kubectl get pvc $pvc_name -o jsonpath='{.spec.storageClassName}')
            kubectl get storageclass $storage_class
            ;;
        "Bound")
            echo "PVC已绑定，检查Pod挂载..."
            local pod_name=$(kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' | head -1)
            kubectl describe pod $pod_name | grep -A 10 "Volumes:"
            ;;
        *)
            echo "PVC状态异常: $pvc_status"
            ;;
    esac
}
```

### 5. 镜像相关问题

#### 镜像拉取失败

**问题现象**：
- "ImagePullBackOff"状态
- "ErrImagePull"错误
- 镜像仓库连接超时

**诊断命令**：
```bash
# 1. 检查Pod事件
kubectl describe pod <pod-name> | grep -A 10 "Events:"

# 2. 测试镜像仓库连接
docker pull <image-name>
curl -v https://registry-1.docker.io/v2/

# 3. 检查镜像标签
docker images | grep <image-name>
```

**解决方案**：
```bash
# 镜像拉取问题解决
solve_image_pull() {
    local pod_name=$1
    
    # 获取镜像拉取错误详情
    local error_msg=$(kubectl describe pod $pod_name | grep -A 5 "Failed to pull image")
    
    case $error_msg in
        *"not found"*)
            echo "镜像不存在，检查镜像名称和标签"
            ;;
        *"unauthorized"*)
            echo "认证失败，配置镜像仓库凭证"
            kubectl create secret docker-registry regcred \
                --docker-server=<registry-server> \
                --docker-username=<username> \
                --docker-password=<password>
            ;;
        *"timeout"*)
            echo "连接超时，配置镜像加速器"
            # 配置Docker镜像加速器
            ;;
        *)
            echo "其他镜像问题，尝试重新拉取"
            kubectl delete pod $pod_name
            ;;
    esac
}
```

## 🛠️ 自动化诊断工具

### 1. 综合诊断脚本

```bash
#!/bin/bash
# Kubernetes本地环境综合诊断工具

DIAGNOSTIC_VERSION="1.0.0"
LOG_FILE="/tmp/k8s-diagnostic-$(date +%Y%m%d-%H%M%S).log"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

success() {
    echo -e "${GREEN}✓${NC} $1" | tee -a $LOG_FILE
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1" | tee -a $LOG_FILE
}

error() {
    echo -e "${RED}✗${NC} $1" | tee -a $LOG_FILE
}

# 系统环境检查
check_system_environment() {
    log "开始系统环境检查..."
    
    # macOS版本
    local macos_version=$(sw_vers -productVersion)
    log "macOS版本: $macos_version"
    
    # 硬件资源
    local cpu_cores=$(sysctl -n hw.ncpu)
    local memory_gb=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}')
    log "CPU核心数: $cpu_cores"
    log "内存大小: ${memory_gb}GB"
    
    # 资源充足性检查
    if [ $cpu_cores -lt 4 ]; then
        warning "CPU核心数较少，可能影响性能"
    fi
    
    if [ $memory_gb -lt 8 ]; then
        warning "内存较小，建议增加到8GB以上"
    fi
}

# Docker环境检查
check_docker_environment() {
    log "检查Docker环境..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker未安装"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        error "Docker服务未运行"
        return 1
    fi
    
    local docker_version=$(docker --version | awk '{print $3}' | sed 's/,//')
    log "Docker版本: $docker_version"
    
    # 资源分配检查
    local docker_memory=$(docker info | grep "Total Memory" | awk '{print $3}' | sed 's/GiB//')
    log "Docker分配内存: ${docker_memory}GB"
    
    if (( $(echo "$docker_memory < 4.0" | bc -l) )); then
        warning "Docker内存分配不足4GB"
    fi
    
    success "Docker环境正常"
}

# Kubernetes工具检查
check_k8s_tools() {
    log "检查Kubernetes工具..."
    
    local tools=("kubectl" "minikube" "kind")
    local missing_tools=()
    
    for tool in "${tools[@]}"; do
        if command -v $tool &> /dev/null; then
            local version=$($tool version --short 2>/dev/null | head -1)
            log "$tool: $version"
            success "$tool 已安装"
        else
            error "$tool 未安装"
            missing_tools+=($tool)
        fi
    done
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        warning "缺少工具: ${missing_tools[*]}"
        return 1
    fi
}

# 集群连接检查
check_cluster_connection() {
    log "检查Kubernetes集群连接..."
    
    if ! kubectl cluster-info &> /dev/null; then
        error "无法连接到Kubernetes集群"
        return 1
    fi
    
    local context=$(kubectl config current-context)
    log "当前上下文: $context"
    
    local nodes=$(kubectl get nodes --no-headers 2>/dev/null | wc -l)
    if [ $nodes -eq 0 ]; then
        error "没有可用的节点"
        return 1
    fi
    
    log "节点数量: $nodes"
    success "集群连接正常"
}

# 资源使用检查
check_resource_usage() {
    log "检查资源使用情况..."
    
    # 节点资源
    if kubectl top nodes &> /dev/null; then
        log "节点资源使用:"
        kubectl top nodes
    else
        warning "无法获取节点资源信息（metrics-server可能未安装）"
    fi
    
    # 系统Pod状态
    log "系统组件状态:"
    kubectl get pods -n kube-system -o wide
    
    # 检查异常Pod
    local failed_pods=$(kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded --no-headers 2>/dev/null | wc -l)
    if [ $failed_pods -gt 0 ]; then
        warning "发现 $failed_pods 个异常Pod"
        kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded
    fi
}

# 网络连通性检查
check_network_connectivity() {
    log "检查网络连通性..."
    
    # DNS解析测试
    if kubectl run dns-test --image=busybox --rm -it --restart=Never -- sh -c "nslookup kubernetes.default" &>/dev/null; then
        success "DNS解析正常"
    else
        error "DNS解析失败"
    fi
    
    # 外部网络测试
    if kubectl run network-test --image=busybox --rm -it --restart=Never -- sh -c "ping -c 3 8.8.8.8" &>/dev/null; then
        success "外部网络连接正常"
    else
        warning "外部网络连接可能有问题"
    fi
}

# 存储检查
check_storage() {
    log "检查存储配置..."
    
    # 存储类
    local storage_classes=$(kubectl get storageclass --no-headers 2>/dev/null | wc -l)
    log "存储类数量: $storage_classes"
    
    if [ $storage_classes -eq 0 ]; then
        warning "没有配置存储类"
    fi
    
    # 持久卷状态
    local pv_count=$(kubectl get pv --no-headers 2>/dev/null | wc -l)
    local pvc_count=$(kubectl get pvc --all-namespaces --no-headers 2>/dev/null | wc -l)
    log "持久卷数量: $pv_count"
    log "持久卷声明数量: $pvc_count"
}

# 运行完整诊断
run_full_diagnostic() {
    log "开始Kubernetes本地环境完整诊断 (版本: $DIAGNOSTIC_VERSION)"
    log "日志文件: $LOG_FILE"
    
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Kubernetes环境诊断报告${NC}"
    echo -e "${BLUE}================================${NC}"
    
    check_system_environment
    echo ""
    
    check_docker_environment
    echo ""
    
    check_k8s_tools
    echo ""
    
    check_cluster_connection
    echo ""
    
    check_resource_usage
    echo ""
    
    check_network_connectivity
    echo ""
    
    check_storage
    echo ""
    
    log "诊断完成"
    echo -e "${GREEN}诊断报告已保存到: $LOG_FILE${NC}"
}

# 快速检查
run_quick_check() {
    log "运行快速检查..."
    
    check_cluster_connection
    check_resource_usage
    
    log "快速检查完成"
}

# 根据参数执行不同检查
case "${1:-full}" in
    "full")
        run_full_diagnostic
        ;;
    "quick")
        run_quick_check
        ;;
    "system")
        check_system_environment
        check_docker_environment
        ;;
    "cluster")
        check_cluster_connection
        check_resource_usage
        ;;
    "network")
        check_network_connectivity
        ;;
    "storage")
        check_storage
        ;;
    *)
        echo "用法: $0 [full|quick|system|cluster|network|storage]"
        echo "  full    - 完整诊断（默认）"
        echo "  quick   - 快速检查"
        echo "  system  - 系统环境检查"
        echo "  cluster - 集群状态检查"
        echo "  network - 网络连通性检查"
        echo "  storage - 存储配置检查"
        ;;
esac
```

### 2. 问题修复脚本

```bash
#!/bin/bash
# Kubernetes常见问题自动修复工具

FIX_VERSION="1.0.0"

# 修复函数定义
fix_common_issues() {
    echo "开始自动修复常见问题..."
    
    # 1. 修复kubectl配置问题
    fix_kubectl_config() {
        echo "修复kubectl配置..."
        if ! kubectl cluster-info &>/dev/null; then
            echo "重新生成kubeconfig..."
            case $(kubectl config current-context 2>/dev/null) in
                *minikube*)
                    minikube update-context
                    ;;
                *kind*)
                    kind export kubeconfig
                    ;;
                *k3s*)
                    sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
                    chmod 600 ~/.kube/config
                    ;;
            esac
        fi
    }
    
    # 2. 清理失败的Pod
    cleanup_failed_pods() {
        echo "清理失败的Pod..."
        kubectl delete pods --field-selector=status.phase==Failed --all-namespaces
        kubectl delete pods --field-selector=status.phase==Unknown --all-namespaces
    }
    
    # 3. 重启核心组件
    restart_core_components() {
        echo "重启核心组件..."
        kubectl rollout restart deployment coredns -n kube-system
        if kubectl get deployment metrics-server -n kube-system &>/dev/null; then
            kubectl rollout restart deployment metrics-server -n kube-system
        fi
    }
    
    # 4. 清理Docker资源
    cleanup_docker_resources() {
        echo "清理Docker资源..."
        docker system prune -f
        docker volume prune -f
    }
    
    # 执行修复
    fix_kubectl_config
    cleanup_failed_pods
    restart_core_components
    cleanup_docker_resources
    
    echo "自动修复完成！"
    echo "请重新检查集群状态：kubectl get nodes"
}

# 交互式修复
interactive_fix() {
    echo "Kubernetes问题交互式修复工具"
    echo "请选择要执行的修复操作："
    echo "1) 修复kubectl配置连接问题"
    echo "2) 清理失败的Pod"
    echo "3) 重启核心组件"
    echo "4) 清理Docker资源"
    echo "5) 执行所有修复"
    echo "6) 退出"
    
    read -p "请输入选项 (1-6): " choice
    
    case $choice in
        1)
            fix_kubectl_config
            ;;
        2)
            cleanup_failed_pods
            ;;
        3)
            restart_core_components
            ;;
        4)
            cleanup_docker_resources
            ;;
        5)
            fix_common_issues
            ;;
        6)
            echo "退出修复工具"
            exit 0
            ;;
        *)
            echo "无效选项"
            ;;
    esac
}

# 主程序
if [ "$#" -eq 0 ]; then
    interactive_fix
else
    case "$1" in
        "auto")
            fix_common_issues
            ;;
        "interactive")
            interactive_fix
            ;;
        *)
            echo "用法: $0 [auto|interactive]"
            echo "  auto        - 自动执行所有修复"
            echo "  interactive - 交互式选择修复操作"
            ;;
    esac
fi
```

## 📊 问题统计和预防

### 1. 常见问题统计

| 问题类型 | 发生频率 | 平均解决时间 | 预防措施 |
|----------|----------|--------------|----------|
| 启动失败 | 高 | 10-15分钟 | 定期清理环境 |
| 连接问题 | 中 | 5-10分钟 | 备份配置文件 |
| 资源不足 | 中 | 15-20分钟 | 合理规划资源 |
| 网络问题 | 低 | 10-15分钟 | 配置网络策略 |
| 存储问题 | 低 | 5-10分钟 | 预配置存储类 |

### 2. 预防性维护

```bash
# 定期维护脚本
cat <<'EOF' > k8s-preventive-maintenance.sh
#!/bin/bash
# Kubernetes预防性维护脚本

MAINTENANCE_VERSION="1.0.0"
LOG_FILE="/tmp/k8s-maintenance-$(date +%Y%m%d).log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 每日检查任务
daily_checks() {
    log "执行每日检查..."
    
    # 检查集群健康状态
    if ! kubectl cluster-info &>/dev/null; then
        log "ERROR: 集群连接失败"
        return 1
    fi
    
    # 检查节点状态
    local unhealthy_nodes=$(kubectl get nodes | grep -v "Ready" | wc -l)
    if [ $unhealthy_nodes -gt 0 ]; then
        log "WARNING: 发现 $unhealthy_nodes 个不健康节点"
    fi
    
    # 检查失败的Pod
    local failed_pods=$(kubectl get pods --all-namespaces --field-selector=status.phase==Failed --no-headers | wc -l)
    if [ $failed_pods -gt 0 ]; then
        log "WARNING: 发现 $failed_pods 个失败的Pod"
    fi
    
    log "每日检查完成"
}

# 每周维护任务
weekly_maintenance() {
    log "执行每周维护..."
    
    # 清理资源
    kubectl delete pods --field-selector=status.phase==Succeeded --all-namespaces
    kubectl delete pods --field-selector=status.phase==Failed --all-namespaces
    
    # 清理Docker资源
    docker system prune -f
    
    # 备份重要配置
    local backup_dir="/tmp/k8s-backup-$(date +%Y%m%d)"
    mkdir -p $backup_dir
    kubectl get all --all-namespaces -o yaml > $backup_dir/all-resources.yaml
    
    log "每周维护完成"
}

# 每月深度维护
monthly_maintenance() {
    log "执行每月深度维护..."
    
    # 更新工具版本
    brew update && brew upgrade kubectl minikube kind
    
    # 重启集群
    case $(kubectl config current-context) in
        *minikube*)
            minikube stop && minikube start
            ;;
        *kind*)
            local cluster_name=$(kind get clusters | head -1)
            kind delete cluster --name $cluster_name
            kind create cluster --name $cluster_name
            ;;
    esac
    
    # 完整备份
    local full_backup="/tmp/k8s-full-backup-$(date +%Y%m%d)"
    mkdir -p $full_backup
    cp -r ~/.kube $full_backup/
    cp -r ~/.minikube $full_backup/ 2>/dev/null || true
    
    log "每月深度维护完成"
}

# 根据参数执行不同维护任务
case "${1:-daily}" in
    "daily")
        daily_checks
        ;;
    "weekly")
        weekly_maintenance
        ;;
    "monthly")
        monthly_maintenance
        ;;
    "all")
        daily_checks
        weekly_maintenance
        monthly_maintenance
        ;;
    *)
        echo "用法: $0 [daily|weekly|monthly|all]"
        echo "  daily   - 每日检查（默认）"
        echo "  weekly  - 每周维护"
        echo "  monthly - 每月深度维护"
        echo "  all     - 执行所有维护任务"
        ;;
esac
EOF

chmod +x k8s-preventive-maintenance.sh
```

---

> **💡 提示**: 建议将诊断和维护脚本添加到系统的定时任务中，实现自动化监控和维护。

**更新时间**: 2026年2月6日  
**维护状态**: ✅ 活跃维护中