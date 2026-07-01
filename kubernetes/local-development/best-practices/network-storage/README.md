# 🌐💾 Kubernetes 网络与存储最佳配置指南

> 本地 Kubernetes 环境中的网络和存储配置最佳实践

## 🎯 概述

在本地 Kubernetes 开发环境中，网络和存储配置对应用性能和开发体验至关重要。本指南将介绍如何为本地环境配置最佳的网络和存储方案。

### 📋 核心内容
- **网络配置**：CNI 插件选择、服务发现、负载均衡
- **存储配置**：持久化存储、动态供应、存储性能优化
- **性能调优**：网络和存储性能优化技巧
- **故障排除**：常见网络和存储问题的解决方法

## 🌐 网络配置最佳实践

### 1. CNI 插件选择

#### 本地开发环境推荐

```bash
# 不同工具的默认 CNI 插件
# kind: 默认使用 kindnet (基于 Calico)
# minikube: 默认使用 Bridge CNI
# k3s: 默认使用 Flannel
# Docker Desktop: 默认使用内置网络

# 为 kind 配置高级 CNI (Calico)
install_calico_kind() {
    # 创建 kind 集群配置
    cat <<EOF > kind-calico.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF

    # 创建集群
    kind create cluster --config kind-calico.yaml --name calico-cluster
    
    # 安装 Calico
    kubectl apply -k github.com/projectcalico/calico?ref=v3.26.1
}

# 为 minikube 配置 CNI
configure_minikube_cni() {
    # 使用特定 CNI 插件
    minikube start --cni=calico
    # 或
    minikube start --cni=cilium
    # 或
    minikube start --cni=auto  # 自动选择
}
```

#### 网络策略配置

```yaml
# 网络策略示例 - 限制应用间通信
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-app-communication
  namespace: development
spec:
  podSelector:
    matchLabels:
      app: restricted-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: trusted
    - podSelector:
        matchLabels:
          role: trusted
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: trusted
    ports:
    - protocol: TCP
      port: 53  # DNS
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
```

### 2. 服务发现和负载均衡

#### DNS 配置优化

```bash
# 优化 CoreDNS 配置
optimize_coredns() {
    # 查看当前 CoreDNS 配置
    kubectl get cm coredns -n kube-system -o yaml
    
    # 创建优化的 CoreDNS 配置
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
EOF

    # 重启 CoreDNS
    kubectl rollout restart deployment coredns -n kube-system
}

# 测试 DNS 性能
test_dns_performance() {
    # 创建 DNS 测试 Pod
    kubectl run dns-test --image=nicolaka/netshoot --rm -it --restart=Never -- \
        bash -c "time nslookup kubernetes.default.svc.cluster.local"
}
```

#### Ingress 配置

```bash
# 本地开发环境 Ingress 配置
setup_ingress_for_dev() {
    # 为 kind 集群安装 Nginx Ingress Controller
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
    
    # 等待 Ingress Controller 就绪
    kubectl wait --namespace ingress-nginx \
      --for=condition=ready pod \
      --selector=app.kubernetes.io/component=controller \
      --timeout=90s
    
    # 创建测试 Ingress
    cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dev-app-ingress
  namespace: development
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: dev.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: dev-app-service
            port:
              number: 80
EOF
}

# Ingress 调试
debug_ingress() {
    # 检查 Ingress 状态
    kubectl get ingress -A
    
    # 检查 Ingress Controller 日志
    kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
    
    # 测试 Ingress 连接
    curl -H "Host: dev.local" http://localhost
}
```

### 3. 网络性能优化

```bash
# 网络性能测试
test_network_performance() {
    # 创建网络性能测试 Pod
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: network-test-server
  namespace: development
spec:
  containers:
  - name: server
    image: nicolaka/netshoot
    command: ["iperf3", "-s"]
---
apiVersion: v1
kind: Service
metadata:
  name: network-test-service
  namespace: development
spec:
  selector:
    name: network-test-server
  ports:
  - protocol: TCP
    port: 5201
    targetPort: 5201
EOF

    # 运行客户端测试
    kubectl run network-test-client --image=nicolaka/netshoot --rm -it --restart=Never -- \
        iperf3 -c network-test-service -t 10
}

# 网络延迟测试
test_network_latency() {
    kubectl run latency-test --image=nicolaka/netshoot --rm -it --restart=Never -- \
        bash -c "for i in {1..10}; do time curl -s http://kubernetes.default 2>&1 >/dev/null; done"
}
```

## 💾 存储配置最佳实践

### 1. 本地存储方案

#### HostPath 存储

```bash
# HostPath 存储配置
setup_hostpath_storage() {
    # 创建 HostPath 持久卷
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  hostPath:
    path: /tmp/local-data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: local-pvc
  namespace: development
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: local-storage
EOF
}

# 验证 HostPath 存储
verify_hostpath_storage() {
    # 创建测试 Pod
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: storage-test-pod
  namespace: development
spec:
  containers:
  - name: test-container
    image: busybox
    command: ["sh", "-c", "echo 'Hello from PV' > /data/hello.txt && sleep 3600"]
    volumeMounts:
    - name: test-volume
      mountPath: /data
  volumes:
  - name: test-volume
    persistentVolumeClaim:
      claimName: local-pvc
EOF

    # 验证数据写入
    sleep 10
    kubectl exec -n development storage-test-pod -- cat /data/hello.txt
}
```

#### Local Path Provisioner

```bash
# 安装 Local Path Provisioner（适用于 k3s 和本地环境）
install_local_path_provisioner() {
    # 创建 Local Path Provisioner
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: local-path-storage
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: local-path-provisioner-service-account
  namespace: local-path-storage
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: local-path-provisioner-role
rules:
- apiGroups: [""]
  resources: ["nodes", "persistentvolumeclaims"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["endpoints", "persistentvolumes", "pods"]
  verbs: ["*"]
- apiGroups: [""]
  resources: ["events"]
  verbs: ["create", "patch"]
- apiGroups: ["storage.k8s.io"]
  resources: ["storageclasses"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: local-path-provisioner-bind
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: local-path-provisioner-role
subjects:
- kind: ServiceAccount
  name: local-path-provisioner-service-account
  namespace: local-path-storage
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: local-path-provisioner
  namespace: local-path-storage
spec:
  replicas: 1
  selector:
    matchLabels:
      app: local-path-provisioner
  template:
    metadata:
      labels:
        app: local-path-provisioner
    spec:
      serviceAccountName: local-path-provisioner-service-account
      containers:
      - name: local-path-provisioner
        image: rancher/local-path-provisioner:v0.0.24
        imagePullPolicy: IfNotPresent
        env:
        - name: LOG_LEVEL
          value: debug
        - name: BACKEND_TYPE
          value: "exec"
        - name: SHARED_FS
          value: "true"
        volumeMounts:
        - name: data
          mountPath: /data
        - name: config-volume
          mountPath: /etc/config
      volumes:
      - name: data
        hostPath:
          path: /opt/local-path-provisioner
          type: DirectoryOrCreate
      - name: config-volume
        configMap:
          name: local-path-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-path-config
  namespace: local-path-storage
data:
  config.json: |-
        {
                "nodePathMap":[
                {
                        "node":"DEFAULT_PATH_FOR_NON_LISTED_NODES",
                        "paths":["/opt/local-path-provisioner"]
                }
                ]
        }
  setup: |-
        #!/bin/sh
        set -eu
        mkdir -m 0777 -p "\$VOLPATH"
  teardown: |-
        #!/bin/sh
        set -eu
        rm -rf "\$VOLPATH"
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
EOF

    echo "Local Path Provisioner 安装完成"
    echo "现在可以使用默认存储类创建 PVC"
}

# 使用默认存储类创建 PVC
create_default_pvc() {
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: default-pvc
  namespace: development
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  # 不指定 storageClassName，使用默认存储类
EOF
}
```

### 2. 存储性能优化

#### 性能测试

```bash
# 存储性能测试
test_storage_performance() {
    # 创建存储性能测试 Pod
    cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: storage-performance-test
  namespace: development
spec:
  containers:
  - name: fio-test
    image: polinux/stress
    command: ["/bin/bash", "-c"]
    args:
    - |
      dd if=/dev/zero of=/mnt/test.dat bs=1G count=1 oflag=dsync status=progress
      dd if=/dev/zero of=/mnt/test2.dat bs=1M count=1024 oflag=dsync status=progress
      sync
    volumeMounts:
    - name: test-storage
      mountPath: /mnt
  volumes:
  - name: test-storage
    persistentVolumeClaim:
      claimName: default-pvc
EOF

    # 等待测试完成
    kubectl wait --for=condition=Ready pod/storage-performance-test -n development --timeout=300s
    kubectl logs storage-performance-test -n development
    kubectl delete pod storage-performance-test -n development
}
```

#### 存储类配置

```bash
# 创建高性能存储类
create_high_performance_sc() {
    cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: high-performance
provisioner: rancher.io/local-path
parameters:
  # 文件系统类型
  fsType: ext4
  # 挂载选项
  mountOptions: ["noatime", "nodiratime"]
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
EOF
}

# 创建低延迟存储类
create_low_latency_sc() {
    cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: low-latency
provisioner: rancher.io/local-path
parameters:
  # 优化参数
  block: "true"
  # 挂载选项
  mountOptions: ["noatime", "nodiratime", "nobarrier"]
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
EOF
}
```

### 3. 存储监控和管理

```bash
# 存储使用监控
monitor_storage_usage() {
    echo "=== 存储使用情况 ==="
    
    # 查看 PV 和 PVC
    echo "持久卷 (PV):"
    kubectl get pv -o wide
    
    echo -e "\n持久卷声明 (PVC):"
    kubectl get pvc --all-namespaces -o wide
    
    # 查看存储类
    echo -e "\n存储类 (StorageClass):"
    kubectl get storageclass -o wide
    
    # 检查节点磁盘使用
    echo -e "\n节点磁盘使用情况:"
    kubectl get nodes -o json | jq -r '.items[] | {name: .metadata.name, diskPressure: .status.conditions[] | select(.type == "DiskPressure") | .status}'
}

# 存储故障诊断
diagnose_storage_issues() {
    local pvc_name=$1
    local namespace=${2:-default}
    
    if [ -z "$pvc_name" ]; then
        echo "用法: diagnose_storage_issues <pvc-name> [namespace]"
        return 1
    fi
    
    echo "=== 诊断 PVC: $pvc_name ==="
    
    # 检查 PVC 状态
    echo "1. PVC 状态:"
    kubectl describe pvc $pvc_name -n $namespace
    
    # 检查关联的 PV
    local pv_name=$(kubectl get pvc $pvc_name -n $namespace -o jsonpath='{.spec.volumeName}' 2>/dev/null)
    if [ -n "$pv_name" ]; then
        echo -e "\n2. 关联 PV 状态:"
        kubectl describe pv $pv_name
    fi
    
    # 检查绑定状态
    local status=$(kubectl get pvc $pvc_name -n $namespace -o jsonpath='{.status.phase}')
    echo -e "\n3. 绑定状态: $status"
    
    # 检查事件
    echo -e "\n4. 相关事件:"
    kubectl get events -n $namespace --sort-by='.lastTimestamp' | grep -i $pvc_name
}
```

## 🔧 网络和存储性能调优

### 1. 综合性能测试

```bash
# 网络和存储综合测试
comprehensive_performance_test() {
    echo "=== 综合性能测试 ==="
    
    # 1. 网络性能测试
    echo "1. 网络性能测试..."
    test_network_performance
    
    # 2. 存储性能测试
    echo "2. 存储性能测试..."
    test_storage_performance
    
    # 3. 应用性能测试
    echo "3. 应用性能测试..."
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: perf-test-app
  namespace: development
spec:
  replicas: 1
  selector:
    matchLabels:
      app: perf-test-app
  template:
    metadata:
      labels:
        app: perf-test-app
    spec:
      containers:
      - name: app
        image: nginx:alpine
        ports:
        - containerPort: 80
        volumeMounts:
        - name: test-storage
          mountPath: /data
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
      volumes:
      - name: test-storage
        persistentVolumeClaim:
          claimName: default-pvc
EOF

    # 等待应用就绪
    kubectl wait --for=condition=Ready pod -l app=perf-test-app -n development --timeout=120s
    
    # 测试应用响应时间
    kubectl run test-client --image=nicolaka/netshoot --rm -it --restart=Never -n development -- \
        bash -c "time curl -s http://perf-test-app"
    
    # 清理测试资源
    kubectl delete deployment perf-test-app -n development
}
```

### 2. 资源配置优化

```bash
# 网络和存储资源优化配置
optimize_resources() {
    # 为应用配置合理的网络和存储资源
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: optimized-app
  namespace: development
spec:
  replicas: 1
  selector:
    matchLabels:
      app: optimized-app
  template:
    metadata:
      labels:
        app: optimized-app
      annotations:
        # 网络注解
        kubectl.kubernetes.io/default-container: app
    spec:
      # Pod 级别的网络配置
      hostNetwork: false  # 不使用主机网络
      dnsPolicy: ClusterFirst  # 使用集群 DNS
      # 容器配置
      containers:
      - name: app
        image: nginx:alpine
        ports:
        - containerPort: 80
        # 资源限制
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
            ephemeral-storage: "100Mi"
          limits:
            memory: "256Mi"
            cpu: "200m"
            ephemeral-storage: "500Mi"
        # 存储配置
        volumeMounts:
        - name: app-data
          mountPath: /usr/share/nginx/html
          readOnly: false
        # 网络配置
        securityContext:
          readOnlyRootFilesystem: false
          allowPrivilegeEscalation: false
      # 存储卷
      volumes:
      - name: app-data
        persistentVolumeClaim:
          claimName: default-pvc
      # 安全上下文
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
EOF
}
```

## 🚨 故障排除和诊断

### 1. 网络故障诊断

```bash
# 网络故障诊断脚本
diagnose_network_issues() {
    echo "=== 网络故障诊断 ==="
    
    # 1. 检查节点网络状态
    echo "1. 节点网络状态:"
    kubectl get nodes -o wide
    
    # 2. 检查系统组件
    echo "2. 系统组件状态:"
    kubectl get pods -n kube-system -o wide
    
    # 3. 检查 CoreDNS
    echo "3. CoreDNS 状态:"
    kubectl get pods -n kube-system -l k8s-app=kube-dns
    
    # 4. 检查 CNI 插件
    echo "4. CNI 插件状态:"
    kubectl get pods -n kube-system -l k8s-app=calico,k8s-app=flannel,k8s-app=cilium 2>/dev/null || echo "未找到 CNI 插件"
    
    # 5. DNS 解析测试
    echo "5. DNS 解析测试:"
    kubectl run dns-test --image=busybox --rm -it --restart=Never -- nslookup kubernetes.default
    
    # 6. 网络连通性测试
    echo "6. 网络连通性测试:"
    kubectl run connectivity-test --image=busybox --rm -it --restart=Never -- ping -c 3 kubernetes.default
}

# Pod 网络连通性测试
test_pod_connectivity() {
    local source_pod=$1
    local target_service=$2
    local namespace=${3:-default}
    
    if [ -z "$source_pod" ] || [ -z "$target_service" ]; then
        echo "用法: test_pod_connectivity <source-pod> <target-service> [namespace]"
        return 1
    fi
    
    kubectl exec $source_pod -n $namespace -- nslookup $target_service
    kubectl exec $source_pod -n $namespace -- ping -c 3 $target_service
}
```

### 2. 存储故障诊断

```bash
# 存储故障诊断脚本
diagnose_storage_issues_detailed() {
    echo "=== 存储故障诊断 ==="
    
    # 1. 检查 PV 状态
    echo "1. 持久卷状态:"
    kubectl get pv -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,CAPACITY:.spec.capacity.storage,STORAGECLASS:.spec.storageClassName
    
    # 2. 检查 PVC 状态
    echo "2. 持久卷声明状态:"
    kubectl get pvc --all-namespaces -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,CAPACITY:.spec.resources.requests.storage,STORAGECLASS:.spec.storageClassName
    
    # 3. 检查存储类
    echo "3. 存储类状态:"
    kubectl get storageclass -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner,RECLAIMPOLICY:.reclaimPolicy,VOLUMEBINDINGMODE:.volumeBindingMode
    
    # 4. 检查事件
    echo "4. 存储相关事件:"
    kubectl get events --all-namespaces --field-selector reason=ProvisioningFailed,reason=FailedBinding --sort-by='.lastTimestamp'
    
    # 5. 检查 Pod 挂载状态
    echo "5. Pod 挂载状态:"
    kubectl get pods --all-namespaces -o yaml | grep -A 20 volumeMounts
}
```

## 📊 监控和告警

### 1. 自定义监控脚本

```bash
#!/bin/bash
# 网络和存储监控脚本 - network-storage-monitor.sh

MONITOR_VERSION="1.0.0"

show_help() {
    echo "Kubernetes 网络和存储监控工具 $MONITOR_VERSION"
    echo "用法: $0 [command] [options]"
    echo ""
    echo "命令:"
    echo "  status                    - 显示网络和存储状态"
    echo "  performance              - 运行性能测试"
    echo "  diagnose NETWORK|STORAGE - 诊断特定组件"
    echo "  report                   - 生成监控报告"
    echo ""
    echo "示例:"
    echo "  $0 status"
    echo "  $0 performance"
    echo "  $0 diagnose NETWORK"
}

show_status() {
    echo "=== Kubernetes 网络和存储状态 ==="
    
    echo "网络状态:"
    echo "- 节点网络: $(kubectl get nodes --no-headers | wc -l) 个节点"
    echo "- CoreDNS: $(kubectl get pods -n kube-system -l k8s-app=kube-dns --no-headers | wc -l) 个实例"
    echo "- Services: $(kubectl get services --all-namespaces --no-headers | wc -l) 个服务"
    echo "- Endpoints: $(kubectl get endpoints --all-namespaces --no-headers | wc -l) 个端点"
    
    echo -e "\n存储状态:"
    echo "- PV: $(kubectl get pv --no-headers | wc -l) 个卷"
    echo "- PVC: $(kubectl get pvc --all-namespaces --no-headers | wc -l) 个声明"
    echo "- StorageClass: $(kubectl get storageclass --no-headers | wc -l) 个类"
    
    # 检查资源使用
    if kubectl top nodes &>/dev/null; then
        echo -e "\n节点资源使用:"
        kubectl top nodes
    fi
}

run_performance_tests() {
    echo "运行性能测试..."
    test_network_performance
    test_storage_performance
}

diagnose_component() {
    local component=$1
    case $component in
        "NETWORK")
            diagnose_network_issues
            ;;
        "STORAGE")
            diagnose_storage_issues_detailed
            ;;
        *)
            echo "错误: 未知组件 $component，支持 NETWORK 或 STORAGE"
            return 1
            ;;
    esac
}

generate_report() {
    local report_file="/tmp/network-storage-report-$(date +%Y%m%d-%H%M%S).txt"
    echo "生成监控报告: $report_file"
    
    {
        echo "Kubernetes 网络和存储监控报告"
        echo "================================"
        echo "生成时间: $(date)"
        echo ""
        
        echo "网络状态:"
        kubectl get nodes -o wide
        echo ""
        
        echo "存储状态:"
        kubectl get pv,pvc --all-namespaces
        echo ""
        
        echo "存储类:"
        kubectl get storageclass
        echo ""
        
        echo "CoreDNS 状态:"
        kubectl get pods -n kube-system -l k8s-app=kube-dns
        echo ""
        
        echo "事件:"
        kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20
    } > $report_file
    
    echo "报告已生成: $report_file"
}

# 主程序逻辑
case "${1:-status}" in
    "status")
        show_status
        ;;
    "performance")
        run_performance_tests
        ;;
    "diagnose")
        if [ -z "$2" ]; then
            echo "错误: 请指定要诊断的组件 (NETWORK|STORAGE)"
            exit 1
        fi
        diagnose_component "$2"
        ;;
    "report")
        generate_report
        ;;
    "help"|*)
        show_help
        ;;
esac
```

## 🎯 最佳实践总结

### 网络最佳实践
1. **选择合适的 CNI 插件**：根据需求选择 Calico、Flannel 或 Cilium
2. **配置网络策略**：使用 NetworkPolicy 限制不必要的网络访问
3. **优化 DNS 配置**：调整缓存和负载均衡设置
4. **使用 Ingress 控制器**：合理配置负载均衡和 SSL 终结

### 存储最佳实践
1. **选择合适的存储方案**：根据性能需求选择 HostPath、Local Path 或动态供应
2. **配置存储类**：使用 StorageClass 实现动态存储供应
3. **设置资源限制**：为存储设置合理的请求和限制
4. **监控存储使用**：定期检查存储使用情况和性能

### 性能优化
1. **合理配置资源**：为应用设置合适的 CPU、内存和存储资源
2. **使用 SSD 存储**：在可能的情况下使用 SSD 作为存储后端
3. **优化网络配置**：使用合适的网络插件和配置
4. **定期维护**：清理未使用的资源，更新配置

---

> **💡 提示**: 网络和存储配置对 Kubernetes 集群性能至关重要。根据应用需求选择合适的配置，并定期监控和优化。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日
## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 🚀 快速开始

### 部署资源

```bash
./scripts/apply.sh
```

### 检查状态

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

```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
