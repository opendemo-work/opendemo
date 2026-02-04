# ⎈ K8s 命令行速查表 (k8s-cli.md)

> 生产环境必备的 Kubernetes 命令行参考手册，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [集群管理](#集群管理)
- [命名空间操作](#命名空间操作)
- [Pod 管理](#pod-管理)
- [工作负载管理](#工作负载管理)
- [服务发现](#服务发现)
- [网络管理](#网络管理)
- [网络连通性速查](#网络连通性速查)
- [运行态监控与诊断](#运行态监控与诊断)
- [存储管理](#存储管理)
- [配置管理](#配置管理)
- [安全管理与合规](#安全管理与合规)
- [监控诊断](#监控诊断)
- [调试排错](#调试排错)
- [升级维护](#升级维护)
- [安全加固](#安全加固)
- [性能优化](#性能优化)
- [AI/ML 特殊命令](#aiml-特殊命令)
- [故障应急处理](#故障应急处理)
- [容灾切换演练](#容灾切换演练)
- [性能压测方案](#性能压测方案)
- [功能演示工具](#功能演示工具)
- [Pod内应用问题排查](#pod内应用问题排查)
- [运维自动化](#运维自动化)
- [最佳实践总结](#最佳实践总结)
- [运维场景补充命令](#运维场景补充命令)
  - [集群联邦和多集群管理](#集群联邦和多集群管理)
  - [Helm和包管理](#helm和包管理)
  - [Operator和自定义资源](#operator和自定义资源)
  - [服务网格扩展](#服务网格扩展)
  - [事件驱动和消息队列](#事件驱动和消息队列)
  - [数据库和中间件](#数据库和中间件)
  - [监控告警系统](#监控告警系统)
  - [日志收集系统](#日志收集系统)
  - [CI/CD和GitOps](#cicd和gitops)
  - [安全和合规工具](#安全和合规工具)
  - [备份和灾难恢复](#备份和灾难恢复)
  - [性能和容量规划](#性能和容量规划)
  - [开发者工具集成](#开发者工具集成)
  - [自动化运维平台](#自动化运维平台)
  - [现代可观测性工具](#现代可观测性工具)
  - [边缘计算和多云管理](#边缘计算和多云管理)
  - [GitOps和声明式管理](#gitops和声明式管理)
  - [安全和合规增强](#安全和合规增强)
  - [服务网格现代化](#服务网格现代化)
  - [AI/ML平台集成](#aiml平台集成)
  - [数据库和中间件Operator](#数据库和中间件operator)
  - [存储和备份现代化](#存储和备份现代化)
  - [网络和安全增强](#网络和安全增强)
  - [开发者体验工具](#开发者体验工具)
  - [监控和告警增强](#监控和告警增强)
  - [容器运行时和镜像管理](#容器运行时和镜像管理)
  - [测试和质量保证](#测试和质量保证)
  - [性能和容量规划](#性能和容量规划)
  - [灾难恢复和备份](#灾难恢复和备份)
  - [云原生安全](#云原生安全)
  - [边缘和物联网](#边缘和物联网)
  - [无服务器和函数计算](#无服务器和函数计算)
  - [Linux系统运维基础命令](#linux系统运维基础命令)
    - [系统信息和状态监控](#系统信息和状态监控)
    - [进程和资源管理](#进程和资源管理)
    - [文件系统和存储管理](#文件系统和存储管理)
    - [网络基础命令](#网络基础命令)
    - [安全基础命令](#安全基础命令)
    - [系统维护和故障排除](#系统维护和故障排除)
    - [自动化运维脚本](#自动化运维脚本)
    - [监控和告警](#监控和告警)
    - [性能基准测试](#性能基准测试)
    - [容器化环境命令](#容器化环境命令)
  - [Linux系统运维基础命令](#linux系统运维基础命令)
    - [系统信息和状态监控](#系统信息和状态监控)
    - [进程和资源管理](#进程和资源管理)
    - [文件系统和存储管理](#文件系统和存储管理)
    - [网络基础命令](#网络基础命令)
    - [安全基础命令](#安全基础命令)
    - [系统维护和故障排除](#系统维护和故障排除)
    - [自动化运维脚本](#自动化运维脚本)
    - [监控和告警](#监控和告警)
    - [性能基准测试](#性能基准测试)
    - [容器化环境命令](#容器化环境命令)  - [AI基础设施核心命令](#ai基础设施核心命令)
    - [LLM训练平台管理](#llm训练平台管理)
    - [模型推理服务管理](#模型推理服务管理)
    - [LLM微调和优化](#llm微调和优化)
    - [AI平台运维管理](#ai平台运维管理)
    - [AI资源调度和优化](#ai资源调度和优化)
    - [AI模型监控和可观测性](#ai模型监控和可观测性)
    - [AI安全和合规](#ai安全和合规)
    - [AI平台巡检和健康检查](#ai平台巡检和健康检查)
    - [AI平台故障诊断](#ai平台故障诊断)
    - [AI平台性能优化](#ai平台性能优化)
    - [AI平台容量规划](#ai平台容量规划)
    - [AI平台备份和恢复](#ai平台备份和恢复)
    - [AI平台安全加固](#ai平台安全加固)
    - [AI数据管理平台](#ai数据管理平台)
    - [AI模型注册中心](#ai模型注册中心)
    - [AI实验管理平台](#ai实验管理平台)
    - [AI平台成本优化](#ai平台成本优化)
    - [AI平台多租户管理](#ai平台多租户管理)
- [实用技巧](#实用技巧)

---

## 集群管理

### 集群信息查看
```bash
# 查看集群基本信息
kubectl cluster-info

# 查看集群版本
kubectl version --short

# 查看集群组件状态
kubectl get componentstatuses

# 查看集群节点
kubectl get nodes -o wide

# 查看节点详情
kubectl describe node <node-name>

# 查看节点资源使用情况
kubectl top nodes

# 查看节点标签
kubectl get nodes --show-labels

# 给节点打标签
kubectl label nodes <node-name> <label-key>=<label-value>

# 移除节点标签
kubectl label nodes <node-name> <label-key>-
```

### 节点管理
```bash
# 污点节点（阻止调度）
kubectl taint nodes <node-name> key=value:NoSchedule

# 移除节点污点
kubectl taint nodes <node-name> key=value:NoSchedule-

# 驱逐节点上的Pod
kubectl drain <node-name> --ignore-daemonsets --delete-local-data

# 取消节点维护状态
kubectl uncordon <node-name>

# 设置节点不可调度
kubectl cordon <node-name>
```

### 集群健康检查
```bash
# 检查API Server连通性
kubectl get --raw='/healthz?verbose'

# 检查etcd健康状态
kubectl exec -n kube-system etcd-$(hostname) -- etcdctl endpoint health

# 查看集群事件
kubectl get events --sort-by='.lastTimestamp' -A

# 查看警告事件
kubectl get events --field-selector type=Warning -A
```

---

## 命名空间操作

```bash
# 查看所有命名空间
kubectl get namespaces

# 创建命名空间
kubectl create namespace <namespace-name>

# 删除命名空间（谨慎操作）
kubectl delete namespace <namespace-name>

# 切换默认命名空间
kubectl config set-context --current --namespace=<namespace-name>

# 查看当前上下文和命名空间
kubectl config current-context
kubectl config view | grep namespace

# 临时指定命名空间
kubectl get pods -n <namespace-name>
```

---

## Pod 管理

### Pod 基础操作
```bash
# 查看Pod列表
kubectl get pods [-n <namespace>]

# 查看Pod详细信息
kubectl describe pod <pod-name> [-n <namespace>]

# 查看Pod YAML配置
kubectl get pod <pod-name> -o yaml [-n <namespace>]

# 实时查看Pod日志
kubectl logs <pod-name> [-n <namespace>] -f

# 查看Pod资源使用
kubectl top pod <pod-name> [-n <namespace>]

# 进入Pod容器
kubectl exec -it <pod-name> [-n <namespace>] -- sh
kubectl exec -it <pod-name> [-n <namespace>] -- bash

# 删除Pod
kubectl delete pod <pod-name> [-n <namespace>]

# 强制删除卡住的Pod
kubectl delete pod <pod-name> --force --grace-period=0 [-n <namespace>]
```

### Pod 高级操作
```bash
# 查看Pod重启次数
kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[*].restartCount}'

# 查看Pod IP地址
kubectl get pod <pod-name> -o jsonpath='{.status.podIP}'

# 查看Pod所在节点
kubectl get pod <pod-name> -o jsonpath='{.spec.nodeName}'

# 复制文件到Pod
kubectl cp <local-file> <namespace>/<pod-name>:<pod-path>

# 从Pod复制文件
kubectl cp <namespace>/<pod-name>:<pod-path> <local-file>

# 查看Pod环境变量
kubectl exec <pod-name> -- env

# 测试Pod网络连通性
kubectl exec <pod-name> -- ping <target-ip>
kubectl exec <pod-name> -- nc -z <host> <port>
```

### Pod 调试技巧
```bash
# 创建临时调试Pod
kubectl run debug-pod --image=busybox --rm -it -- sh

# 在现有Pod中添加调试容器
kubectl debug <pod-name> -it --image=nicolaka/netshoot -- sh

# 临时修改Pod镜像进行调试
kubectl patch pod <pod-name> -p '{"spec":{"containers":[{"name":"<container-name>","image":"busybox"}]}}'
```

---

## 工作负载管理

### Deployment 操作
```bash
# 查看Deployment
kubectl get deployments [-n <namespace>]

# 查看Deployment详情
kubectl describe deployment <deployment-name> [-n <namespace>]

# 更新Deployment镜像
kubectl set image deployment/<deployment-name> <container-name>=<new-image>[:tag]

# 回滚Deployment
kubectl rollout undo deployment/<deployment-name>

# 查看回滚历史
kubectl rollout history deployment/<deployment-name>

# 扩缩容Deployment
kubectl scale deployment/<deployment-name> --replicas=<number>

# 暂停Deployment更新
kubectl rollout pause deployment/<deployment-name>

# 恢复Deployment更新
kubectl rollout resume deployment/<deployment-name>

# 重启Deployment
kubectl rollout restart deployment/<deployment-name>
```

### StatefulSet 操作
```bash
# 查看StatefulSet
kubectl get statefulsets [-n <namespace>]

# 扩缩容StatefulSet
kubectl scale statefulset/<statefulset-name> --replicas=<number>

# 删除StatefulSet但保留Pod
kubectl delete statefulset <statefulset-name> --cascade=orphan

# 强制删除StatefulSet Pod
kubectl delete pod <pod-name> --force --grace-period=0
```

### Job/CronJob 操作
```bash
# 查看Job状态
kubectl get jobs [-n <namespace>]

# 查看CronJob
kubectl get cronjobs [-n <namespace>]

# 手动触发CronJob
kubectl create job --from=cronjob/<cronjob-name> <job-name>

# 删除Job及其Pod
kubectl delete job <job-name>
```

---

## 服务发现

### Service 操作
```bash
# 查看Service列表
kubectl get services [-n <namespace>]

# 查看Service详情
kubectl describe service <service-name> [-n <namespace>]

# 查看Service端点
kubectl get endpoints <service-name> [-n <namespace>]

# 测试Service连通性
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- curl <service-name>.<namespace>:<port>

# 临时暴露Service
kubectl port-forward service/<service-name> <local-port>:<service-port>

# 查看Service关联的Pod
kubectl get pods -l <label-selector> [-n <namespace>]

# 测试Service DNS解析
kubectl exec <pod-name> -- nslookup <service-name>.<namespace>.svc.cluster.local

# Service性能测试
kubectl run perf-test --rm -i --tty --image nicolaka/netshoot -- \
  hey -z 30s -c 10 http://<service-name>.<namespace>:<port>

# Service压力测试
kubectl run stress-test --rm -i --tty --image busybox -- \
  while true; do curl -s http://<service-name>.<namespace>:<port>; done
```

### Ingress 操作
```bash
# 查看Ingress规则
kubectl get ingress [-n <namespace>]

# 查看Ingress详情
kubectl describe ingress <ingress-name> [-n <namespace>]

# 测试Ingress访问
curl -H "Host: <host>" http://<ingress-controller-ip>

# 查看Ingress控制器日志
kubectl logs -n <ingress-namespace> deployment/<ingress-controller>

# 验证Ingress TLS配置
openssl s_client -connect <host>:443 -servername <host>

# Ingress性能测试
kubectl run ingress-test --rm -i --tty --image nicolaka/netshoot -- \
  ab -n 1000 -c 10 https://<host>/

# Ingress路径测试
for path in /api/v1 /health /metrics; do
  echo "Testing path: $path"
  curl -H "Host: <host>" http://<ingress-ip>$path -w "%{http_code}\n"
done
```

### 服务网格相关（Istio/Linkerd）
```bash
# 查看服务网格状态
istioctl ps
istioctl proxy-status

# 查看虚拟服务
kubectl get virtualservices [-n <namespace>]

# 查看目标规则
kubectl get destinationrules [-n <namespace>]

# 测试服务网格流量
kubectl exec <source-pod> -c istio-proxy -- curl http://<service-name>:<port>

# 查看服务网格配置
istioctl pc routes <pod-name>.<namespace>
istioctl pc listeners <pod-name>.<namespace>

# 服务网格流量监控
kubectl exec <pod-name> -c istio-proxy -- pilot-agent request GET stats/prometheus

# 服务网格证书检查
kubectl exec <pod-name> -c istio-proxy -- curl http://localhost:15000/certs
```

---

## 网络连通性速查

### Kubernetes集群内部连通性验证
```bash
# 方式1: 使用现有Pod（推荐-零资源消耗）
kubectl exec -it <existing-pod> -- nslookup kubernetes.default
kubectl exec -it <existing-pod> -- ping -c 4 kubernetes.default
kubectl exec -it <existing-pod> -- wget --spider --timeout=5 https://kubernetes.default/api/v1/namespaces

# 方式2: 新建临时Pod（完整环境）
kubectl run dns-test --rm -i --tty --image busybox -- nslookup kubernetes.default
kubectl run connectivity-test --rm -i --tty --image busybox -- \
  sh -c "ping -c 4 kubernetes.default && echo '✅ DNS解析正常'"
kubectl run api-test --rm -i --tty --image busybox -- \
  wget --spider --timeout=5 https://kubernetes.default/api/v1/namespaces

# 方式3: 使用Netshoot工具箱（高级诊断）
kubectl run netshoot-test --rm -i --tty --image nicolaka/netshoot -- \
  sh -c "nslookup kubernetes.default && ping -c 4 kubernetes.default"
```

### Pod网络连通性诊断
```bash
# 方式1: 使用现有源Pod（推荐）
TARGET_POD_IP=$(kubectl get pod <target-pod> -o jsonpath='{.status.podIP}')
kubectl exec -it <existing-source-pod> -- ping -c 4 $TARGET_POD_IP
kubectl exec -it <existing-source-pod> -- nc -z $TARGET_POD_IP 80

# 方式2: 新建测试Pod
kubectl run pod-connectivity-test --rm -i --tty --image busybox -- \
  sh -c "TARGET_IP=\$(kubectl get pod <target-pod> -o jsonpath='{.status.podIP}'); ping -c 4 \$TARGET_IP"

# 方式3: 批量测试（使用现有Pod）
kubectl get pods -o jsonpath='{range .items[*]}{.status.podIP}{"\n"}{end}' | \
  xargs -I {} kubectl exec -it <test-pod> -- ping -c 1 {}
```

### Service网络连通性测试
```bash
# 方式1: 使用现有Pod测试（推荐）
SERVICE_CLUSTER_IP=$(kubectl get svc <service-name> -o jsonpath='{.spec.clusterIP}')
kubectl exec -it <existing-pod> -- ping -c 4 $SERVICE_CLUSTER_IP
kubectl exec -it <existing-pod> -- nslookup <service-name>.<namespace>.svc.cluster.local

# 方式2: 新建专用测试Pod
kubectl run service-test --rm -i --tty --image busybox -- ping -c 4 $SERVICE_CLUSTER_IP
kubectl run dns-svc-test --rm -i --tty --image busybox -- \
  nslookup <service-name>.<namespace>.svc.cluster.local

# 方式3: 端点连通性测试
kubectl get endpoints <service-name> -o jsonpath='{range .subsets[*].addresses[*]}{.ip}{"\n"}{end}' | \
  xargs -I {} kubectl exec -it <existing-pod> -- nc -zv {} <port>
```

### Ingress网络连通性诊断
```bash
# 方式1: 集群外直接测试（最简）
INGRESS_IP=$(kubectl get ingress <ingress-name> -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -H "Host: <host>" http://$INGRESS_IP/
curl -H "Host: <host>" https://$INGRESS_IP/ -k

# 方式2: 使用现有Pod测试
curl命令可在任何有网络访问的环境中执行，不局限于K8s集群内

# 方式3: Ingress控制器内部测试
kubectl exec -n ingress-nginx -l app=ingress-controller -- \
  curl -H "Host: <host>" http://localhost/
```

### CoreDNS网络连通性验证
```bash
# 方式1: 使用现有Pod测试（推荐）
COREDNS_SERVICE_IP=$(kubectl get svc kube-dns -n kube-system -o jsonpath='{.spec.clusterIP}')
kubectl exec -it <existing-pod> -- nc -zv $COREDNS_SERVICE_IP 53
kubectl exec -it <existing-pod> -- sh -c "time nslookup kubernetes.default"

# 方式2: CoreDNS Pod内部测试
kubectl exec -n kube-system -l k8s-app=coredns -- nslookup google.com 127.0.0.1

# 方式3: 新建测试Pod
kubectl run coredns-test --rm -i --tty --image busybox -- nc -zv $COREDNS_SERVICE_IP 53
kubectl run dns-perf-test --rm -i --tty --image busybox -- \
  sh -c "time nslookup kubernetes.default"
```

### CSI存储网络连通性测试
```bash
# 方式1: 使用现有Pod测试（推荐）
STORAGE_BACKEND_IP=$(kubectl get pods -n kube-system -l app=csi-controller -o jsonpath='{.items[0].status.podIP}')
kubectl exec -it <existing-pod> -- nc -zv $STORAGE_BACKEND_IP <storage-port>

# 方式2: 存储插件Pod内部测试
kubectl exec -n kube-system -l app=csi-controller -- nc -zv <storage-backend-ip> <port>

# 方式3: 新建测试环境
kubectl run csi-connectivity-test --rm -i --tty --image busybox -- \
  nc -zv $STORAGE_BACKEND_IP <storage-port>
```

### 网络策略连通性验证
```bash
# 方式1: 使用现有Pod测试（推荐）
kubectl exec -it <existing-pod> -- nc -zv <target-pod-ip> <port>

# 方式2: 新建专门测试Pod
kubectl run allowed-test --rm -i --tty --image busybox -- \
  nc -zv <target-pod-ip> <port>

# 方式3: 策略效果对比测试
# 允许的流量
kubectl exec -it <allowed-pod> -- nc -zv <target> <port>
# 被阻止的流量
kubectl exec -it <blocked-pod> -- timeout 5 nc -zv <target> <port> || echo "流量被正确阻止"
```

### 网络故障诊断工具集
```bash
# 方式1: 使用现有Pod（基础工具）
kubectl exec -it <existing-pod> -- sh
# 在容器内执行:
# ping, nslookup, nc, curl, wget 等基础命令

# 方式2: Netshoot工具箱（高级诊断）
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- sh
# 可用工具: tcpdump, traceroute, mtr, nmap, dig 等

# 方式3: 多工具组合测试
kubectl exec -it <debug-pod> -- sh -c "
  echo '抓包开始'; tcpdump -i any -nn host <target-ip> -c 10 &
  echo '路由追踪'; traceroute <destination>
  echo '端口扫描'; nmap -p 80,443 <target-ip>
"
```

### 网络连通性自动化检查
```bash
# 方式1: 最简检查脚本（使用现有Pod）
cat > minimal-network-check.sh << 'MINIMAL'
#!/bin/bash
TEST_POD=$(kubectl get pods --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}' -n <namespace>)

echo "使用现有Pod: $TEST_POD"

echo "1. DNS测试:"
kubectl exec -n <namespace> $TEST_POD -- nslookup kubernetes.default

echo "2. 外部连通性:"
kubectl exec -n <namespace> $TEST_POD -- ping -c 3 8.8.8.8

echo "3. CoreDNS连通性:"
COREDNS_IP=$(kubectl get svc kube-dns -n kube-system -o jsonpath='{.spec.clusterIP}')
kubectl exec -n <namespace> $TEST_POD -- nc -zv $COREDNS_IP 53
MINIMAL

chmod +x minimal-network-check.sh

# 方式2: 完整检查脚本（新建Pod）
cat > comprehensive-network-check.sh << 'COMPREHENSIVE'
#!/bin/bash
echo "=== 完整网络连通性检查 ==="

echo "1. DNS解析测试:"
kubectl run dns-check --rm -i --tty --image busybox -- nslookup kubernetes.default

echo "2. API Server连通性:"
kubectl run api-check --rm -i --tty --image busybox -- \
  timeout 10 wget --spider --timeout=5 https://kubernetes.default/api/v1/namespaces

echo "3. CoreDNS状态:"
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide

echo "4. 网络插件状态:"
kubectl get pods -n kube-system -l k8s-app=calico-node -o wide
COMPREHENSIVE

chmod +x comprehensive-network-check.sh

# 方式3: 混合模式脚本
cat > hybrid-network-check.sh << 'HYBRID'
#!/bin/bash

echo "=== 混合模式网络检查 ==="

# 优先使用现有Pod
if TEST_POD=$(kubectl get pods --field-selector=status.phase=Running -o jsonpath='{.items[0].metadata.name}' -n default 2>/dev/null); then
  echo "使用现有Pod进行基础测试"
  kubectl exec $TEST_POD -- nslookup kubernetes.default
  kubectl exec $TEST_POD -- ping -c 3 8.8.8.8
else
  echo "未找到现有Pod，创建临时测试Pod"
  kubectl run temp-test --rm -i --tty --image busybox -- \
    sh -c "nslookup kubernetes.default && ping -c 3 8.8.8.8"
fi

# 关键组件状态检查始终新建Pod以确保准确性
kubectl run component-check --rm -i --tty --image busybox -- \
  sh -c "echo 'CoreDNS Pods:'; kubectl get pods -n kube-system -l k8s-app=kube-dns --no-headers | wc -l"
HYBRID

chmod +x hybrid-network-check.sh
```

### 网络连通性测试选择指南

#### 场景1: 日常快速检查
```bash
# 推荐使用现有Pod方式
kubectl exec -it <running-pod> -- nslookup kubernetes.default
kubectl exec -it <running-pod> -- ping -c 4 8.8.8.8
```

#### 场景2: 生产环境诊断
```bash
# 推荐混合模式：基础测试用现有Pod，深度诊断用专用工具
./hybrid-network-check.sh
```

#### 场景3: 完整环境验证
```bash
# 推荐新建专用测试环境
./comprehensive-network-check.sh
```

#### 场景4: 高级网络分析
```bash
# 推荐Netshoot工具箱
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- sh
```

### 性能对比说明

| 方式 | 资源消耗 | 启动速度 | 环境一致性 | 适用场景 |
|------|----------|----------|------------|----------|
| 现有Pod | 零额外消耗 | 立即执行 | 高 | 日常检查 |
| 新建Pod | 轻微消耗 | 数秒延迟 | 标准化 | 深度诊断 |
| Netshoot | 中等消耗 | 较快启动 | 专业化 | 高级分析 |
| 混合模式 | 动态消耗 | 智能选择 | 平衡 | 综合场景 |

### Service 详解操作
```bash
# 查看所有Service
kubectl get services [-n <namespace>]

# 查看Service详细信息
kubectl describe service <service-name> [-n <namespace>]

# 查看Service YAML配置
kubectl get service <service-name> -o yaml [-n <namespace>]

# 查看Service端点
kubectl get endpoints <service-name> [-n <namespace>]

# 查看Service关联的Pod
kubectl get pods -l <label-selector> [-n <namespace>]

# 测试Service ClusterIP连通性
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- curl <service-cluster-ip>:<port>

# 测试Service DNS解析
kubectl run tmp-shell --rm -i --tty --image busybox -- nslookup <service-name>.<namespace>.svc.cluster.local

# 临时暴露Service到本地端口
kubectl port-forward service/<service-name> <local-port>:<service-port>

# 创建临时测试Pod访问Service
kubectl run curl-test --rm -i --tty --image curlimages/curl -- curl http://<service-name>.<namespace>:<port>
```

### Service 类型管理
```bash
# 创建ClusterIP Service
kubectl expose deployment <deployment-name> --port=<port> --target-port=<target-port> --name=<service-name>

# 创建NodePort Service
kubectl expose deployment <deployment-name> --type=NodePort --port=<port> --target-port=<target-port> --name=<service-name>

# 创建LoadBalancer Service
kubectl expose deployment <deployment-name> --type=LoadBalancer --port=<port> --target-port=<target-port> --name=<service-name>

# 创建Headless Service
kubectl create service clusterip <service-name> --clusterip="None" --tcp=<port>:<target-port>

# 修改Service类型
kubectl patch service <service-name> -p '{"spec":{"type":"NodePort"}}'

# 查看NodePort分配的端口
kubectl get service <service-name> -o jsonpath='{.spec.ports[0].nodePort}'
```

### Ingress 操作
```bash
# 查看Ingress规则
kubectl get ingress [-n <namespace>]

# 查看Ingress详情
kubectl describe ingress <ingress-name> [-n <namespace>]

# 查看Ingress控制器
kubectl get pods -n <ingress-namespace> -l app=<ingress-controller-name>

# 测试Ingress访问
curl -H "Host: <host>" http://<ingress-controller-ip>

# 查看Ingress控制器日志
kubectl logs -n <ingress-namespace> deployment/<ingress-controller>

# 创建TLS Ingress
kubectl create secret tls <secret-name> --cert=<cert-file> --key=<key-file>
kubectl apply -f ingress-tls.yaml
```

### 网络策略
```bash
# 查看网络策略
kubectl get networkpolicies [-n <namespace>]

# 查看网络策略详情
kubectl describe networkpolicy <policy-name> [-n <namespace>]

# 测试网络连通性
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- sh

# 验证网络策略效果
kubectl exec <pod-name> -- nc -z <target-service> <port>
```

### DNS 调试与CoreDNS管理
```bash
# 测试内部DNS解析
kubectl run dns-test --rm -i --tty --image busybox -- nslookup kubernetes.default

# 查看CoreDNS配置
kubectl get configmap coredns -n kube-system -o yaml

# 编辑CoreDNS配置
kubectl edit configmap coredns -n kube-system

# 重启CoreDNS
kubectl rollout restart deployment/coredns -n kube-system

# 查看CoreDNS Pod状态
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 查看CoreDNS日志
kubectl logs -n kube-system -l k8s-app=kube-dns

# 测试Service DNS解析
kubectl exec <pod-name> -- nslookup <service-name>.<namespace>.svc.cluster.local

# 测试外部域名解析
kubectl exec <pod-name> -- nslookup google.com

# 查看DNS搜索域配置
kubectl exec <pod-name> -- cat /etc/resolv.conf

# 验证CoreDNS指标
kubectl exec -n kube-system <coredns-pod> -- curl http://localhost:9153/metrics

# 检查CoreDNS配置语法
kubectl get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}'
```

### nslookup 详细使用
```bash
# 基础DNS查询
kubectl exec <pod-name> -- nslookup <domain-name>

# 指定DNS服务器查询
kubectl exec <pod-name> -- nslookup <domain-name> <dns-server-ip>

# 查询特定记录类型
kubectl exec <pod-name> -- nslookup -type=A <domain-name>
kubectl exec <pod-name> -- nslookup -type=CNAME <domain-name>
kubectl exec <pod-name> -- nslookup -type=TXT <domain-name>

# 反向DNS查询
kubectl exec <pod-name> -- nslookup <ip-address>

# 查询所有记录
kubectl exec <pod-name> -- nslookup -type=ANY <domain-name>
```

### dig 命令详解
```bash
# 基础DNS查询
kubectl exec <pod-name> -- dig <domain-name>

# 查询特定记录类型
kubectl exec <pod-name> -- dig <domain-name> A
kubectl exec <pod-name> -- dig <domain-name> AAAA
kubectl exec <pod-name> -- dig <domain-name> MX
kubectl exec <pod-name> -- dig <domain-name> NS
kubectl exec <pod-name> -- dig <domain-name> TXT

# 指定DNS服务器
kubectl exec <pod-name> -- dig @<dns-server-ip> <domain-name>

# 详细输出模式
kubectl exec <pod-name> -- dig +trace <domain-name>
kubectl exec <pod-name> -- dig +short <domain-name>

# 查询统计信息
kubectl exec <pod-name> -- dig +stats <domain-name>

# 反向DNS查询
kubectl exec <pod-name> -- dig -x <ip-address>
```

### telnet 网络连通性测试
```bash
# 测试TCP端口连通性
kubectl exec <pod-name> -- telnet <host> <port>

# 测试Service端口
kubectl exec <pod-name> -- telnet <service-name>.<namespace> <port>

# 测试外部服务连通性
kubectl exec <pod-name> -- telnet google.com 80

# 批量端口测试
for port in 80 443 8080; do 
  echo "Testing port $port";
  kubectl exec <pod-name> -- timeout 5 telnet <host> $port;
done

# 持续连接测试
count=0;
while true; do
  ((count++));
  echo "Attempt $count";
  kubectl exec <pod-name> -- telnet <host> <port>;
  sleep 1;
done
```

### 高级网络诊断工具
```bash
# 使用netshoot工具箱
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- sh

# 在netshoot中进行综合诊断
# 查看网络接口
ip addr show

# 查看路由表
ip route show

# 测试网络延迟
ping <target-ip>

# 路径跟踪
traceroute <target-host>

# 端口扫描
nmap -p 80,443,8080 <target-host>

# 网络性能测试
iperf3 -c <target-host>

# SSL证书检查
openssl s_client -connect <host>:443 -servername <host>

# HTTP调试
curl -v http://<service-name>.<namespace>:<port>
```

### 网络故障排查完整流程
```bash
# 1. 基础连通性检查
kubectl exec <pod-name> -- ping -c 4 8.8.8.8
kubectl exec <pod-name> -- ping -c 4 kubernetes.default

# 2. DNS解析检查
kubectl exec <pod-name> -- nslookup kubernetes.default
kubectl exec <pod-name> -- dig kubernetes.default

# 3. Service连通性测试
kubectl exec <pod-name> -- telnet <service-cluster-ip> <port>
kubectl exec <pod-name> -- curl -v http://<service-name>.<namespace>:<port>

# 4. 网络策略验证
kubectl get networkpolicies -A
kubectl describe networkpolicy <policy-name> -n <namespace>

# 5. Endpoint检查
kubectl get endpoints <service-name> -n <namespace>
kubectl describe endpoints <service-name> -n <namespace>

# 6. iptables规则检查
kubectl exec -n kube-system <kube-proxy-pod> -- iptables-save | grep <service-name>

# 7. CoreDNS状态检查
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100

# 8. 网络插件状态
kubectl get pods -n kube-system -l <network-plugin-label>
```

### 常见网络问题诊断
```bash
# DNS解析失败
# 检查CoreDNS配置
kubectl get configmap coredns -n kube-system -o yaml
# 检查Pod的resolv.conf
kubectl exec <pod-name> -- cat /etc/resolv.conf

# Service无法访问
# 检查Endpoints
kubectl get endpoints <service-name>
# 检查Selector匹配
kubectl get service <service-name> -o jsonpath='{.spec.selector}'
kubectl get pods -l <selector-labels>

# 网络策略阻断
# 查看所有网络策略
kubectl get networkpolicies --all-namespaces
# 检查特定Pod受影响的策略
kubectl describe networkpolicy -A | grep -A 10 <pod-label>

# 端口不通
# 检查容器端口监听
kubectl exec <pod-name> -- netstat -tlnp
# 检查Service端口配置
kubectl describe service <service-name>
```

### 网络性能监控
```bash
# 网络延迟监控
kubectl exec <pod-name> -- ping -i 1 <target-host> | while read line; do 
  echo "$(date): $line";
done

# 带宽测试
kubectl exec <pod-name> -- iperf3 -c <target-host> -t 30

# 连接数统计
kubectl exec <pod-name> -- netstat -an | grep ESTABLISHED | wc -l

# 网络错误统计
kubectl exec <pod-name> -- netstat -i

# Socket状态分析
kubectl exec <pod-name> -- ss -tuln
```

### 网络故障排查
```bash
# 检查Pod网络状态
kubectl get pods -o wide [-n <namespace>]

# 查看网络插件状态
kubectl get pods -n kube-system -l k8s-app=<network-plugin>

# 检查网络策略影响
kubectl get networkpolicies -A

# 测试跨命名空间通信
kubectl exec <source-pod> -- curl http://<service-name>.<target-namespace>.svc.cluster.local

# 查看网络接口信息
kubectl exec <pod-name> -- ip addr show

# 检查iptables规则
kubectl exec -n kube-system <kube-proxy-pod> -- iptables-save | grep <service-name>
```

---

## 运行态监控与诊断

### Pod 运行状态深度分析
```bash
# 查看Pod详细状态
kubectl get pods -o wide [-n <namespace>]

# 查看Pod生命周期事件
kubectl describe pod <pod-name> [-n <namespace>]

# 实时监控Pod状态变化
kubectl get pods --watch [-n <namespace>]

# 查看Pod重启历史
kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[*].restartCount}'

# 分析Pod启动失败原因
kubectl get events --field-selector involvedObject.name=<pod-name> [--sort-by=.lastTimestamp]

# 查看Pod资源使用详情
kubectl top pod <pod-name> [-n <namespace>] --containers

# 监控Pod资源限制
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].resources}'

# 查看Pod健康检查配置
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].livenessProbe,.spec.containers[*].readinessProbe}'
```

### 容器运行时诊断
```bash
# 查看容器运行时状态
kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.containerRuntimeVersion}'

# 检查容器运行时健康
kubectl get nodes -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}'

# 查看节点上的Pod列表
kubectl get pods --field-selector spec.nodeName=<node-name> -A

# 检查容器镜像拉取状态
kubectl describe pod <pod-name> | grep -A 10 "Container ID"

# 查看容器日志（多容器Pod）
kubectl logs <pod-name> -c <container-name> [-n <namespace>]

# 实时查看所有容器日志
kubectl logs <pod-name> --all-containers=true -f
```

### 应用性能监控
```bash
# 查看应用响应时间
kubectl exec <pod-name> -- time curl -s http://localhost:<port>/health

# 监控应用内存使用
kubectl exec <pod-name> -- ps aux | grep <process-name>

# 查看JVM应用堆内存
kubectl exec <pod-name> -- jstat -gc <pid>

# 监控应用线程状态
kubectl exec <pod-name> -- jstack <pid>

# 查看应用GC日志
kubectl logs <pod-name> | grep "GC\|garbage collection"

# 应用连接池监控
kubectl exec <pod-name> -- netstat -an | grep :<port> | wc -l
```

### 节点健康检查
```bash
# 查看节点详细状态
kubectl describe node <node-name>

# 检查节点资源压力
kubectl get nodes -o jsonpath='{.items[*].status.conditions[?(@.type=="DiskPressure"||@.type=="MemoryPressure"||@.type=="PIDPressure")].message}'

# 查看节点容量和分配
kubectl get nodes -o jsonpath='{.items[*].status.capacity,.items[*].status.allocatable}'

# 监控节点组件状态
kubectl get componentstatuses

# 检查节点网络插件
kubectl get pods -n kube-system -l k8s-app=<network-plugin>

# 查看节点内核参数
kubectl exec -n kube-system <node-exporter-pod> -- cat /proc/sys/net/ipv4/ip_forward
```

### 集群组件健康检查
```bash
# 检查API Server状态
kubectl get --raw='/healthz?verbose'

# 检查etcd集群健康
kubectl exec -n kube-system etcd-<node-name> -- etcdctl endpoint health

# 查看调度器状态
kubectl get pods -n kube-system -l component=kube-scheduler

# 检查控制器管理器
kubectl get pods -n kube-system -l component=kube-controller-manager

# 监控核心组件日志
kubectl logs -n kube-system -l component=kube-apiserver --tail=100
```

### 运行态故障排查
```bash
# 查找CrashLoopBackOff的Pod
kubectl get pods --field-selector=status.phase=Running -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[*].restartCount}{"\n"}{end}' | sort -k2 -n

# 分析Pending状态Pod
kubectl get pods --field-selector=status.phase=Pending -o jsonpath='{.items[*].metadata.name}'

# 检查资源不足问题
kubectl describe nodes | grep -A 5 "Resource .* Requests"

# 查看Pod调度约束
kubectl get pod <pod-name> -o jsonpath='{.spec.affinity,.spec.tolerations,.spec.nodeSelector}'

# 监控Pod驱逐事件
kubectl get events --field-selector reason=Evicted -A
```

### 自动化健康检查脚本
```bash
# 创建集群健康检查脚本
cat > cluster-health-check.sh << 'EOF'
#!/bin/bash

echo "=== 集群健康检查报告 ==="
echo "检查时间: $(date)"

echo "\n1. 节点状态:"
kubectl get nodes

echo "\n2. 核心组件状态:"
kubectl get componentstatuses

echo "\n3. 异常Pod统计:"
kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded | wc -l

echo "\n4. 资源使用概况:"
kubectl top nodes

echo "\n5. 最近警告事件:"
kubectl get events --field-selector type=Warning --sort-by=.lastTimestamp -A | tail -10
EOF

chmod +x cluster-health-check.sh
./cluster-health-check.sh
```

### 存储管理与排查

### PV/PVC 深度操作
```bash
# 查看PersistentVolume
kubectl get pv

# 查看PersistentVolumeClaim
kubectl get pvc [-n <namespace>]

# 查看存储类
kubectl get storageclass

# 查看PV详情
kubectl describe pv <pv-name>

# 查看PVC详情
kubectl describe pvc <pvc-name> [-n <namespace>]

# 手动绑定PV到PVC
kubectl patch pv <pv-name> -p '{"spec":{"claimRef":{"namespace":"<namespace>","name":"<pvc-name>"}}}'

# 强制删除卡住的PVC
kubectl patch pvc <pvc-name> -p '{"metadata":{"finalizers":null}}'

# 查看PV/PVC绑定状态
kubectl get pv,pvc -A

# 检查存储类默认设置
kubectl get storageclass -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.storageclass\\.kubernetes\\.io/is-default-class}{"\n"}{end}'
```

### 存储性能监控
```bash
# 查看存储使用情况
kubectl exec <pod-name> -- df -h

# 测试存储读写性能
kubectl exec <pod-name> -- dd if=/dev/zero of=/mount-path/test bs=1M count=100 oflag=direct

# 监控存储I/O
kubectl exec <pod-name> -- iostat -x 1 5

# 查看存储挂载点
kubectl exec <pod-name> -- mount | grep <volume-name>

# 检查存储配额
kubectl get resourcequota [-n <namespace>]

# 存储延迟测试
kubectl exec <pod-name> -- time dd if=/mount-path/test of=/dev/null bs=1M count=100
```

### 存储故障排查
```bash
# 查看挂载失败的Pod
kubectl get pods --field-selector=status.phase=Pending -o jsonpath='{.items[*].metadata.name}' | xargs -I {} kubectl describe pod {}

# 检查PV/PVC状态异常
kubectl get pv --field-selector=status.phase!=Bound
kubectl get pvc --field-selector=status.phase!=Bound

# 查看存储插件状态
kubectl get pods -n kube-system -l app=<storage-plugin>

# 检查存储节点亲和性
kubectl get pv <pv-name> -o jsonpath='{.spec.nodeAffinity}'

# 存储容量监控
kubectl get pv -o jsonpath='{.items[*].spec.capacity.storage}'

# 查看存储卷详细信息
kubectl get pv <pv-name> -o yaml
```

### CSI存储插件诊断
```bash
# 查看CSI驱动状态
kubectl get csidrivers

# 查看CSI节点信息
kubectl get csinodes

# 检查CSI控制器Pod
kubectl get pods -n kube-system -l app=<csi-driver>

# 查看CSI卷附件
kubectl get volumeattachments

# CSI插件日志分析
kubectl logs -n kube-system -l app=<csi-driver> --tail=100

# 验证CSI功能
kubectl get csinodes -o jsonpath='{.items[*].spec.drivers[*].name}'
```

### 存储安全检查
```bash
# 检查存储权限设置
kubectl get pv <pv-name> -o jsonpath='{.spec.persistentVolumeReclaimPolicy}'

# 查看存储加密状态
kubectl get secret -n <namespace> | grep encryption

# 存储访问控制检查
kubectl get pvc <pvc-name> -o jsonpath='{.spec.accessModes}'

# 多租户存储隔离验证
kubectl get pv -o jsonpath='{.items[*].spec.claimRef.namespace}'

# 存储备份状态检查
kubectl get volumesnapshot [-n <namespace>]
```

### 存储优化建议
```bash
# 存储类型性能对比
kubectl top pods -n <namespace> | grep storage-intensive

# 存储压缩效果检查
kubectl exec <pod-name> -- du -sh /mount-path

# 存储快照管理
kubectl get volumesnapshotcontents

# 存储迁移准备
kubectl get pv -o jsonpath='{.items[*].spec.storageClassName}'

# 存储成本分析
kubectl get pv -o jsonpath='{.items[*].spec.capacity.storage,.items[*].spec.storageClassName}'
```

---

## 配置管理

### ConfigMap 操作
```bash
# 查看ConfigMap
kubectl get configmaps [-n <namespace>]

# 查看ConfigMap内容
kubectl get cm <configmap-name> -o yaml [-n <namespace>]

# 从文件创建ConfigMap
kubectl create configmap <configmap-name> --from-file=<file-path>

# 从键值对创建ConfigMap
kubectl create configmap <configmap-name> --from-literal=key1=value1 --from-literal=key2=value2

# 更新ConfigMap
kubectl patch configmap <configmap-name> -p='{"data":{"key":"new-value"}}'
```

### Secret 操作
```bash
# 查看Secret
kubectl get secrets [-n <namespace>]

# 查看Secret详情（Base64编码）
kubectl get secret <secret-name> -o yaml [-n <namespace>]

# 创建通用Secret
kubectl create secret generic <secret-name> --from-literal=username=admin --from-literal=password=secret

# 从文件创建Secret
kubectl create secret generic <secret-name> --from-file=<file-path>

# 从Docker配置创建镜像拉取Secret
kubectl create secret docker-registry <secret-name> \
  --docker-server=<registry-url> \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email>
```

---

## 安全管理与合规

### RBAC 权限深度管理
```bash
# 查看ServiceAccount
kubectl get serviceaccounts [-n <namespace>]

# 查看Role
kubectl get roles [-n <namespace>]

# 查看RoleBinding
kubectl get rolebindings [-n <namespace>]

# 查看ClusterRole
kubectl get clusterroles

# 查看ClusterRoleBinding
kubectl get clusterrolebindings

# 测试用户权限
kubectl auth can-i get pods --as=<user-name>
kubectl auth can-i get pods --as=system:serviceaccount:<namespace>:<sa-name>

# 查看用户角色绑定
kubectl get rolebindings,clusterrolebindings --all-namespaces -o wide

# 分析权限继承关系
kubectl get clusterroles -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep -E '(admin|edit|view)'
```

### 安全策略检查
```bash
# 查看Pod安全策略(PSP)
kubectl get podsecuritypolicies

# 检查网络策略
kubectl get networkpolicies --all-namespaces

# 查看安全上下文
kubectl get pod <pod-name> -o jsonpath='{.spec.securityContext,.spec.containers[*].securityContext}'

# 检查特权容器
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].securityContext.privileged}{"\n"}{end}' | grep true

# 验证运行用户
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].securityContext.runAsUser}'
```

### 证书与密钥管理
```bash
# 查看证书签名请求
kubectl get csr

# 批准证书请求
kubectl certificate approve <csr-name>

# 拒绝证书请求
kubectl certificate deny <csr-name>

# 查看Secret类型
kubectl get secrets --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.type}{"\n"}{end}'

# 检查TLS Secret
kubectl get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout

# 验证证书有效期
kubectl get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

### 安全扫描与合规检查
```bash
# 检查镜像漏洞
kubectl get pods --all-namespaces -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u

# 扫描不安全配置
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].securityContext.allowPrivilegeEscalation}{"\n"}{end}' | grep true

# 检查资源限制
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.limits}{"\n"}{end}' | grep -v '{}' 

# 验证网络安全策略
kubectl get networkpolicies --all-namespaces -o jsonpath='{.items[*].spec.policyTypes}'
```

### 安全日志分析
```bash
# 查看认证失败事件
kubectl get events --field-selector reason=FailedAuthentication -A

# 监控权限变更
kubectl get events --field-selector reason=PolicyRuleResolutionErrors -A

# 检查安全相关Pod
kubectl get pods --all-namespaces -l app in (falco,sysdig,anchore)

# 分析安全告警
kubectl logs -n <security-namespace> -l app=<security-tool> | grep -i "alert\|warning\|violation"

# 审计日志检查
kubectl get pods -n kube-system -l component=kube-apiserver -o jsonpath='{.items[*].spec.containers[*].command}' | grep audit
```

### 安全加固建议
```bash
# 检查默认ServiceAccount自动挂载
kubectl get serviceaccounts --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.automountServiceAccountToken}{"\n"}{end}' | grep -v false

# 验证API Server安全配置
kubectl get pod -n kube-system -l component=kube-apiserver -o jsonpath='{.items[*].spec.containers[*].command}'

# 检查etcd加密配置
kubectl get pod -n kube-system -l component=etcd -o jsonpath='{.items[*].spec.containers[*].command}' | grep encryption-provider

# 网络插件安全检查
kubectl get pods -n kube-system -l k8s-app in (calico,cilium,flannel) -o jsonpath='{.items[*].spec.containers[*].securityContext}'
```

### 合规性检查
```bash
# CIS基准检查
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].securityContext.readOnlyRootFilesystem}{"\n"}{end}' | grep -v true

# PCI DSS合规检查
kubectl get secrets --all-namespaces | grep -E "(tls|certificate|key)"

# GDPR数据保护检查
kubectl get configmaps --all-namespaces -o jsonpath='{.items[*].metadata.name}' | grep -i "personal\|user\|customer"

# HIPAA合规验证
kubectl get pods --all-namespaces -o jsonpath='{.items[*].spec.volumes[*].persistentVolumeClaim.claimName}' | xargs -I {} kubectl get pvc {} -o jsonpath='{.spec.resources.requests.storage}'
```

### 安全工具集成
```bash
# Falco安全监控
kubectl get pods -n falco -l app=falco
kubectl logs -n falco -l app=falco | grep -i "violation\|alert"

# Sysdig安全平台
kubectl get pods -n sysdig -l app=sysdig
kubectl exec -n sysdig <sysdig-pod> -- sysdig -M 30 -p "%evt.time %evt.type %proc.name" evt.type=open

# Anchore镜像扫描
kubectl get pods -n anchore -l app=anchore
kubectl port-forward -n anchore svc/anchore-api 8228:8228

curl -u admin:foobar -X GET http://localhost:8228/v1/images

# Aqua安全平台
kubectl get pods -n aqua -l app=aqua
kubectl logs -n aqua -l app=aqua | grep -i "threat\|malware"
```

---

## 监控诊断

### 资源监控
```bash
# 查看节点资源使用
kubectl top nodes

# 查看Pod资源使用
kubectl top pods [-n <namespace>]

# 按CPU排序查看Pod
kubectl top pods --sort-by=cpu

# 按内存排序查看Pod
kubectl top pods --sort-by=memory
```

### 日志分析
```bash
# 查看最近的日志
kubectl logs <pod-name> --tail=100

# 查看前一小时的日志
kubectl logs <pod-name> --since=1h

# 查看特定时间范围的日志
kubectl logs <pod-name> --since-time=2023-01-01T00:00:00Z --until-time=2023-01-01T01:00:00Z

# 查看多个容器日志
kubectl logs <pod-name> -c <container-name>

# 查看所有Pod的日志（按标签筛选）
kubectl logs -l app=<app-name> --all-containers=true
```

### 事件监控
```bash
# 查看所有事件
kubectl get events --sort-by='.lastTimestamp' -A

# 查看特定对象的事件
kubectl describe pod <pod-name>

# 实时监控事件
kubectl get events --watch -A

# 查看警告事件
kubectl get events --field-selector type=Warning -A
```

---

## 调试排错

### 常见问题诊断
```bash
# 检查Pod状态异常原因
kubectl describe pod <pod-name>

# 检查Pending状态的Pod
kubectl get pods --field-selector=status.phase=Pending

# 检查CrashLoopBackOff的Pod
kubectl get pods --field-selector=status.phase=Running -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[*].restartCount}{"\n"}{end}' | sort -k2 -n

# 查看Pod启动失败原因
kubectl get events --field-selector involvedObject.name=<pod-name>

# 检查资源不足问题
kubectl describe nodes | grep -A 5 "Resource .* Requests"
```

### 网络问题诊断
```bash
# 测试Pod间网络连通性
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- sh

# 在Pod内测试DNS
kubectl exec <pod-name> -- nslookup kubernetes.default

# 测试服务连接
kubectl exec <pod-name> -- curl <service-name>.<namespace>:<port>

# 查看网络策略影响
kubectl get networkpolicies -A
```

### 存储问题诊断
```bash
# 检查PV/PVC绑定状态
kubectl get pv,pvc -A

# 查看挂载问题
kubectl describe pod <pod-name> | grep -A 20 "Volumes:"

# 检查存储类配置
kubectl get storageclass -o yaml
```

---

## 升级维护

### 集群升级
```bash
# 查看升级计划
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.kubeletVersion}{"\n"}{end}'

# 节点平滑升级
kubectl drain <node-name> --ignore-daemonsets --delete-local-data
# 执行系统升级...
kubectl uncordon <node-name>
```

### 应用滚动升级
```bash
# 设置镜像并触发滚动升级
kubectl set image deployment/<deployment-name> <container-name>=<new-image>:<tag>

# 监控滚动升级进度
kubectl rollout status deployment/<deployment-name>

# 暂停滚动升级
kubectl rollout pause deployment/<deployment-name>

# 恢复滚动升级
kubectl rollout resume deployment/<deployment-name>

# 查看升级历史
kubectl rollout history deployment/<deployment-name>
```

---

## 安全加固

### 安全扫描
```bash
# 检查特权容器
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].securityContext.privileged}{"\n"}{end}' | grep true

# 检查以root运行的容器
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].securityContext.runAsNonRoot}{"\n"}{end}' | grep -v true

# 检查资源限制设置
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.limits}{"\n"}{end}'
```

### 安全配置检查
```bash
# 检查网络策略配置
kubectl get networkpolicies -A

# 检查RBAC配置
kubectl get clusterroles,clusterrolebindings -A

# 检查Secret管理
kubectl get secrets -A | wc -l
```

---

## 性能优化

### 资源调优
```bash
# 查看资源请求和限制
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.cpu}{"\t"}{.spec.containers[*].resources.limits.cpu}{"\n"}{end}'

# 批量调整Deployment资源
kubectl patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","resources":{"requests":{"cpu":"100m","memory":"128Mi"},"limits":{"cpu":"200m","memory":"256Mi"}}}]}}}}'

# 查看资源使用趋势
kubectl top nodes --sort-by=cpu
kubectl top pods --sort-by=memory -A
```

### 调度优化
```bash
# 查看节点亲和性配置
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.affinity}{"\n"}{end}'

# 查看Pod反亲和性
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.topologySpreadConstraints}{"\n"}{end}'

# 检查污点容忍度
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.tolerations}{"\n"}{end}'
```

---

## AI/ML 特殊命令

### GPU 管理
```bash
# 查看GPU节点
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.nvidia\.com/gpu}{"\n"}{end}'

# 查看GPU使用情况
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.nvidia\.com/gpu}{"\n"}{end}'

# 测试GPU可用性
kubectl run gpu-test --rm -i --tty --image=nvidia/cuda:11.0-base -- nvidia-smi
```

### 训练任务管理
```bash
# 查看训练Pod状态
kubectl get pods -l app=training-job -A

# 监控训练进度日志
kubectl logs -l app=training-job -f --tail=100

# 查看训练资源使用
kubectl top pods -l app=training-job -A

# 批量删除训练任务
kubectl delete pods -l app=training-job --force --grace-period=0
```

### 模型服务管理
```bash
# 查看推理服务
kubectl get pods -l app=inference-service -A

# 测试模型API
kubectl port-forward svc/<inference-service> 8080:80
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"input": "test"}'

# 监控推理延迟
kubectl logs -l app=inference-service --tail=1000 | grep "latency"
```

---

## 故障应急处理

### 紧急故障诊断
```bash
# 快速集群健康检查
cat > emergency-check.sh << 'EOF'
#!/bin/bash
echo "🚨 紧急故障诊断报告"
echo "时间: $(date)"

echo "\n1. 节点状态快速检查:"
kubectl get nodes | grep -v Ready || echo "❌ 发现异常节点!"

echo "\n2. 核心组件状态:"
kubectl get componentstatuses | grep -v Healthy || echo "❌ 组件异常!"

echo "\n3. 关键Pod状态:"
kubectl get pods -n kube-system | grep -E "(kube-apiserver|etcd|kube-controller)" | grep -v Running || echo "❌ 核心组件Pod异常!"

echo "\n4. 严重事件检查:"
kubectl get events --field-selector type=Warning --sort-by=.lastTimestamp -A | tail -5
EOF

chmod +x emergency-check.sh
./emergency-check.sh

# 一键获取所有异常信息
kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded -o wide

# 快速查看最近错误日志
kubectl get events --field-selector type=Warning --sort-by=.lastTimestamp -A | tail -10

# 检查API Server可用性
timeout 10 kubectl get --raw='/healthz' || echo "❌ API Server无响应!"
```

### Pod故障应急处理
```bash
# 快速重启异常Pod
kubectl delete pod <pod-name> --force --grace-period=0

# 批量重启CrashLoopBackOff的Pod
kubectl get pods --field-selector=status.phase=Running -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[*].restartCount}{"\n"}{end}' | awk '$2 > 10 {print $1}' | xargs -r kubectl delete pod --force --grace-period=0

# 紧急扩容Deployment应对流量激增
kubectl scale deployment <deployment-name> --replicas=<new-count>

# 快速回滚到上一版本
kubectl rollout undo deployment/<deployment-name>

# 紧急暂停滚动更新
kubectl rollout pause deployment/<deployment-name>
```

### 节点故障应急
```bash
# 紧急驱逐节点上的所有Pod
kubectl drain <node-name> --ignore-daemonsets --delete-local-data --force

# 快速查看节点资源压力
kubectl describe node <node-name> | grep -A 10 "Conditions:"

# 检查节点磁盘使用情况
kubectl get nodes -o jsonpath='{.items[*].status.conditions[?(@.type=="DiskPressure")].status}'

# 紧急标记节点为不可调度
kubectl cordon <node-name>

# 批量处理NotReady节点
kubectl get nodes | grep NotReady | awk '{print $1}' | xargs -I {} kubectl cordon {}
```

### 网络故障应急
```bash
# 快速测试CoreDNS是否正常
kubectl run dns-test --rm -i --tty --image busybox -- nslookup kubernetes.default

# 重启CoreDNS解决DNS解析问题
kubectl rollout restart deployment/coredns -n kube-system

# 检查网络插件Pod状态
kubectl get pods -n kube-system -l k8s-app=<network-plugin>

# 紧急刷新iptables规则
kubectl exec -n kube-system <kube-proxy-pod> -- iptables-restore < /tmp/iptables.rules

# 快速测试Service连通性
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- curl -m 5 http://<service-name>.<namespace>:<port>
```

### 存储故障应急
```bash
# 快速检查PV/PVC绑定状态
kubectl get pv,pvc --all-namespaces | grep -E "(Failed|Pending|Lost)"

# 强制删除卡住的PVC
kubectl patch pvc <pvc-name> -p '{"metadata":{"finalizers":null}}'

# 检查存储插件状态
kubectl get pods -n kube-system -l app=<storage-plugin> | grep -v Running

# 紧急重新挂载存储卷
kubectl delete pod <pod-name> && kubectl get pod <pod-name> -o yaml | kubectl replace --force -f -
```

### 应急联系人和流程
```bash
# 创建应急响应模板
cat > incident-response-template.yaml << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: incident-response-pod
  labels:
    purpose: emergency-debug
spec:
  containers:
  - name: debug-container
    image: nicolaka/netshoot
    command: ["sleep", "3600"]
  restartPolicy: Never
EOF

# 应急检查清单
echo "应急响应检查清单:"
echo "1. ✅ 集群节点状态"
echo "2. ✅ 核心组件运行情况"
echo "3. ✅ 关键应用Pod状态"
echo "4. ✅ 网络连通性测试"
echo "5. ✅ 存储系统健康检查"
echo "6. ✅ 监控告警状态"
echo "7. ✅ 日志异常分析"
echo "8. ✅ 备份恢复准备"
```

## 容灾切换演练

### 多集群容灾准备
```bash
# 集群状态同步检查
cat > dr-readiness-check.sh << 'EOF'
#!/bin/bash
echo "=== 容灾就绪性检查 ==="

echo "\n📋 主集群状态:"
kubectl config use-context primary-cluster
kubectl get nodes -o wide
echo "主集群应用状态:"
kubectl get deployments,statefulsets -A | head -10

echo "\n📋 备份集群状态:"
kubectl config use-context backup-cluster
kubectl get nodes -o wide
echo "备份集群资源配额:"
kubectl get resourcequotas -A

# 检查关键配置同步状态
echo "\n📋 配置同步检查:"
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  echo "Namespace: $ns"
  kubectl get configmaps -n $ns --context=primary-cluster | head -5
  kubectl get secrets -n $ns --context=backup-cluster | head -5
done
EOF

chmod +x dr-readiness-check.sh

# 多集群上下文管理
kubectl config get-contexts | grep -E "(primary|backup|dr)"

# 集群间资源配置对比
kubectl get deployments --context=primary-cluster -A -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | sort > primary-deployments.txt
kubectl get deployments --context=backup-cluster -A -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | sort > backup-deployments.txt
diff primary-deployments.txt backup-deployments.txt
```

### 故障切换演练
```bash
# 模拟主集群故障
cat > simulate-failure.sh << 'EOF'
#!/bin/bash

echo "⚠️  模拟主集群故障场景"

echo "1. 标记主集群为不可用"
kubectl config use-context primary-cluster
kubectl get nodes | awk 'NR>1 {print $1}' | xargs -I {} kubectl cordon {}

# 模拟API Server无响应
echo "2. 模拟API Server故障"
echo "执行: kubectl proxy --port=0 & kill $!"

# 切换到备份集群
echo "3. 自动切换到备份集群"
kubectl config use-context backup-cluster
echo "✅ 已切换到备份集群"

# 验证服务可用性
echo "4. 验证关键服务状态"
kubectl get deployments -n production | grep -E "(frontend|backend|database)"
EOF

chmod +x simulate-failure.sh

# 自动故障检测和切换
cat > auto-failover.sh << 'EOF'
#!/bin/bash
PRIMARY_CONTEXT="primary-cluster"
BACKUP_CONTEXT="backup-cluster"

# 检查主集群健康状态
check_primary_cluster() {
  kubectl config use-context $PRIMARY_CONTEXT
  if kubectl get nodes --request-timeout=5s >/dev/null 2>&1; then
    NODES_READY=$(kubectl get nodes 2>/dev/null | grep -c " Ready ")
    TOTAL_NODES=$(kubectl get nodes 2>/dev/null | wc -l)
    if [ "$NODES_READY" -ge "$((TOTAL_NODES * 3/4))" ]; then
      return 0  # 健康
    fi
  fi
  return 1  # 不健康
}

# 执行故障切换
failover_to_backup() {
  echo "🔄 执行故障切换到备份集群"
  kubectl config use-context $BACKUP_CONTEXT
  
  # 启动关键应用
  kubectl get deployments -n production -o name | xargs -I {} kubectl scale {} --replicas=1
  
  echo "✅ 故障切换完成"
}

# 主循环
while true; do
  if ! check_primary_cluster; then
    echo "❌ 检测到主集群故障"
    failover_to_backup
    break
  fi
  sleep 30
done
EOF

chmod +x auto-failover.sh
```

### 数据同步和一致性检查
```bash
# ETCD数据备份和恢复
# 备份ETCD
cat > etcd-backup.sh << 'EOF'
#!/bin/bash
ETCD_POD=$(kubectl get pods -n kube-system -l component=etcd -o jsonpath='{.items[0].metadata.name}')

# 创建备份
ekubectl exec -n kube-system $ETCD_POD -- \
  etcdctl snapshot save /tmp/etcd-snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# 复制备份到本地
kubectl cp kube-system/$ETCD_POD:/tmp/etcd-snapshot.db ./etcd-backup-$(date +%Y%m%d-%H%M%S).db
EOF

chmod +x etcd-backup.sh

# 验证数据一致性
check_data_consistency() {
  PRIMARY_NS="production"
  BACKUP_NS="production"
  
  echo "🔍 数据一致性检查"
  
  # 检查ConfigMap一致性
  kubectl get configmaps -n $PRIMARY_NS --context=primary-cluster -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | sort > primary-cms.txt
  kubectl get configmaps -n $BACKUP_NS --context=backup-cluster -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | sort > backup-cms.txt
  
  echo "ConfigMap差异:"
  diff primary-cms.txt backup-cms.txt || echo "发现差异"
  
  # 检查Secret一致性
  kubectl get secrets -n $PRIMARY_NS --context=primary-cluster --no-headers | wc -l
  kubectl get secrets -n $BACKUP_NS --context=backup-cluster --no-headers | wc -l
}

# 存储卷数据同步
sync_pv_data() {
  echo "🔄 同步持久化数据"
  
  # 使用Velero备份恢复示例
  velero backup create dr-backup-$(date +%Y%m%d-%H%M%S) \
    --include-namespaces=production \
    --snapshot-volumes=true
  
  # 在备份集群恢复
  velero restore create --from-backup dr-backup-$(date +%Y%m%d-%H%M%S) \
    --namespace-mappings production:production-dr
}
```

### 容灾演练报告
```bash
# 生成演练报告
cat > dr-exercise-report.sh << 'EOF'
#!/bin/bash
REPORT_FILE="dr-exercise-report-$(date +%Y%m%d-%H%M%S).md"

cat > $REPORT_FILE << 'REPORT'
# 容灾演练报告

## 演练基本信息
- 演练时间: $(date)
- 参与人员: $USER
- 演练类型: 完整故障切换演练

## 演练步骤记录

### 1. 初始状态检查
```bash
# 主集群状态
$(kubectl get nodes --context=primary-cluster)

# 备份集群状态
$(kubectl get nodes --context=backup-cluster)
```

### 2. 故障注入
- 模拟主集群API Server无响应
- 模拟关键节点失效
- 模拟网络分区

### 3. 故障检测
- 监控系统告警触发
- 健康检查失败
- 自动切换机制激活

### 4. 切换执行
- 上下文自动切换
- 应用在备份集群启动
- 服务恢复验证

### 5. 服务验证
- 关键接口可用性测试
- 数据一致性校验
- 性能基准对比

## 发现问题
1. [ ] 切换时间超过SLA要求
2. [ ] 部分配置未同步
3. [ ] 监控告警延迟

## 改进建议
1. 优化健康检查间隔
2. 完善配置同步机制
3. 增强监控告警灵敏度

## 演练结论
✅ 演练完成时间: $(date)
✅ 主要目标达成: 是/否
✅ 下次演练计划: 30天后
REPORT

echo "✅ 容灾演练报告已生成: $REPORT_FILE"
EOF

chmod +x dr-exercise-report.sh
```
```bash
# 批量删除Evicted状态的Pod
kubectl get pods --field-selector=status.phase=Failed -o name | xargs kubectl delete

# 批量重启Deployment
kubectl get deployments -o name | xargs -I {} kubectl rollout restart {}

# 批量添加标签
kubectl label pods --all app=new-label -n <namespace>

# 批量删除资源
kubectl delete pods,svc,deployments -l app=test-app

# 批量查看资源状态
kubectl get pods,svc,deployments -n <namespace> -o wide

# 批量导出资源配置
kubectl get deployments -o yaml | kubectl neat > deployments-backup.yaml
```

### 上下文管理
```bash
# 查看所有上下文
kubectl config get-contexts

# 切换上下文
kubectl config use-context <context-name>

# 设置默认命名空间
kubectl config set-context --current --namespace=<namespace-name>

# 重命名上下文
kubectl config rename-context <old-name> <new-name>

# 查看当前配置
kubectl config view

# 删除上下文
kubectl config delete-context <context-name>
```

### 高级调试技巧
```bash
# 创建专用调试环境
kubectl run debug-env --image=nicolaka/netshoot --rm -it -- sh

# 多集群上下文切换
kubectl config use-context production && kubectl get nodes
kubectl config use-context staging && kubectl get nodes

# 资源使用率排序
kubectl top pods --sort-by=cpu -A | head -20
kubectl top pods --sort-by=memory -A | head -20

# 快速定位问题Pod
kubectl get pods --field-selector=status.phase!=Running -A -o wide

# 查看详细事件日志
kubectl get events --sort-by=.lastTimestamp -A --watch
```

### 性能分析工具
```bash
# 系统性能监控
kubectl top nodes
kubectl top pods -A

# 资源请求与限制对比
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.cpu}{"\t"}{.spec.containers[*].resources.limits.cpu}{"\n"}{end}'

# 内存泄漏检测
kubectl exec <pod-name> -- ps aux --sort=-%mem | head -10

# 网络性能分析
kubectl exec <pod-name> -- sar -n DEV 1 5

# 磁盘I/O监控
kubectl exec <pod-name> -- iotop -o
```

### 故障恢复命令
```bash
# 快速恢复服务
kubectl rollout undo deployment/<deployment-name>

# 重建有问题的Pod
kubectl delete pod <pod-name> --force --grace-period=0

# 恢复配置文件
kubectl apply -f backup-config.yaml

# 重启整个应用
kubectl rollout restart deployment/<deployment-name> -n <namespace>

# 清理僵尸资源
kubectl get pods --field-selector=status.phase=Failed -o name | xargs kubectl delete
```

### 别名设置（推荐）
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias k='kubectl'
alias kgn='kubectl get nodes'
alias kgp='kubectl get pods'
alias kdp='kubectl describe pod'
alias kl='kubectl logs'
alias ke='kubectl exec -it'

# 更多别名
alias kga='kubectl get all'
alias kgpa='kubectl get pods --all-namespaces'
alias kgpw='kubectl get pods --watch'
alias ktp='kubectl top pods'
alias ktn='kubectl top nodes'
alias kctx='kubectl config use-context'
alias kns='kubectl config set-context --current --namespace'

# 生产环境安全别名
alias kprod='kubectl config use-context production'
alias kstaging='kubectl config use-context staging'
```

### 自动化脚本集合
```bash
# 创建集群状态检查脚本
cat > cluster-status.sh << 'EOF'
#!/bin/bash

echo "=== Kubernetes集群状态报告 ==="
echo "生成时间: $(date)"

echo "\n📋 节点状态:"
kubectl get nodes -o wide

echo "\n⚠️  异常Pod:"
kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded

echo "\n📊 资源使用TOP 10 (CPU):"
kubectl top pods --sort-by=cpu --all-namespaces | head -11

echo "\n📊 资源使用TOP 10 (内存):"
kubectl top pods --sort-by=memory --all-namespaces | head -11

echo "\n🔔 最近警告事件:"
kubectl get events --field-selector type=Warning --sort-by=.lastTimestamp --all-namespaces | tail -10
EOF

chmod +x cluster-status.sh

# 创建Pod健康检查脚本
cat > pod-health-check.sh << 'EOF'
#!/bin/bash

NAMESPACE=${1:-default}
echo "检查命名空间: $NAMESPACE"

echo "\n🔍 Pod健康状态检查:"
kubectl get pods -n $NAMESPACE -o wide

echo "\n🔄 重启次数统计:"
kubectl get pods -n $NAMESPACE -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[*].restartCount}{"\n"}{end}' | sort -k2 -nr | head -10

echo "\n🌡️  资源使用情况:"
kubectl top pods -n $NAMESPACE
EOF

chmod +x pod-health-check.sh
```

---

> **📌 注意事项**：
> - 生产环境中执行删除操作前务必确认
> - 使用 `--dry-run=client -o yaml` 预览变更
> - 重要操作建议先在测试环境验证
> - 定期备份关键资源配置
> - 遵循最小权限原则配置RBAC
> - 使用别名前确保团队统一规范
> - 定期更新kubectl版本以获得最新功能
> - 敏感操作建议使用审计日志记录
> - 大规模操作前先在小范围测试
> - 保持命令历史记录以便问题追溯

## 运维场景补充命令

### 集群联邦和多集群管理
```bash
# 查看集群联邦状态
kubectl get federatedclusters -A

# 跨集群资源管理
kubectl config use-context cluster1 && kubectl get pods
kubectl config use-context cluster2 && kubectl get pods

# 多集群资源同步检查
for context in $(kubectl config get-contexts -o name); do
  echo "=== 集群: $context ==="
  kubectl config use-context $context
  kubectl get nodes --no-headers | wc -l
  kubectl get pods --all-namespaces --no-headers | wc -l
done

# 联邦Deployment管理
kubectl get federateddeployments -A
kubectl describe federateddeployment <name> -n <namespace>

# 跨集群服务发现
kubectl get federatedservices -A
kubectl get federatedserviceplacements -A
```

### Helm和包管理
```bash
# Helm仓库管理
helm repo list
helm repo update
helm search repo <chart-name>

# Release管理
helm list -A
helm status <release-name> -n <namespace>

# Helm Chart部署
helm install <release-name> <chart-name> --namespace <namespace>
helm upgrade <release-name> <chart-name> --namespace <namespace>
helm rollback <release-name> <revision> -n <namespace>

# Helm值配置检查
helm get values <release-name> -n <namespace>
helm get manifest <release-name> -n <namespace>

# Helm Chart模板调试
helm template <chart-name> --debug
helm lint <chart-directory>
```

### Operator和自定义资源
```bash
# 查看自定义资源定义
kubectl get crds
kubectl explain <crd-name>

# Operator状态检查
kubectl get pods -n <operator-namespace> -l app=<operator-name>

# 自定义资源实例管理
kubectl get <custom-resource> [-n <namespace>]
kubectl describe <custom-resource> <instance-name> [-n <namespace>]

# Operator日志分析
kubectl logs -n <operator-namespace> deployment/<operator-deployment> --tail=100

# 自定义控制器状态
kubectl get controllerrevisions -A
kubectl get statefulsets -o jsonpath='{.items[*].metadata.name}'
```

### 服务网格扩展
```bash
# Istio网格配置
istioctl analyze -A
istioctl proxy-config clusters <pod-name>.<namespace>
istioctl proxy-config routes <pod-name>.<namespace>
istioctl proxy-config listeners <pod-name>.<namespace>

# 服务网格流量管理
kubectl get gateways -A
kubectl get virtualservices -A
kubectl get destinationrules -A

# 网格安全配置
kubectl get authorizationpolicies -A
kubectl get peerauthentications -A
kubectl get requestauthentications -A

# 服务网格监控
istioctl dashboard prometheus
istioctl dashboard grafana
istioctl dashboard kiali

# 网格故障排除
istioctl proxy-status
istioctl authz check <pod-name>.<namespace>
```

### 事件驱动和消息队列
```bash
# Kafka Operator管理
kubectl get kafkas -A
kubectl get kafkausers -A
kubectl get kafkatopics -A

# RabbitMQ集群状态
kubectl get rabbitmqclusters -A
kubectl get rabbitmqusers -A

# Redis集群管理
kubectl get redisfailovers -A
kubectl get redisclusters -A

# 消息队列监控
kubectl port-forward svc/<mq-service> 15672:15672  # RabbitMQ UI
kubectl port-forward svc/<kafka-service> 9092:9092  # Kafka
```

### 数据库和中间件
```bash
# MySQL Operator
kubectl get mysqls -A
kubectl get mysqlbackups -A
kubectl get mysqlrestores -A

# PostgreSQL Operator
kubectl get postgresqls -A
kubectl get pgclusters -A

# MongoDB Operator
kubectl get mongodb -A
kubectl get mongodbcommunity -A

# Elasticsearch集群
kubectl get elasticsearches -A
kubectl get kibanas -A

# 中间件状态检查
kubectl get statefulsets -l app in (mysql,postgresql,mongodb,elasticsearch) -A
```

### 监控告警系统
```bash
# Prometheus Operator
kubectl get prometheuses -A
kubectl get servicemonitors -A
kubectl get prometheusrules -A

# Alertmanager配置
kubectl get alertmanagers -A
kubectl get alertmanagerconfigs -A

# Grafana仪表板
kubectl get grafanas -A
kubectl port-forward svc/grafana 3000:3000

# 监控组件状态
kubectl get pods -n monitoring -l app in (prometheus,alertmanager,grafana)

# 告警规则检查
kubectl get prometheusrules -A -o jsonpath='{.items[*].spec.groups[*].name}'
```

### 日志收集系统
```bash
# Fluentd/Fluent Bit
kubectl get fluentdconfigs -A
kubectl get fluentbitconfigs -A
kubectl get fluentdstatefulsets -A

# Loki日志系统
kubectl get lokis -A
kubectl get promtails -A

# EFK/ELK堆栈
kubectl get elasticsearches -A
kubectl get kibanas -A
kubectl get fluentds -A

# 日志收集器状态
kubectl get daemonsets -n logging -l app in (fluentd,fluent-bit,logstash)

# 日志配置检查
kubectl get configmaps -n logging -l app in (fluentd,fluent-bit)
```

### CI/CD和GitOps
```bash
# Argo CD管理
kubectl get applications -A
kubectl get appprojects -A
argocd app list
argocd app sync <app-name>

# Flux CD
kubectl get helmreleases -A
kubectl get kustomizations -A
kubectl get gitrepositories -A

# Tekton流水线
kubectl get pipelines -A
kubectl get pipelineruns -A
kubectl get taskruns -A

# Jenkins Operator
kubectl get jenkins -A
kubectl get jenkinsimages -A

# GitOps状态检查
kubectl get gitopssystems -A
kubectl get gitopsconfigs -A
```

### 安全和合规工具
```bash
# Falco安全监控
kubectl get falcos -A
kubectl get falcorules -A
kubectl logs -n falco -l app=falco --tail=100

# Kyverno策略引擎
kubectl get clusterpolicies
kubectl get policies -A
kyverno apply <policy-file> --resource <resource-file>

# Trivy镜像扫描
trivy image <image-name>
trivy k8s --report summary cluster

# Aqua Security
kubectl get aquaconfigs -A
kubectl get aquascans -A

# 安全合规检查
kubectl get podsecuritypolicies
kubectl get clusterconfigaudits -A
```

### 备份和灾难恢复
```bash
# Velero备份
velero backup create <backup-name> --include-namespaces <namespace>
velero backup describe <backup-name>
velero restore create --from-backup <backup-name>

# Kasten K10
kubectl get k10s -A
kubectl get backupactions -A
kubectl get restoreactions -A

# Stash备份
kubectl get backupconfigurations -A
kubectl get restoresessions -A

# 备份状态检查
kubectl get backups -A
kubectl get restores -A

# 存储快照管理
kubectl get volumesnapshots -A
kubectl get volumesnapshotcontents
```

### 性能和容量规划
```bash
# 集群容量分析
kubectl describe nodes | grep -A 5 "Allocated resources"

# 资源请求vs限制分析
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.cpu}{"\t"}{.spec.containers[*].resources.limits.cpu}{"\n"}{end}'

# 节点资源使用率
kubectl top nodes --sort-by=cpu | head -10
kubectl top nodes --sort-by=memory | head -10

# 应用资源优化建议
kubectl get hpa -A
kubectl get vpa -A

# 集群伸缩建议
kubectl get clusterautoscaler -A
```

### 开发者工具集成
```bash
# Skaffold开发
skaffold dev
skaffold run
skaffold debug

# Telepresence调试
telepresence connect
telepresence intercept <deployment-name>

# Stern日志查看
stern <pod-name> -n <namespace>
stern "<app-name>-.*" --tail 100

# K9s终端UI
k9s
k9s --namespace <namespace>

# Popeye集群扫描
popeye
popeye --save --out html
```

### 自动化运维平台
```bash
# Rancher管理
kubectl get clusters.management.cattle.io -A
kubectl get projects.management.cattle.io -A

# OpenShift
oc get projects
oc get dc -A
oc get builds -A

# Tanzu Kubernetes Grid
kubectl get tanzukubernetesclusters -A
kubectl get tanzukubernetesreleases -A

# 云原生平台
kubectl get cloudnativeplatforms -A
kubectl get managedclusters -A

# 平台组件状态
kubectl get platformcomponents -A
kubectl get platformoperators -A
```

### 现代可观测性工具
```bash
# OpenTelemetry Collector
kubectl get opentelemetrycollectors -A
kubectl get instrumentations -A

# Tempo分布式追踪
kubectl get tempoes -A
kubectl port-forward svc/tempo 3100:3100

# Thanos长期存储
kubectl get thanosrulers -A
kubectl get thanosstores -A

# Mimir指标存储
kubectl get mimirs -A

# Pyroscope持续性能分析
kubectl get pyroscopes -A
kubectl port-forward svc/pyroscope 4040:4040
```

### 边缘计算和多云管理
```bash
# KubeEdge边缘计算
kubectl get edgeclusters -A
kubectl get edgedevices -A

# OpenYurt
kubectl get yurthubs -A
kubectl get yurtapps -A

# Karmada多云管理
kubectl get federatedclusters -A
kubectl get propagationpolicies -A

# Cluster API
kubectl get clusters.cluster.x-k8s.io -A
kubectl get machinedeployments.cluster.x-k8s.io -A

# Crossplane云资源管理
kubectl get providers -A
kubectl get compositions -A
kubectl get claims -A
```

### GitOps和声明式管理
```bash
# Flux CD
flux check
flux get sources git
flux get kustomizations -A
flux get helmreleases -A

# Argo Rollouts
kubectl get rollouts -A
kubectl argo rollouts list rollouts -A

# Kustomize
kustomize build <kustomization-dir>
kustomize cfg tree <dir> --graph-structure=directory

# Carvel工具套件
ytt -f <template-file>
vendir sync
kbld -f <config-file>
imgpkg copy -i <image> --to-repo <repo>
```

### 安全和合规增强
```bash
# SPIFFE/SPIRE身份管理
kubectl get spiffeids -A
kubectl get clusterSPIFFEIDs -A

# OPA/Gatekeeper策略管理
kubectl get constrainttemplates
kubectl get k8srequiredlabels.constraints.gatekeeper.sh

# cert-manager证书管理
kubectl get certificates -A
kubectl get certificaterequests -A
kubectl get issuers -A

# Sealed Secrets加密
kubectl get sealedsecrets -A
kubeseal --fetch-cert > pub-cert.pem

# Vault集成
kubectl get vaults -A
kubectl get vaultauths -A
kubectl get vaultconnections -A
```

### 服务网格现代化
```bash
# Linkerd服务网格
linkerd check
linkerd viz stat deploy
linkerd viz tap deploy/<deployment-name>

# Consul Connect
kubectl get servicedefaults -A
kubectl get serviceintentions -A

# Cilium Service Mesh
cilium status
cilium service list

# Network Service Mesh
kubectl get networkservicendpoints -A
kubectl get networkservices -A
```

### AI/ML平台集成
```bash
# Kubeflow Pipelines
kubectl get workflows -A
kubectl get scheduledworkflows -A

# KServe模型服务
kubectl get inferenceservices -A
kubectl get servingruntimes -A

# Volcano批处理
kubectl get queues -A
kubectl get elasticresourcequotas -A

# Spark Operator
kubectl get sparkapplications -A
kubectl get scheduledsparkapplications -A

# Ray集群
kubectl get rayclusters -A
kubectl get rayservices -A
```

### 数据库和中间件Operator
```bash
# Vitess数据库编排
kubectl get vitessclusters -A
kubectl get vitesskeyspaces -A

# CockroachDB Operator
kubectl get cockroachdbs -A

# Etcd Operator
kubectl get etcdclusters -A

# Redis Operator
kubectl get redisclusters -A
kubectl get redisfailovers -A

# Kafka Strimzi
kubectl get kafkas -A
kubectl get kafkatopics -A
kubectl get kafkausers -A
```

### 存储和备份现代化
```bash
# Rook Ceph存储
kubectl get cephclusters -A
kubectl get cephblockpools -A
kubectl get cephfilesystems -A

# Longhorn存储
kubectl get longhornsettings -A
kubectl get longhornvolumes -A

# MinIO对象存储
kubectl get tenants.minio.min.io -A

# Kanister备份框架
kubectl get profiles.config.kanister.io -A
kubectl get actions.cr.kanister.io -A

# Restic备份
restic snapshots
restic check
restic prune
```

### 网络和安全增强
```bash
# Cilium网络和安全
cilium connectivity test
cilium status --verbose
cilium identity list

# Calico网络策略
calicoctl get networkpolicies -A
calicoctl get globalnetworkpolicies
calicoctl ipam show

# Multus CNI
kubectl get network-attachment-definitions -A

# MetalLB负载均衡
kubectl get IPAddressPools -A
kubectl get L2Advertisements -A

# ExternalDNS
kubectl get dnsendpoints -A
kubectl get dnsrecords -A
```

### 开发者体验工具
```bash
# Tilt开发环境
tilt up
tilt down
tilt dump engine

# DevSpace开发
devspace dev
devspace deploy
devspace purge

# Garden开发平台
garden deploy
garden test
garden dev

# Nocalhost开发
nh install
nh uninstall
nh dev start <workload>

# Okteto开发
okteto up
okteto down
okteto deploy
```

### 监控和告警增强
```bash
# kube-state-metrics
kubectl get ksmresources -A

# Metrics Server增强
kubectl get nodemetrics -A
kubectl get podmetrics -A

# kube-prometheus-stack
kubectl get prometheuses.monitoring.coreos.com -A
kubectl get servicemonitors.monitoring.coreos.com -A
kubectl get prometheusrules.monitoring.coreos.com -A

# kubevious配置验证
kubevious check
kubevious lint

# Robusta自动化运维
kubectl get roburtareactors -A
kubectl get alertrelays -A

# BotKube聊天机器人
kubectl get botkubeplugins -A
```

### 容器运行时和镜像管理
```bash
# Containerd管理
ctr -n k8s.io containers ls
ctr -n k8s.io images ls

# BuildKit构建
buildctl build --frontend dockerfile.v0 --local context=. --local dockerfile=.

# img镜像工具
img build -t <image-name> .
img push <image-name>

# crane镜像操作
crane ls <repository>
crane copy <src-image> <dst-image>
crane validate <image>

# cosign签名验证
cosign sign <image>
cosign verify <image>
```

### 测试和质量保证
```bash
# Sonobuoy合规测试
sonobuoy run --mode certified-conformance
sonobuoy status
sonobuoy retrieve

# kube-score静态分析
kube-score score <manifest-file>

# Polaris配置检查
polaris audit --audit-path <manifest-dir>

# kube-linter静态检查
kube-linter lint <manifest-dir>

# conftest策略测试
conftest test <manifest-file> --policy <rego-policy-dir>

# kuttl端到端测试
kubectl kuttl test <test-suite>
```

### 性能和容量规划
```bash
# kube-capacity资源分析
kube-capacity --util --available

# goldpinger网络延迟
kubectl port-forward svc/goldpinger 8080:8080

# ksniff网络抓包
ksniff pod <pod-name> -n <namespace>

# ktop资源监控
ktop nodes
ktop pods -n <namespace>

# popeye集群扫描
popeye -n <namespace>
popeye --save --out html

# pluto版本检查
pluto detect-helm -o wide
pluto detect-files <dir>
```

### 灾难恢复和备份
```bash
# Kanister备份恢复
kanctl create actionset --action backup --namespace kanister
kanctl create actionset --action restore --namespace kanister

# Kasten K10
kubectl get k10s -A
kubectl get backupactions -A
kubectl get restoreactions -A

# Arkade工具安装器
arkade get kubectl
arkade get helm
arkade get istioctl

# krew kubectl插件管理
kubectl krew install <plugin-name>
kubectl krew upgrade
kubectl krew list
```

### 云原生安全
```bash
# Aqua Security
kubectl get aquaconfigs -A
kubectl get aquascans -A

# Sysdig Secure
kubectl get sysdigagents -A
kubectl get sysdigscanners -A

# Twistlock
kubectl get twistlockconfigs -A

# NeuVector安全
kubectl get neuvectorconfigs -A
kubectl get nvsecurityrules -A

# Prisma Cloud
kubectl get prismacloudconfigs -A
```

### 边缘和物联网
```bash
# Akri设备发现
kubectl get akriinstances -A
kubectl get akricrds -A

# OpenYurt边缘
kubectl get nodepools -A
kubectl get yurtstaticsets -A

# KubeEdge
kubectl get device -A
kubectl get devicemodel -A

# SuperEdge
kubectl get nodeunits -A
kubectl get servicegrid -A
```

### 无服务器和函数计算
```bash
# Knative Serving
kubectl get kservices -A
kubectl get revisions -A

# OpenFaaS
kubectl get functions.fission.io -A

# KEDA自动扩缩容
kubectl get scaledobjects -A
kubectl get triggerauthentications -A

# Nuclio函数平台
kubectl get nucliofunctions -A
kubectl get nuclioprojects -A

# Fission函数
kubectl get functions -A
kubectl get environments -A
```

### AI基础设施核心命令

#### LLM训练平台管理
```bash
# Kubeflow Training Operators
kubectl get tfjobs -A                    # TensorFlow训练任务
kubectl get pytorchjobs -A              # PyTorch训练任务
kubectl get mpijobs -A                  # MPI分布式训练
kubectl get mxjobs -A                   # MXNet训练任务
kubectl get xgboostjobs -A              # XGBoost训练任务

# Training Operator状态检查
kubectl get trainingoperators -A
kubectl describe trainingoperator -n kubeflow

# 训练任务生命周期管理
kubectl get runs -A                     # Kubeflow Pipelines运行
kubectl get experiments -A             # 实验管理
kubectl get recurringruns -A           # 定期运行
```

#### 模型推理服务管理
```bash
# KServe推理服务
kubectl get inferenceservices -A
kubectl get servingruntimes -A
kubectl get clusterservingruntimes -A

# 推理服务状态监控
kubectl get predictor -A
kubectl get transformer -A
kubectl get explainer -A

# 模型注册和版本管理
kubectl get modelregistries -A
kubectl get modelversions -A
```

#### LLM微调和优化
```bash
# HuggingFace Transformers
kubectl get huggingfacejobs -A
kubectl get peftjobs -A                 # Parameter-Efficient Fine-Tuning

# LoRA微调任务
kubectl get loraconfigs -A
kubectl get qloraconfigs -A             # Quantized LoRA

# 模型压缩和量化
kubectl get modelcompressionjobs -A
kubectl get quantizationconfigs -A
```

#### AI平台运维管理
```bash
# Kubeflow Central Dashboard
kubectl port-forward svc/centraldashboard -n kubeflow 8080:80

# Jupyter Notebook管理
kubectl get notebooks -A
kubectl get notebookcontrollers -A

# 用户和权限管理
kubectl get profiles -A
kubectl get workspaces -A
```

#### AI资源调度和优化
```bash
# GPU资源管理
kubectl get nvidiagpus -A
kubectl get gpuallocations -A
kubectl get gpuclaims -A

# RDMA和高性能网络
kubectl get rdmanetworks -A
kubectl get highspeednetworks -A

# 内存和存储优化
kubectl get memoryoptimizations -A
kubectl get storageprofiles -A
```

#### AI模型监控和可观测性
```bash
# MLflow实验跟踪
kubectl port-forward svc/mlflow -n kubeflow 5000:5000
kubectl get mlflowtracking -A

# TensorBoard日志
kubectl port-forward svc/tensorboard -n kubeflow 6006:6006
kubectl get tensorboards -A

# 模型性能监控
kubectl get modelmonitors -A
kubectl get modeldrifts -A

# 推理指标收集
kubectl get inferencestats -A
kubectl get predictionlogs -A
```

#### AI安全和合规
```bash
# 模型安全扫描
kubectl get modelscanners -A
kubectl get adversarialexamples -A

# 数据隐私保护
kubectl get differentialprivacy -A
kubectl get federatedlearning -A

# 模型治理
kubectl get modelgovernance -A
kubectl get modelcatalogs -A

# 合规性检查
kubectl get aicompliance -A
kubectl get ethicalreviews -A
```

#### AI平台巡检和健康检查
```bash
# 平台整体健康检查
cat > ai-platform-health-check.sh << 'HEALTH'
#!/bin/bash
echo "=== AI基础设施平台健康检查 ==="
echo "检查时间: $(date)"

echo "\n1. 核心组件状态:"
kubectl get pods -n kubeflow | grep -E "(centraldashboard|notebook|training|serving)" | grep Running | wc -l
echo "正常运行的核心组件数量"

echo "\n2. GPU资源状态:"
kubectl get nodes -o jsonpath='{.items[*].status.allocatable.nvidia\\.com/gpu}' | tr ' ' '\n' | awk '{sum+=$1} END {print "总GPU数量: " sum}'

echo "\n3. 训练任务状态:"
kubectl get tfjobs,pytorchjobs -A --no-headers | wc -l
echo "当前训练任务总数"

echo "\n4. 推理服务状态:"
kubectl get inferenceservices -A --no-headers | grep -v NAME | grep -E "(Ready|Failed)" | wc -l
echo "推理服务状态统计"
HEALTH

chmod +x ai-platform-health-check.sh
```

#### AI平台故障诊断
```bash
# 训练任务故障诊断
diagnose_training_job() {
  JOB_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "🔍 诊断训练任务: $JOB_NAME"
  
  # 检查任务状态
  kubectl describe tfjob/$JOB_NAME -n $NAMESPACE
  
  # 查看Pod状态
  kubectl get pods -n $NAMESPACE -l training.kubeflow.org/job-name=$JOB_NAME
  
  # 查看训练日志
  TRAINING_POD=$(kubectl get pods -n $NAMESPACE -l training.kubeflow.org/job-name=$JOB_NAME -o jsonpath='{.items[0].metadata.name}')
  kubectl logs $TRAINING_POD -n $NAMESPACE --tail=100
}

# 推理服务故障诊断
diagnose_inference_service() {
  SERVICE_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "🔍 诊断推理服务: $SERVICE_NAME"
  
  # 检查服务状态
  kubectl describe inferenceservice/$SERVICE_NAME -n $NAMESPACE
  
  # 检查Predictor状态
  kubectl get predictor $SERVICE_NAME-predictor-default -n $NAMESPACE
  
  # 查看服务日志
  PREDICTOR_POD=$(kubectl get pods -n $NAMESPACE -l component=predictor -o jsonpath='{.items[0].metadata.name}')
  kubectl logs $PREDICTOR_POD -n $NAMESPACE --tail=50
}

# GPU资源故障诊断
diagnose_gpu_resources() {
  echo "🔍 GPU资源诊断"
  
  # 检查GPU节点
  kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.nvidia\\.com/gpu}{"\n"}{end}'
  
  # 检查GPU插件
  kubectl get pods -n kube-system -l app=nvidia-device-plugin
  
  # 检查GPU使用情况
  kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.nvidia\\.com/gpu}{"\n"}{end}' | grep -v '<no value>'
}
```

#### AI平台性能优化
```bash
# 训练性能分析
analyze_training_performance() {
  JOB_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "📊 训练性能分析: $JOB_NAME"
  
  # GPU利用率监控
  TRAINING_POD=$(kubectl get pods -n $NAMESPACE -l training.kubeflow.org/job-name=$JOB_NAME -o jsonpath='{.items[0].metadata.name}')
  kubectl exec $TRAINING_POD -n $NAMESPACE -- nvidia-smi
  
  # 内存使用分析
  kubectl exec $TRAINING_POD -n $NAMESPACE -- free -h
}

# 推理性能优化
optimize_inference_performance() {
  SERVICE_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "⚡ 推理性能优化: $SERVICE_NAME"
  
  # 批处理大小优化
  kubectl patch inferenceservice $SERVICE_NAME -n $NAMESPACE -p '{"spec":{"predictor":{"batching":{"maxBatchSize":32}}}}' --type=merge
  
  # 资源调整
  kubectl patch inferenceservice $SERVICE_NAME -n $NAMESPACE -p '{"spec":{"predictor":{"containers":[{"name":"kfserving-container","resources":{"requests":{"cpu":"2","memory":"4Gi"},"limits":{"cpu":"4","memory":"8Gi"}}}]}}}' --type=merge
}
```

#### AI平台容量规划
```bash
# 资源需求预测
predict_resource_requirements() {
  MODEL_SIZE=$1      # 模型大小(GB)
  BATCH_SIZE=$2      # 批处理大小
  REPLICAS=$3        # 副本数
  
  echo "📈 资源需求预测"
  
  # GPU内存需求估算
  GPU_MEMORY_GB=$((MODEL_SIZE * 2))  # 通常需要2倍模型大小的GPU内存
  echo "预估GPU内存需求: ${GPU_MEMORY_GB}GB"
  
  # CPU需求估算
  CPU_CORES=$((BATCH_SIZE * REPLICAS))
  echo "预估CPU核心数: ${CPU_CORES}"
  
  # 内存需求估算
  MEMORY_GB=$((MODEL_SIZE * 4 * REPLICAS))  # 4倍模型大小
  echo "预估内存需求: ${MEMORY_GB}GB"
}

# 集群容量评估
evaluate_cluster_capacity() {
  echo "📊 集群容量评估"
  
  # 总GPU资源
  TOTAL_GPUS=$(kubectl get nodes -o jsonpath='{.items[*].status.allocatable.nvidia\\.com/gpu}' | tr ' ' '+' | bc)
  echo "集群总GPU数量: $TOTAL_GPUS"
  
  # 已使用GPU
  USED_GPUS=$(kubectl get pods -A -o jsonpath='{.items[*].spec.containers[*].resources.requests.nvidia\\.com/gpu}' | tr ' ' '+' | bc)
  echo "已使用GPU数量: $USED_GPUS"
  
  # 可用GPU
  AVAILABLE_GPUS=$((TOTAL_GPUS - USED_GPUS))
  echo "可用GPU数量: $AVAILABLE_GPUS"
}
```

#### AI平台备份和恢复
```bash
# 模型备份
backup_ai_models() {
  BACKUP_DIR="/backup/ai-models/$(date +%Y%m%d_%H%M%S)"
  mkdir -p $BACKUP_DIR
  
  echo "💾 备份AI模型到: $BACKUP_DIR"
  
  # 备份训练模型
  kubectl get tfjobs -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\n"}{end}' | while read namespace job; do
    echo "备份训练任务: $namespace/$job"
    kubectl get tfjob $job -n $namespace -o yaml > $BACKUP_DIR/${namespace}_${job}_config.yaml
  done
  
  # 备份推理模型
  kubectl get inferenceservices -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\n"}{end}' | while read namespace service; do
    echo "备份推理服务: $namespace/$service"
    kubectl get inferenceservice $service -n $namespace -o yaml > $BACKUP_DIR/${namespace}_${service}_config.yaml
  done
}

# 平台配置备份
backup_platform_config() {
  BACKUP_DIR="/backup/ai-platform/$(date +%Y%m%d_%H%M%S)"
  mkdir -p $BACKUP_DIR
  
  echo "💾 备份AI平台配置到: $BACKUP_DIR"
  
  # 备份Kubeflow配置
  kubectl get kfdefs -A -o yaml > $BACKUP_DIR/kfdefs.yaml
  
  # 备份用户配置
  kubectl get profiles -A -o yaml > $BACKUP_DIR/profiles.yaml
  
  # 备份网络策略
  kubectl get networkpolicies -n kubeflow -o yaml > $BACKUP_DIR/networkpolicies.yaml
}
```

#### AI平台安全加固
```bash
# 模型安全扫描
scan_model_security() {
  MODEL_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "🛡️ 模型安全扫描: $MODEL_NAME"
  
  # 检查模型来源
  kubectl get inferenceservice $MODEL_NAME -n $NAMESPACE -o jsonpath='{.spec.predictor.modelUri}'
  
  # 检查模型权限
  kubectl get inferenceservice $MODEL_NAME -n $NAMESPACE -o jsonpath='{.spec.predictor.serviceAccountName}'
}

# 推理服务访问控制
secure_inference_access() {
  SERVICE_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "🔐 推理服务访问控制: $SERVICE_NAME"
  
  # 启用认证
  kubectl patch inferenceservice $SERVICE_NAME -n $NAMESPACE -p '{"spec":{"predictor":{"containers":[{"name":"kfserving-container","env":[{"name":"ENABLE_AUTH","value":"true"}]}]}}}' --type=merge
}
```

## 功能演示工具

### 演示环境快速搭建
```bash
# 创建演示命名空间
kubectl create namespace demo-env

# 部署示例应用
cat > demo-app.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
  namespace: demo-env
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo
  template:
    metadata:
      labels:
        app: demo
    spec:
      containers:
      - name: demo-container
        image: nginx:alpine
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: demo-service
  namespace: demo-env
spec:
  selector:
    app: demo
  ports:
  - port: 80
    targetPort: 80
EOF

kubectl apply -f demo-app.yaml

# 等待应用就绪
kubectl wait --for=condition=ready pod -l app=demo -n demo-env --timeout=300s
```

### 交互式演示脚本
```bash
# 创建演示脚本
cat > interactive-demo.sh << 'DEMO'
#!/bin/bash

echo "🎯 Kubernetes功能演示"
echo "======================"

PS3="请选择演示项目: "

options=(
  "查看集群状态"
  "部署新应用"
  "扩缩容演示"
  "滚动更新"
  "故障恢复"
  "退出演示"
)

select opt in "${options[@]}"
do
  case $opt in
    "查看集群状态")
      echo "📋 集群节点状态:"
      kubectl get nodes -o wide
      echo "\n应用查看:"
      kubectl get pods -n demo-env
      ;;
    "部署新应用")
      echo "🚀 部署示例应用..."
      kubectl create deployment demo-test --image=nginx:alpine -n demo-env
      kubectl expose deployment demo-test --port=80 --type=NodePort -n demo-env
      ;;
    "扩缩容演示")
      echo "📈 扩容演示:"
      kubectl scale deployment demo-app -n demo-env --replicas=5
      kubectl get pods -n demo-env --watch
      ;;
    "滚动更新")
      echo "🔄 滚动更新演示:"
      kubectl set image deployment/demo-app demo-container=nginx:latest -n demo-env
      kubectl rollout status deployment/demo-app -n demo-env
      ;;
    "故障恢复")
      echo "🔧 故障恢复演示:"
      kubectl delete pod -l app=demo -n demo-env --force --grace-period=0
      kubectl get pods -n demo-env --watch
      ;;
    "退出演示")
      echo "👋 演示结束"
      break
      ;;
    *) echo "无效选项 $REPLY";;
esac
done
DEMO

chmod +x interactive-demo.sh
```

### 自动化演示流程
```bash
# 创建完整演示流程
cat > full-demo.sh << 'FULL_DEMO'
#!/bin/bash

echo "🚀 Kubernetes完整功能演示"

demo_step() {
  echo "\n🎯 演示步骤: $1"
  echo "===================$2"
  read -p "按Enter继续..." 
}

# 1. 集群概览
demo_step "集群概览" "===="
echo "集群节点:"
kubectl get nodes -o wide
echo "\n命名空间:"
kubectl get namespaces

# 2. 应用部署
demo_step "应用部署" "===="
echo "部署示例应用:"
kubectl create deployment nginx-demo --image=nginx:alpine
echo "创建服务:"
kubectl expose deployment nginx-demo --port=80 --type=NodePort
echo "\n应用状态:"
kubectl get pods,svc -l app=nginx-demo

# 3. 扩缩容演示
demo_step "自动扩缩容" "==="
echo "手动扩容到3个副本:"
kubectl scale deployment nginx-demo --replicas=3
echo "观察Pod创建:"
kubectl get pods -l app=nginx-demo --watch &
WATCH_PID=$!
sleep 10
kill $WATCH_PID

# 4. 更新演示
demo_step "滚动更新" "===="
echo "更新到新版本:"
kubectl set image deployment/nginx-demo nginx-demo=nginx:latest
echo "观察更新过程:"
kubectl rollout status deployment/nginx-demo

# 5. 故障恢复
demo_step "故障恢复" "===="
echo "模拟Pod故障:"
kubectl delete pod -l app=nginx-demo --force --grace-period=0
echo "观察自动恢复:"
kubectl get pods -l app=nginx-demo --watch &
WATCH_PID=$!
sleep 10
kill $WATCH_PID

# 6. 清理资源
demo_step "清理资源" "===="
echo "删除演示资源:"
kubectl delete deployment,services -l app=nginx-demo
echo "演示完成!"
FULL_DEMO

chmod +x full-demo.sh
```

### 演示监控面板
```bash
# 创建实时监控面板
cat > demo-dashboard.sh << 'DASHBOARD'
#!/bin/bash

echo "📊 演示监控面板"
echo "==============="

while true; do
  clear
  echo "⏰ 当前时间: $(date)"
  echo "==================="
  
  echo "\n📋 集群状态:"
  kubectl get nodes | head -5
  
  echo "\n应用查看:"
  kubectl get pods --all-namespaces | grep -E "(Running|demo)" | head -10
  
  echo "\n📈 资源使用:"
  kubectl top nodes 2>/dev/null | head -5
  
  echo "\n🔔 最近事件:"
  kubectl get events --sort-by=.lastTimestamp --all-namespaces | tail -3
  
  echo "\n🔄 按Ctrl+C退出监控"
  sleep 5
done
DASHBOARD

chmod +x demo-dashboard.sh
```

### 教学辅助工具
```bash
# 创建教学笔记模板
cat > teaching-notes.md << 'NOTES'
# Kubernetes教学演示笔记

## 演示目标
- 展示Kubernetes核心概念
- 演示基本操作命令
- 体验自动化运维能力

## 演示环境
```bash
# 环境准备命令
kubectl create namespace teaching-demo
kubectl config set-context --current --namespace=teaching-demo
```

## 核心概念演示

### 1. Pod概念
- 最小部署单元
- 包含一个或多个容器
- 共享网络和存储

### 2. Deployment管理
- 声明式应用管理
- 自动故障恢复
- 滚动更新支持

### 3. Service发现
- 服务抽象层
- 负载均衡
- 服务发现

## 互动环节
- 学生提问时间
- 实际操作练习
- 问题解答
NOTES

# 演示评估清单
echo "✅ 演示准备检查清单:"
echo "1. [ ] 集群连接正常"
echo "2. [ ] 演示脚本可执行"
echo "3. [ ] 网络访问畅通"
echo "4. [ ] 资源配额充足"
echo "5. [ ] 备份恢复方案"
```

## Pod内应用问题排查

### 通用应用诊断工具
```bash
# 进入Pod Shell进行调试
kubectl exec -it <pod-name> -c <container-name> -- sh
kubectl exec -it <pod-name> -c <container-name> -- bash

# 查看应用进程状态
kubectl exec <pod-name> -- ps aux
kubectl exec <pod-name> -- ps -ef | grep <process-name>

# 查看应用监听端口
kubectl exec <pod-name> -- netstat -tlnp
kubectl exec <pod-name> -- ss -tlnp

# 检查应用日志文件
kubectl exec <pod-name> -- ls -la /var/log/
kubectl exec <pod-name> -- tail -f /var/log/application.log

# 查看应用配置文件
kubectl exec <pod-name> -- cat /etc/app/config.conf
kubectl exec <pod-name> -- env | grep APP_
```

### OpenResty/Nginx应用排查
```bash
# 检查OpenResty进程
kubectl exec <pod-name> -- ps aux | grep nginx

# 查看Nginx配置语法
kubectl exec <pod-name> -- nginx -t

# 重新加载Nginx配置
kubectl exec <pod-name> -- nginx -s reload

# 查看Nginx错误日志
kubectl exec <pod-name> -- tail -f /var/log/nginx/error.log

# 查看Nginx访问日志
kubectl exec <pod-name> -- tail -f /var/log/nginx/access.log

# 检查Nginx状态
kubectl exec <pod-name> -- curl -s http://localhost/nginx_status

# 测试Nginx配置
kubectl exec <pod-name> -- nginx -T

# 查看Worker进程
kubectl exec <pod-name> -- ps aux | grep "nginx: worker"
```

### Java应用排查
```bash
# 查找Java进程
kubectl exec <pod-name> -- jps -v
kubectl exec <pod-name> -- pgrep java

# 查看JVM参数
kubectl exec <pod-name> -- jinfo <pid>

# JVM堆内存分析
kubectl exec <pod-name> -- jstat -gc <pid> 1s 5

# 线程Dump分析
kubectl exec <pod-name> -- jstack <pid> > thread_dump.txt
kubectl cp <namespace>/<pod-name>:thread_dump.txt ./thread_dump.txt

# 堆内存Dump
kubectl exec <pod-name> -- jmap -dump:format=b,file=heap.hprof <pid>
kubectl cp <namespace>/<pod-name>:heap.hprof ./heap.hprof

# GC日志查看
kubectl exec <pod-name> -- tail -f /var/log/gc.log

# JMX连接测试
kubectl port-forward <pod-name> 9999:9999
jconsole localhost:9999
```

### Node.js应用排查
```bash
# 查找Node进程
kubectl exec <pod-name> -- ps aux | grep node

# 查看Node版本
kubectl exec <pod-name> -- node --version

# Node.js进程信息
kubectl exec <pod-name> -- node -e "console.log(process.memoryUsage())"

# 查看npm包信息
kubectl exec <pod-name> -- npm list --depth=0

# Node.js错误日志
kubectl exec <pod-name> -- tail -f /var/log/nodejs/error.log

# 内存使用情况
kubectl exec <pod-name> -- node -e "console.log(process.memoryUsage())"

# CPU使用分析
kubectl exec <pod-name> -- top -b -n 1 | grep node
```

### Python应用排查
```bash
# 查找Python进程
kubectl exec <pod-name> -- ps aux | grep python

# 查看Python版本
kubectl exec <pod-name> -- python --version

# Python包依赖
kubectl exec <pod-name> -- pip list

# Python错误日志
kubectl exec <pod-name> -- tail -f /var/log/python/app.log

# Python内存分析
kubectl exec <pod-name> -- python -c "import psutil; print(psutil.virtual_memory())"

# 查看Python traceback
kubectl exec <pod-name> -- cat /tmp/python_error.log
```

### 数据库应用排查
```bash
# MySQL连接测试
kubectl exec <pod-name> -- mysql -u root -p -e "SHOW STATUS LIKE 'Threads_connected';"

# MySQL慢查询日志
kubectl exec <pod-name> -- tail -f /var/log/mysql/slow.log

# PostgreSQL连接测试
kubectl exec <pod-name> -- psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Redis连接测试
kubectl exec <pod-name> -- redis-cli ping
kubectl exec <pod-name> -- redis-cli info memory

# MongoDB状态检查
kubectl exec <pod-name> -- mongo --eval "db.serverStatus()"
```

### 应用性能分析
```bash
# 应用响应时间测试
kubectl exec <pod-name> -- time curl -s http://localhost:8080/health

# 应用内存泄漏检测
kubectl exec <pod-name> -- ps aux --sort=-%mem | head -10

# 应用CPU使用分析
kubectl exec <pod-name> -- top -b -n 1 | head -20

# 应用文件句柄检查
kubectl exec <pod-name> -- lsof -p $(pgrep <app-name>) | wc -l

# 应用网络连接分析
kubectl exec <pod-name> -- netstat -an | grep ESTABLISHED | wc -l

# 应用启动时间分析
kubectl exec <pod-name> -- systemd-analyze blame | grep <service-name>
```

### 应用日志深度分析
```bash
# 实时日志监控
kubectl exec <pod-name> -- tail -f /var/log/application.log

# 错误日志过滤
kubectl exec <pod-name> -- grep -i "error\|exception\|fatal" /var/log/application.log

# 日志级别调整
kubectl exec <pod-name> -- sed -i 's/INFO/DEBUG/g' /etc/app/logging.conf

# 日志轮转检查
kubectl exec <pod-name> -- ls -la /var/log/ | grep application

# 应用日志采样
kubectl exec <pod-name> -- head -100 /var/log/application.log

# 日志聚合分析
kubectl exec <pod-name> -- awk '/ERROR/ {count++} END {print "Error count:", count}' /var/log/application.log
```

### 应用健康检查
```bash
# 应用存活探针测试
kubectl exec <pod-name> -- curl -f http://localhost:8080/health || echo "Health check failed"

# 应用就绪探针测试
kubectl exec <pod-name> -- curl -f http://localhost:8080/ready || echo "Readiness check failed"

# 应用启动探针测试
kubectl exec <pod-name> -- curl -f http://localhost:8080/startup || echo "Startup check failed"

# 自定义健康检查端点
kubectl exec <pod-name> -- curl -s http://localhost:8080/metrics
kubectl exec <pod-name> -- curl -s http://localhost:8080/info
```

### 应用调试技巧
```bash
# 动态调整应用配置
kubectl exec <pod-name> -- sed -i 's/debug=false/debug=true/' /etc/app/config.properties

# 应用重启（优雅关闭）
kubectl exec <pod-name> -- kill -TERM $(pgrep <app-name>)

# 应用强制重启
kubectl delete pod <pod-name> --force --grace-period=0

# 应用版本验证
kubectl exec <pod-name> -- /app/bin/version.sh

# 应用依赖检查
kubectl exec <pod-name> -- ldd /app/bin/application

# 应用权限检查
kubectl exec <pod-name> -- ls -la /app/
kubectl exec <pod-name> -- id
```
#### AI数据管理平台
```bash
# 数据集管理
kubectl get datasets -A
kubectl get datasetversions -A

# 数据管道管理
kubectl get datapipelines -A
kubectl get dataprocessors -A

# 特征存储管理
kubectl get featurestores -A
kubectl get featureviews -A

# 数据血缘追踪
kubectl get datalineages -A
kubectl get datacatalogs -A

# 数据质量监控
kubectl get dataqualitychecks -A
kubectl get dataprofilings -A

# 数据版本控制
kubectl get dataversions -A
kubectl get dataschemas -A
```

#### AI模型注册中心
```bash
# 模型注册管理
kubectl get modelregistries -A
kubectl get registeredmodels -A

# 模型元数据管理
kubectl get modelmetadata -A
kubectl get modelartifacts -A

# 模型版本控制
kubectl get modelversions -A
kubectl get modeltags -A

# 模型依赖管理
kubectl get modeldependencies -A
kubectl get modelrequirements -A

# 模型文档管理
kubectl get modeldocs -A
kubectl get modelreadmes -A

# 模型审计日志
kubectl get modelaudits -A
kubectl get modelchangelogs -A
```

#### AI实验管理平台
```bash
# 实验跟踪管理
kubectl get experiments -A
kubectl get experimentruns -A

# 超参数优化
kubectl get hyperparametertunes -A
kubectl get bayesianoptimizations -A

# A/B测试管理
kubectl get abtests -A
kubectl get multivariantests -A

# 实验对比分析
kubectl get experimentcomparisons -A
kubectl get experimentdashboards -A

# 实验模板管理
kubectl get experimenttemplates -A
kubectl get experimentblueprints -A

# 实验审批流程
kubectl get experimentapprovals -A
kubectl get experimentreviews -A
```

#### AI平台成本优化
```bash
# 资源成本分析
cost_analysis() {
  echo "💰 AI平台成本分析"
  
  # GPU资源成本统计
  kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.nvidia\.com/gpu}{"\n"}{end}' | \
    grep -v '<no value>' | awk '{gpu[$1]+=$3} END {for(ns in gpu) print ns "\t" gpu[ns] " GPUs"}'
  
  # 训练任务成本估算
  kubectl get tfjobs,pytorchjobs -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.startTime}{"\n"}{end}'
  
  # 推理服务成本分析
  kubectl get inferenceservices -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.predictor.replicas}{"\n"}{end}'
}

# 自动扩缩容优化
optimize_autoscaling() {
  SERVICE_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "📉 优化自动扩缩容: $SERVICE_NAME"
  
  # 配置HPA
  kubectl autoscale inferenceservice $SERVICE_NAME -n $NAMESPACE --cpu-percent=70 --min=1 --max=10
  
  # 配置VPA
  kubectl patch inferenceservice $SERVICE_NAME -n $NAMESPACE -p '{"spec":{"predictor":{"verticalPodAutoscaler":{"enabled":true}}}}' --type=merge
  
  # 资源推荐
  kubectl top pods -n $NAMESPACE -l serving.kubeflow.org/inferenceservice=$SERVICE_NAME
}

# Spot实例优化
spot_instance_optimization() {
  echo "⚡ Spot实例成本优化"
  
  # 检查Spot节点
  kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.beta\.kubernetes\.io/instance-type}{"\n"}{end}' | grep spot
  
  # Spot中断处理
  kubectl get poddisruptionbudgets -n kubeflow
  
  # 混合实例组配置
  kubectl get machinepools -A
}
```

#### AI平台多租户管理
```bash
# 租户隔离管理
kubectl get tenants -A
kubectl get tenantnamespaces -A

# 资源配额管理
kubectl get resourcequotas -A | grep -E "(gpu|memory|cpu)"
kubectl get limitranges -A

# 网络隔离
kubectl get networkpolicies -A | grep tenant
kubectl get tenantnetworks -A

# 存储隔离
kubectl get tenantstorages -A
kubectl get storageclasses -A | grep tenant

# 身份认证集成
kubectl get tenantidentities -A
kubectl get ssoconfigs -A

# 租户计费管理
kubectl get tenantbilling -A
kubectl get costallocations -A
```

---
## Linux系统运维基础命令

### 系统信息和状态监控
```bash
# 基础系统信息
uname -a                           # 系统内核版本
cat /etc/os-release               # 操作系统信息
hostnamectl                       # 主机名和系统信息
uptime                            # 系统运行时间和负载
whoami                            # 当前用户
id                                # 用户ID和组信息
w                                 # 当前登录用户
last                              # 最近登录记录

# 硬件信息
lscpu                             # CPU信息
free -h                           # 内存使用情况
df -h                             # 磁盘空间使用
lsblk                             # 块设备信息
lshw -short                       # 硬件列表
dmidecode -t system              # 系统硬件信息
lsmod                             # 加载的内核模块

# 系统性能监控
top                               # 实时系统监控
htop                              # 增强版top
iostat -x 1                       # IO统计信息
vmstat 1                          # 虚拟内存统计
sar -u 1 5                        # 系统活动报告
dstat                             # 多功能系统统计
```

### 进程和资源管理
```bash
# 进程管理
ps aux                            # 所有进程详情
ps -ef | grep <process-name>      # 查找特定进程
pstree                            # 进程树
kill <PID>                        # 终止进程
kill -9 <PID>                     # 强制终止进程
pkill <process-name>              # 按名称终止进程
nohup <command> &                 # 后台运行命令

# 资源限制和控制
ulimit -a                         # 查看系统限制
nice -n 10 <command>              # 设置进程优先级
renice 5 <PID>                    # 调整运行中进程优先级
cgroups                           # 控制组管理

# 系统调用跟踪
strace <command>                  # 跟踪系统调用
ltrace <command>                  # 跟踪库调用
```

### 文件系统和存储管理
```bash
# 文件操作基础
ls -la                            # 详细文件列表
find /path -name "*.log"          # 查找文件
du -sh /path                      # 目录大小统计
stat <filename>                   # 文件详细信息
file <filename>                   # 文件类型识别
ln -s <target> <link>             # 创建软链接
md5sum <filename>                 # 文件MD5校验

# 磁盘和分区管理
fdisk -l                          # 磁盘分区信息
lsblk -f                          # 块设备文件系统
mount                             # 挂载点信息
umount /mount/point               # 卸载文件系统
mkfs.ext4 /dev/sdX                # 创建文件系统
resize2fs /dev/sdX                # 调整文件系统大小

# 存储性能测试
dd if=/dev/zero of=testfile bs=1M count=1000  # 写入性能测试
dd if=testfile of=/dev/null bs=1M              # 读取性能测试
hdparm -Tt /dev/sdX               # 磁盘性能测试
iotop                             # IO使用监控
```

### 网络基础命令
```bash
# 网络接口和配置
ip addr show                      # IP地址信息
ip route show                     # 路由表
ss -tuln                          # 网络连接状态
netstat -tulnp                    # 网络连接详情
ifconfig                          # 网络接口配置
nmcli device status               # NetworkManager状态

# 网络诊断工具
ping -c 4 google.com              # 网络连通性测试
traceroute google.com             # 路由追踪
mtr google.com                    # 网络质量分析
nslookup google.com               # DNS查询
dig google.com                    # 详细DNS查询
host google.com                   # 主机名解析

# 端口和服务管理
nmap -p 1-1000 <host>             # 端口扫描
nc -zv <host> <port>              # 端口连通性测试
telnet <host> <port>              # Telnet连接测试
curl -I http://example.com        # HTTP头信息
wget http://example.com/file      # 文件下载

# 防火墙管理
ufw status                        # UFW防火墙状态
iptables -L                       # iptables规则
firewall-cmd --list-all           # firewalld配置
```

### 安全基础命令
```bash
# 用户和权限管理
useradd <username>                # 添加用户
passwd <username>                 # 设置密码
usermod -aG sudo <username>       # 添加到sudo组
groups <username>                 # 查看用户组
chmod 755 <file>                  # 修改文件权限
chown user:group <file>           # 修改文件所有者
visudo                            # 编辑sudo配置

# 系统安全检查
lastlog                           # 最后登录记录
faillog                           # 登录失败记录
authconfig --test                 # 认证配置测试
chkrootkit                        # rootkit检测
rkhunter --check                  # 恶意软件扫描

# 日志安全分析
journalctl -f                     # 实时系统日志
grep "Failed password" /var/log/auth.log  # 登录失败记录
awk '/Accepted/{print $1,$2,$3,$9}' /var/log/auth.log  # 成功登录
grep "Invalid user" /var/log/auth.log     # 无效用户尝试

# 加密和证书管理
openssl genrsa -out key.pem 2048          # 生成RSA私钥
openssl req -new -key key.pem -out csr.pem # 生成CSR
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem  # 签发证书
gpg --gen-key                             # 生成GPG密钥
```

### 系统维护和故障排除
```bash
# 系统日志管理
tail -f /var/log/syslog           # 实时查看系统日志
journalctl -u <service>           # 特定服务日志
dmesg                             # 内核日志
logrotate -d /etc/logrotate.conf  # 日志轮转测试

# 系统备份和恢复
tar -czf backup.tar.gz /path      # 创建备份
tar -xzf backup.tar.gz            # 恢复备份
rsync -av /source/ /destination/  # 同步文件
dd if=/dev/sdX of=/backup.img     # 磁盘镜像备份

# 系统性能调优
sysctl -a                         # 内核参数查看
sysctl vm.swappiness=10           # 调整交换分区使用
tuned-adm active                  # 性能调优配置
iotune                            # IO性能调优

# 紧急故障处理
shutdown -h now                   # 立即关机
reboot                            # 重启系统
sync                              # 同步文件系统
fsck /dev/sdX                     # 文件系统检查修复
```

### 自动化运维脚本
```bash
# 系统健康检查脚本
cat > system-health-check.sh << 'HEALTH'
#!/bin/bash
echo "=== 系统健康检查报告 ==="
echo "检查时间: $(date)"

echo -e "\n📋 系统基本信息:"
uname -a
uptime
df -h | head -10

echo -e "\n📋 内存使用情况:"
free -h

echo -e "\n📋 CPU负载:"
top -bn1 | head -20

echo -e "\n📋 网络连接:"
ss -tuln | head -10

echo -e "\n📋 磁盘IO:"
iostat -x 1 1

echo -e "\n📋 关键服务状态:"
systemctl list-units --type=service --state=running | head -10
HEALTH

chmod +x system-health-check.sh

# 批量服务器管理
cat > batch-server-manager.sh << 'BATCH'
#!/bin/bash
SERVERS=("server1" "server2" "server3")
COMMAND="$1"

for server in "${SERVERS[@]}"; do
    echo "🔧 在 $server 上执行: $COMMAND"
    ssh "$server" "$COMMAND"
done
BATCH

chmod +x batch-server-manager.sh

# 日志分析脚本
cat > log-analyzer.sh << 'LOGANALYZER'
#!/bin/bash
LOG_FILE="/var/log/application.log"
ERROR_KEYWORD="ERROR"

echo "=== 日志分析报告 ==="
echo "分析文件: $LOG_FILE"
echo "错误关键字: $ERROR_KEYWORD"

echo -e "\n📊 错误统计:"
grep "$ERROR_KEYWORD" "$LOG_FILE" | wc -l

echo -e "\n📊 错误类型分布:"
grep "$ERROR_KEYWORD" "$LOG_FILE" | cut -d' ' -f5 | sort | uniq -c | sort -nr

echo -e "\n📊 最近10条错误:"
grep "$ERROR_KEYWORD" "$LOG_FILE" | tail -10
LOGANALYZER

chmod +x log-analyzer.sh
```

### 监控和告警
```bash
# 系统监控配置
cat > /etc/monit/monitrc.d/system << 'MONIT'
check system localhost
    if loadavg (1min) > 4 then alert
    if loadavg (5min) > 2 then alert
    if memory usage > 75% then alert
    if cpu usage (user) > 70% then alert
    if cpu usage (system) > 30% then alert
MONIT

# 自定义监控脚本
cat > custom-monitor.sh << 'CUSTOM'
#!/bin/bash
THRESHOLD=80
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $USAGE -gt $THRESHOLD ]; then
    echo "磁盘使用率超过阈值: ${USAGE}%"
    # 发送告警邮件或其他通知
fi
CUSTOM

chmod +x custom-monitor.sh

# 定时监控任务
(crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/custom-monitor.sh") | crontab -
```

### 性能基准测试
```bash
# CPU性能测试
sysbench --test=cpu --cpu-max-prime=20000 run

# 内存性能测试
sysbench --test=memory --memory-block-size=1K --memory-total-size=100G run

# 磁盘IO测试
fio --name=randwrite --ioengine=libaio --iodepth=16 --rw=randwrite --bs=4k --direct=1 --size=1G --numjobs=4

# 网络性能测试
iperf3 -s &                         # 服务端
iperf3 -c <server-ip> -t 30         # 客户端测试
```

### 容器化环境命令
```bash
# Docker基础命令
docker ps -a                      # 所有容器状态
docker images                     # 镜像列表
docker stats                      # 容器资源使用
docker logs <container>           # 容器日志
docker exec -it <container> bash  # 进入容器

# 容器网络诊断
docker network ls                 # 网络列表
docker inspect <container>        # 容器详细信息
docker port <container>           # 端口映射

# 容器资源限制
docker run --memory=1g --cpus=1.5 <image>  # 资源限制运行
docker update --memory=2g <container>      # 动态调整资源
```

