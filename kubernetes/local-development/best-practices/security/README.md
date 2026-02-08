# 🔐 Kubernetes 本地开发安全最佳实践指南

> 本地 Kubernetes 环境的安全配置、管理与最佳实践

## 🎯 安全概述

在本地 Kubernetes 开发环境中，安全性同样重要。虽然这是开发环境，但仍需要遵循安全最佳实践，以培养良好的安全习惯并防止潜在风险。

### 📋 核心安全原则
- **最小权限原则**：只授予必要的权限
- **分层防护**：多层安全控制
- **安全默认**：默认启用安全配置
- **持续监控**：实时监控安全状态
- **定期审计**：定期审查安全配置

## 🔐 RBAC 配置最佳实践

### 1. 基础 RBAC 配置

```yaml
# 开发者角色定义
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer-role
  namespace: development
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "create", "update", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets", "daemonsets"]
  verbs: ["get", "list", "create", "update", "delete"]
- apiGroups: ["batch"]
  resources: ["jobs", "cronjobs"]
  verbs: ["get", "list", "create", "update", "delete"]

---
# 开发者角色绑定
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: development
subjects:
- kind: User
  name: developer@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
```

### 2. 命名空间级别的权限管理

```bash
# 创建开发环境命名空间
kubectl create namespace dev-environment

# 为不同团队创建独立的命名空间
kubectl create namespace team-a-dev
kubectl create namespace team-b-dev

# 创建命名空间管理员角色
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: namespace-admin
  namespace: dev-environment
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: namespace-admin-binding
  namespace: dev-environment
subjects:
- kind: User
  name: admin@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: namespace-admin
  apiGroup: rbac.authorization.k8s.io
EOF
```

### 3. RBAC 审计和管理

```bash
# 查看所有 Role 和 RoleBinding
kubectl get roles,rolebindings --all-namespaces

# 查看特定用户的权限
kubectl auth can-i get pods --as=developer@example.com -n development

# 审计 RBAC 配置
audit_rbac() {
    echo "=== RBAC 配置审计 ==="
    
    echo "ClusterRoles:"
    kubectl get clusterroles --no-headers | wc -l
    
    echo "Roles:"
    kubectl get roles --all-namespaces --no-headers | wc -l
    
    echo "ClusterRoleBindings:"
    kubectl get clusterrolebindings --no-headers | wc -l
    
    echo "RoleBindings:"
    kubectl get rolebindings --all-namespaces --no-headers | wc -l
    
    # 检查过度宽松的权限
    echo "检查过度宽松的角色..."
    kubectl get clusterroles -o json | jq '.items[] | select(.rules[].verbs[] == "*") | .metadata.name'
}

# 清理未使用的 RBAC 资源
cleanup_unused_rbac() {
    echo "清理未使用的 RBAC 资源..."
    
    # 查找没有绑定的角色
    for role in $(kubectl get roles --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'); do
        namespace=$(echo $role | cut -d'/' -f1)
        role_name=$(echo $role | cut -d'/' -f2)
        
        binding_count=$(kubectl get rolebindings -n $namespace -o json | jq --arg rolename "$role_name" '[.items[] | select(.roleRef.name == $rolename)] | length')
        
        if [ "$binding_count" -eq 0 ]; then
            echo "未使用的 Role: $role"
            # kubectl delete role $role_name -n $namespace  # 取消注释以实际删除
        fi
    done
}
```

## 🛡️ 网络安全策略

### 1. NetworkPolicy 配置

```yaml
# 默认拒绝所有流量的策略
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: development
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# 允许 DNS 查询
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: development
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53

---
# 应用间通信策略
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-communication
  namespace: development
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 8080
```

### 2. 网络策略管理脚本

```bash
# 网络策略验证工具
validate_network_policies() {
    echo "=== 网络策略验证 ==="
    
    # 检查是否存在默认拒绝策略
    default_deny_exists=$(kubectl get networkpolicy --all-namespaces -o json | jq '[.items[] | select(.spec.podSelector.matchLabels == null and .spec.podSelector.matchExpressions == null)] | length')
    
    if [ "$default_deny_exists" -gt 0 ]; then
        echo "✅ 存在默认拒绝策略"
    else
        echo "⚠️  缺少默认拒绝策略"
    fi
    
    # 检查各命名空间的策略
    for ns in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
        policy_count=$(kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l)
        echo "命名空间 $ns: $policy_count 个网络策略"
    done
}

# 网络连通性测试
test_network_connectivity() {
    local source_pod=$1
    local target_service=$2
    local namespace=${3:-default}
    
    if [ -z "$source_pod" ] || [ -z "$target_service" ]; then
        echo "用法: test_network_connectivity <source-pod> <target-service> [namespace]"
        return 1
    fi
    
    echo "测试网络连通性: $source_pod -> $target_service"
    
    # 创建测试 Pod
    kubectl run connectivity-test --image=nicolaka/netshoot --rm -it --restart=Never -n $namespace -- \
        timeout 10 curl -s -o /dev/null -w "%{http_code}" http://$target_service
}
```

## 🔑 Secret 管理和加密

### 1. Secret 最佳实践

```yaml
# 使用 Secret 的 Deployment 示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-secrets
  namespace: development
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-with-secrets
  template:
    metadata:
      labels:
        app: app-with-secrets
    spec:
      containers:
      - name: app
        image: myapp:latest
        env:
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: api-key
        volumeMounts:
        - name: secret-volume
          mountPath: /etc/secrets
          readOnly: true
      volumes:
      - name: secret-volume
        secret:
          secretName: app-secrets
          items:
          - key: cert.pem
            path: ssl/cert.pem
          - key: key.pem
            path: ssl/key.pem
```

### 2. Secret 管理工具

```bash
# 创建加密的 Secret
create_encrypted_secret() {
    local secret_name=$1
    local namespace=$2
    shift 2
    
    if [ -z "$secret_name" ] || [ -z "$namespace" ]; then
        echo "用法: create_encrypted_secret <secret-name> <namespace> <key1>=<value1> <key2>=<value2> ..."
        return 1
    fi
    
    # 创建临时文件
    local temp_file=$(mktemp)
    
    echo "apiVersion: v1" > $temp_file
    echo "kind: Secret" >> $temp_file
    echo "metadata:" >> $temp_file
    echo "  name: $secret_name" >> $temp_file
    echo "  namespace: $namespace" >> $temp_file
    echo "type: Opaque" >> $temp_file
    echo "data:" >> $temp_file
    
    # 添加数据项
    for arg in "$@"; do
        key=$(echo $arg | cut -d'=' -f1)
        value=$(echo $arg | cut -d'=' -f2-)
        encoded_value=$(echo -n "$value" | base64)
        echo "  $key: $encoded_value" >> $temp_file
    done
    
    # 应用 Secret
    kubectl apply -f $temp_file
    rm $temp_file
    
    echo "Secret $secret_name 创建成功"
}

# Secret 审计工具
audit_secrets() {
    echo "=== Secret 审计 ==="
    
    # 检查明文 Secret
    echo "检查明文配置..."
    kubectl get secrets --all-namespaces -o json | jq -r '.items[] | select(.data != null) | "\(.metadata.namespace)/\(.metadata.name): \(.data | keys[])"'
    
    # 检查过大 Secret
    echo "检查过大的 Secret..."
    kubectl get secrets --all-namespaces -o json | jq -r '.items[] | select(.data != null) | .data | to_entries[] | select((.value | length) > 10000) | "\(.key): 大小超过 10KB"'
    
    # 统计各类型 Secret
    echo "Secret 类型统计:"
    kubectl get secrets --all-namespaces -o json | jq -r '.items[].type' | sort | uniq -c
}
```

### 3. 外部密钥管理系统集成

```bash
# HashiCorp Vault 集成示例
setup_vault_integration() {
    # 安装 Vault Operator
    helm repo add hashicorp https://helm.releases.hashicorp.com
    helm install vault hashicorp/vault --set "server.dev.enabled=true" --namespace vault --create-namespace
    
    # 等待 Vault 就绪
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=vault -n vault --timeout=300s
    
    # 配置 Vault Injector
    kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-vault
  namespace: development
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-with-vault
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "app-role"
        vault.hashicorp.com/agent-inject-secret-database-config: "secret/database/config"
        vault.hashicorp.com/agent-inject-template-database-config: |
          {{- with secret "secret/database/config" -}}
          {
            "username": "{{ .Data.username }}",
            "password": "{{ .Data.password }}"
          }
          {{- end }}
      labels:
        app: app-with-vault
    spec:
      serviceAccountName: app-with-vault
      containers:
      - name: app
        image: myapp:latest
        volumeMounts:
        - name: vault-secrets
          mountPath: /vault/secrets
          readOnly: true
      volumes:
      - name: vault-secrets
        emptyDir:
          medium: Memory
EOF
}
```

## 🛡️ 镜像安全

### 1. 镜像扫描配置

```bash
# 安装 Trivy 镜像扫描器
install_trivy() {
    brew install aquasecurity/trivy/trivy
    
    # 扫描本地镜像
    scan_local_image() {
        local image_name=$1
        if [ -z "$image_name" ]; then
            echo "用法: scan_local_image <image-name>"
            return 1
        fi
        
        trivy image --severity HIGH,CRITICAL $image_name
    }
    
    # 集成到构建流程
    secure_build() {
        local image_name=$1
        if [ -z "$image_name" ]; then
            echo "用法: secure_build <image-name>"
            return 1
        fi
        
        # 构建镜像
        docker build -t $image_name .
        
        # 扫描镜像
        if ! trivy image --exit-code 1 --severity HIGH,CRITICAL $image_name; then
            echo "❌ 镜像扫描发现高危漏洞，构建失败"
            return 1
        fi
        
        echo "✅ 镜像安全检查通过"
        docker push $image_name
    }
}

# 在集群中部署镜像扫描
deploy_image_scanner() {
    # 部署 Clair 扫描器
    kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: clair-scanner
  namespace: security
spec:
  replicas: 1
  selector:
    matchLabels:
      app: clair-scanner
  template:
    metadata:
      labels:
        app: clair-scanner
    spec:
      containers:
      - name: clair
        image: quay.io/coreos/clair:v4.0.0
        ports:
        - containerPort: 6060
        volumeMounts:
        - name: config
          mountPath: /etc/clair/
      volumes:
      - name: config
        configMap:
          name: clair-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: clair-config
  namespace: security
data:
  config.yaml: |
    http_listen_addr: ":6060"
    introspection_addr: ":6061"
    log_level: "info"
    indexer:
      conn_string: "host=postgres port=5432 dbname=clair user=clair password=clair sslmode=disable"
      scan_lock_retry: 10
      layer_scan_concurrency: 5
      migrations: true
    matcher:
      conn_string: "host=postgres port=5432 dbname=clair user=clair password=clair sslmode=disable"
      max_conn_pool: 100
      migrations: true
EOF
}
```

### 2. 运行时安全配置

```yaml
# Pod 安全策略示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: development
spec:
  replicas: 1
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        image: myapp:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
        - name: var-tmp-volume
          mountPath: /var/tmp
      volumes:
      - name: tmp-volume
        emptyDir: {}
      - name: var-tmp-volume
        emptyDir: {}
```

## 🔍 安全监控和审计

### 1. 审计日志配置

```bash
# 启用审计日志
enable_audit_logging() {
    # 创建审计策略文件
    cat <<EOF > audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets", "configmaps"]
  - group: "rbac.authorization.k8s.io"
    resources: ["roles", "rolebindings", "clusterroles", "clusterrolebindings"]
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods", "services"]
  verbs: ["create", "update", "delete"]
- level: None
EOF

    # 配置 API Server 审计
    # 注意：这通常需要修改 Kubernetes 控制平面配置
    echo "审计日志配置文件已创建: audit-policy.yaml"
    echo "请根据您的部署工具相应地配置审计日志"
}

# 审计日志分析工具
analyze_audit_logs() {
    local log_file=${1:-"/var/log/kubernetes/audit.log"}
    
    if [ ! -f "$log_file" ]; then
        echo "审计日志文件不存在: $log_file"
        return 1
    fi
    
    echo "=== 审计日志分析 ==="
    
    # 统计操作类型
    echo "操作类型统计:"
    jq -r '.verb' $log_file | sort | uniq -c | sort -nr
    
    # 统计资源类型
    echo "资源类型统计:"
    jq -r '.objectRef.resource' $log_file | sort | uniq -c | sort -nr
    
    # 查找可疑活动
    echo "可疑活动 (删除操作):"
    jq -r 'select(.verb == "delete") | "\(.user.username) 删除了 \(.objectRef.resource)/\(.objectRef.name) 在 \(.objectRef.namespace)"' $log_file
    
    # 查找权限变更
    echo "权限变更活动:"
    jq -r 'select(.objectRef.resource == "roles" or .objectRef.resource == "rolebindings") | "\(.user.username) 修改了 \(.objectRef.resource)/\(.objectRef.name)"' $log_file
}
```

### 2. 安全事件监控

```bash
# 创建安全监控脚本
security_monitor() {
    echo "=== 安全监控 ==="
    
    # 检查特权容器
    echo "检查特权容器:"
    kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(.spec.containers[].securityContext.privileged == true) | "\(.metadata.namespace)/\(.metadata.name)"'
    
    # 检查以 root 运行的容器
    echo "检查 root 容器:"
    kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(.spec.containers[].securityContext.runAsUser == 0) | "\(.metadata.namespace)/\(.metadata.name)"'
    
    # 检查可写根文件系统
    echo "检查可写根文件系统:"
    kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(.spec.containers[].securityContext.readOnlyRootFilesystem == false) | "\(.metadata.namespace)/\(.metadata.name)"'
    
    # 检查网络策略缺失
    echo "检查缺少网络策略的命名空间:"
    for ns in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
        policy_count=$(kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l)
        if [ "$policy_count" -eq 0 ]; then
            echo "命名空间 $ns 缺少网络策略"
        fi
    done
}

# 实时安全监控
setup_realtime_monitoring() {
    # 创建安全监控 CronJob
    kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: security-audit
  namespace: security
spec:
  schedule: "0 */6 * * *"  # 每6小时运行一次
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: security-auditor
            image: aquasec/kube-bench:latest
            command:
            - kube-bench
            - run
            - --targets
            - master,node,controlplane,policies
            volumeMounts:
            - name: var-lib-etcd
              mountPath: /var/lib/etcd
              readOnly: true
            - name: var-lib-kubelet
              mountPath: /var/lib/kubelet
              readOnly: true
            - name: etc-systemd
              mountPath: /etc/systemd
              readOnly: true
            - name: lib-systemd
              mountPath: /lib/systemd/
              readOnly: true
            - name: srv-kubernetes
              mountPath: /srv/kubernetes/
              readOnly: true
            - name: etc-kubernetes
              mountPath: /etc/kubernetes
              readOnly: true
            - name: usr-bin
              mountPath: /usr/bin
              readOnly: true
          volumes:
          - name: var-lib-etcd
            hostPath:
              path: "/var/lib/etcd"
          - name: var-lib-kubelet
            hostPath:
              path: "/var/lib/kubelet"
          - name: etc-systemd
            hostPath:
              path: "/etc/systemd"
          - name: lib-systemd
            hostPath:
              path: "/lib/systemd"
          - name: srv-kubernetes
            hostPath:
              path: "/srv/kubernetes"
          - name: etc-kubernetes
            hostPath:
              path: "/etc/kubernetes"
          - name: usr-bin
            hostPath:
              path: "/usr/bin"
          restartPolicy: OnFailure
EOF
}
```

## 🚨 应急响应

### 1. 安全事件响应流程

```bash
# 安全事件响应脚本
security_incident_response() {
    local incident_type=$1
    
    case $incident_type in
        "unauthorized-access")
            echo "处理未授权访问事件..."
            # 1. 隔离受影响的资源
            kubectl scale deployment suspicious-app --replicas=0 -n affected-namespace
            
            # 2. 收集证据
            kubectl get pods -n affected-namespace -o yaml > incident-pods.yaml
            kubectl get events -n affected-namespace --sort-by='.lastTimestamp' > incident-events.log
            
            # 3. 通知相关人员
            echo "安全事件: 检测到未授权访问" | mail -s "Security Alert" security-team@example.com
            ;;
            
        "malicious-pod")
            echo "处理恶意 Pod 事件..."
            # 1. 立即删除恶意 Pod
            kubectl delete pod malicious-pod -n compromised-namespace
            
            # 2. 检查相关资源
            kubectl get deployments,daemonsets,statefulsets -n compromised-namespace
            
            # 3. 扫描镜像
            kubectl get pods -n compromised-namespace -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u | while read image; do
                trivy image $image
            done
            ;;
            
        "privilege-escalation")
            echo "处理权限升级事件..."
            # 1. 撤销异常权限
            kubectl delete rolebinding suspicious-binding -n affected-namespace
            
            # 2. 审查 RBAC 配置
            kubectl get roles,rolebindings -n affected-namespace -o yaml > rbac-review.yaml
            
            # 3. 重置服务账户
            kubectl delete serviceaccount compromised-sa -n affected-namespace
            kubectl create serviceaccount compromised-sa -n affected-namespace
            ;;
            
        *)
            echo "未知事件类型: $incident_type"
            echo "支持的事件类型: unauthorized-access, malicious-pod, privilege-escalation"
            ;;
    esac
}

# 创建应急响应检查清单
create_incident_checklist() {
    cat <<EOF > security-incident-checklist.md
# Kubernetes 安全事件响应检查清单

## 立即行动
- [ ] 隔离受影响的资源
- [ ] 收集相关日志和证据
- [ ] 通知安全团队
- [ ] 评估影响范围

## 调查阶段
- [ ] 分析审计日志
- [ ] 检查 RBAC 配置
- [ ] 审查网络策略
- [ ] 扫描相关镜像

## 修复阶段
- [ ] 删除恶意资源
- [ ] 重置受损配置
- [ ] 加强安全控制
- [ ] 验证修复效果

## 后续措施
- [ ] 更新安全策略
- [ ] 加强监控告警
- [ ] 团队安全培训
- [ ] 文档事件过程
EOF
}
```

## 🎯 安全最佳实践总结

### 实施优先级
1. **立即实施**：RBAC 配置、网络策略、Secret 管理
2. **短期目标**：镜像安全扫描、运行时安全配置
3. **长期规划**：安全监控、审计日志、应急响应

### 关键要点
- 始终遵循最小权限原则
- 定期审查和更新安全配置
- 建立完善的安全监控体系
- 制定清晰的应急响应流程
- 持续进行安全意识培训

---

> **💡 提示**: 安全是一个持续的过程，需要定期评估和改进。即使在开发环境中也要保持良好的安全习惯。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日