# Kubernetes CLI命令详解

本文档详细解释Kubernetes常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. kubectl get

### 用途
`kubectl get` 是Kubernetes中最常用的命令之一，用于获取集群中各种资源对象的列表信息。该命令可以查询Pods、Services、Deployments、StatefulSets、DaemonSets、Jobs、ConfigMaps、Secrets、Nodes等几乎所有Kubernetes资源对象的基本信息。支持多种输出格式（wide、yaml、json等），并且可以通过标签选择器、字段选择器等条件进行过滤。

### 输出示例
```bash
# 基本Pod查询
$ kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
my-app-6b6b7c7c7c-7x7x7    1/1     Running   0          10d
nginx-deployment-7c7c7c7c   1/1     Running   0          5d

# 指定命名空间查询
$ kubectl get pods -n kube-system
NAME                              READY   STATUS    RESTARTS   AGE
coredns-558bd4d5db-2scbw          1/1     Running   0          30d
etcd-minikube                     1/1     Running   0          30d
kube-apiserver-minikube           1/1     Running   0          30d

# 详细信息查询（wide格式）
$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
my-app-6b6b7c7c7c-7x7x7    1/1     Running   0          10d   172.17.0.10  minikube   <none>           <none>
nginx-deployment-7c7c7c7c   1/1     Running   0          5d    172.17.0.11  minikube   <none>           <none>

# YAML格式输出
$ kubectl get pod my-app-6b6b7c7c7c-7x7x7 -o yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app-6b6b7c7c7c-7x7x7
  namespace: default
  ...
spec:
  containers:
  - name: my-app
    image: nginx:latest
    ...

# JSON格式输出
$ kubectl get pods -o json
{
  "apiVersion": "v1",
  "items": [
    {
      "apiVersion": "v1",
      "kind": "Pod",
      "metadata": {
        "name": "my-app-6b6b7c7c7c-7x7x7",
        ...
      },
      "spec": {...},
      "status": {...}
    }
  ],
  "kind": "List"
}

# 使用标签选择器
$ kubectl get pods -l app=nginx
NAME                        READY   STATUS    RESTARTS   AGE
nginx-deployment-7c7c7c7c   1/1     Running   0          5d

# 查询所有命名空间的资源
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                              READY   STATUS    RESTARTS   AGE
default       my-app-6b6b7c7c7c-7x7x7         1/1     Running   0          10d
kube-system   coredns-558bd4d5db-2scbw          1/1     Running   0          30d

# 自定义列输出
$ kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
NAME                        STATUS    NODE
my-app-6b6b7c7c7c-7x7x7    Running   minikube
nginx-deployment-7c7c7c7c   Running   minikube
```

### 内容解析
- **NAME**: 资源对象的名称，遵循DNS子域名规范（小写字母、数字、连字符，最大253字符）
- **READY**: 准备就绪的容器数量/总容器数量，格式为X/Y，其中X是就绪容器数，Y是总容器数
- **STATUS**: 资源对象的当前状态
  - `Running`: Pod正在运行
  - `Pending`: Pod已被接受但容器尚未运行（可能是拉取镜像、调度中等）
  - `ContainerCreating`: 正在创建容器
  - `Terminating`: Pod正在终止
  - `Succeeded`: Pod中的所有容器已成功终止（主要用于Jobs）
  - `Failed`: Pod中的所有容器已终止，且至少一个容器以失败状态退出
  - `Unknown`: 节点状态未知
- **RESTARTS**: 容器重启次数，频繁重启可能表示存在问题
- **AGE**: 资源对象存在的时间
- **IP**: Pod的IP地址（当使用-o wide时显示）
- **NODE**: Pod被调度到的节点名称（当使用-o wide时显示）

### 常用参数详解
- `-n, --namespace=<namespace>`: 指定命名空间，默认为default
- `-A, --all-namespaces`: 查询所有命名空间
- `-o, --output=<format>`: 指定输出格式（json, yaml, wide, name, custom-columns等）
- `-l, --selector=<key>=<value>`: 使用标签选择器过滤资源
- `-f, --field-selector=<field>=<value>`: 使用字段选择器过滤资源
- `--show-labels`: 显示资源的标签
- `-w, --watch`: 监控资源变化
- `--sort-by=<jsonpath>`: 按指定字段排序

### 实际应用场景
1. **日常监控**: 定期检查应用Pod状态
2. **故障排查**: 查找处于异常状态的资源
3. **容量规划**: 统计资源使用情况
4. **部署验证**: 确认新部署的资源是否正常运行

### 注意事项
- 使用`-n`或`--namespace`参数指定命名空间
- 可以使用`-o wide`查看更多信息（如节点信息）
- 使用`--watch`参数可以实时监控资源状态变化
- 对于大规模集群，建议使用标签选择器缩小查询范围
- 频繁查询可能对API服务器造成压力，应适度使用

### 生产安全风险
- 不会直接修改集群状态，但可能暴露敏感信息（如Pod名称、标签、IP地址等）
- 在多租户环境中，确保只访问有权限的命名空间
- 某些资源信息可能暴露内部服务架构

## 2. kubectl describe

### 用途
`kubectl describe` 命令用于显示资源对象的详细状态和事件信息，是Kubernetes故障排查的核心工具。该命令会聚合资源对象的配置、状态、事件、资源使用情况等多种信息，为用户提供一个全面的资源视图。与`kubectl get`相比，`describe`提供更丰富的上下文信息，特别是在调试Pod启动失败、服务不可达等问题时非常有用。它可以显示Pod的调度过程、事件时间线、资源限制、挂载卷、容器状态等详细信息。

### 输出示例
```bash
# 基本Pod描述
$ kubectl describe pod my-app-6b6b7c7c7c-7x7x7
Name:             my-app-6b6b7c7c7c-7x7x7
Namespace:        default
Priority:         0
Node:             node-1/10.0.0.1
Start Time:       Mon, 01 Jan 2024 10:00:00 +0000
Labels:           app=my-app
                 version=1.0
Annotations:      kubernetes.io/psp: eks.privileged
Status:           Running
IP:               172.17.0.10
IPs:
  IP:           172.17.0.10
Controlled By:  ReplicaSet/my-app-6b6b7c7c7c
Containers:
  my-app:
    Container ID:   docker://abc123def456ghi789jkl012mno345pqr678stu90vwx123yz
    Image:          nginx:latest
    Image ID:       docker-pullable://nginx@sha256:abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx1234yzab5678cdef
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Mon, 01 Jan 2024 10:00:00 +0000
    Ready:          True
    Restart Count:  0
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:        100m
      memory:     128Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xyz12 (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-xyz12:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   Burstable
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  10d   default-scheduler  Successfully assigned default/my-app-6b6b7c7c7c-7x7x7 to node-1
  Normal  Pulling    10d   kubelet            Pulling image "nginx:latest"
  Normal  Pulled     10d   kubelet            Successfully pulled image "nginx:latest" in 2.345s
  Normal  Created    10d   kubelet            Created container my-app
  Normal  Started    10d   kubelet            Started container my-app

# 服务描述
$ kubectl describe service nginx-service
Name:              nginx-service
Namespace:         default
Labels:            <none>
Annotations:       <none>
Selector:          app=nginx
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.100.123.45
IPs:               10.100.123.45
Port:              http  80/TCP
TargetPort:        8080/TCP
Endpoints:         172.17.0.10:8080,172.17.0.11:8080
Session Affinity:  None
Events:            <none>

# Deployment描述
$ kubectl describe deployment my-app
Name:                   my-app
Namespace:              default
CreationTimestamp:      Mon, 01 Jan 2024 10:00:00 +0000
Labels:                 app=my-app
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=my-app
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=my-app
  Containers:
   my-app:
    Image:      nginx:latest
    Port:       <none>
    Host Port:  <none>
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:        100m
      memory:     128Mi
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   my-app-6b6b7c7c7c (1/1 replicas created)

# 节点描述
$ kubectl describe node worker-node-1
Name:               worker-node-1
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=worker-node-1
Annotations:        node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 01 Jan 2024 09:00:00 +0000
Taints:             <none>
Unschedulable:      false
Lease:
  HolderIdentity:  worker-node-1
  AcquireTime:     <unset>
  RenewTime:       Wed, 10 Jan 2024 15:30:45 +0000
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  NetworkUnavailable  False   Wed, 10 Jan 2024 15:30:00 +0000   Wed, 10 Jan 2024 15:30:00 +0000   RouteCreated                 RouteController created a route
  MemoryPressure      False   Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure        False   Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure         False   Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready               True    Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletReady                 kubelet is posting ready status
Addresses:
  InternalIP:  10.0.1.100
  Hostname:    worker-node-1
Capacity:
  cpu:                4
  ephemeral-storage:  41415752Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             8173828Ki
  pods:               110
Allocatable:
  cpu:                4
  ephemeral-storage:  38195531Ki
  hugepages-1Gi:      0
  hugepages-2Mi:      0
  memory:             8071428Ki
  pods:               110
System Info:
  Machine ID:                 abcdef1234567890abcdef1234567890
  System UUID:                abcd-ef12-3456-7890-abcdef123456
  Boot ID:                    12345678-90ab-cdef-1234-567890abcdef
  Kernel Version:             5.4.0-1031-aws
  OS Image:                   Ubuntu 20.04.1 LTS
  Operating System:           linux
  Architecture:               amd64
  Container Runtime Version:  docker://19.3.13
  Kubelet Version:            v1.21.0
  Kube-Proxy Version:         v1.21.0
Non-terminated Pods:          (3 in total)
  Namespace                   Name                      CPU Requests  CPU Limits  Memory Requests  Memory Limits  AGE
  ---------                   ----                      ------------  ----------  ---------------  -------------  ---
  default                     my-app-6b6b7c7c7c-7x7x7  100m (2%)     500m (12%)  128Mi (1%)       512Mi (6%)     10d
  kube-system                 kube-proxy-abc123        100m (2%)     0 (0%)      0 (0%)           0 (0%)         30d
  kube-system                 fluent-bit-xyz789        100m (2%)     100m (2%)   64Mi (0%)        128Mi (1%)     15d
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted)
  Resource           Requested  Limit
  --------           ---------  -----
  cpu                300m (7%)  600m (15%)
  memory             192Mi (2%) 640Mi (8%)
  ephemeral-storage  0 (0%)     0 (0%)
  hugepages-1Gi      0 (0%)     0 (0%)
  hugepages-2Mi      0 (0%)     0 (0%)
Events:              <none>
```

### 内容解析
**Pod描述信息包括：**
- **基本信息**: 名称、命名空间、优先级、节点、启动时间、标签、注解
- **状态信息**: 运行状态、IP地址、控制器引用
- **容器详情**: 镜像、状态、重启次数、资源限制和请求、环境变量、挂载卷
- **条件状态**: 初始化、就绪、容器就绪、Pod调度等条件的布尔状态
- **卷信息**: 挂载的卷类型和配置
- **服务质量**: QoS类别（Guaranteed、Burstable、BestEffort）
- **调度信息**: 节点选择器、容忍度
- **事件日志**: 按时间顺序排列的事件，从调度到启动的全过程

**服务描述信息包括：**
- **服务配置**: 类型、IP、端口、目标端口、端点
- **选择器**: 用于选择后端Pod的标签选择器
- **会话亲和性**: 负载均衡策略

**Deployment描述信息包括：**
- **副本状态**: 期望、更新、总数、可用、不可用的副本数
- **滚动更新策略**: 最大不可用和最大涌浪百分比
- **Pod模板**: 容器配置、资源限制等
- **条件状态**: 进度和可用性条件

### 常用参数详解
- `-n, --namespace=<namespace>`: 指定命名空间，默认为default
- `-A, --all-namespaces`: 查询所有命名空间的资源
- `-f, --filename=<file>`: 从文件或目录描述资源
- `-R, --recursive`: 递归处理-f参数指定的目录
- `--selector=<key>=<value>`: 使用标签选择器过滤资源

### 实际应用场景
1. **Pod故障排查**: 分析Pod事件日志，找出启动失败的原因（如镜像拉取失败、配置错误等）
2. **服务连接问题**: 检查服务端点是否正确指向Pod
3. **资源争用**: 查看节点资源分配和使用情况
4. **调度问题**: 检查Pod调度失败的原因（如资源不足、节点污点等）
5. **配置验证**: 确认实际运行的配置与预期一致

### 注意事项
- 输出信息较多，可使用grep等工具过滤特定信息
- 重点关注Events部分，通常包含关键错误信息
- 结合kubectl get命令一起使用，获得更全面的信息
- 在大规模集群中，指定具体资源名称而不是使用标签选择器，避免输出过多信息

### 生产安全风险
- 可能暴露内部配置细节（如环境变量、卷路径等）
- 事件日志可能包含敏感路径、配置信息或错误详情
- 某些信息可能泄露系统架构或内部服务关系

## 3. kubectl create

### 用途
`kubectl create` 命令用于创建新的Kubernetes资源对象，是部署应用和服务的基础命令。它可以从命令行参数、YAML/JSON配置文件或直接通过命令行参数指定的方式创建资源。该命令支持创建几乎所有的Kubernetes资源类型，包括Deployments、Services、ConfigMaps、Secrets、Jobs、CronJobs、Namespaces等。与`kubectl apply`不同的是，`create`命令是幂等性操作，如果资源已存在会报错，而`apply`会尝试更新资源。`create`命令适用于首次创建资源的场景，确保不会意外覆盖现有配置。

### 输出示例
```bash
# 创建Deployment
$ kubectl create deployment nginx --image=nginx
deployment.apps/nginx created

# 创建带有副本数的Deployment
$ kubectl create deployment my-app --image=my-app:latest --replicas=3
deployment.apps/my-app created

# 从文件创建资源
$ kubectl create -f deployment.yaml
deployment.apps/my-app created

# 创建多个资源
$ kubectl create -f configmap.yaml -f secret.yaml -f deployment.yaml
configmap/app-config created
secret/db-secret created
deployment.apps/my-app created

# 创建带有环境变量的Deployment
$ kubectl create deployment my-app --image=my-app:latest --env="ENV=production" --env="DB_HOST=db-service"
deployment.apps/my-app created

# 创建Service
$ kubectl create service clusterip my-service --tcp=80:8080
service/my-service created

# 创建带有标签的资源
$ kubectl create deployment labeled-app --image=my-app:latest --labels="env=prod,team=backend"
deployment.apps/labeled-app created

# 创建ConfigMap
$ kubectl create configmap app-config --from-literal=database_url=postgresql://db:5432/mydb --from-literal=log_level=info
configmap/app-config created

# 创建Secret
$ kubectl create secret generic db-credentials --from-literal=username=admin --from-literal=password=mypassword
secret/db-credentials created

# 创建Namespace
$ kubectl create namespace production
namespace/production created

# 创建Job
$ kubectl create job cleanup-job --image=busybox -- echo "Cleaning up..."
job.batch/cleanup-job created

# 创建CronJob
$ kubectl create cronjob daily-backup --schedule="0 2 * * *" --restart=OnFailure --image=my-backup-image -- /backup-script.sh
cronjob.batch/daily-backup created

# 创建带有资源限制的Deployment
$ kubectl create deployment resource-limited-app --image=my-app:latest --limits=cpu=500m,memory=512Mi --requests=cpu=100m,memory=128Mi
deployment.apps/resource-limited-app created

# 使用dry-run预览创建（不实际创建）
$ kubectl create deployment test-app --image=nginx --dry-run=client -o yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  name: test-app
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-app
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: test-app
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
status: {}

# 创建ServiceAccount
$ kubectl create serviceaccount my-service-account
serviceaccount/my-service-account created

# 创建Role和RoleBinding
$ kubectl create role pod-reader --verb=get,list,watch --resource=pods
role.rbac.authorization.k8s.io/pod-reader created
$ kubectl create rolebinding read-pods-binding --role=pod-reader --user=john@example.com
rolebinding.rbac.authorization.k8s.io/read-pods-binding created
```

### 内容解析
**主要子命令和选项：**
- `kubectl create deployment`: 创建Deployment资源，用于管理应用副本
- `kubectl create service`: 创建Service资源，提供网络访问
- `kubectl create configmap`: 创建ConfigMap资源，存储配置数据
- `kubectl create secret`: 创建Secret资源，存储敏感数据
- `kubectl create namespace`: 创建命名空间，用于资源隔离
- `kubectl create job`: 创建Job资源，执行一次性任务
- `kubectl create cronjob`: 创建CronJob资源，执行定时任务

**常用参数详解：**
- `--image=<image>`: 指定容器镜像
- `--replicas=<count>`: 指定副本数量
- `--port=<port>`: 指定服务端口
- `--target-port=<port>`: 指定目标端口
- `--labels=<key=value>`: 添加标签
- `--env=<key=value>`: 添加环境变量
- `--from-literal=<key=value>`: 从字面量创建ConfigMap或Secret
- `--from-file=<file>`: 从文件创建ConfigMap或Secret
- `--dry-run=<client|server>`: 预览操作而不实际执行
- `-o, --output=<format>`: 指定输出格式（yaml, json等）
- `-n, --namespace=<namespace>`: 指定命名空间

**资源创建过程：**
1. **验证**: 检查资源定义的有效性
2. **序列化**: 将资源定义转换为API对象
3. **发送请求**: 向API服务器发送创建请求
4. **确认**: 确认资源创建成功并返回结果

### 常用参数详解
- `-f, --filename=<file>`: 从文件或目录创建资源
- `-R, --recursive`: 递归处理-f参数指定的目录
- `--dry-run=<client|server|none>`: 预览操作（client: 客户端验证，server: 服务端验证但不创建）
- `-o, --output=<format>`: 指定输出格式（json, yaml, name等）
- `-n, --namespace=<namespace>`: 指定命名空间
- `--save-config`: 将配置保存到annotation中（用于kubectl apply）
- `--validate=<true|false>`: 是否验证资源配置

### 实际应用场景
1. **应用部署**: 创建新的应用Deployment
2. **服务配置**: 创建ConfigMap和Secret
3. **网络配置**: 创建Service和Ingress
4. **命名空间管理**: 创建隔离环境
5. **批处理任务**: 创建Job和CronJob
6. **权限配置**: 创建RBAC资源（Role, RoleBinding等）
7. **资源预览**: 使用dry-run选项预览资源定义

### 注意事项
- `create`命令是幂等性操作，如果资源已存在会报错
- 使用`--dry-run`选项预览资源定义，避免错误配置
- 在生产环境中，建议使用`kubectl apply`而不是`create`，以便于后续更新
- 创建资源时要注意资源命名规范和命名空间选择
- 确保有足够的权限创建指定类型的资源

### 生产安全风险
- 创建资源可能改变集群状态和配置
- 某些资源类型（如Privileged Pod）可能存在安全风险
- 创建Secret时要小心处理敏感信息
- 确保只在授权的命名空间中创建资源
- 检查创建的资源是否有适当的资源限制，避免资源耗尽攻击
- 创建的资源可能消耗集群资源

## 4. kubectl apply

### 用途
`kubectl apply` 是Kubernetes声明式配置管理的核心命令，用于将配置文件应用到集群中，创建或更新资源。与`kubectl create`不同，`apply`命令采用服务器端应用策略（Server-Side Apply），能够智能地合并配置变更，只更新发生变化的部分，保留集群中手动修改的字段。它是生产环境中推荐的资源管理方式，支持增量更新、回滚和配置同步。`apply`命令使用"last applied configuration"的概念，记录上次应用的配置状态，从而能够精确计算出配置差异并执行相应操作。

### 输出示例
```bash
# 应用单个资源文件
$ kubectl apply -f deployment.yaml
deployment.apps/my-app configured

# 应用目录下所有资源
$ kubectl apply -f ./
deployment.apps/my-app created
service/my-app-service created
configmap/app-config configured

# 应用远程资源
$ kubectl apply -f https://raw.githubusercontent.com/user/repo/main/deployment.yaml
deployment.apps/remote-app created

# 应用多个文件
$ kubectl apply -f configmap.yaml -f deployment.yaml -f service.yaml
configmap/app-config created
deployment.apps/my-app created
service/my-app-service created

# 使用stdin输入
$ cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stdin-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: stdin-app
  template:
    metadata:
      labels:
        app: stdin-app
    spec:
      containers:
      - name: app
        image: nginx:latest
EOF
deployment.apps/stdin-deployment created

# 使用dry-run预览变更
$ kubectl apply -f deployment.yaml --dry-run=server
deployment.apps/my-app configured (server dry run)

# 强制替换资源
$ kubectl apply -f deployment.yaml --force
deployment.apps/my-app replaced

# 查看差异
$ kubectl diff -f deployment.yaml
diff -u -N /tmp/LIVE-407300387/apps_v1_Deployment_default_my-app /tmp/MERGED-2308181816/apps_v1_Deployment_default_my-app
--- /tmp/LIVE-407300387/apps_v1_Deployment_default_my-app 2024-01-01 10:00:00.000000000 +0000
+++ /tmp/MERGED-2308181816/apps_v1_Deployment_default_my-app 2024-01-01 10:00:00.000000000 +0000
@@ -1,5 +1,5 @@
 spec:
   replicas: 3
-  selector:
+  selector:
     matchLabels:
       app: my-app
@@ -10,7 +10,7 @@
     spec:
       containers:
       - name: my-app
-        image: nginx:1.19
+        image: nginx:1.20

# 应用并等待就绪
$ kubectl apply -f deployment.yaml --wait
deployment.apps/my-app configured

# 应用并验证
$ kubectl apply -f deployment.yaml --validate=true
deployment.apps/my-app configured

# 递归应用目录下所有文件
$ kubectl apply -f manifests/ --recursive
configmap/app-config created
deployment.apps/my-app created
service/my-app-service created
ingress.extensions/my-app-ingress created

# 使用patch更新特定字段
$ kubectl patch deployment/my-app -p '{"spec":{"replicas":5}}'
deployment.apps/my-app patched

# 使用策略性合并patch
$ kubectl patch deployment/my-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"my-app","resources":{"requests":{"cpu":"200m"}}}]}}}}'
deployment.apps/my-app patched
```

### 内容解析
**输出状态含义：**
- `created`: 资源不存在，新创建成功
- `configured`: 资源已存在，配置已更新
- `unchanged`: 资源已存在但配置无变化
- `patched`: 资源通过patch更新

**Server-Side Apply机制：**
1. **字段所有权**: Kubernetes跟踪每个字段的最后应用者
2. **冲突检测**: 检测并报告字段冲突
3. **合并策略**: 智能合并配置变更
4. **状态管理**: 维护"last applied configuration"状态

**配置管理流程：**
1. **读取配置**: 从文件或stdin读取新配置
2. **计算差异**: 比较新配置与当前状态
3. **应用变更**: 只更新发生变化的字段
4. **记录状态**: 更新"last applied configuration"

### 常用参数详解
- `-f, --filename=<file>`: 指定配置文件或目录
- `-R, --recursive`: 递归处理目录中的所有文件
- `--dry-run=<client|server|none>`: 预览操作而不实际执行
- `-o, --output=<format>`: 指定输出格式
- `--prune`: 删除不再定义的资源
- `--selector=<selector>`: 只处理匹配标签的资源
- `--force`: 强制替换资源（不推荐在生产环境使用）
- `--wait`: 等待资源就绪后再返回
- `--timeout=<duration>`: 等待操作完成的超时时间
- `--validate=<true|false>`: 验证配置文件格式
- `--server-side`: 使用服务器端应用（推荐）

### 实际应用场景
1. **持续部署**: 在CI/CD流水线中部署应用
2. **配置管理**: 管理应用的配置变更
3. **多环境部署**: 使用相同命令部署到不同环境
4. **基础设施即代码**: 将Kubernetes配置纳入版本控制
5. **配置同步**: 保持集群状态与配置文件一致
6. **蓝绿部署**: 通过配置变更实现无缝更新

### 注意事项
- 使用`kubectl diff`预览变更，避免意外修改
- 在生产环境中避免使用`--force`参数
- 保持配置文件版本控制，便于审计和回滚
- 使用`--dry-run`验证配置语法
- 合理使用`--prune`清理不再需要的资源
- 确保配置文件格式正确（YAML/JSON）

### 生产安全风险
- 配置文件可能包含敏感信息，需要适当保护
- 错误的配置可能导致服务中断
- 不当的资源配置可能引发安全漏洞
- 确保只有授权人员可以应用配置变更
- 使用RBAC限制对关键资源的修改权限

### 生产安全风险
- 可能意外修改生产配置
- 应限制对生产环境的apply权限
- 需要审查配置变更

## 5. kubectl delete

### 用途
`kubectl delete` 命令用于删除集群中的资源对象，是Kubernetes资源管理的重要组成部分。该命令支持删除几乎所有的Kubernetes资源类型，包括Pods、Deployments、Services、ConfigMaps、Secrets、Namespaces等。删除操作是不可逆的，因此在执行时需要格外谨慎，特别是在生产环境中。该命令支持多种删除策略，包括优雅删除（graceful deletion）和强制删除（force deletion）。优雅删除允许资源在指定的时间内完成清理工作，而强制删除会立即终止资源。删除操作会触发资源的终结器（finalizers）执行清理逻辑，确保资源被正确清理。

### 输出示例
```bash
# 删除单个Pod
$ kubectl delete pod my-app-6b6b7c7c7c-7x7x7
pod "my-app-6b6b7c7c7c-7x7x7" deleted

# 删除Deployment
$ kubectl delete deployment my-app
deployment.apps "my-app" deleted

# 从文件删除资源
$ kubectl delete -f deployment.yaml
deployment.apps "my-app" deleted

# 删除多个资源
$ kubectl delete -f configmap.yaml -f deployment.yaml -f service.yaml
configmap "app-config" deleted
deployment.apps "my-app" deleted
service "my-app-service" deleted

# 删除所有Pods
$ kubectl delete pods --all
pod "my-app-6b6b7c7c7c-7x7x7" deleted
pod "nginx-deployment-7c7c7c7c-8y8y8" deleted

# 使用标签选择器删除
$ kubectl delete pods -l app=nginx
pod "nginx-deployment-7c7c7c7c-8y8y8" deleted

# 删除指定命名空间的所有资源
$ kubectl delete all --all -n my-namespace
pod "my-app-pod" deleted
service "my-app-service" deleted
deployment.apps "my-app" deleted

# 优雅删除（默认30秒宽限期）
$ kubectl delete pod my-app-pod --grace-period=30
pod "my-app-pod" deleted

# 立即删除（0秒宽限期）
$ kubectl delete pod my-app-pod --grace-period=0 --force
warning: Immediate deletion does not wait for confirmation that the running resource has been terminated. The resource may continue to run on the cluster indefinitely.
pod "my-app-pod" deleted

# 强制删除（绕过终结器）
$ kubectl delete pod my-app-pod --force --grace-period=0
warning: Immediate deletion does not wait for confirmation that the running resource has been terminated. The resource may continue to run on the cluster indefinitely.
pod "my-app-pod" deleted

# 删除并等待完成
$ kubectl delete deployment my-app --wait=true
deployment.apps "my-app" deleted

# 不等待删除完成
$ kubectl delete deployment my-app --wait=false
deployment.apps "my-app" deleted

# 使用dry-run预览删除操作
$ kubectl delete pod my-app-pod --dry-run=client
pod "my-app-pod" deleted (dry run)

# 删除特定字段的资源
$ kubectl delete pods -l app=nginx --field-selector=status.phase==Running
pod "running-pod-1" deleted
pod "running-pod-2" deleted

# 删除命名空间（会删除其中所有资源）
$ kubectl delete namespace production
namespace "production" deleted

# 删除并忽略不存在的资源
$ kubectl delete pod nonexistent-pod --ignore-not-found=true
Warning: pods "nonexistent-pod" not found

# 删除具有特定注解的资源
$ kubectl delete pods -l app=nginx --selector='!critical=true'
pod "nginx-pod-1" deleted
pod "critical-nginx-pod" not deleted (has critical=true annotation)

# 删除并查看删除过程
$ kubectl delete deployment my-app --v=6
I0101 10:00:00.000000   12345 round_trippers.go:432] DELETE https://cluster-endpoint/api/v1/namespaces/default/pods/my-app-6b6b7c7c7c-7x7x7
I0101 10:00:00.000000   12345 round_trippers.go:554] Response Headers:
deployment.apps "my-app" deleted
```

### 内容解析
**删除过程：**
1. **标记阶段**: Kubernetes将资源标记为"terminating"状态
2. **终结器执行**: 执行资源的终结器（finalizers）进行清理
3. **优雅宽限期**: 等待指定时间让应用正常关闭
4. **强制终止**: 如果宽限期结束后仍未终止，则强制终止
5. **资源清理**: 从etcd中完全删除资源

**删除策略：**
- **优雅删除**: 默认策略，允许资源在grace period内完成清理
- **强制删除**: 立即删除，可能留下孤儿资源
- **级联删除**: 删除父资源及其所有子资源
- **孤儿删除**: 只删除父资源，保留子资源

**宽限期(grace period)：**
- 默认值: 30秒
- 设置为0: 立即删除，不等待优雅终止
- 设置为负数: 使用资源默认的宽限期

### 常用参数详解
- `-f, --filename=<file>`: 从文件或目录删除资源
- `-l, --selector=<selector>`: 使用标签选择器删除资源
- `-n, --namespace=<namespace>`: 指定命名空间
- `--grace-period=<seconds>`: 指定优雅删除的宽限期
- `--force`: 强制删除，绕过服务器验证
- `--wait=<true|false>`: 是否等待删除完成
- `--timeout=<duration>`: 等待删除完成的超时时间
- `--cascade=<true|false|background|orphan>`: 级联删除策略
- `--ignore-not-found=<true|false>`: 是否忽略不存在的资源
- `--dry-run=<client|server|none>`: 预览操作而不实际执行
- `-A, --all-namespaces`: 删除所有命名空间中的资源
- `--field-selector=<field>=<value>`: 使用字段选择器删除资源

### 实际应用场景
1. **故障恢复**: 删除异常的Pod以触发重新调度
2. **资源清理**: 清理不再需要的资源
3. **应用更新**: 删除旧版本应用以部署新版本
4. **环境清理**: 清理测试环境中的资源
5. **安全响应**: 删除被入侵的Pod或Deployment
6. **容量管理**: 删除不需要的资源以释放资源

### 注意事项
- 删除操作是不可逆的，执行前请确认
- 使用`--dry-run`参数预览删除操作
- 在生产环境中，确保有适当的备份和恢复计划
- 注意删除操作对依赖服务的影响
- 考虑使用Deployment等控制器而不是直接删除Pod
- 了解级联删除的影响，避免意外删除依赖资源

### 生产安全风险
- 直接影响服务可用性，可能导致服务中断
- 在生产环境中删除关键资源可能导致业务中断
- 强制删除可能留下孤儿资源，影响集群稳定性
- 删除操作无法撤销，需谨慎操作
- 确保只有授权人员可以执行删除操作
- 删除命名空间会删除其中的所有资源，影响范围较大
- 必须严格控制删除权限

## 6. kubectl logs

### 用途
`kubectl logs` 命令用于查看Pod中容器的日志输出，是Kubernetes调试和监控的核心工具。该命令可以显示容器的标准输出(stdout)和标准错误(stderr)，帮助开发人员和运维人员了解应用程序的运行状态、错误信息和性能指标。支持实时日志跟踪、历史日志查询、多容器日志查看等功能。在生产环境中，日志是故障排查和性能分析的重要依据。需要注意的是，日志只包含从容器启动到现在的输出，不包括已轮转的旧日志文件。对于多容器Pod，需要明确指定容器名称才能查看特定容器的日志。

### 输出示例
```bash
# 查看Pod日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7
2024/01/01 10:00:00 Starting application...
2024/01/01 10:00:01 Connected to database
2024/01/01 10:00:02 Application ready on port 8080

# 实时跟踪日志输出
$ kubectl logs -f my-app-6b6b7c7c7c-7x7x7
2024/01/01 10:00:03 Processing request from 172.17.0.5
2024/01/01 10:00:04 Request completed in 125ms
...

# 查看多容器Pod中特定容器的日志
$ kubectl logs my-multi-container-pod -c sidecar-container
2024/01/01 10:00:00 Sidecar initialized
2024/01/01 10:00:01 Proxy started on port 9080

# 查看最近的几行日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 --tail=10
2024/01/01 10:00:50 Last log entry 10
2024/01/01 10:00:51 Last log entry 9
...
2024/01/01 10:01:00 Last log entry 1

# 查看过去一小时的日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 --since=1h
2024/01/01 09:01:00 Starting application...
2024/01/01 09:01:01 Connected to database
...

# 查看特定时间段的日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 --since-time="2024-01-01T09:00:00Z"
2024/01/01 09:00:01 Application started
2024/01/01 09:00:02 Database connection established

# 查看Pod中所有容器的日志
$ kubectl logs my-multi-container-pod --all-containers=true
[container1] 2024/01/01 10:00:00 Container 1 started
[container2] 2024/01/01 10:00:00 Container 2 started
[sidecar] 2024/01/01 10:00:00 Sidecar started

# 查看之前实例的日志（Pod重启后）
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 --previous
2024/01/01 09:30:00 Starting application...
2024/01/01 09:30:01 Error connecting to database: timeout
2024/01/01 09:30:02 Pod terminating due to failure

# 使用标签选择器查看日志
$ kubectl logs -l app=nginx
Error: a pod name is required, but multiple pods match the selector

# 使用标签选择器配合其他命令查看日志
$ kubectl get pods -l app=nginx -o name | xargs -I {} kubectl logs {}

# 持续监控多个Pod的日志
$ kubectl get pods -l app=my-app -o name | xargs -I {} kubectl logs -f {}

# 查看带时间戳的日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 --timestamps
2024-01-01T10:00:00.123456789Z Starting application...
2024-01-01T10:00:01.234567890Z Connected to database

# 结合grep过滤日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 | grep ERROR
2024/01/01 10:05:30 ERROR Database connection failed

# 查看JSON格式的日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 --output=json
{"log":"2024/01/01 10:00:00 Starting application...","stream":"stdout","time":"2024-01-01T10:00:00.123456789Z"}
{"log":"2024/01/01 10:00:01 Connected to database","stream":"stdout","time":"2024-01-01T10:00:01.234567890Z"}

# 查看最近几分钟的日志
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 --since=5m
2024/01/01 09:56:00 Processing batch job
2024/01/01 09:57:00 Batch job completed successfully

# 使用正则表达式过滤日志（结合外部工具）
$ kubectl logs my-app-6b6b7c7c7c-7x7x7 | grep -E '[0-9]{4}/[0-9]{2}/[0-9]{2}.*ERROR'
2024/01/01 10:05:30 ERROR Database connection failed

# 持续监控并保存日志到文件
$ kubectl logs -f my-app-6b6b7c7c7c-7x7x7 > app.log 2>&1 &

# 查看失败Pod的日志
$ kubectl logs failed-pod --previous
2024/01/01 10:00:00 Starting application...
2024/01/01 10:00:01 Fatal error: Missing required environment variable DB_PASSWORD
```

### 内容解析
**日志输出类型：**
- **标准输出(stdout)**: 应用程序的正常输出信息
- **标准错误(stderr)**: 应用程序的错误信息
- **系统日志**: Kubernetes组件产生的日志

**日志轮转机制：**
- Kubernetes会自动轮转容器日志以节省磁盘空间
- 默认情况下，保留3个旧日志文件，每个文件最大10MB
- 使用`--limit-bytes`参数可以限制单个日志文件大小

**日志存储位置：**
- 日志通常存储在节点的`/var/log/pods/`目录下
- 按照Pod名称和容器名称组织
- 使用软链接连接到实际的容器日志文件

### 常用参数详解
- `-f, --follow`: 实时跟踪日志输出
- `--tail=<number>`: 显示最后N行日志
- `--since=<duration>`: 显示从指定时间以来的日志（如1h, 30m, 10s）
- `--since-time=<RFC3339>`: 显示从指定时间点以来的日志
- `-c, --container=<name>`: 指定容器名称（多容器Pod）
- `--previous`: 查看之前容器实例的日志
- `--timestamps`: 在日志中显示时间戳
- `--all-containers`: 显示Pod中所有容器的日志
- `--selector=<selector>`: 使用标签选择器选择Pod
- `--limit-bytes=<number>`: 限制日志输出的最大字节数
- `--since-seconds=<seconds>`: 显示从指定秒数以来的日志

### 实际应用场景
1. **故障排查**: 查看错误日志定位问题
2. **性能分析**: 分析响应时间和处理时间
3. **安全审计**: 检查访问日志和安全事件
4. **应用监控**: 监控应用运行状态
5. **调试开发**: 验证应用功能是否正常
6. **合规性检查**: 满足日志保留和审计要求

### 注意事项
- 日志只包含从容器启动到现在的内容
- 对于已删除的Pod，日志将不可访问
- 大量日志可能影响节点磁盘空间
- 敏感信息不应记录在日志中
- 在生产环境中应配置集中式日志收集系统

### 生产安全风险
- 可能暴露敏感数据、密码或令牌
- 错误信息可能暴露系统内部结构
- 日志可能包含用户个人信息，需符合隐私法规
- 过多的日志记录可能影响应用性能
- 确保日志访问权限受到适当控制
- 日志中可能包含API密钥、数据库连接信息等

## 7. kubectl exec

### 用途
在正在运行的容器中执行命令。这是一个非常重要的调试和故障排除命令，允许您进入正在运行的Pod并直接与其交互，查看内部状态、日志文件或运行诊断命令。

### 参数详解
- `-it`：分配一个伪终端并保持stdin打开（交互模式）
- `-c <container-name>`：指定Pod中的特定容器（当Pod有多个容器时）
- `--`：分隔kubectl参数和容器内命令参数
- `--request-timeout=TIMEOUT`：设置请求超时时间
- `--stdin`：将标准输入连接到容器
- `--tty`：分配TTY

### 输出示例
```bash
# 进入Pod的交互式shell
$ kubectl exec -it my-app-6b6b7c7c7c-7x7x7 -- /bin/bash
root@my-app-6b6b7c7c7c-7x7x7:/#

# 在Pod中执行单个命令
$ kubectl exec my-app-6b6b7c7c7c-7x7x7 -- ls -la
total 72
drwxr-xr-x   1 root root 4096 Jan  1 10:00 .
drwxr-xr-x   1 root root 4096 Jan  1 10:00 ..
-rwxr-xr-x   1 root root    0 Jan  1 10:00 .dockerenv

# 在多容器Pod中指定容器执行命令
$ kubectl exec -it my-pod -c my-container -- /bin/sh
/ #

# 执行命令并获取返回值
$ kubectl exec my-app-pod -- /bin/bash -c "echo 'Hello World'"
Hello World
```

### 实际应用场景
1. **调试应用程序**：进入Pod检查应用程序状态、配置文件或日志
2. **故障排除**：运行网络诊断命令（如ping、curl）检查网络连通性
3. **文件系统检查**：验证挂载点、文件权限或磁盘空间
4. **进程监控**：检查运行中的进程、内存使用情况
5. **配置验证**：确认环境变量和配置是否正确加载

### 安全风险与注意事项
- 执行命令需要对Pod具有`exec`权限
- 在生产环境中应限制对关键Pod的exec访问
- 避免在生产环境中执行可能影响应用稳定性的命令
- 对于特权容器，exec操作可能带来更高安全风险
- 应启用审计日志记录exec操作

### 内容解析
- 在指定容器中执行命令
- `-it`参数提供交互式终端

### 注意事项
- 需要容器中存在对应的shell或命令
- 可能影响容器内进程

### 生产安全风险
- 提供对容器的直接访问权限
- 可能被用于执行恶意操作
- 严格限制exec权限在生产环境

## 8. kubectl port-forward

### 用途
将本地端口转发到Pod的端口。这是一个非常实用的调试工具，允许您通过本地端口安全地访问Kubernetes集群内部的服务，而无需暴露服务到外部网络。常用于开发和调试阶段访问集群内的数据库、Web服务或其他内部API。

### 参数详解
- `<resource/name>`：指定要转发的目标资源（Pod、Service等）
- `<local_port>:<pod_port>`：本地端口到Pod端口的映射
- `<local_port>:<pod_port>/<protocol>`：指定协议（tcp或udp）
- `--address=IP`：绑定到特定的本地IP地址（默认为localhost）
- `--pod-running-timeout=DURATION`：等待Pod运行的时间（默认4分钟）

### 输出示例
```bash
# 将本地8080端口转发到Pod的80端口
$ kubectl port-forward my-app-6b6b7c7c7c-7x7x7 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080

# 转发到Service而不是Pod
$ kubectl port-forward service/my-service 8080:80
Forwarding from 127.0.0.1:8080 -> 80
Handling connection for 8080

# 绑定到所有网络接口
$ kubectl port-forward --address 0.0.0.0 pod/my-pod 8080:80
Forwarding from 0.0.0.0:8080 -> 80

# 同时转发多个端口
$ kubectl port-forward my-app-pod 8080:80 9090:9090
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from 127.0.0.1:9090 -> 9090
Handling connection for 8080
Handling connection for 9090

# 转发到命名空间中的Pod
$ kubectl port-forward -n production pod/mysql-pod 3306:3306
Forwarding from 127.0.0.1:3306 -> 3306
```

### 实际应用场景
1. **开发调试**：在本地开发环境中连接到集群内的数据库或缓存服务
2. **服务测试**：临时访问未对外暴露的内部服务
3. **安全访问**：安全地访问管理界面或内部API，无需暴露到公网
4. **故障排除**：直接访问Pod进行健康检查和问题诊断
5. **数据迁移**：在不暴露服务的情况下进行数据库备份或迁移

### 安全风险与注意事项
- port-forward会绕过服务网格的安全策略，请谨慎使用
- 在生产环境中应限制对敏感服务的port-forward访问
- 转发连接会占用客户端资源，长时间运行可能导致资源泄漏
- 使用完毕后应及时终止转发进程（Ctrl+C）
- 不应用于生产环境的长期服务访问，应使用Ingress或LoadBalancer

### 内容解析
- 将本地端口映射到Pod的指定端口
- 用于调试和临时访问服务
- 支持TCP和UDP协议转发
- 可以同时转发多个端口
- 支持绑定到特定IP地址

### 注意事项
- 连接是临时的，断开后需重新建立
- 不适用于长期连接需求

### 生产安全风险
- 暴露内部服务到本地网络
- 可能绕过网络安全策略

## 9. kubectl scale

### 用途
调整Deployment、ReplicaSet或ReplicationController的副本数量。此命令允许您动态地增加或减少应用程序实例的数量，以应对负载变化或进行容量规划。它是实现水平扩展（Horizontal Scaling）的关键工具，可以在不停机的情况下调整应用程序的可用实例数。

### 参数详解
- `--current-replicas=count`：仅当当前副本数等于指定值时才进行缩放
- `--replicas=count`：指定目标副本数量
- `--resource-version=version`：仅当资源版本匹配时才进行缩放
- `-f, --filename=[]`：从文件或目录指定资源进行缩放
- `-o, --output=FORMAT`：输出格式（json、yaml、wide等）

### 输出示例
```bash
# 将Deployment的副本数扩展到5个
$ kubectl scale deployment my-app --replicas=5
deployment.apps/my-app scaled

# 将副本数缩小到2个
$ kubectl scale deployment my-app --replicas=2
deployment.apps/my-app scaled

# 根据当前副本数进行缩放（只有当前副本数为3时才缩放到5）
$ kubectl scale deployment my-app --current-replicas=3 --replicas=5
deployment.apps/my-app scaled

# 缩放ReplicaSet
$ kubectl scale rs/my-replicaset --replicas=3
replicaset.extensions/my-replicaset scaled

# 从文件缩放资源
$ kubectl scale -f my-deployment.yaml --replicas=4
deployment.apps/my-deployment scaled

# 在特定命名空间中缩放
$ kubectl scale deployment my-app -n production --replicas=10
deployment.apps/my-app scaled

# 查看缩放后的状态
$ kubectl get deployments
NAME     READY   UP-TO-DATE   AVAILABLE   AGE
my-app   5/5     5            5           10m
```

### 实际应用场景
1. **负载应对**：在高流量时段增加副本数以处理更多请求
2. **成本优化**：在低峰时段减少副本数以节省资源
3. **滚动发布**：在发布新版本前预先扩展副本数
4. **故障恢复**：快速恢复因故障而减少的实例数
5. **容量规划**：根据预期负载调整服务容量

### 安全风险与注意事项
- 缩放操作需要对目标资源具有`patch`权限
- 确保集群有足够的节点资源来容纳新增的Pod
- 监控集群整体资源使用情况，避免资源耗尽
- 考虑服务的资源请求和限制配置，防止资源争用
- 在生产环境中建议配合HPA（Horizontal Pod Autoscaler）使用
- 缩放操作会触发Pod的创建或删除，可能影响服务的可用性

### 内容解析
- 动态调整副本数量
- 立即生效，无需重新部署
- 支持多种资源类型（Deployment、ReplicaSet、RC等）
- 可以基于条件进行缩放（如当前副本数）
- 支持从文件或资源定义进行缩放
- 可以跨命名空间操作

### 注意事项
- 确保集群有足够的资源来运行更多副本
- 监控资源使用情况
- 考虑Pod的调度约束和节点亲和性设置
- 缩放操作可能会触发Pod驱逐和重新调度
- 建议结合HPA实现自动化的弹性伸缩

### 生产安全风险
- 可能消耗过多集群资源
- 影响其他应用的资源分配

## 10. kubectl rollout

### 用途
管理Deployment的滚动更新。这是Kubernetes中管理应用程序更新和回滚的核心命令，支持零停机部署、版本回滚、暂停和恢复部署等功能。对于确保应用程序在更新过程中持续可用至关重要。

### 参数详解
- `history`：查看资源的滚动更新历史
- `undo`：撤销到之前的版本
- `status`：查看滚动更新的状态
- `pause`：暂停资源的滚动更新
- `resume`：恢复暂停的滚动更新
- `--to-revision=N`：回滚到特定修订版本
- `--timeout=DURATION`：设置操作超时时间
- `--watch`：监视滚动更新进度

### 输出示例
```bash
# 查看滚动更新历史
$ kubectl rollout history deployment/my-app
deployment.apps/my-app
REVISION    CHANGE-CAUSE
1           <none>
2           kubectl apply --filename=deployment.yaml
3           kubectl set image deployment/my-app my-app=image:v2.0

# 查看特定修订版本的详细信息
$ kubectl rollout history deployment/my-app --revision=2
deployment.apps/my-app with revision #2
Pod Template:
  Labels:       app=my-app
                pod-template-hash=6b6b7c7c7c
  Containers:
   my-app:
    Image:      my-app:v2.0
    Port:       <none>
    Host Port:  <none>

# 回滚到上一版本
$ kubectl rollout undo deployment/my-app
deployment.apps/my-app rolled back

# 回滚到特定版本
$ kubectl rollout undo deployment/my-app --to-revision=1
deployment.apps/my-app rolled back

# 查看滚动更新状态
$ kubectl rollout status deployment/my-app
Waiting for deployment "my-app" rollout to finish: 1 of 3 updated replicas are available...
Waiting for deployment "my-app" rollout to finish: 2 of 3 updated replicas are available...
deployment "my-app" successfully rolled out

# 暂停部署
$ kubectl rollout pause deployment/my-app
deployment.apps/my-app paused

# 恢复部署
$ kubectl rollout resume deployment/my-app
deployment.apps/my-app resumed

# 监视部署进度
$ kubectl rollout status deployment/my-app --watch
Waiting for deployment "my-app" rollout to finish: 1 out of 3 new replicas have been updated...
deployment "my-app" successfully rolled out
```

### 实际应用场景
1. **版本回滚**：当新版本出现问题时快速回滚到稳定版本
2. **部署监控**：实时监控部署进度和状态
3. **灰度发布**：通过暂停和恢复实现分阶段发布
4. **变更追踪**：通过历史记录追踪每次部署的变更原因
5. **故障恢复**：在部署失败时快速恢复服务

### 安全风险与注意事项
- rollout操作需要对Deployment资源具有相应的RBAC权限
- 回滚操作会立即触发新的滚动更新，需确保集群资源充足
- 在生产环境中执行回滚前应评估影响范围
- 频繁的回滚操作可能表明CI/CD流程存在问题
- 应结合健康检查和就绪探针确保回滚后服务正常

### 内容解析
- 管理Deployment的滚动更新生命周期
- 支持查看历史、回滚、状态检查等多种操作
- 可以暂停和恢复滚动更新过程
- 支持特定版本的回滚操作
- 提供实时状态监控功能

### 注意事项
- 回滚操作不可逆，请确认后再执行
- 确保有足够的资源来运行回滚操作
- 监控回滚过程中的服务可用性
- 结合健康检查确保回滚后服务正常运行

### 生产安全风险
- 错误的回滚操作可能导致服务中断
- 频繁回滚可能掩盖根本问题
# 暂停更新
$ kubectl rollout pause deployment/my-app
deployment.apps/my-app paused

# 恢复更新
$ kubectl rollout resume deployment/my-app
deployment.apps/my-app resumed
```

### 内容解析
- 管理部署的更新过程
- 支持回滚、暂停、恢复等操作

### 注意事项
- 滚动更新过程中服务不会中断
- 回滚操作会恢复到上一稳定版本

### 生产安全风险
- 错误的回滚可能导致服务降级
- 暂停/恢复操作影响部署流程

## 11. kubectl get events

### 用途
查看集群中的事件。

### 输出示例
```bash
$ kubectl get events --all-namespaces
NAMESPACE     LAST SEEN   TYPE      REASON                    OBJECT                              MESSAGE
default       10m         Normal    Scheduled                 pod/my-app-6b6b7c7c7c-7x7x7        Successfully assigned default/my-app-6b6b7c7c7c-7x7x7 to node-1
default       9m          Normal    Pulling                   pod/my-app-6b6b7c7c7c-7x7x7        Pulling image "nginx:latest"
default       8m          Normal    Pulled                    pod/my-app-6b6b7c7c7c-7x7x7        Successfully pulled image "nginx:latest" in 50.123456789s
```

### 内容解析
- 显示集群中发生的各种事件
- 包括调度、拉取镜像、启动等事件

### 注意事项
- 事件保留时间有限（默认1小时）
- 有助于了解系统行为

### 生产安全风险
- 事件可能包含敏感配置信息
- 大量事件可能影响集群性能

## 12. kubectl top

### 用途
显示资源使用情况（需要Metrics Server）。这是一个重要的监控命令，用于查看Pod和节点的CPU及内存使用情况，帮助管理员了解集群资源的实时使用状况，进行容量规划和性能优化。该命令依赖Metrics Server来收集和提供资源指标数据。

### 参数详解
- `-n, --namespace`：指定要查看的命名空间
- `--containers`：显示Pod中各个容器的资源使用情况
- `--heapster-namespace`：指定Heapster服务的命名空间（旧版）
- `--heapster-port`：指定Heapster服务的端口（旧版）
- `--heapster-scheme`：指定Heapster服务的协议（旧版）
- `--selector=label-selector`：通过标签选择器过滤资源

### 输出示例
```bash
# 查看默认命名空间中所有Pod的资源使用
$ kubectl top pods
NAME                        CPU(cores)   MEMORY(bytes)
my-app-6b6b7c7c7c-7x7x7    10m          20Mi
nginx-deployment-7c7c7c7c   5m           15Mi

# 查看特定命名空间中Pod的资源使用
$ kubectl top pods -n production
NAME                         CPU(cores)   MEMORY(bytes)
api-server-7b7b7c7c7c-8y8y8  50m          100Mi
db-server-8c8c8d8d8d-9z9z9   100m         250Mi

# 查看Pod中各容器的资源使用情况
$ kubectl top pods --containers
NAME                        CONTAINER   CPU(cores)   MEMORY(bytes)
my-app-6b6b7c7c7c-7x7x7    app         8m           15Mi
my-app-6b6b7c7c7c-7x7x7    sidecar     2m           5Mi

# 通过标签选择器查看特定Pod的资源使用
$ kubectl top pods -l app=my-app
NAME                       CPU(cores)   MEMORY(bytes)
my-app-6b6b7c7c7c-7x7x7   10m          20Mi

# 查看所有节点的资源使用
$ kubectl top nodes
NAME        CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
node-1      200m         10%    1Gi           25%
node-2      150m         8%     800Mi         20%
node-3      300m         15%    2Gi           40%

# 查看特定节点的资源使用
$ kubectl top nodes node-1
NAME        CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
node-1      200m         10%    1Gi           25%

# 按资源使用排序查看Pod
$ kubectl get pods --sort-by=.status.containerStatuses[0].restartCount
```

### 实际应用场景
1. **性能监控**：实时监控应用程序的资源消耗情况
2. **容量规划**：基于历史数据规划集群扩容需求
3. **故障排查**：识别资源消耗异常的应用程序
4. **资源优化**：调整容器的资源请求和限制配置
5. **成本分析**：了解资源使用情况以优化成本

### 安全风险与注意事项
- top命令需要Metrics Server服务正常运行
- 需要对metrics.k8s.io API具有相应的访问权限
- Metrics Server需要适当的RBAC权限才能收集节点指标
- 资源数据可能存在一定的延迟（通常为15-60秒）
- 在大规模集群中频繁使用可能对Metrics Server造成压力

### 内容解析
- 需要Metrics Server作为指标聚合器
- 支持查看Pod和Node级别的资源使用情况
- 可以显示CPU和内存使用量及百分比
- 支持命名空间和标签选择器过滤
- 提供容器级别资源使用详情（使用--containers参数）

### 注意事项
- 确保Metrics Server已正确部署和配置
- 资源数据有一定延迟，不适合实时监控
- 需要适当的RBAC权限访问metrics API
- 在资源受限的环境中，Metrics Server本身也会消耗资源

### 生产安全风险
- Metrics Server配置不当可能暴露敏感指标信息
- 未授权访问可能获取集群资源使用模式
- 显示CPU和内存使用情况
- 有助于容量规划和性能监控

### 注意事项
- 需要安装Metrics Server
- 数据为近似值

### 生产安全风险
- 资源使用信息可能暴露系统配置
- 频繁查询可能影响性能

## 13. kubectl label

### 用途
为资源添加或修改标签。标签是Kubernetes中用于标识和组织资源的重要元数据，通过键值对的形式为对象附加任意非标识性元信息。标签广泛用于选择器、服务发现、资源分组和策略管理等方面。

### 参数详解
- `--overwrite`：覆盖已存在的标签
- `-l, --selector=label-selector`：选择具有特定标签的资源
- `--all`：选择所有资源
- `-f, --filename=[]`：从文件中读取资源定义
- `--resource-version=version`：仅当资源版本匹配时才更新
- `--dry-run=none|server|client`：模拟操作而不实际执行

### 输出示例
```bash
# 为Pod添加单个标签
$ kubectl label pods my-app-pod env=production
pod/my-app-pod labeled

# 为Pod添加多个标签
$ kubectl label pods my-app-pod tier=frontend team=engineering
pod/my-app-pod labeled

# 覆盖已存在的标签
$ kubectl label --overwrite pods my-app-pod env=staging
pod/my-app-pod labeled

# 为命名空间中的所有Pod添加标签
$ kubectl label pods -l app=my-app env=production -n my-namespace
pod/app1 labeled
pod/app2 labeled

# 从文件为资源添加标签
$ kubectl label -f my-pod.yaml region=us-west
pod/my-pod labeled

# 移除标签
$ kubectl label pods my-app-pod env-
pod/my-app-pod unlabeled

# 使用dry-run预览操作
$ kubectl label pods my-app-pod env=production --dry-run=client
pod/my-app-pod labeled (dry run)

# 条件更新（仅当资源版本匹配时）
$ kubectl label pods my-app-pod env=production --resource-version=12345
pod/my-app-pod labeled
```

### 实际应用场景
1. **环境管理**：标记不同环境（dev、staging、prod）的资源
2. **资源分组**：按团队、应用或功能对资源进行逻辑分组
3. **调度策略**：配合节点选择器和亲和性规则实现调度
4. **服务发现**：通过标签选择器匹配服务和Pod
5. **监控告警**：基于标签进行资源分类和监控
6. **成本追踪**：标记资源归属以进行成本分摊

### 安全风险与注意事项
- label操作需要对目标资源具有`patch`权限
- 修改标签可能影响现有选择器匹配，导致服务中断
- 避免使用过于通用的标签值，可能导致意外的资源匹配
- 标签命名应遵循Kubernetes命名规范（字母、数字、连字符、点号、下划线）
- 在生产环境中修改标签前应充分测试其影响

### 内容解析
- 标签格式为`key=value`形式，用于添加或更新标签
- 标签格式为`key-`形式，用于移除指定标签
- 支持批量操作和选择器匹配
- 可以覆盖已存在的标签值
- 支持dry-run模式预览操作结果

### 注意事项
- 标签键值长度有限制（最大63字符）
- 避免在生产环境中随意更改标签
- 修改标签可能影响服务发现和负载均衡
- 建议使用一致的标签命名约定

### 生产安全风险
- 错误的标签可能导致资源被错误调度
- 标签更改可能影响现有的选择器和服务关联
- 标签可用于选择和分组资源
- 避免使用过于通用的标签键

### 生产安全风险
- 标签可能影响网络策略和RBAC规则
- 错误的标签可能导致服务发现问题

## 14. kubectl annotate

### 用途
为资源添加或修改注解。注解是Kubernetes中用于存储资源附加信息的键值对，与标签不同，注解不用于标识或选择资源，而是用于存储更详细的元数据，如构建信息、文档链接、维护说明等。注解在工具集成、配置管理、审计追踪等方面发挥重要作用。

### 参数详解
- `--overwrite`：覆盖已存在的注解
- `-l, --selector=label-selector`：选择具有特定标签的资源进行注解
- `--all`：选择所有资源进行注解
- `-f, --filename=[]`：从文件中读取资源定义进行注解
- `--resource-version=version`：仅当资源版本匹配时才更新
- `--dry-run=none|server|client`：模拟操作而不实际执行

### 输出示例
```bash
# 为Pod添加单个注解
$ kubectl annotate pods my-app-pod description="Production application pod"
pod/my-app-pod annotated

# 为Pod添加多个注解
$ kubectl annotate pods my-app-pod maintainer="admin@example.com" build-id="build-12345"
pod/my-app-pod annotated

# 覆盖已存在的注解
$ kubectl annotate --overwrite pods my-app-pod description="Updated description"
pod/my-app-pod annotated

# 为命名空间中的所有Pod添加注解
$ kubectl annotate pods -l app=my-app deployment-time="2023-01-01T10:00:00Z" -n my-namespace
pod/app1 annotated
pod/app2 annotated

# 从文件为资源添加注解
$ kubectl annotate -f my-deployment.yaml release-notes="https://example.com/releases/v1.2.3"
deployment/my-deployment annotated

# 移除注解
$ kubectl annotate pods my-app-pod description-
pod/my-app-pod annotated

# 使用dry-run预览操作
$ kubectl annotate pods my-app-pod version="v1.2.3" --dry-run=client
pod/my-app-pod annotated (dry run)

# 为服务添加健康检查注解
$ kubectl annotate service my-service service.alpha.kubernetes.io/tolerate-unready-endpoints="true"
service/my-service annotated
```

### 实际应用场景
1. **构建信息**：存储构建ID、镜像版本、提交哈希等CI/CD相关信息
2. **文档链接**：提供相关文档、运行手册或故障排除指南的链接
3. **维护信息**：记录负责人、维护窗口、联系信息等
4. **审计追踪**：记录变更历史、操作人员、变更原因等
5. **工具集成**：为第三方工具（如监控、日志、安全扫描工具）提供配置信息
6. **配置元数据**：存储特定于应用的配置参数或启动选项

### 安全风险与注意事项
- annotate操作需要对目标资源具有`patch`权限
- 注解值不应包含敏感信息（密码、密钥等），应使用Secret存储
- 注解值大小有限制（每个注解值最大1MB，整个对象元数据最大1MB）
- 避免在注解中存储可能影响系统行为的配置，应使用适当的资源配置字段
- 注解主要用于非标识性元数据，不应替代标签的选择功能

### 内容解析
- 注解格式为`key=value`形式，用于添加或更新注解
- 注解格式为`key-`形式，用于移除指定注解
- 支持批量操作和选择器匹配
- 可以覆盖已存在的注解值
- 支持复杂值（包含空格、特殊字符等）的注解
- 注解不影响资源的选择和匹配逻辑

### 注意事项
- 注解键值长度有限制（最大63字符，值最大1MB）
- 避免在注解中存储敏感信息
- 注解主要用于存储非标识性的元数据
- 使用一致的注解命名约定以提高可维护性

### 生产安全风险
- 在注解中存储敏感信息可能导致信息泄露
- 过大的注解值可能影响API服务器性能
- 错误的注解可能影响第三方工具的正常工作
- 用于记录额外信息

### 生产安全风险
- 注解可能包含敏感信息
- 存储大量注解可能影响性能

## 15. kubectl patch

### 用途
部分更新资源对象。与`kubectl apply`不同，patch命令允许对现有资源进行局部修改，而不需要提供完整的资源配置。这在需要快速修改特定字段或进行自动化脚本操作时非常有用。支持多种补丁策略，包括strategic merge patch、JSON patch和JSON merge patch，可根据不同场景选择最适合的方式。

### 参数详解
- `-p, --patch=<patch-content>`：指定补丁内容
- `--type=<patch-type>`：指定补丁类型（strategic、merge、json）
- `-f, --filename=[]`：从文件读取资源进行patch
- `-o, --output=FORMAT`：输出格式（json、yaml、name等）
- `--dry-run=none|server|client`：模拟操作而不实际执行
- `--record`：记录当前命令到资源的注解中
- `--subresource=<subresource>`：指定要更新的子资源

### 输出示例
```bash
# 使用Strategic Merge Patch更新副本数（默认类型）
$ kubectl patch deployment my-app -p '{"spec":{"replicas":5}}'
deployment.apps/my-app patched

# 使用JSON Merge Patch添加标签
$ kubectl patch deployment my-app -p '{"metadata":{"labels":{"env":"production"}}}'
deployment.apps/my-app patched

# 使用JSON Patch进行数组操作（RFC 6902格式）
$ kubectl patch deployment my-app --type='json' -p='[{"op": "replace", "path": "/spec/replicas", "value": 3}]'
deployment.apps/my-app patched

# 从文件应用补丁
$ kubectl patch deployment my-app -p "$(cat patch-file.json)"
deployment.apps/my-app patched

# 使用YAML格式的补丁
$ kubectl patch deployment my-app -p '
spec:
  template:
    spec:
      containers:
      - name: my-app
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
'
deployment.apps/my-app patched

# 更新Pod的安全上下文
$ kubectl patch pod my-pod -p '{"spec":{"securityContext":{"runAsNonRoot":true,"runAsUser":1000}}}'
pod/my-pod patched

# 添加多个注解
$ kubectl patch deployment my-app -p '{"metadata":{"annotations":{"deployment.kubernetes.io/revision":"3","last-updated":"2024-01-01T10:00:00Z"}}}'
deployment.apps/my-app patched

# 修改服务端口
$ kubectl patch service my-service -p '{"spec":{"ports":[{"port":8080,"targetPort":8080,"protocol":"TCP","name":"http"}]}}'
service/my-service patched

# 使用dry-run预览操作
$ kubectl patch deployment my-app -p '{"spec":{"replicas":4}}' --dry-run=client
deployment.apps/my-app patched (dry run)

# 更新资源限制
$ kubectl patch deployment my-app --type='merge' -p '{"spec":{"template":{"spec":{"containers":[{"name":"my-app","resources":{"limits":{"memory":"1Gi","cpu":"1000m"}}}]}}}}'
deployment.apps/my-app patched

# 更新环境变量
$ kubectl patch deployment my-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"my-app","env":[{"name":"ENV_VAR","value":"new_value"}]}]}}}}'
deployment.apps/my-app patched
```

### 实际应用场景
1. **紧急修复**：快速修改资源配置，如资源限制、副本数等
2. **自动化脚本**：在CI/CD流程中动态修改资源配置
3. **蓝绿部署**：临时修改服务配置进行流量切换
4. **安全加固**：快速更新安全上下文或安全策略
5. **容量调整**：根据负载情况动态调整资源配额
6. **配置注入**：在不重建资源的情况下添加环境变量或卷

### 安全风险与注意事项
- patch操作需要对目标资源具有`patch`权限
- 错误的补丁内容可能导致资源不可用
- 某些字段受准入控制器限制，无法直接patch
- JSON Patch操作可能在复杂对象上产生意外结果
- 在生产环境中使用前应在测试环境验证补丁效果
- 避免在关键资源上进行可能影响服务可用性的修改

### 内容解析
- 支持多种补丁策略（Strategic、Merge、JSON）
- Strategic Patch：智能合并，适用于Kubernetes原生资源
- JSON Merge Patch：简单合并，RFC 7386标准
- JSON Patch：精确操作，RFC 6902标准
- 支持嵌套对象的部分更新
- 可以同时修改多个字段
- 支持从文件或标准输入读取补丁内容

### 注意事项
- 确保JSON/YAML语法正确，格式错误会导致操作失败
- 在生产环境中使用`--dry-run`验证补丁效果
- 某些资源字段可能受保护，无法通过patch修改
- 考虑补丁操作对依赖资源的影响
- 记录重要的patch操作以便后续审计

### 生产安全风险
- 可能意外修改关键配置导致服务中断
- 错误的补丁可能引入安全漏洞
- 未经过充分测试的补丁可能影响系统稳定性
- 应限制对生产资源的patch权限

## 16. kubectl config

### 用途
管理kubeconfig文件，用于配置集群访问凭据和上下文。

### 输出示例
```bash
# 查看当前上下文
$ kubectl config current-context
minikube

# 查看所有上下文
$ kubectl config get-contexts
CURRENT   NAME       CLUSTER    AUTHINFO       NAMESPACE
*         minikube   minikube   minikube-admin
          prod       prod       prod-user      production

# 切换上下文
$ kubectl config use-context prod
Switched to context "prod".

# 设置命名空间
$ kubectl config set-context --current --namespace=production
Context "prod" modified.
```

### 内容解析
- `current-context`: 查看当前使用的集群上下文
- `get-contexts`: 列出所有可用的上下文
- `use-context`: 切换到指定的上下文
- `set-context`: 修改上下文设置

### 注意事项
- 上下文包含集群、用户和命名空间信息
- 更改上下文会影响后续所有kubectl命令的目标

### 生产安全风险
- 配置错误的上下文可能导致操作错误的集群
- 访问凭证可能被泄露

## 17. kubectl run

### 用途
在集群中创建并运行一个或多个容器。

### 输出示例
```bash
$ kubectl run nginx --image=nginx --port=80
pod/nginx created

$ kubectl run busybox --image=busybox --rm -it --restart=Never -- /bin/sh
/ #
```

### 内容解析
- 创建临时Pod进行测试或调试
- 可以指定端口、环境变量、命令等参数

### 注意事项
- 通常用于一次性任务或调试
- 使用`--rm`参数可在退出后自动删除Pod

### 生产安全风险
- 可能运行不安全的容器镜像
- 临时容器可能绕过安全策略

## 18. kubectl expose

### 用途
为Pod、Deployment或ReplicaSet创建Service。

### 输出示例
```bash
$ kubectl expose deployment nginx --port=80 --target-port=8080 --type=LoadBalancer
service/nginx exposed
```

### 内容解析
- 创建服务以公开应用程序
- 可指定端口映射和服务类型

### 注意事项
- 需要确保目标端口正确
- 服务类型影响外部访问方式

### 生产安全风险
- 可能意外暴露内部服务
- LoadBalancer类型会创建公有IP

## 19. kubectl set

### 用途
配置应用程序资源的特定属性。这是一个复合命令，包含多个子命令用于修改现有资源的不同方面，如容器镜像、环境变量、资源限制、卷、服务账户等。相比于完整的资源更新，set命令提供了更便捷的方式来修改资源的特定配置，特别适合在CI/CD流程中的渐进式更新。

### 子命令详解
- `set image`: 更新容器镜像
- `set env`: 更新环境变量
- `set resources`: 更新资源请求和限制
- `set serviceaccount`: 更新服务账户
- `set subject`: 更新RBAC角色绑定的主题
- `set volume`: 更新卷配置
- `set selector`: 更新资源选择器
- `set affinity`: 更新亲和性规则
- `set tolerations`: 更新容忍度配置

### 输出示例
```bash
# 设置容器镜像（最常用）
$ kubectl set image deployment/my-app my-app=my-image:v2.0
deployment.apps/my-app image updated

# 设置多个容器的镜像
$ kubectl set image deployment/my-app my-app=my-app:v2.0 sidecar=sidecar:v1.5
deployment.apps/my-app image updated

# 设置环境变量
$ kubectl set env deployment/my-app ENV=production DB_HOST=db-prod
deployment.apps/my-app env updated

# 设置资源请求和限制
$ kubectl set resources deployment/my-app --limits=cpu=200m,memory=512Mi --requests=cpu=100m,memory=256Mi
deployment.apps/my-app resource requirements updated

# 设置环境变量从ConfigMap
$ kubectl set env deployment/my-app --from=configmap/app-config
deployment.apps/my-app env updated

# 设置环境变量从Secret
$ kubectl set env deployment/my-app --from=secret/app-secret
deployment.apps/my-app env updated

# 设置服务账户
$ kubectl set serviceaccount deployment/my-app my-service-account
deployment.apps/my-app serviceaccount updated

# 设置卷（添加持久卷声明）
$ kubectl set volume deployment/my-app --add --name=data --mount-path=/data --type=persistentVolumeClaim --claim-name=data-pvc
deployment.apps/my-app volume updated

# 设置卷（移除卷）
$ kubectl set volume deployment/my-app --remove --name=old-volume
deployment.apps/my-app volume updated

# 从文件设置环境变量
$ kubectl set env deployment/my-app --env-file=./env.list
deployment.apps/my-app env updated

# 移除环境变量
$ kubectl set env deployment/my-app ENV-
deployment.apps/my-app env updated

# 使用dry-run预览操作
$ kubectl set image deployment/my-app my-app=my-app:v2.0 --dry-run=client
deployment.apps/my-app image updated (dry run)

# 设置资源并记录变更
$ kubectl set resources deployment/my-app --limits=cpu=500m,memory=1Gi --requests=cpu=200m,memory=512Mi --record
deployment.apps/my-app resource requirements updated

# 为特定命名空间中的资源设置环境变量
$ kubectl set env deployment/my-app NEW_VAR=new_value -n production
deployment.apps/my-app env updated
```

### 实际应用场景
1. **镜像更新**：在不停机的情况下更新应用程序镜像
2. **配置变更**：动态修改环境变量或配置参数
3. **资源调整**：根据负载情况调整资源请求和限制
4. **安全更新**：更新服务账户或安全配置
5. **卷管理**：动态添加或移除存储卷
6. **扩缩容准备**：修改资源配置以适应不同的负载需求

### 安全风险与注意事项
- set操作需要对目标资源具有相应的更新权限
- 错误的配置可能导致应用程序不可用
- 环境变量中的敏感信息应通过Secret管理，而非直接设置
- 镜像更新会触发滚动更新，需确保新镜像兼容现有配置
- 资源限制的修改可能影响Pod的调度和运行
- 在生产环境中使用前应在测试环境验证配置变更

### 内容解析
- 提供专门的子命令来修改资源的特定属性
- 支持对Deployment、StatefulSet、DaemonSet等多种资源类型
- 可以同时修改多个容器的配置
- 支持从ConfigMap和Secret导入环境变量
- 支持批量操作和选择器匹配
- 提供dry-run模式预览操作结果

### 注意事项
- 修改镜像会触发滚动更新，可能影响服务可用性
- 资源限制的修改需要考虑节点资源可用性
- 环境变量的修改需要应用程序支持热重载
- 验证镜像名称和标签的有效性
- 考虑配置变更对依赖服务的影响

### 生产安全风险
- 错误的配置可能导致服务中断
- 敏感信息可能意外暴露在配置中
- 不兼容的镜像可能导致应用故障
- `set env`: 设置环境变量
- `set resources`: 设置资源限制

### 注意事项
- 会导致滚动更新
- 需要验证新配置的兼容性

### 生产安全风险
- 镜像更新可能引入安全漏洞
- 资源配置不当可能影响性能

## 20. kubectl edit

### 用途
直接编辑服务器上资源的定义。

### 输出示例
```bash
$ kubectl edit deployment/my-app
# 在编辑器中打开部署配置
# 保存后立即应用更改
```

### 内容解析
- 打开默认编辑器进行在线编辑
- 保存后立即应用更改

### 注意事项
- 编辑时需要谨慎，语法错误会导致更新失败
- 建议优先使用`kubectl patch`

### 生产安全风险
- 直接修改生产配置有风险
- 需要适当的访问控制

## 21. kubectl api-resources

### 用途
列出所有可用的API资源。

### 输出示例
```bash
$ kubectl api-resources
NAME                              SHORTNAMES   APIGROUP                       NAMESPACED   KIND
bindings                                                                      true         Binding
componentstatuses                 cs                                          false        ComponentStatus
configmaps                        cm                                          true         ConfigMap
endpoints                         ep                                          true         Endpoints
events                            ev                                          true         Event
limitranges                       limits                                      true         LimitRange
namespaces                        ns                                          false        Namespace
nodes                             no                                          false        Node
persistentvolumeclaims            pvc                                         true         PersistentVolumeClaim
persistentvolumes                 pv                                          false        PersistentVolume
pods                              po                                          true         Pod
replicationcontrollers            rc                                          true         ReplicationController
resourcequotas                    quota                                       true         ResourceQuota
secrets                           sec                                         true         Secret
services                          svc                                         true         Service
mutatingwebhookconfigurations                  admissionregistration.k8s.io   false        MutatingWebhookConfiguration
```

### 内容解析
- NAME: 资源名称
- SHORTNAMES: 简称
- APIGROUP: API组
- NAMESPACED: 是否受命名空间限制
- KIND: 资源类型

### 注意事项
- 有助于了解可用的资源类型
- 可用于发现自定义资源定义

### 生产安全风险
- 无直接安全风险
- 可能暴露内部API信息

## 22. kubectl api-versions

### 用途
列出服务器支持的API版本。

### 输出示例
```bash
$ kubectl api-versions
admissionregistration.k8s.io/v1
apiextensions.k8s.io/v1
apiregistration.k8s.io/v1
apps/v1
authentication.k8s.io/v1
authorization.k8s.io/v1
autoscaling/v1
batch/v1
certificates.k8s.io/v1
coordination.k8s.io/v1
events.k8s.io/v1
extensions/v1beta1
networking.k8s.io/v1
policy/v1
rbac.authorization.k8s.io/v1
scheduling.k8s.io/v1
storage.k8s.io/v1
v1
```

### 内容解析
- 显示集群支持的所有API版本
- 有助于确定可用功能

### 注意事项
- 用于检查集群功能兼容性
- 帮助编写兼容的配置文件

### 生产安全风险
- 无直接安全风险
- 可能暴露集群版本信息

## 23. kubectl explain

### 用途
显示资源字段的文档。这是Kubernetes中最实用的内置文档查询工具，允许用户在不离开命令行的情况下查看任何资源类型或其字段的详细文档说明。无论是初学者还是经验丰富的开发者，都可以通过此命令了解资源结构、字段类型、必需字段等信息，极大地提高了配置编写效率和准确性。该命令直接从集群API服务器获取最新的资源定义，确保文档的准确性和时效性。

### 参数详解
- `--recursive=true|false`：显示资源的所有字段和子字段的详细说明（默认false）
- `--api-version=version`：指定API版本以获取特定版本的文档
- `--help`：显示命令帮助信息

### 输出示例
```bash
# 解释Pod资源的基本信息
$ kubectl explain pod
KIND:     Pod
VERSION:  v1

DESCRIPTION:
     Pod is a collection of containers that can run on a host. This resource is
     created by clients and scheduled onto hosts.

# 解释Pod的特定字段
$ kubectl explain pod.spec.containers
KIND:     Pod
VERSION:  v1

FIELD:    containers <[]Object>

DESCRIPTION:
     List of containers belonging to the pod. Containers cannot currently be
     added or removed. There must be at least one container in a Pod.

     A single application container that you want to run within a pod.

# 解释容器的端口字段
$ kubectl explain pod.spec.containers.ports
KIND:     Pod
VERSION:  v1

FIELD:    ports <[]Object>

DESCRIPTION:
     List of ports to expose from the container. Exposing a port here gives
     the system additional information about the network connections a
     container uses, but is primarily informational. Not specifying a port
     here DOES NOT prevent that port from being exposed. Any port which is
     listening on the default "0.0.0.0" address inside a container will be
     accessible from the network.

# 递归显示Deployment的所有字段
$ kubectl explain deployment --recursive
KIND:     Deployment
VERSION:  apps/v1

DESCRIPTION:
     Deployment enables declarative updates for Pods and ReplicaSets.

FIELDS:
   apiVersion	<string>
   kind	<string>
   metadata	<Object>
     annotations	<map[string]string>
     clusterName	<string>
     creationTimestamp	<string>
     deletionGracePeriodSeconds	<integer>
     deletionTimestamp	<string>
     finalizers	<[]string>
     generateName	<string>
     generation	<integer>
     labels	<map[string]string>
     managedFields	<[]Object>
     name	<string>
     namespace	<string>
     ownerReferences	<[]Object>
     resourceVersion	<string>
     selfLink	<string>
     uid	<string>
   spec	<Object>
     minReadySeconds	<integer>
     paused	<boolean>
     progressDeadlineSeconds	<integer>
     replicas	<integer>
     revisionHistoryLimit	<integer>
     selector	<Object>
       matchExpressions	<[]Object>
         key	<string>
         operator	<string>
         values	<[]string>
       matchLabels	<map[string]string>
     strategy	<Object>
       rollingUpdate	<Object>
         maxSurge	<string>
         maxUnavailable	<string>
       type	<string>
     template	<Object>
       metadata	<Object>
         annotations	<map[string]string>
         finalizers	<[]string>
         labels	<map[string]string>
         name	<string>
         namespace	<string>
       spec	<Object>
         activeDeadlineSeconds	<integer>
         affinity	<Object>
         automountServiceAccountToken	<boolean>
         containers	<[]Object>
         dnsConfig	<Object>
         dnsPolicy	<string>
         enableServiceLinks	<boolean>
         ephemeralContainers	<[]Object>
         hostAliases	<[]Object>
         hostIPC	<boolean>
         hostNetwork	<boolean>
         hostPID	<boolean>
         hostname	<string>
         imagePullSecrets	<[]Object>
         initContainers	<[]Object>
         nodeName	<string>
         nodeSelector	<map[string]string>
         preemptionPolicy	<string>
         priority	<integer>
         priorityClassName	<string>
         readinessGates	<[]Object>
         restartPolicy	<string>
         runtimeClassName	<string>
         schedulerName	<string>
         securityContext	<Object>
         serviceAccount	<string>
         serviceAccountName	<string>
         setHostnameAsFQDN	<boolean>
         shareProcessNamespace	<boolean>
         subdomain	<string>
         terminationGracePeriodSeconds	<integer>
         tolerations	<[]Object>
         topologySpreadConstraints	<[]Object>
         volumes	<[]Object>
   status	<Object>
     availableReplicas	<integer>
     collisionCount	<integer>
     conditions	<[]Object>
     observedGeneration	<integer>
     readyReplicas	<integer>
     replicas	<integer>
     unavailableReplicas	<integer>
     updatedReplicas	<integer>

# 解释特定API版本的资源
$ kubectl explain ingress --api-version=networking.k8s.io/v1
KIND:     Ingress
VERSION:  networking.k8s.io/v1

DESCRIPTION:
     Ingress is a collection of rules that allow inbound connections to reach
     the endpoints defined by a backend. An Ingress can be configured to give
     services externally-reachable urls, load balance traffic, terminate SSL,
     offer name based virtual hosting etc.

# 解释Job资源
$ kubectl explain job.spec.template.spec.restartPolicy
KIND:     Job
VERSION:  batch/v1

FIELD:    restartPolicy <string>

DESCRIPTION:
     Restart policy for all containers within the pod. One of Always,
     OnFailure, Never. Default to Never.

# 查看字段是否必需
$ kubectl explain pod.spec.containers.image
KIND:     Pod
VERSION:  v1

FIELD:    image <string>

DESCRIPTION:
     Docker image name. More info:
     https://kubernetes.io/docs/concepts/containers/images This field is
     optional to allow higher level config management to default or override
     container images in workload controllers like Deployments and Jobs.

# 使用grep过滤特定字段
$ kubectl explain deployment.spec | grep -A 10 replicas
     replicas	<integer>
     Number of desired pods. This is a pointer to distinguish between explicit
     zero and not specified. Defaults to 1.
```

### 实际应用场景
1. **配置编写**：编写YAML配置文件时验证字段名称和结构
2. **学习探索**：了解新资源类型或字段的用法
3. **调试验证**：验证配置中的字段拼写和层级关系
4. **API参考**：获取实时的API字段文档，无需查阅在线文档
5. **自动化脚本**：在脚本中验证资源结构

### 安全风险与注意事项
- explain命令只读取API服务器的公开文档，无安全风险
- 提供离线文档查询功能，不依赖外部网络
- 始终显示当前集群支持的API版本文档
- 递归输出可能很长，建议结合grep等工具过滤
- 某些自定义资源可能需要安装CRD后才能解释

### 内容解析
- 直接从集群API服务器获取资源定义
- 支持查看任意深度的嵌套字段
- 显示字段类型（字符串、整数、布尔值、对象数组等）
- 提供字段的详细描述和用途说明
- 显示字段是否为必需项
- 支持所有内置和自定义资源类型

### 注意事项
- 输出信息来源于集群的实际API版本
- 对于自定义资源，需要先安装对应的CRD
- 使用--recursive参数时输出可能非常长
- 可以结合管道命令过滤输出内容
- 是开发和运维过程中的必备工具

### 生产安全风险
- 无安全风险，纯只读操作

## 24. kubectl attach

### 用途
附加到正在运行的容器。

### 输出示例
```bash
$ kubectl attach my-pod -c my-container
# 连接到正在运行的容器
```

### 内容解析
- 连接到容器的标准输入、输出和错误
- 类似于`kubectl exec`但不启动新命令

### 注意事项
- 仅当容器已经运行某个命令时才有意义
- 适合监控长时间运行的进程

### 生产安全风险
- 提供对容器的直接访问
- 需要适当的权限控制

## 25. kubectl cp

### 用途
在Pod和本地文件系统之间复制文件。

### 输出示例
```bash
# 从Pod复制文件到本地
$ kubectl cp default/my-pod:/tmp/file.txt ./local-file.txt

# 从本地复制文件到Pod
$ kubectl cp ./local-file.txt default/my-pod:/tmp/file.txt
```

### 内容解析
- 跨越Pod边界传输文件
- 需要指定命名空间/Pod名和路径

### 注意事项
- 需要tar命令在容器中可用
- 需要适当的权限

### 生产安全风险
- 可能传输敏感数据
- 可能上传恶意文件到容器

## 26. kubectl diff

### 用途
比较本地配置与服务器上配置的差异。

### 输出示例
```bash
$ kubectl diff -f deployment.yaml
diff -u -N /tmp/LIVE-433408308/apps/v1/Deployment/default/nginx /tmp/MERGED-893139549/apps/v1/Deployment/default/nginx
--- /tmp/LIVE-433408308/apps/v1/Deployment/default/nginx	2024-01-01T10:00:00Z
+++ /tmp/MERGED-893139549/apps/v1/Deployment/default/nginx	2024-01-01T10:00:00Z
@@ -1,5 +1,5 @@
 apiVersion: apps/v1
 kind: Deployment
 metadata:
-  name: nginx
+  name: nginx-updated
```

### 内容解析
- 显示配置文件与集群中实际配置的差异
- 使用类似diff的格式

### 注意事项
- 不会修改任何资源
- 有助于预览变更的影响

### 生产安全风险
- 无直接安全风险
- 可能暴露配置信息

## 27. kubectl replace

### 用途
通过文件或stdin替换资源。

### 输出示例
```bash
$ kubectl replace -f deployment.yaml
deployment.apps/my-app replaced
```

### 内容解析
- 完全替换现有资源
- 与apply不同，完全替换配置

### 注意事项
- 会完全替换资源，不合并配置
- 需要提供完整的资源配置

### 生产安全风险
- 可能意外覆盖重要的生产配置
- 应谨慎使用，优先考虑apply

## 28. kubectl wait

### 用途
等待一个或多个资源达到特定条件。

### 输出示例
```bash
# 等待Pod变为运行状态
$ kubectl wait --for=condition=Ready pod/my-pod
pod/my-pod condition met

# 等待Pod被删除
$ kubectl wait --for=delete pod/my-pod
pod/my-pod deleted

# 设置超时
$ kubectl wait --for=condition=Ready pod/my-pod --timeout=300s
```

### 内容解析
- 等待资源满足特定条件
- 可设置超时时间

### 注意事项
- 用于脚本自动化场景
- 可以等待多种条件

### 生产安全风险
- 无直接安全风险
- 长时间等待可能影响脚本执行

## 29. kubectl drain

### 用途
安全地排空节点上的Pod，将节点置于维护模式。该命令会优雅地驱逐节点上的所有Pod（不包括DaemonSet管理的Pod），确保在节点进行维护、升级或删除之前，所有工作负载都已安全迁移到其他节点。这是生产环境中进行节点维护的关键命令，可以确保在维护期间服务的连续性。

### 参数详解
- `--ignore-daemonsets=true|false`：忽略DaemonSet管理的Pod（默认false）
- `--delete-emptydir-data=true|false`：删除使用EmptyDir卷的Pod（默认false）
- `--force=true|false`：强制驱逐即使不受控制器管理的Pod（默认false）
- `--grace-period=SECONDS`：指定Pod终止的宽限期（秒），-1表示使用Pod的默认值
- `--timeout=DURATION`：等待Pod终止的超时时间（默认300s）
- `--delete-local-data=true|false`：删除使用本地存储的Pod（默认false）

### 输出示例
```bash
# 基本节点排空操作
$ kubectl drain node-1 --ignore-daemonsets
node/node-1 cordoned
WARNING: ignoring DaemonSet-managed pods: kube-system/kube-flannel-ds-amd64-xxx, kube-system/kube-proxy-xxx
evicting pod "my-app-pod-xxx"
evicting pod "nginx-pod-xxx"
pod/my-app-pod-xxx evicted
pod/nginx-pod-xxx evicted
node/node-1 drained

# 强制排空节点（包括本地数据Pod）
$ kubectl drain node-2 --ignore-daemonsets --delete-local-data --force
node/node-2 cordoned
WARNING: ignoring DaemonSet-managed pods: kube-system/kube-proxy-xxx
evicting pod "local-storage-pod-xxx"
pod/local-storage-pod-xxx evicted
node/node-2 drained

# 设置较长的宽限期和超时时间
$ kubectl drain node-3 --ignore-daemonsets --grace-period=300 --timeout=600s
node/node-3 cordoned
evicting pod "long-running-pod-xxx"
pod/long-running-pod-xxx evicted
node/node-3 drained

# 仅排空特定命名空间的Pod
# 注意：kubectl drain不支持命名空间过滤，需要先标记节点然后使用污点

# 模拟排空操作（dry-run）
$ kubectl drain node-1 --ignore-daemonsets --dry-run=client
node/node-1 cordoned (dry run)
pod/my-app-pod-xxx evicted (dry run)

# 排空节点并等待完成
$ kubectl drain node-1 --ignore-daemonsets --timeout=10m
node/node-1 cordoned
evicting pod "my-app-pod-xxx"
pod/my-app-pod-xxx evicted
node/node-1 drained

# 检查节点状态
$ kubectl get nodes
NAME     STATUS                     ROLES    AGE   VERSION
node-1   Ready,SchedulingDisabled   <none>   10d   v1.21.0
node-2   Ready                      <none>   10d   v1.21.0
```

### 实际应用场景
1. **节点维护**：在进行硬件维护、操作系统升级或内核更新前排空节点
2. **节点缩容**：在缩减集群规模时安全移除节点
3. **故障隔离**：当检测到节点硬件问题时，将工作负载迁移到其他节点
4. **安全加固**：在节点上应用安全补丁或配置变更前排空Pod
5. **容量调整**：在节点间重新平衡工作负载分布

### 安全风险与注意事项
- drain操作需要对Node资源具有`cordon/uncordon/drain`权限
- 排空节点会导致Pod被重新调度，需确保集群有足够的备用容量
- DaemonSet的Pod默认不会被驱逐，除非使用`--delete-emptydir-data`参数
- 使用`--force`参数可能导致数据丢失，应谨慎使用
- 在多租户环境中，节点排空可能影响其他用户的Pod
- 排空操作会触发Pod的优雅终止流程，确保应用有足够时间清理资源

### 内容解析
- 自动执行cordon操作，禁止新Pod调度到该节点
- 逐个驱逐节点上的Pod，触发Pod的优雅终止流程
- 等待Pod终止后，节点进入drained状态
- 可以通过`kubectl uncordon`命令恢复节点的调度
- 支持多种策略来处理不同类型的Pod和存储

### 注意事项
- 确保集群有足够的备用节点来容纳被驱逐的Pod
- 在生产环境中提前测试排空操作的影响
- 考虑PodDisruptionBudgets对排空操作的限制
- 使用适当的超时时间避免无限等待
- 排空前检查节点上的关键工作负载

### 生产安全风险
- 可能导致服务暂时不可用，如果备用容量不足
- 强制排空可能导致数据丢失
- 错误的参数可能导致意外驱逐关键Pod
- 需要确保操作人员具有适当的权限

## 30. kubectl cordon

### 用途
将节点标记为不可调度，阻止新的Pod被调度到该节点，但不会驱逐已运行的Pod。这是节点维护的第一步，通常在执行`kubectl drain`之前使用，或者在只想停止接收新工作负载但不影响现有工作负载的场景下使用。

### 参数详解
- 无特定参数，主要是节点名称

### 输出示例
```bash
# 标记节点为不可调度
$ kubectl cordon node-1
node/node-1 cordoned

# 验证节点状态
$ kubectl get nodes
NAME     STATUS                     ROLES    AGE   VERSION
node-1   Ready,SchedulingDisabled   <none>   10d   v1.21.0
node-2   Ready                      <none>   10d   v1.21.0

# 查看节点详细信息
$ kubectl describe node node-1 | grep -A 5 Conditions
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  Ready            True    Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletReady                 kubelet is posting ready status
  DiskPressure     False   Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletHasNoDiskPressure     kubelet has no disk pressure
  MemoryPressure   False   Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletHasSufficientMemory   kubelet has sufficient memory available
  PIDPressure      False   Wed, 10 Jan 2024 15:30:45 +0000   Mon, 01 Jan 2024 09:00:00 +0000   KubeletHasSufficientPID      kubelet has sufficient PID available

# 模拟cordon操作
$ kubectl cordon node-2 --dry-run=client
node/node-2 cordoned (dry run)

# 同时标记多个节点
$ kubectl cordon node-1 node-2 node-3
node/node-1 cordoned
node/node-2 cordoned
node/node-3 cordoned
```

### 实际应用场景
1. **准备节点维护**：在排空节点前先阻止新Pod调度
2. **节点调试**：在不影响现有工作负载的情况下停止接收新Pod
3. **资源预留**：为特定目的预留节点资源
4. **安全隔离**：将可疑节点置于观察状态，不允许新Pod调度

### 安全风险与注意事项
- cordon操作需要对Node资源具有`cordon/uncordon`权限
- 不会影响已运行的Pod，仅阻止新Pod调度
- 在多可用区集群中，过度使用可能导致调度问题
- 需要人工监控cordoned节点的状态

### 内容解析
- 修改节点的unschedulable字段为true
- 节点仍处于Ready状态，但标记为SchedulingDisabled
- 不影响现有的Pod，只阻止新Pod调度
- 可以通过uncordon命令恢复节点调度

### 注意事项
- cordoned节点仍会参与服务发现和负载均衡
- 不会驱逐现有Pod，需要手动删除或使用drain命令
- 定期检查cordoned节点，避免忘记恢复
- 在高可用环境中合理使用，避免影响服务可用性

### 生产安全风险
- 可能导致集群资源利用率下降
- 过度使用可能影响Pod调度能力
- 需要确保操作人员具有适当的权限

## 31. kubectl uncordon

### 用途
恢复节点的调度能力，将之前使用`kubectl cordon`标记为不可调度的节点重新标记为可调度状态。该命令会清除节点的SchedulingDisabled状态，使新的Pod可以被调度到该节点。通常在节点维护完成后使用，以恢复节点的正常工作负载接收能力。

### 参数详解
- 无特定参数，主要是节点名称

### 输出示例
```bash
# 恢复节点调度
$ kubectl uncordon node-1
node/node-1 uncordoned

# 验证节点状态恢复正常
$ kubectl get nodes
NAME     STATUS   ROLES    AGE   VERSION
node-1   Ready    <none>   10d   v1.21.0
node-2   Ready    <none>   10d   v1.21.0

# 检查节点详细状态
$ kubectl describe node node-1 | grep -A 5 -E "(Unschedulable|SchedulingDisabled)"
# 应该看不到SchedulingDisabled状态

# 模拟uncordon操作
$ kubectl uncordon node-1 --dry-run=client
node/node-1 uncordoned (dry run)

# 恢复多个节点
$ kubectl uncordon node-1 node-2 node-3
node/node-1 uncordoned
node/node-2 uncordoned
node/node-3 uncordoned

# 检查Pod是否会调度到刚恢复的节点
$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
my-app-6b6b7c7c7c-7x7x7    1/1     Running   0          10d   172.17.0.10  node-1     <none>           <none>
new-app-7c7c7d7d7d-8y8y8    1/1     Running   0          5m    172.17.0.11  node-1     <none>           <none>

# 验证节点资源可用性
$ kubectl top nodes
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
node-1   200m         5%     1000Mi          12%       
node-2   400m         10%    2000Mi          25%       
```

### 实际应用场景
1. **维护完成**：节点维护完成后恢复节点的正常调度
2. **故障恢复**：解决节点问题后重新启用节点
3. **容量恢复**：在临时隔离后恢复集群容量
4. **滚动更新**：在节点更新完成后重新加入集群

### 安全风险与注意事项
- uncordon操作需要对Node资源具有`cordon/uncordon`权限
- 确保节点在恢复调度前已完成维护并处于健康状态
- 检查节点资源是否充足以接收新Pod
- 在恢复前验证节点的网络连接和存储可用性

### 内容解析
- 修改节点的unschedulable字段为false
- 清除SchedulingDisabled状态
- 节点重新变为可调度状态
- 新Pod可以被调度到该节点

### 注意事项
- 在uncordon前验证节点健康状态
- 监控新调度到节点的Pod状态
- 考虑逐步恢复以避免资源竞争
- 记录节点维护和恢复的时间

### 生产安全风险
- 恢复有问题的节点可能导致服务不稳定
- 需要确保节点在恢复前已完全准备好
- 可能影响集群的负载均衡

## 32. kubectl auth

### 用途
检查认证和授权相关信息。

### 输出示例
```bash
# 检查当前用户权限
$ kubectl auth can-i get pods
yes

$ kubectl auth can-i create deployments
no

# 获取授权评估
$ kubectl auth can-i --list
Resources                                       Non-Resource URLs   Resource Names   Verbs
selfsubjectreviews.certificates.k8s.io         []                  []               [create]
selfsubjectaccessreviews.authorization.k8s.io  []                  []               [create]
                                                [/api/*]            []               [get]
                                                [/apis/*]           []               [get]
```

### 内容解析
- `can-i`: 检查是否有权限执行特定操作
- `--list`: 列出当前用户的权限

### 注意事项
- 用于权限诊断
- 帮助理解RBAC配置

### 生产安全风险
- 用于权限验证，无直接风险
- 可能暴露权限信息

## 30. kubectl autoscale

### 用途
为Deployment、ReplicaSet或ReplicationController创建HPA（Horizontal Pod Autoscaler）。

### 输出示例
```bash
$ kubectl autoscale deployment my-app --cpu-percent=70 --min=3 --max=10
horizontalpodautoscaler.autoscaling/my-app autoscaled
```

### 内容解析
- 自动调整副本数量基于资源使用情况
- 配置最小和最大副本数

### 注意事项
- 需要Metrics Server
- 需要适当的监控指标

### 生产安全风险
- 可能导致资源消耗激增
- 需要合理设置阈值

## 31. kubectl certificate

### 用途
管理TLS证书。

### 输出示例
```bash
# approve CSRs
$ kubectl certificate approve csr-12345

# deny CSRs
$ kubectl certificate deny csr-67890
```

### 内容解析
- `approve`: 批准证书签名请求
- `deny`: 拒绝证书签名请求

### 注意事项
- 用于管理集群证书
- 需要适当的安全验证

### 生产安全风险
- 证书管理涉及安全认证
- 错误批准可能引入安全风险

## 32. kubectl proxy

### 用途
运行代理服务器到Kubernetes API服务器。

### 输出示例
```bash
$ kubectl proxy
Starting to serve on 127.0.0.1:8001

# 现在可以通过 http://localhost:8001/api 访问API
```

### 内容解析
- 创建本地到API服务器的代理
- 用于安全访问API

### 注意事项
- 默认绑定到localhost
- 可以指定端口和地址

### 生产安全风险
- 暴露API接口到本地网络
- 需要限制代理访问权限

## 33. kubectl debug

### 用途
为现有Pod创建调试会话。

### 输出示例
```bash
$ kubectl debug my-pod -it --image=busybox
Defaulting debug container name to debugger-jtxbg.
If you don't see a command prompt, try pressing enter.
/ # 

# 创建Ephemeral容器进行调试
$ kubectl debug -it my-pod --image=busybox --target=my-container
```

### 内容解析
- 创建临时调试容器
- 用于故障排查

### 注意事项
- 不修改原Pod配置
- 调试完成后自动清理

### 生产安全风险
- 调试容器可能绕过安全策略
- 需要适当权限控制

## 34. helm

### 用途
Kubernetes包管理器，用于管理和部署应用包（Charts）。

### 输出示例
```bash
# 查看版本
$ helm version
version.BuildInfo{Version:"v3.12.0", GitCommit:"c3563fb814e93d1c72222a7e65b73a8f5d10d3cc", GitTreeState:"clean", GoVersion:"go1.20.4"}

# 列出所有发布
$ helm list -A
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
my-app          default         1               2024-01-01 10:00:00.000000 +0000 UTC  deployed        my-app-1.0.0            1.0.0

# 安装Chart
$ helm install my-release my-chart/
NAME: my-release
LAST DEPLOYED: Mon Jan  1 10:00:00 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None

# 升级发布
$ helm upgrade my-release my-chart/
Release "my-release" has been upgraded. Happy Helming!
```

### 内容解析
- `version`: 显示Helm版本信息
- `list`: 列出所有发布的chart
- `install`: 安装新的chart
- `upgrade`: 升级现有chart
- `rollback`: 回滚到以前的版本
- `uninstall`: 卸载chart

### 注意事项
- 需要预先配置Chart仓库
- Chart是预配置的Kubernetes资源包
- Helm 3不再使用Tiller

### 生产安全风险
- Chart可能包含恶意配置
- 需要适当的权限控制
- 不安全的Chart可能导致集群安全问题

## 35. istioctl

### 用途
Istio服务网格的命令行工具，用于安装、配置和调试Istio。

### 输出示例
```bash
# 检查Istio安装状态
$ istioctl analyze
✔ No validation issues found when analyzing namespace: default.

# 安装Istio
$ istioctl install --set profile=demo -y
✔ Istio core installed
✔ Istiod installed
✔ Ingress gateways installed
✔ Installation complete

# 检查配置
$ istioctl proxy-status
NAME                                   CLUSTER        LOCALITY        VERSION        STATUS        PILOT
details-v1-5498c86cf5-2z7gk.default   Kubernetes                     1.17.0         SYNCED        istiod-558d7589c5-5l2v9
productpage-v1-7655f67bff-5g2n5.defa   Kubernetes                     1.17.0         SYNCED        istiod-558d7589c5-5l2v9

# 注入sidecar
$ istioctl kube-inject -f deployment.yaml | kubectl apply -f -
deployment/my-app configured
```

### 内容解析
- `analyze`: 分析Istio配置
- `install`: 安装Istio控制平面
- `proxy-status`: 检查Envoy代理同步状态
- `kube-inject`: 注入Istio sidecar

### 注意事项
- 需要Istio已安装在集群中
- 版本兼容性很重要

### 生产安全风险
- 配置错误可能影响服务网格功能
- 不当的网络策略可能暴露服务

## 36. kustomize

### 用途
Kubernetes原生配置管理工具，用于定制和组合Kubernetes资源。

### 输出示例
```bash
# 构建配置
$ kustomize build overlays/staging/
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-staging
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: my-app
        image: nginx:1.19
        env:
        - name: ENV
          value: staging

# 使用kubectl与kustomize集成
$ kubectl apply -k overlays/production/
deployment.apps/my-app-production created
service/my-app-service created
```

### 内容解析
- `build`: 渲染kustomization.yaml文件
- 基于base和overlay模式组织配置
- 支持补丁、变量替换等功能

### 注意事项
- 需要kustomization.yaml文件定义配置
- 支持base和overlay模式

### 生产安全风险
- 不当的补丁可能修改关键配置
- 需要验证配置变更

## 37. velero

### 用途
Kubernetes集群备份和迁移工具，用于灾难恢复和集群迁移。

### 输出示例
```bash
# 创建备份
$ velero backup create daily-backup --schedule="0 2 * * *"
Backup request "daily-backup" submitted successfully.
Run 'velero backup describe daily-backup' for more details.

# 列出备份
$ velero backup get
NAME            STATUS            ERRORS    WARNINGS    CREATED                         EXPIRES    STORAGE LOCATION    SELECTOR
daily-backup    InProgress        0         0           2024-01-01 02:00:00 +0000 UTC   29d        default             <none>

# 恢复备份
$ velero restore create --from-backup daily-backup
Restore request "daily-backup-20240101020000" submitted successfully.

# 查看恢复状态
$ velero restore get
NAME                                BACKUP          STATUS      STARTED                         COMPLETED                       ERRORS   WARNINGS   CREATED                         SELECTOR
daily-backup-20240101020000         daily-backup    Completed   2024-01-01 02:05:00 +0000 UTC   2024-01-01 02:08:00 +0000 UTC   0        0          2024-01-01 02:05:00 +0000 UTC   <none>
```

### 内容解析
- `backup create`: 创建备份
- `backup get`: 列出备份
- `restore create`: 从备份恢复
- `restore get`: 查看恢复状态

### 注意事项
- 需要配置存储位置（如S3、Azure Blob等）
- 定期测试备份和恢复过程

### 生产安全风险
- 备份数据需要加密保护
- 恢复操作可能覆盖现有数据
- 需要严格的访问控制

## 38. calicoctl

### 用途
Calico网络插件的命令行工具，用于管理和配置Calico网络策略。

### 输出示例
```bash
# 查看所有网络策略
$ calicoctl get networkpolicies --all-namespaces
NAMESPACE   NAME                    ORDER   SELECTOR
default     allow-ui-service        100     role == 'ui'
kube-system   allow-all-kube-system   1000    all()

# 查看BGP配置
$ calicoctl get bgppeers -o wide
GROUP   PEERIP   NODE   ASN   METADATA
global  10.0.0.1   node-1   65100   <none>

# 查看IP池
$ calicoctl get ippools -o wide
NAME           CIDR          NAT    IPIPMODE   VXLANMODE   DISABLED
default-ipv4   192.168.0.0/16   Enabled   Always     Never       false
```

### 内容解析
- `get`: 获取Calico资源
- 支持多种资源类型：networkpolicies, bgppeers, ippools等
- 用于网络策略和路由管理

### 注意事项
- 需要Calico CNI插件
- 网络策略影响服务连通性

### 生产安全风险
- 错误的网络策略可能阻断服务
- 需要仔细验证网络配置

## 39. cilium

### 用途
Cilium CNI插件的命令行工具，用于管理和监控基于eBPF的网络策略。

### 输出示例
```bash
# 检查Cilium状态
$ cilium status
    /¯¯\
 /¯¯\__/¯¯\    Cilium:         OK
 \__/¯¯\__/    Operator:       OK
 /¯¯\__/¯¯\    Envoy Daemon:   disabled
 \__/¯¯\__/    Hubble:         disabled
    \__/

# 查看网络策略
$ cilium policy get
Name                Labels    Selector
default/deny-all    map[]     map[reserved:host->world]

# 查看端点
$ cilium endpoint list
ENDPOINT   POLICY (ingress)   POLICY (egress)   IDENTITY   LABELS (source:key[=value])   IPv6   IPv4          STATUS   
           ENFORCEMENT        ENFORCEMENT
275        Disabled           Disabled          30282      k8s:io.cilium.k8s.policy.cluster=default          10.1.1.150    readying   
           k8s:io.cilium.k8s.policy.serviceaccount=default                                                        
           k8s:io.kubernetes.pod.namespace=default                                                                
           k8s:zgroup=app
```

### 内容解析
- `status`: 检查Cilium组件状态
- `policy get`: 获取网络策略
- `endpoint list`: 列出网络端点

### 注意事项
- 需要Cilium CNI插件
- 依赖eBPF内核功能

### 生产安全风险
- 网络策略错误可能影响服务通信
- eBPF程序错误可能影响系统稳定性

## 40. kind

### 用途
Kubernetes in Docker，用于在Docker容器中快速创建Kubernetes集群。

### 输出示例
```bash
# 创建集群
$ kind create cluster --name my-cluster
Creating cluster "my-cluster" ...
 ✓ Ensuring node image (kindest/node:v1.27.3) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-my-cluster"

# 列出集群
$ kind get clusters
my-cluster

# 加载本地镜像到集群
$ kind load docker-image my-app:latest --name my-cluster
Image: "my-app:latest" with ID "sha256:abc123" not yet present on node "my-cluster-control-plane", loading...

# 删除集群
$ kind delete cluster --name my-cluster
Deleting cluster "my-cluster" ...
```

### 内容解析
- `create cluster`: 创建本地Kubernetes集群
- `get clusters`: 列出所有kind集群
- `load docker-image`: 将本地镜像加载到集群
- `delete cluster`: 删除集群

### 注意事项
- 仅用于开发和测试环境
- 需要Docker运行时

### 生产安全风险
- 不应用于生产环境
- 本地镜像加载可能引入安全风险

## 41. minikube

### 用途
本地Kubernetes环境，用于在单机上运行Kubernetes。

### 输出示例
```bash
# 启动集群
$ minikube start
😄  minikube v1.30.1 on Darwin 13.4
✨  Automatically selected the docker driver
👍  Starting control plane node minikube in cluster minikube
🔥  Creating docker container (CPUs=2, Memory=6000MB) ...
🐳  Preparing Kubernetes v1.26.3 on Docker 20.10.23 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Network Interface) ...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  The 'storage-provisioner' addon is enabled by default
💡  kubectl not found, will skip adding user to docker group
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

# 停止集群
$ minikube stop
✋  Stopping node "minikube"  ...
🛑  Powering off "minikube" via SSH ...

# 获取服务URL
$ minikube service my-service --url
http://127.0.0.1:50000
```

### 内容解析
- `start`: 启动本地Kubernetes集群
- `stop`: 停止集群
- `service`: 获取服务URL
- `dashboard`: 访问Kubernetes仪表板

### 注意事项
- 主要用于开发和测试
- 需要合适的虚拟化支持

### 生产安全风险
- 不应用于生产环境
- 本地开发环境可能有安全配置不足的风险

## 42. skaffold

### 用途
简化Kubernetes应用开发的命令行工具，自动化构建、推送和部署流程。

### 输出示例
```bash
# 开发模式，自动重建和部署
$ skaffold dev
Listing files to watch...
 - my-app
Generating tags...
 - my-app -> my-app:latest
Checking cache...
 - my-app: Found. Pushing
The push refers to repository [docker.io/library/my-app]
latest: digest: sha256:abc123 size: 737
Tags used in deployment:
 - my-app -> my-app:latest
Starting deploy...
 - deployment.apps/my-app created
Watching for changes...
[my-app-xyz] Hello World!

# 构建镜像
$ skaffold build
Generating tags...
 - my-app -> my-app:latest
Building [my-app]...
Sending build context to Docker daemon  3.072kB
Step 1/4 : FROM nginx:alpine
 ---> f7da64e52f02
Step 2/4 : COPY index.html /usr/share/nginx/html/
 ---> Using cache
 ---> 5a1b2c3d4e5f
Successfully built 5a1b2c3d4e5f
Successfully tagged my-app:latest

# 部署应用
$ skaffold run
Tags used in deployment:
 - my-app -> my-app:latest
Starting deploy...
 - deployment.apps/my-app created
```

### 内容解析
- `dev`: 开发模式，自动监听文件变化
- `build`: 构建应用镜像
- `run`: 构建并部署应用
- 需要skaffold.yaml配置文件

### 注意事项
- 需要skaffold.yaml配置文件
- 自动化开发流程

### 生产安全风险
- 自动部署可能引入未经充分测试的代码
- 需要验证构建和部署流程

## 43. k9s

### 用途
Kubernetes终端UI，提供可视化界面管理Kubernetes资源。

### 输出示例
```bash
# 启动k9s界面
$ k9s
# 进入交互式界面，可使用快捷键操作

# 指定命名空间启动
$ k9s -n production
# 在生产命名空间中启动k9s

# 查看特定资源
$ k9s -c pod
# 直接跳转到Pod视图
```

### 内容解析
- 提供彩色终端界面
- 支持实时监控和操作
- 快捷键操作资源

### 注意事项
- 基于终端的UI工具
- 需要kubectl配置

### 生产安全风险
- 提供便捷的资源操作界面，增加误操作风险
- 需要适当的访问控制

## 44. stern

### 用途
多Pod和容器日志查看器，用于同时观察多个Pod的日志。

### 输出示例
```bash
# 观察特定标签的Pod日志
$ stern my-app
+ my-app-6b6b7c7c7c-7x7x7 › my-app
+ my-app-6b6b7c7c7c-8y8y8 › my-app
my-app-6b6b7c7c7c-7x7x7 my-app 2024-01-01T10:00:00.000Z Starting application...
my-app-6b6b7c7c7c-8y8y8 my-app 2024-01-01T10:00:01.000Z Connected to database

# 按正则表达式过滤日志
$ stern my-app --tail 100 --since 1h
# 显示最近1小时的最后100行日志

# 跟踪特定容器
$ stern my-app --container nginx
# 仅跟踪名为nginx的容器
```

### 内容解析
- 支持同时查看多个Pod日志
- 支持正则表达式过滤
- 实时日志流

### 注意事项
- 用于日志聚合查看
- 支持多种过滤选项

### 生产安全风险
- 可能暴露敏感日志信息
- 大量日志输出可能影响性能

## 45. telepresence

### 用途
Kubernetes本地开发工具，允许将本地服务连接到远程Kubernetes集群。

### 输出示例
```bash
# 连接到集群中的服务
$ telepresence connect
Connected to context default (https://kubernetes.docker.internal:6443)

# 代理到特定服务
$ telepresence intercept my-service --port 8080
Using Deployment my-service
intercepted
    State: ACTIVE
    Destination: 127.0.0.1:8080
    Volume Mount Point: /var/folders/...
    Intercepting: all connections
```

### 内容解析
- `connect`: 连接到Kubernetes集群
- `intercept`: 拦截服务流量到本地
- 用于本地开发和调试

### 注意事项
- 需要适当的网络配置
- 用于开发调试场景

### 生产安全风险
- 将本地服务暴露给集群可能带来安全风险
- 需要验证本地环境安全性

## 46. tilt

### 用途
Kubernetes本地开发工具，自动化开发和部署循环。

### 输出示例
```bash
# 启动Tilt开发环境
$ tilt up
Tilt started on http://localhost:10350
v0.31.7, built 2024-01-01

Primary CLI log:
  (Tiltfile) file 'Tiltfile' was created
  Beginning Tiltfile execution
  Successfully loaded Tiltfile
  (main) live_update_demo.go was created
  (main) successfully built and deployed (4.8s)
     Deployed live_update_demo
     Serving on http://localhost:10351

# 停止Tilt
$ tilt down
Stopping Tilt...
```

### 内容解析
- `up`: 启动开发环境
- `down`: 停止开发环境
- 自动化构建和部署

### 注意事项
- 需要Tiltfile配置
- 自动化开发流程

### 生产安全风险
- 主要用于开发环境
- 配置错误可能影响开发流程

## 47. kubectl plugins (如krew)

### 用途
kubectl插件管理系统，扩展kubectl功能。

### 输出示例
```bash
# 查看已安装插件
$ kubectl krew list
PLUGIN          VERSION
ctx             v0.9.0
ns              v0.9.0
view-secret     v0.7.0
who-can         v2.1.0

# 搜索可用插件
$ kubectl krew search
PLUGIN                    DESCRIPTION
affinity                  Generates pod affinity/anti-affinity YAML manifests
apparmor                  View AppArmor profiles
bench                     Run benchmarks against cluster resources
ca-cert                   Print CA certificate of current cluster
conntrack                 Manage conntrack limits in cluster nodes
ctx                       Switch context
dns-test                  Test DNS in cluster
downward                  Print downward API examples

# 安装插件
$ kubectl krew install ctx
Updated the local copy of plugin index.
Installing plugin: ctx
Installed plugin: ctx
\`kubectl ctx\` is now ready to use

# 使用插件
$ kubectl ctx production
Switched to context "production".
```

### 内容解析
- `list`: 列出已安装插件
- `search`: 搜索可用插件
- `install`: 安装插件
- `uninstall`: 卸载插件

### 注意事项
- 插件扩展kubectl功能
- 社区提供丰富的插件

### 生产安全风险
- 插件可能引入安全漏洞
- 需要验证插件来源

## 48. kubectl get componentstatuses

### 用途
获取集群组件的状态信息，如etcd、controller-manager、scheduler等。

### 输出示例
```bash
$ kubectl get componentstatuses
NAME                 STATUS      MESSAGE                                                                                     ERROR
scheduler            Healthy     ok                                                                                          
controller-manager   Healthy     ok                                                                                          
etcd-0               Healthy     {"health":"true"}                                                                           
etcd-1               Healthy     {"health":"true"}                                                                           
etcd-2               Healthy     {"health":"true"}
```

### 内容解析
- 显示集群核心组件的健康状态
- STATUS: 组件当前状态（Healthy/Unhealthy）
- MESSAGE: 状态描述信息

### 注意事项
- 该命令已被弃用，建议使用`kubectl get cs`
- 仅显示控制平面组件状态

### 生产安全风险
- 可能暴露集群内部组件信息
- 有助于攻击者了解集群架构

## 49. kubectl get events

### 用途
获取集群中的事件信息。

### 输出示例
```bash
$ kubectl get events -A
NAMESPACE     LAST SEEN   TYPE      REASON                    OBJECT                              MESSAGE
default       10m         Normal    Scheduled                 pod/my-app-6b6b7c7c7c-7x7x7        Successfully assigned default/my-app-6b6b7c7c7c-7x7x7 to node-1
default       9m          Normal    Pulling                   pod/my-app-6b6b7c7c7c-7x7x7        Pulling image "nginx:latest"
default       8m          Normal    Pulled                    pod/my-app-6b6b7c7c7c-7x7x7        Successfully pulled image "nginx:latest" in 50.123456789s
default       8m          Normal    Created                   pod/my-app-6b6b7c7c7c-7x7x7        Created container my-app
default       8m          Normal    Started                   pod/my-app-6b6b7c7c7c-7x7x7        Started container my-app

$ kubectl get events --sort-by='.lastTimestamp' -A
# 按时间戳排序事件

$ kubectl get events --field-selector type=Warning -A
# 只显示警告事件
```

### 内容解析
- LAST SEEN: 最近一次看到事件的时间
- TYPE: 事件类型（Normal/Warning）
- REASON: 事件原因
- OBJECT: 关联的对象
- MESSAGE: 事件描述

### 注意事项
- 事件有保留期限
- 可用于监控和故障排查

### 生产安全风险
- 事件可能包含敏感配置信息
- 警告事件可能暴露系统弱点

## 50. kubectl get namespaces

### 用途
获取集群中的命名空间列表。

### 输出示例
```bash
$ kubectl get namespaces
NAME              STATUS   AGE
default           Active   365d
kube-node-lease   Active   365d
kube-public       Active   365d
kube-system       Active   365d
production        Active   30d
staging           Active   15d
development       Active   45d
```

### 内容解析
- NAME: 命名空间名称
- STATUS: 命名空间状态（Active/Terminating）
- AGE: 命名空间存在时间

### 注意事项
- 默认命名空间包括default、kube-system等
- 命名空间用于资源隔离

### 生产安全风险
- 显示所有命名空间可能暴露环境信息
- 命名空间权限配置不当可能影响安全

## 51. kubectl create namespace

### 用途
创建新的命名空间。

### 输出示例
```bash
$ kubectl create namespace staging
namespace/staging created

$ kubectl create namespace production --dry-run=client -o yaml
apiVersion: v1
kind: Namespace
metadata:
  creationTimestamp: null
  name: production
```

### 内容解析
- 创建隔离的资源区域
- 可用于环境分离（开发、测试、生产）

### 注意事项
- 命名空间名称必须唯一
- 使用`--dry-run`验证配置

### 生产安全风险
- 创建命名空间需要相应权限
- 需要实施适当的配额管理

## 52. kubectl delete namespace

### 用途
删除命名空间及其包含的所有资源。

### 输出示例
```bash
$ kubectl delete namespace temp-namespace
namespace "temp-namespace" deleted
```

### 内容解析
- 删除命名空间会删除其内的所有资源
- 操作不可逆

### 注意事项
- 操作不可逆，需谨慎执行
- 删除过程中命名空间状态为Terminating

### 生产安全风险
- 可能导致数据丢失
- 影响依赖此命名空间的服务

## 53. kubectl get pods

### 用途
获取Pod列表。

### 输出示例
```bash
$ kubectl get pods -n production
NAME                        READY   STATUS    RESTARTS   AGE
my-app-6b6b7c7c7c-7x7x7    1/1     Running   0          10d
my-app-6b6b7c7c7c-8y8y8    1/1     Running   0          10d
my-app-6b6b7c7c7c-9z9z9    0/1     CrashLoopBackOff   152    10d

$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
my-app-6b6b7c7c7c-7x7x7    1/1     Running   0          10d   10.1.2.10    node-1     <none>           <none>
```

### 内容解析
- READY: 准备就绪的容器数/总容器数
- STATUS: Pod状态（Running, Pending, CrashLoopBackOff等）
- RESTARTS: 重启次数
- AGE: Pod运行时间
- IP: Pod IP地址
- NODE: Pod所在节点

### 注意事项
- 使用`-o wide`显示更多信息
- 高重启次数可能表示存在问题

### 生产安全风险
- 显示Pod信息可能暴露内部结构
- 状态信息可能揭示系统问题

## 54. kubectl delete pod

### 用途
删除Pod。

### 输出示例
```bash
$ kubectl delete pod my-app-6b6b7c7c7c-7x7x7 -n production
pod "my-app-6b6b7c7c7c-7x7x7" deleted

$ kubectl delete pod my-app-6b6b7c7c7c-7x7x7 --force --grace-period=0 -n production
warning: Immediate deletion does not wait for confirmation that the running resource has been terminated. The resource may continue to run on the cluster indefinitely.
pod "my-app-6b6b7c7c7c-7x7x7" force deleted
```

### 内容解析
- 正常删除会等待优雅终止
- `--force --grace-period=0`强制立即删除

### 注意事项
- 对于由控制器管理的Pod，删除后会被重新创建
- 强制删除可能导致数据不一致

### 生产安全风险
- 可能导致服务中断
- 强制删除可能影响数据完整性

## 55. kubectl get deployments

### 用途
获取Deployment列表。

### 输出示例
```bash
$ kubectl get deployments -n production
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
my-app     3/3     3            3           30d
api-svc    2/2     2            2           45d

$ kubectl get deployments -o wide
NAME       READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES         SELECTOR
my-app     3/3     3            3           30d   my-app       nginx:latest   app=my-app
```

### 内容解析
- READY: 就绪副本数/期望副本数
- UP-TO-DATE: 已更新的副本数
- AVAILABLE: 可用副本数
- AGE: Deployment存在时间

### 注意事项
- 显示Deployment的滚动更新状态
- 有助于了解应用部署情况

### 生产安全风险
- 显示应用部署信息可能暴露架构细节
- 镜像信息可能揭示软件版本

## 56. kubectl set image

### 用途
更新Deployment中的容器镜像。

### 输出示例
```bash
$ kubectl set image deployment/my-app my-app=nginx:1.21 -n production
deployment.apps/my-app image updated
```

### 内容解析
- `deployment/name`: 指定Deployment
- `container=image`: 指定容器名和新镜像

### 注意事项
- 触发滚动更新
- 需要验证新镜像的兼容性

### 生产安全风险
- 镜像更新可能引入安全漏洞
- 需要验证镜像来源和完整性

## 57. kubectl rollout restart

### 用途
重启Deployment、DaemonSet或StatefulSet。

### 输出示例
```bash
$ kubectl rollout restart deployment/my-app -n production
deployment.apps/my-app restarted
```

### 内容解析
- 通过更新注解触发滚动重启
- 用于重新加载配置等场景

### 注意事项
- 会导致Pod重新创建
- 服务会短暂中断

### 生产安全风险
- 重启操作可能导致服务中断
- 需要在合适的时间窗口执行

## 59. etcdctl

### 用途
etcd命令行工具，用于与etcd分布式键值存储交互。

### 输出示例
```bash
# 检查etcd成员状态
$ etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key member list
8e9e05c52164694d, started, default, https://localhost:2380, https://localhost:2379, false

# 检查健康状态
$ etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key endpoint health
https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 2.300612ms

# 创建快照
$ etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot save /tmp/etcd-snapshot.db
Snapshot saved at /tmp/etcd-snapshot.db

# 列出键
$ etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key get / --prefix --keys-only
```

### 内容解析
- `member list`: 列出etcd集群成员
- `endpoint health`: 检查etcd端点健康状态
- `snapshot save`: 创建数据快照
- `get`: 获取键值对

### 注意事项
- 需要正确的证书和认证信息
- etcd是Kubernetes的关键组件，操作需谨慎

### 生产安全风险
- 直接访问etcd可能修改集群状态
- 快照可能包含敏感数据

## 60. oc (OpenShift CLI)

### 用途
OpenShift命令行工具，Red Hat OpenShift容器平台的CLI。

### 输出示例
```bash
# 查看项目
$ oc get projects
NAME              DISPLAY NAME   STATUS
default                          Active
kube-public                      Active
kube-system                      Active
openshift                        Active
my-project                       Active

# 查看构建
$ oc get builds -A
NAMESPACE       NAME                    TYPE     FROM          STATUS     STARTED          DURATION
my-project      my-app-1                Source   Git@master    Complete   2 hours ago      2m34s

# 查看部署配置
$ oc get dc -A
NAMESPACE       NAME              REVISION   DESIRED   CURRENT   TRIGGERED BY
my-project      my-app            1          1         1         config,image(my-app:latest)
```

### 内容解析
- `get projects`: 获取OpenShift项目
- `get builds`: 获取构建信息
- `get dc`: 获取部署配置

### 注意事项
- OpenShift基于Kubernetes，但有额外功能
- 与Kubernetes API兼容但有扩展

### 生产安全风险
- 与kubectl类似的安全风险
- OpenShift特有的安全上下文

## 61. argocd

### 用途
Argo CD命令行工具，用于GitOps持续交付。

### 输出示例
```bash
# 列出应用
$ argocd app list
NAME                CLUSTER                         NAMESPACE       PROJECT  STATUS     HEALTH   SYNCPOLICY  CONDITIONS
my-app              https://kubernetes.default:443  default         default  Synced     Healthy  <none>      <none>
frontend            https://kubernetes.default:443  frontend        default  OutOfSync  Healthy  <none>      <none>

# 同步应用
$ argocd app sync my-app
TIMESTAMP                  GROUP        KIND  NAMESPACE  NAME          STATUS    HEALTH        HOOK  MESSAGE
2024-01-01T10:00:00+00:00  apps    Deployment  default    my-app    OutOfSync  Missing            
2024-01-01T10:00:01+00:00  apps    Deployment  default    my-app     Synced  Progressing        

Name:               my-app
Project:            default
Server:             https://kubernetes.default:443
Namespace:          default
URL:                https://argocd.example.com/applications/my-app
Repo:               https://github.com/example/my-app
Target:             HEAD
Current:            HEAD
Status:             Synced
Health Status:      Healthy
Operation:          Sync
Sync Phase:         Succeeded
```

### 内容解析
- `app list`: 列出所有应用
- `app sync`: 同步应用到期望状态
- GitOps实现，状态与Git仓库同步

### 注意事项
- 需要连接到Argo CD服务器
- 依赖Git仓库作为单一事实源

### 生产安全风险
- 权限管理需要严格控制
- Git仓库安全直接影响部署

## 62. flux

### 用途
GitOps工具集，用于自动化Kubernetes配置和镜像更新。

### 输出示例
```bash
# 检查Flux安装
$ flux check
► checking prerequisites
✔ kubectl: vX.Y.Z >= vX.Y.Z-0
✔ Kubernetes: vX.Y.Z >= vX.Y.Z-0
✔ prerequisites are met
► checking controllers
✔ helm-controller: deployment ready
✔ kustomize-controller: deployment ready
✔ notification-controller: deployment ready
✔ source-controller: deployment ready
✔ all checks passed

# 获取Helm发布
$ flux get helmreleases -A
NAMESPACE   NAME        REVISION  SUSPENDED  READY  MESSAGE
default     my-app      3         False      True   Release reconciliation succeeded

# 获取Kustomization
$ flux get kustomizations -A
NAMESPACE   NAME        READY   MESSAGE
default     my-app      True    Applied revision: main/ba3221e

# 获取Git源
$ flux get sources git
NAME        REPO                                      STATUS   LAST UPDATE
my-repo     ssh://git@example.com/my-repo.git       Ready    2024-01-01T10:00:00Z
```

### 内容解析
- `check`: 验证Flux安装状态
- `get helmreleases`: 获取Helm发布状态
- `get kustomizations`: 获取Kustomize应用状态
- `get sources`: 获取源代码仓库状态

### 注意事项
- 需要Flux控制器在集群中运行
- 基于GitOps的工作流程

### 生产安全风险
- 需要适当的RBAC配置
- Git仓库访问需要安全认证

## 63. kubectl argo rollouts

### 用途
Argo Rollouts控制器的kubectl插件，用于管理高级部署策略。

### 输出示例
```bash
# 列出Rollout资源
$ kubectl argo rollouts list rollouts -A
NAMESPACE   NAME        STRATEGY      STATUS     STEP    SET-WEIGHT  READY  DESIRED
default     my-app      Canary        Healthy    4/4     100         3      3

# 查看Rollout状态
$ kubectl argo rollouts get my-app
Name:            my-app
Namespace:       default
Status:          ✅ Healthy
Strategy:        Canary
Images:          nginx:1.20 (stable)
                 nginx:1.21 (canary)
Replicas:
  Desired:       3
  Current:       3
  Updated:       3
  Ready:         3
  Available:     3
```

### 内容解析
- `list rollouts`: 列出所有Rollout资源
- 高级部署策略（蓝绿、金丝雀等）

### 注意事项
- 需要安装Argo Rollouts控制器
- 提供比原生Deployment更高级的部署策略

### 生产安全风险
- 部署策略配置错误可能影响服务可用性
- 需要适当的权限管理

## 64. arkade

### 用途
Kubernetes应用商店，用于轻松安装Kubernetes工具和应用。

### 输出示例
```bash
# 安装工具
$ arkade get helm
Downloading: helm
Downloading: https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz
Downloaded: /home/user/.arkade/bin/helm

$ arkade get istioctl
Downloading: istioctl
Downloaded: /home/user/.arkade/bin/istioctl

# 列出可用应用
$ arkade get --help
# 显示所有可用的应用和工具
```

### 内容解析
- `get`: 下载和安装Kubernetes工具
- 简化工具安装过程

### 注意事项
- 用于开发和管理工具安装
- 不直接操作集群资源

### 生产安全风险
- 下载的工具需要验证来源
- 主要用于管理节点，不影响集群安全

## 66. coredns

### 用途
Kubernetes集群内部DNS服务，为集群提供域名解析。

### 输出示例
```bash
# 查看CoreDNS配置
$ kubectl get configmap coredns -n kube-system -o yaml
apiVersion: v1
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

# 测试DNS解析
$ kubectl run coredns-test --rm -i --tty --image busybox -- nc -zv $COREDNS_SERVICE_IP 53
# 测试DNS服务是否可达

# 检查CoreDNS Pod日志
$ kubectl exec -n kube-system -l k8s-app=coredns -- nslookup google.com 127.0.0.1
# 测试CoreDNS是否能解析外部域名

# 重启CoreDNS
$ kubectl rollout restart deployment/coredns -n kube-system
deployment.apps/coredns restarted
```

### 内容解析
- CoreDNS是Kubernetes的默认DNS服务
- 配置文件定义了DNS解析规则
- 集群内部服务通过域名访问

### 注意事项
- DNS是集群关键服务，需保证高可用
- 配置修改后需重启Pod才能生效

### 生产安全风险
- DNS配置错误会影响整个集群服务发现
- DNS劫持可能重定向服务调用

## 67. cert-manager

### 用途
Kubernetes证书管理工具，自动化证书申请和续期。

### 输出示例
```bash
# 查看证书资源
$ kubectl get certificates,certificaterequests,orders,challenges -A
NAMESPACE   NAME                               READY   SECRET                     AGE
default     certificate.networking.x-k8s.io    True    my-tls-secret             30d

NAMESPACE   NAME                                     READY   ISSUER              AGE
default     certificaterequest.networking.x-k8s.io   True    letsencrypt-prod    30d

# 查看Issuer状态
$ kubectl describe issuer letsencrypt-prod -n cert-manager
Name:         letsencrypt-prod
Namespace:    cert-manager
Labels:       <none>
Annotations:  <none>
API Version:  cert-manager.io/v1
Kind:         Issuer
Spec:
  Acme:
    Email:            admin@example.com
    Private Key Secret Name:  letsencrypt-prod
    Server:           https://acme-v02.api.letsencrypt.org/directory
Status:
  Conditions:
  - Last Transition Time:  2024-01-01T10:00:00Z
    Message:               The ACME account was registered with the ACME server
    Observed Generation:   1
    Reason:                ACMEAccountRegistered
    Status:                True
    Type:                  Ready
```

### 内容解析
- 自动化管理TLS证书
- 支持Let's Encrypt等CA
- 与Ingress控制器集成

### 注意事项
- 需要配置有效的ACME服务器和邮箱
- 证书续期需要网络访问CA

### 生产安全风险
- 证书私钥需要妥善保护
- ACME挑战可能暴露内部服务

## 68. prometheus

### 用途
监控和告警系统，用于收集和查询时间序列数据。

### 输出示例
```bash
# 查看Prometheus相关Pod
$ kubectl get pods -n monitoring -l app in (prometheus,alertmanager,grafana)
NAME                                  READY   STATUS    RESTARTS   AGE
prometheus-server-7d5b6c5c4-xl2v9     1/1     Running   0          30d
prometheus-alertmanager-6c5b4d4c3-y2v9 1/1    Running   0          30d

# 查看Prometheus配置
$ kubectl get configmap -n monitoring prometheus-server-conf -o yaml
# Prometheus配置文件内容

# 端口转发访问UI
$ kubectl port-forward svc/prometheus-server 9090:80 -n monitoring
Forwarding from 127.0.0.1:9090 -> 9090
```

### 内容解析
- 收集Kubernetes集群和应用指标
- 支持PromQL查询语言
- 可配置告警规则

### 注意事项
- 需要足够的存储空间保存指标
- 查询性能随数据量增长而下降

### 生产安全风险
- 暴露内部系统指标
- 需要适当的访问控制

## 69. grafana

### 用途
数据可视化和监控仪表板工具。

### 输出示例
```bash
# 端口转发访问Grafana UI
$ kubectl port-forward svc/grafana 3000:3000
Forwarding from 127.0.0.1:3000 -> 3000

# 查看Grafana Pod状态
$ kubectl get pods -l app.kubernetes.io/name=grafana
NAME                       READY   STATUS    RESTARTS   AGE
grafana-7d5b6c5c4-xl2v9    1/1     Running   0          30d

# 获取初始密码
$ kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

### 内容解析
- 提供丰富的图表和仪表板
- 支持多种数据源（Prometheus、InfluxDB等）
- 用户认证和权限管理

### 注意事项
- 需要配置数据源
- 仪表板可共享和导出

### 生产安全风险
- 需要强密码和认证
- 仪表板可能暴露敏感信息

## 70. fluentd

### 用途
日志收集和转发工具，常用于Kubernetes日志聚合。

### 输出示例
```bash
# 查看日志收集器Pod
$ kubectl get daemonsets -n logging -l app in (fluentd,fluent-bit,logstash)
NAME        DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
fluentd     3         3         3       3            3           <none>          30d

# 查看日志配置
$ kubectl get configmaps -n logging -l app in (fluentd,fluent-bit)
NAME                 DATA   AGE
fluentd-config       1      30d

# 查看日志收集器状态
$ kubectl logs -n logging -l app=fluentd --tail=10
2024-01-01 10:00:00 +0000 [info]: parsing config file is succeeded path="/fluentd/etc/fluent.conf"
2024-01-01 10:00:01 +0000 [info]: using configuration file: <ROOT>
```

### 内容解析
- 收集节点和Pod日志
- 支持多种输出目标（ES、S3、HTTP等）
- 通常以DaemonSet形式部署

### 注意事项
- 需要足够的磁盘空间存储日志
- 配置错误可能导致日志丢失

### 生产安全风险
- 日志可能包含敏感信息
- 需要安全的日志传输通道

## 71. elasticsearch

### 用途
分布式搜索和分析引擎，常用于日志存储和分析。

### 输出示例
```bash
# 查看Elasticsearch集群状态
$ kubectl get statefulsets -l app in (mysql,postgresql,mongodb,elasticsearch) -A
NAMESPACE   NAME                    READY   AGE
logging     elasticsearch-master    3/3     30d

# 检查集群健康
$ kubectl exec -n logging -c elasticsearch elasticsearch-master-0 -- curl -s -XGET 'localhost:9200/_cluster/health?pretty=true'
{
  "cluster_name" : "elasticsearch",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 3,
  "number_of_data_nodes" : 3,
  "discovered_master" : true,
  "discovered_cluster_manager" : true,
  "active_primary_shards" : 10,
  "active_shards" : 20,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```

### 内容解析
- 分布式搜索和分析引擎
- 常与Fluentd或Logstash组成ELK栈
- 需要持久存储

### 注意事项
- 需要大量内存和存储
- 集群配置需要仔细规划

### 生产安全风险
- 存储大量敏感日志数据
- 需要实施访问控制和加密

## 72. trivy

### 用途
开源的漏洞扫描工具，用于容器镜像、文件系统和IaC配置的安全扫描。

### 输出示例
```bash
# 扫描容器镜像
$ trivy image nginx:latest
2024-01-01T10:00:00.000+0000	INFO	Detected OS: debian
2024-01-01T10:00:00.000+0000	INFO	Detecting Debian vulnerabilities...
2024-01-01T10:00:00.000+0000	INFO	Number of language-specific files: 0

nginx:latest (debian 11.7)
==========================
Total: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)

# 扫描文件系统
$ trivy fs /path/to/project
# 扫描项目文件系统中的依赖包漏洞

# 扫描Kubernetes资源配置
$ trivy config --severity HIGH,CRITICAL /path/to/k8s-manifests/
# 扫描Kubernetes配置文件中的安全问题
```

### 内容解析
- `image`: 扫描容器镜像
- `fs`: 扫描文件系统
- `config`: 扫描配置文件
- 支持多种漏洞数据库

### 注意事项
- 定期更新漏洞数据库
- 可集成到CI/CD流水线

### 生产安全风险
- 扫描结果可能暴露安全漏洞
- 扫描过程本身安全

## 73. kyverno

### 用途
Kubernetes原生策略引擎，用于验证、生成和转换资源。

### 输出示例
```bash
# 查看策略
$ kubectl get policies.kyverno.io -A
NAMESPACE   NAME              BACKGROUND   ACTION
default     add-safe-to-evict   true       Audit
monitoring  require-labels      true       Enforce

# 查看策略报告
$ kubectl get polr -A
NAMESPACE   NAME                           PASS   FAIL   WARN   ERROR   SKIP   AGE
default     polr-ns-default-d41d8cd9      10     0      0      0       5      1d
monitoring  polr-ns-monitoring-c1a2b3d4   5      1      0      0       2      1d

# 查看策略详情
$ kubectl describe clusterpolicy add-safe-to-evict
Name:         add-safe-to-evict
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  kyverno.io/v1
Kind:         ClusterPolicy
Metadata:
  Creation Timestamp:  2024-01-01T10:00:00Z
Spec:
  Background:  true
  Rules:
    Match:
      Resources:
        Kinds:
        - Pod
    Name:    autogen-add-safe-to-evict
    Validate:
      Message:  Label 'safe-to-evict' is required.
      Pattern:
        Metadata:
          Labels:
            safe-to-evict: "?*"
  Validation Failure Action:  audit
Status:
  Average Execution Time:  377µs
  Rules Applied Count:     234
```

### 内容解析
- `ClusterPolicy`: 集群范围的策略
- `Policy`: 命名空间范围的策略
- 支持验证、生成和变异三种操作

### 注意事项
- 策略配置错误可能阻止资源创建
- 需要测试策略效果

### 生产安全风险
- 策略错误配置可能影响业务
- 需要谨慎测试策略变更

## 74. kube-linter

### 用途
Kubernetes配置静态分析工具，用于检测配置中的安全和可靠性反模式。

### 输出示例
```bash
# 扫描配置文件
$ kube-linter lint my-app.yaml
my-app.yaml: (object: <unnamed> apps/v1/Deployment) has no resource limits (check: unset-cpu-requirements, remediation: Set the 'resources.limits.cpu' and 'resources.requests.cpu' values on your object.)

my-app.yaml: (object: <unnamed> apps/v1/Deployment) has no resource limits (check: unset-memory-requirements, remediation: Set the 'resources.limits.memory' and 'resources.requests.memory' values on your object.)

my-app.yaml: (object: <unnamed> apps/v1/Deployment) allows running as root (check: run-as-non-root, remediation: Set 'securityContext.runAsNonRoot' to 'true'.)

# 扫描目录
$ kube-linter lint configs/
configs/deployment.yaml: (object: my-app apps/v1/Deployment) ...
# 多个配置文件的扫描结果
```

### 内容解析
- 检测资源限制缺失
- 检测安全上下文问题
- 检测其他配置反模式

### 注意事项
- 可集成到CI/CD流程
- 支持自定义检查规则

### 生产安全风险
- 检测结果帮助改进安全性
- 工具本身无安全风险

## 75. pluto

### 用途
检测Kubernetes清单中已弃用的API版本。

### 输出示例
```bash
# 检测本地文件
$ pluto detect-files -d my-app.yaml
NAME                    VERSION   REPLACEMENT              DEPRECATED   REMOVED
my-app-deployment       v1beta1   apps/v1                  true         false

# 检测Helm发布
$ pluto detect-helm -o wide
RELEASE NAME            CHART                   VERSION   DEPRECATED   REMOVED   NAMESPACE
my-app                  my-app-1.0.0            v1beta1   true         false     default

# 输出表格格式
$ pluto detect-files -d manifests/ -o json
[
  {
    "name": "my-app-deployment",
    "version": "extensions/v1beta1",
    "replacement": "apps/v1",
    "deprecated": true,
    "removed": false,
    "message": "extensions/v1beta1.Deployment is deprecated in favor of apps/v1.Deployment"
  }
]
```

### 内容解析
- 检测弃用的API版本
- 提供替代建议
- 支持多种输出格式

### 注意事项
- 需要及时更新弃用的API
- 避免升级后出现兼容性问题

### 生产安全风险
- 使用弃用API可能导致未来版本不兼容
- 需要定期检查和更新

## 76. linkerd

### 用途
轻量级服务网格，提供服务间通信的可观测性、可靠性和安全性。

### 输出示例
```bash
# 检查Linkerd安装
$ linkerd check
kubernetes-api: can initialize the client..................................[ok]
kubernetes-version: is running the minimum Kubernetes API version........[ok]
linkerd-existence: control plane exists....................................[ok]
linkerd-config: control plane and cli versions match.......................[ok]

# 查看服务统计
$ linkerd viz stat deploy
NAME          MESHED   SUCCESS      RPS   LATENCY_P50   LATENCY_P95   LATENCY_P99   TCP_CONN
my-app           1/1   100.00%   10.00         15ms         45ms         85ms          3

# 监控服务流量
$ linkerd viz tap deploy/my-app
req id=1 src=10.1.2.10:54320 dst=10.1.2.11:8080 tls=disabled :method=GET :authority=my-app:8080 :path=/
rsp id=1 src=10.1.2.10:54320 dst=10.1.2.11:8080 tls=disabled :status=200 latency=2502µs

# 查看拓扑图
$ linkerd viz edges deploy
SRC_NAMESPACE   SRC_NAME   DST_NAMESPACE   DST_NAME
default         my-app     default         db-service
```

### 内容解析
- `check`: 验证Linkerd安装状态
- `viz stat`: 查看服务统计信息
- `viz tap`: 实时监控服务流量
- 提供零信任安全模型

### 注意事项
- 需要注入Linkerd代理
- 轻量级，资源占用较少

### 生产安全风险
- 增加网络延迟
- 需要管理证书和安全策略

## 77. kiali

### 用途
Istio服务网格的管理控制台，提供可视化和服务网格配置管理。

### 输出示例
```bash
# 通过Istioctl打开Kiali
$ istioctl dashboard kiali
2024-01-01T10:00:00.000000Z	info	Opening Kiali in the browser
2024-01-01T10:00:00.000000Z	info	Using namespace: istio-system
2024-01-01T10:00:00.000000Z	info	Executing command: [/usr/local/bin/kubectl --context=default port-forward -n istio-system svc/kiali 20001:20001]

# 分析Istio配置
$ istioctl analyze -A
✔ No validation issues found when analyzing namespace: default.
```

### 内容解析
- 提供服务网格可视化
- 配置验证和分析
- 与Istio深度集成

### 注意事项
- 需要Istio服务网格
- 提供Web UI和API

### 生产安全风险
- 需要适当的访问控制
- 可能暴露服务网格拓扑信息

## 78. jaeger

### 用途
分布式追踪系统，用于监控和故障排查微服务架构。

### 输出示例
```bash
# 通过Istioctl打开Jaeger
$ istioctl dashboard jaeger
2024-01-01T10:00:00.000000Z	info	Opening Jaeger in the browser
2024-01-01T10:00:00.000000Z	info	Using namespace: istio-system
2024-01-01T10:00:00.000000Z	info	Executing command: [/usr/local/bin/kubectl --context=default port-forward -n istio-system svc/tracing 16686:80]

# 查看追踪信息（通过Istio代理）
$ kubectl exec -n kube-system <istio-proxy-pod> -- pilot-agent request GET stats/prometheus
# 获取代理统计信息
```

### 内容解析
- 分布式追踪和监控
- 请求链路分析
- 性能瓶颈识别

### 注意事项
- 需要应用支持追踪头传播
- 存储和计算资源需求较高

### 生产安全风险
- 追踪数据可能包含敏感信息
- 需要配置适当的保留策略

## 79. tempo

### 用途
CNCF沙箱项目，分布式追踪后端，用于存储和查询追踪数据。

### 输出示例
```bash
# 端口转发访问Tempo
$ kubectl port-forward svc/tempo 3100:3100
Forwarding from 127.0.0.1:3100 -> 3100

# Tempo通常与Grafana集成用于追踪查询
# 在Grafana中配置Tempo作为数据源
```

### 内容解析
- 高性能分布式追踪存储
- 与Grafana深度集成
- 支持多种摄取协议

### 注意事项
- 通常与Grafana配合使用
- 需要适当的存储后端

### 生产安全风险
- 存储大量追踪数据
- 需要访问控制和数据保留策略

## 81. buildctl

### 用途
BuildKit的命令行客户端，用于构建容器镜像，是下一代容器构建工具。

### 输出示例
```bash
# 构建镜像
$ buildctl build --frontend dockerfile.v0 --local context=. --local dockerfile=.
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 306B done
#1 DONE 0.0s
#2 [internal] load .dockerignore
#2 transferring context: 2B done
#2 DONE 0.0s
#3 [internal] load metadata for docker.io/library/nginx:alpine
#3 ...
#5 exporting to image
#5 exporting layers done
#5 writing image sha256:abc123... done
#5 naming to docker.io/library/my-app:latest done
#5 DONE 1.2s

# 使用缓存构建
$ buildctl build --frontend dockerfile.v0 --local context=. --local dockerfile=. --import-cache type=registry,ref=my-registry/my-cache --export-cache type=registry,ref=my-registry/my-cache,mode=max
# 利用远程缓存加速构建
```

### 内容解析
- `--frontend`: 指定前端处理器（如Dockerfile）
- `--local`: 指定本地上下文
- `--import-cache/--export-cache`: 导入/导出构建缓存

### 注意事项
- 需要BuildKit守护进程运行
- 支持并发构建和更好的缓存机制

### 生产安全风险
- 构建过程可能引入恶意代码
- 需要验证构建上下文和基础镜像

## 82. kanctl

### 用途
Kanister的命令行工具，用于应用级数据管理，提供数据库备份、恢复等功能。

### 输出示例
```bash
# 创建备份ActionSet
$ kanctl create actionset --action backup --namespace kanister
actionset "backup-abc123" created

# 创建恢复ActionSet
$ kanctl create actionset --action restore --namespace kanister --blueprint <blueprint-name> --args restoreFrom=<backup-location>
actionset "restore-xyz789" created

# 查看ActionSet状态
$ kubectl get actionsets -n kanister
NAME              STATE      PROGRESS   AGE
backup-abc123     complete   1/1        5m
restore-xyz789    complete   1/1        2m
```

### 内容解析
- `create actionset`: 创建执行操作的动作集
- `--action`: 指定执行的操作类型（backup, restore等）
- 基于Blueprint定义的步骤执行

### 注意事项
- 需要Kanister控制器运行
- 需要定义Blueprint来描述操作步骤

### 生产安全风险
- 备份和恢复操作需要适当的权限
- 需要确保备份数据的安全性

## 83. hostnamectl

### 用途
主机名和操作系统信息的系统管理工具。

### 输出示例
```bash
# 查看系统信息
$ hostnamectl
   Static hostname: my-host
   Pretty hostname: My Kubernetes Node
         Icon name: computer-vm
           Chassis: vm
        Machine ID: abc123...
           Boot ID: def456...
    Virtualization: kvm
  Operating System: Ubuntu 22.04.3 LTS
            Kernel: Linux 5.15.0-78-generic
      Architecture: x86-64
   Hardware Vendor: Red Hat
    Hardware Model: KVM
          Firmware: 1.16.0
   Firmware Version: 0.0.0

# 设置主机名
$ sudo hostnamectl set-hostname k8s-node-01
# 设置静态主机名
```

### 内容解析
- 显示系统主机名、操作系统、内核版本等信息
- 可用于设置主机名

### 注意事项
- 在Kubernetes节点上修改主机名需要谨慎
- 可能影响节点标识和通信

### 生产安全风险
- 修改主机名可能影响集群通信
- 需要确保一致性

## 84. journalctl

### 用途
系统日志查看工具，用于查看systemd日志。

### 输出示例
```bash
# 实时查看系统日志
$ journalctl -f
-- Logs begin at Mon 2024-01-01 00:00:00 UTC, end at Mon 2024-01-01 10:00:00 UTC. --
Jan 01 10:00:00 k8s-node-01 systemd[1]: Started kubelet: The Kubernetes Node Agent.
Jan 01 10:00:01 k8s-node-01 kubelet[1234]: I0101 10:00:01.123456    1234 server.go:1234] Starting kubelet

# 查看特定服务日志
$ journalctl -u kubelet.service
-- Logs begin at Mon 2024-01-01 00:00:00 UTC, end at Mon 2024-01-01 10:00:00 UTC. --
Jan 01 09:00:00 k8s-node-01 systemd[1]: Starting kubelet: The Kubernetes Node Agent...
Jan 01 09:00:01 k8s-node-01 systemd[1]: Started kubelet: The Kubernetes Node Agent.

# 查看特定时间段日志
$ journalctl --since "2024-01-01 09:00:00" --until "2024-01-01 10:00:00"
# 查看指定时间范围的日志
```

### 内容解析
- `-f`: 实时跟踪日志
- `-u`: 查看特定unit日志
- `--since/--until`: 指定时间范围

### 注意事项
- 在Kubernetes节点上用于查看系统服务日志
- 包含kubelet、containerd等关键服务日志

### 生产安全风险
- 日志可能包含敏感信息
- 需要适当的访问控制

## 85. sysctl

### 用途
系统内核参数查看和配置工具。

### 输出示例
```bash
# 查看所有内核参数
$ sysctl -a
abi.vsyscall32 = 1
crypto.fips_enabled = 0
debug.exception-trace = 1
fs.aio-max-nr = 65536
fs.aio-nr = 128
fs.epoll.max_user_watches = 524288
fs.file-max = 9223372036854775807
fs.inotify.max_queued_events = 16384
fs.inotify.max_user_instances = 128
fs.inotify.max_user_watches = 524288
kernel.pid_max = 4194304
net.core.somaxconn = 128
net.ipv4.tcp_keepalive_time = 7200
vm.swappiness = 1
vm.overcommit_memory = 1

# 查看特定参数
$ sysctl vm.swappiness
vm.swappiness = 1

# 设置内核参数（临时）
$ sudo sysctl vm.swappiness=10
vm.swappiness = 10

# 永久设置（写入/etc/sysctl.conf）
$ echo "vm.swappiness=1" | sudo tee -a /etc/sysctl.conf
vm.swappiness=1
```

### 内容解析
- `-a`: 显示所有参数
- 动态调整内核参数
- 影响系统性能和行为

### 注意事项
- 参数调整需要谨慎，不当设置可能影响系统稳定性
- 在Kubernetes节点上可能需要调整某些参数以优化性能

### 生产安全风险
- 不当的内核参数可能影响系统安全
- 需要限制对内核参数的修改权限

## 86. systemctl

### 用途
systemd系统和服务管理器的命令行工具。

### 输出示例
```bash
# 查看运行中的服务
$ systemctl list-units --type=service --state=running
UNIT                           LOAD   ACTIVE SUB     DESCRIPTION
containerd.service             loaded active running containerd
kubelet.service                loaded active running kubelet: The Kubernetes Node Agent
docker.service                 loaded active running Docker Application Container Engine
rpcbind.service                loaded active running RPC Bind Port Mapper
rsyslog.service                loaded active running System Logging Service

# 查看服务状态
$ systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2024-01-01 09:00:00 UTC; 1h 0min ago
     Docs: https://kubernetes.io/docs/
 Main PID: 1234 (kubelet)
    Tasks: 25 (limit: 4915)
   Memory: 123.4M
   CGroup: /system.slice/kubelet.service
           └─1234 /usr/bin/kubelet --bootstrap-kubeconfig=...

# 重启服务
$ sudo systemctl restart kubelet
# 重启Kubernetes节点代理服务
```

### 内容解析
- `list-units`: 列出系统单元
- `status`: 查看服务状态
- `start/stop/restart`: 控制服务运行

### 注意事项
- 在Kubernetes节点上管理关键服务
- 重启关键服务可能影响节点功能

### 生产安全风险
- 服务管理需要管理员权限
- 不当操作可能导致节点不可用

## 87. kube-capacity

### 用途
可视化Kubernetes集群资源容量和请求的工具。

### 输出示例
```bash
# 查看集群资源使用情况
$ kube-capacity --util --available
NODE                      CPU REQUESTS   CPU LIMITS   CPU UTIL   CPU AVAILABLE   MEMORY REQUESTS   MEMORY LIMITS   MEMORY UTIL   MEMORY AVAILABLE
control-plane.example.com   510m (13%)     0 (0%)       949m (24%)    2971m         900Mi (12%)       0 (0%)          2.0Gi (2%)      74Gi
worker-1.example.com        30m (1%)       0 (0%)       2.0Gi (6%)      29Gi          150Mi (2%)        0 (0%)          2.5Gi (3%)      71Gi
worker-2.example.com        30m (1%)       0 (0%)       1.8Gi (5%)      30Gi          150Mi (2%)        0 (0%)          2.3Gi (3%)      72Gi

# 以树形结构显示Pod资源请求
$ kube-capacity -t
NODE                      CPU REQUESTS   CPU LIMITS   MEMORY REQUESTS   MEMORY LIMITS
control-plane.example.com   510m (13%)     0 (0%)       900Mi (12%)       0 (0%)
├─ etcd-control-plane.example.com
│     100m (2%)      0 (0%)       100Mi (1%)        0 (0%)
├─ kube-apiserver-control-plane.example.com
│     250m (6%)      0 (0%)       500Mi (6%)        0 (0%)
└─ kube-scheduler-control-plane.example.com
      100m (2%)      0 (0%)       100Mi (1%)        0 (0%)

worker-1.example.com        30m (1%)       0 (0%)       150Mi (2%)        0 (0%)
└─ some-pod-xyz123
      30m (1%)       0 (0%)       150Mi (2%)        0 (0%)
```

### 内容解析
- `--util`: 显示资源利用率
- `--available`: 显示可用资源
- `-t`: 以树形结构显示Pod资源请求

### 注意事项
- 有助于容量规划和资源管理
- 显示资源请求(requests)和限制(limits)

### 生产安全风险
- 显示集群资源信息，需要适当访问控制
- 无直接安全风险

## 88. kuttl (kubectl uttL - KUbernetes Test TooL)

### 用途
Kubernetes集成测试工具，用于编写和运行Kubernetes端到端测试。

### 输出示例
```bash
# 运行测试套件
$ kubectl kuttl test <test-suite>
=== RUN   kutt-test
=== RUN   kutt-test/test-1
--- PASS: test-1 (5.12s)
=== RUN   kutt-test/test-2
--- PASS: test-2 (3.45s)
=== RUN   kutt-test/test-3
--- FAIL: test-3 (2.10s)
    apply.go:85: resource ServiceAccount/test-sa not found

KUTTL TESTS COMPLETE: 2 passed, 1 failed
exit status 1

# 测试文件示例 (test.yaml)
apiVersion: kutt.test/v1beta1
kind: TestSuite
metadata:
  name: example-test
tests:
- name: create-deployment
  steps:
  - name: create-deployment
    apply:
    - deployment.yaml
  - name: assert-deployment-ready
    assert:
    - deployment.yaml
```

### 内容解析
- 用于Kubernetes声明性测试
- 支持资源应用和断言
- 可以验证资源状态

### 注意事项
- 用于测试环境
- 需要编写测试定义文件

### 生产安全风险
- 测试可能修改集群状态
- 需要适当的测试环境隔离

## 89. sonobuoy

### 用途
Kubernetes集群合规性和诊断工具，用于运行Kubernetes官方一致性测试。

### 输出示例
```bash
# 运行一致性测试
$ sonobuoy run --mode certified-conformance
Sonobuoy is running. Check sonobuoy status with:
  sonobuoy status
To retrieve results:
  sonobuoy retrieve

# 检查测试状态
$ sonobuoy status
PLUGIN     STATUS   RESULT   COUNT
e2e        running  passed   1
systemd-logs running  passed   3

# 获取测试结果
$ sonobuoy retrieve
sonobuoy_results_2024-01-01_10_00_00.tar.gz

# 解压并查看结果
$ mkdir results && tar xzf sonobuoy_results_2024-01-01_10_00_00.tar.gz -C results
$ cat results/plugins/e2e/results/global/e2e.log
# 查看详细的测试结果
```

### 内容解析
- `run`: 执行测试
- `status`: 查看测试进度
- `retrieve`: 获取测试结果
- 支持多种测试模式

### 注意事项
- 用于验证Kubernetes集群一致性
- 可能消耗较多资源

### 生产安全风险
- 运行测试可能影响集群性能
- 需要在维护窗口期间运行

## 90. curl

### 用途
命令行传输工具，常用于测试Kubernetes服务连通性、API调用和健康检查。

### 输出示例
```bash
# 测试服务连通性
$ curl http://my-service.default.svc.cluster.local:8080/health
{"status": "ok", "timestamp": "2024-01-01T10:00:00Z"}

# 测试Ingress访问
$ curl -H "Host: myapp.example.com" http://ingress-controller-ip/status
OK

# 测试HTTPS服务
$ curl -k https://my-service:8443/api/v1/status
{"version": "1.0.0", "status": "healthy"}

# 详细请求信息
$ curl -w "Time: %{time_total}s, Code: %{http_code}\n" -o /dev/null -s http://my-service:8080/
Time: 0.123s, Code: 200

# 与Pod中执行
$ kubectl exec <pod-name> -- curl http://localhost:8080/health
{"status": "ok"}
```

### 内容解析
- 测试服务间的网络连通性
- 检查服务健康状态
- 验证API端点可用性

### 注意事项
- 在Pod内执行可测试集群内部网络
- 使用`-k`参数忽略SSL证书验证（仅测试用）

### 生产安全风险
- 可能暴露服务端点信息
- 敏感信息可能通过请求/响应泄露

## 91. openssl

### 用途
SSL/TLS协议工具，用于证书管理、加密操作和TLS连接测试。

### 输出示例
```bash
# 测试TLS连接
$ openssl s_client -connect my-service.default.svc.cluster.local:443 -servername my-service.default.svc.cluster.local
CONNECTED(00000003)
depth=1 CN = kubernetes
verify error:num=19:self signed certificate in certificate chain
---
Certificate chain
 0 s:/CN=my-service.default.svc.cluster.local
   i:/CN=kubernetes
---

# 检查证书详情
$ echo | openssl s_client -connect my-service:443 2>/dev/null | openssl x509 -noout -dates
notBefore=Jan  1 00:00:00 2024 GMT
notAfter=Dec 31 23:59:59 2024 GMT

# 生成自签名证书
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=my-service.default.svc.cluster.local"
Generating a 2048 bit RSA private key
.............................+++
................+++
writing new private key to 'tls.key'
-----
```

### 内容解析
- `s_client`: SSL客户端连接测试
- 证书验证和详细信息查看
- 证书生成和管理

### 注意事项
- 用于验证TLS连接和证书有效性
- 生产环境应使用有效的证书颁发机构

### 生产安全风险
- 证书管理不当可能导致安全漏洞
- 需要保护私钥安全

## 92. ab (Apache Bench)

### 用途
HTTP服务器压力测试工具，用于测试Kubernetes服务性能。

### 输出示例
```bash
# 基础性能测试
$ ab -n 1000 -c 10 https://my-service.default.svc.cluster.local/api/v1/data
This is ApacheBench, Version 2.3 <$Revision: 1879491 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking my-service.default.svc.cluster.local (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests

Server Software:        nginx/1.20.1
Server Hostname:        my-service.default.svc.cluster.local
Server Port:            443
SSL/TLS Protocol:       TLSv1.3,TLS_AES_256_GCM_SHA384,256,256
TLS Server Name:        my-service.default.svc.cluster.local

Document Path:          /api/v1/data
Document Length:        1234 bytes

Concurrency Level:      10
Time taken for tests:   12.345 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      2345678 bytes
HTML transferred:       1234567 bytes
Requests per second:    81.00 [#/sec] (mean)
Time per request:       123.450 [ms] (mean)
Time per request:       12.345 [ms] (mean, across all concurrent requests)
Transfer rate:          185.23 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        5   12   8.2     10      50
Processing:    50  111  45.6    100     300
Waiting:       45  105  42.1     95     290
Total:         55  123  46.1    110     340
```

### 内容解析
- `-n`: 总请求数
- `-c`: 并发数
- 性能指标分析

### 注意事项
- 在测试环境中使用，避免影响生产服务
- 逐步增加负载测试

### 生产安全风险
- 压力测试可能影响服务性能
- 需要在合适的时间窗口执行

## 93. ping

### 用途
网络连通性测试工具，用于检查Kubernetes Pod和服务之间的网络连接。

### 输出示例
```bash
# 测试集群内部连通性
$ ping -c 4 kubernetes.default.svc.cluster.local
PING kubernetes.default.svc.cluster.local (10.96.0.1): 56 data bytes
64 bytes from 10.96.0.1: icmp_seq=0 ttl=64 time=0.123 ms
64 bytes from 10.96.0.1: icmp_seq=1 ttl=64 time=0.145 ms
64 bytes from 10.96.0.1: icmp_seq=2 ttl=64 time=0.132 ms
64 bytes from 10.96.0.1: icmp_seq=3 ttl=64 time=0.156 ms

--- kubernetes.default.svc.cluster.local ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.123/0.140/0.156/0.013 ms

# 在Pod内测试其他服务
$ kubectl exec my-pod -- ping -c 3 other-service
PING other-service.default.svc.cluster.local (10.1.2.3): 56 data bytes
64 bytes from 10.1.2.3: icmp_seq=0 ttl=63 time=0.456 ms
64 bytes from 10.1.2.3: icmp_seq=1 ttl=63 time=0.345 ms
64 bytes from 10.1.2.3: icmp_seq=2 ttl=63 time=0.567 ms
```

### 内容解析
- 测试网络可达性
- 验证DNS解析
- 检查网络延迟

### 注意事项
- ICMP可能被防火墙或网络策略阻止
- 主要用于基本连通性测试

### 生产安全风险
- 网络探测可能触发安全监控
- 大量ping请求可能被误认为攻击

## 94. nslookup

### 用途
域名解析查询工具，用于测试Kubernetes内部DNS解析。

### 输出示例
```bash
# 查询服务地址
$ nslookup my-service.default.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	my-service.default.svc.cluster.local
Address: 10.1.2.3

# 查询API服务器
$ nslookup kubernetes.default.svc.cluster.local
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	kubernetes.default.svc.cluster.local
Address: 10.96.0.1

# 在Pod内执行DNS查询
$ kubectl exec my-pod -- nslookup other-service
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	other-service.default.svc.cluster.local
Address: 10.10.10.10
```

### 内容解析
- 测试Kubernetes内部DNS解析
- 验证服务发现功能
- 检查DNS配置

### 注意事项
- Kubernetes使用CoreDNS或kube-dns提供服务发现
- 需要确保DNS服务正常运行

### 生产安全风险
- DNS查询可能暴露服务信息
- 需要注意DNS安全配置

## 95. nc (netcat)

### 用途
网络工具，用于测试端口连通性、数据传输和网络调试。

### 输出示例
```bash
# 测试端口连通性
$ nc -zv my-service.default.svc.cluster.local 8080
Connection to my-service.default.svc.cluster.local 8080 port [tcp/http-alt] succeeded!

# 测试目标Pod端口
$ kubectl exec my-pod -- nc -zv target-pod-ip 8080
target-pod-ip (10.1.2.4:8080) open

# 端口扫描
$ nc -zv my-service 80 443 8080
my-service (10.1.2.3:80) open
my-service (10.1.2.3:443) open
my-service (10.1.2.3:8080) open

# 发送简单HTTP请求
$ echo -e "GET / HTTP/1.1\r\nHost: my-service\r\n\r\n" | nc my-service 80
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234
...
```

### 内容解析
- `-z`: 扫描模式（不发送数据）
- `-v`: 详细输出
- 测试端口可用性

### 注意事项
- 常用于网络故障排查
- 可以测试TCP/UDP端口

### 生产安全风险
- 端口扫描可能触发安全监控
- 需要适当的网络策略

## 96. wget

### 用途
网络下载工具，也可用于测试HTTP服务可用性。

### 输出示例
```bash
# 测试API服务器可达性
$ wget --spider --timeout=5 https://kubernetes.default/api/v1/namespaces
Spider mode enabled. Check if remote file exists.
Remote file exists.

# 下载配置文件
$ wget http://config-service.default.svc.cluster.local/config.yaml -O /tmp/config.yaml
--2024-01-01 10:00:00--  http://config-service.default.svc.cluster.local/config.yaml
           => '/tmp/config.yaml'
Resolving config-service.default.svc.cluster.local... 10.1.2.3
Connecting to config-service.default.svc.cluster.local|10.1.2.3|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1234 (1.2K) [application/yaml]
Saving to: '/tmp/config.yaml'

# 静默测试服务
$ wget --spider --quiet --timeout=10 http://my-service:8080/health || echo "Service unavailable"
# 无输出表示服务正常
```

### 内容解析
- `--spider`: 仅检查文件是否存在
- `--timeout`: 设置超时时间
- 用于服务可用性测试

### 注意事项
- 适合简单的HTTP请求测试
- 可用于下载配置文件

### 生产安全风险
- 可能暴露服务端点信息
- 下载的文件需要安全验证

## 98. hey

### 用途
HTTP负载生成和基准测试工具，Go语言编写的现代化HTTP基准测试工具，类似于ab但功能更强大。

### 输出示例
```bash
# 基础性能测试
$ hey -z 30s -c 10 http://my-service.default.svc.cluster.local:8080/api/v1/data
Summary:
  Total:	30.0000 secs
  Slowest:	0.5234 secs
  Fastest:	0.0123 secs
  Average:	0.0891 secs
  Requests/sec:	1123.45

  Total data:	12345678 bytes
  Size/request:	98 bytes

Response time histogram:
  0.012 [1]	|
  0.063 [1234]	|∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  0.114 [2345]	|∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  0.165 [1234]	|∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  0.216 [234]	|∎∎∎∎∎
  0.267 [45]	|
  0.318 [12]	|
  0.369 [3]	|
  0.420 [1]	|
  0.471 [0]	|
  0.523 [1]	|

Latency distribution:
  10% in 0.0234 secs
  25% in 0.0456 secs
  50% in 0.0789 secs
  75% in 0.1234 secs
  90% in 0.2345 secs
  95% in 0.3456 secs
  99% in 0.4567 secs

Status code distribution:
  [200]	45678 responses

# 带认证的测试
$ hey -a "username:password" -z 10s http://protected-service/api/data
# 使用基本认证

# POST请求测试
$ hey -m POST -d '{"key":"value"}' -z 10s http://my-service/api/submit
# 发送POST请求
```

### 内容解析
- `-z`: 测试持续时间
- `-c`: 并发请求数
- `-m`: HTTP方法
- `-d`: 请求体数据
- 详细的性能统计和分布信息

### 注意事项
- 用于性能测试和容量规划
- 在测试环境中使用，避免影响生产服务

### 生产安全风险
- 压力测试可能影响服务性能
- 需要在合适的时间窗口执行

## 99. timeout

### 用途
命令执行超时控制工具，用于限制命令执行时间。

### 输出示例
```bash
# 限制命令执行时间
$ timeout 10s nslookup kubernetes.default
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	kubernetes.default.svc.cluster.local
Address: 10.96.0.1

# 超时测试命令
$ timeout 5 wget --spider --timeout=2 https://slow-service:8443/
# 如果超过5秒则命令被终止

# 在脚本中使用
$ timeout 30 sh -c "while ! curl -sf http://my-service:8080/ready; do sleep 1; done"
# 等待服务就绪，最多等待30秒
```

### 内容解析
- 限制命令执行时间
- 避免长时间挂起
- 在脚本和自动化中很有用

### 注意事项
- 用于防止命令无限期运行
- 信号处理需要考虑

### 生产安全风险
- 无直接安全风险
- 可能影响自动化流程

## docker (在K8s环境中的使用)

### 用途
容器化技术，在Kubernetes环境中用于构建和管理容器镜像。

### 输出示例
```bash
# 构建镜像
$ docker build -t my-app:latest .
Sending build context to Docker daemon  10.24kB
Step 1/4 : FROM nginx:alpine
 ---> f7da64e52f02
Step 2/4 : COPY . /usr/share/nginx/html
 ---> 5a1b2c3d4e5f
Successfully built 5a1b2c3d4e5f
Successfully tagged my-app:latest

# 推送镜像到仓库
$ docker push my-app:latest
The push refers to repository [docker.io/library/my-app]
latest: digest: sha256:abc123 size: 737

# 在K8s中使用本地镜像
$ kind load docker-image my-app:latest
Image: "my-app:latest" with ID "sha256:abc123" not yet present on node "my-cluster-control-plane", loading...
```

### 内容解析
- `build`: 构建容器镜像
- `push`: 推送镜像到仓库
- 与K8s集成使用

### 注意事项
- 镜像是K8s部署的基础
- 需要安全扫描镜像

### 生产安全风险
- 不安全的镜像可能引入漏洞
- 需要镜像签名和验证

## 100. kubeseal

### 用途
Sealed Secrets的命令行工具，用于创建可在Kubernetes中安全存储和分享的加密Secret。

### 输出示例
```bash
# 创建SealedSecret
$ echo '{"apiVersion":"v1","kind":"Secret","metadata":{"name":"mysecret","namespace":"myns"},"data":{"key":"value"}}' | kubeseal | kubectl apply -f -
sealedsecret.bitnami.com/mysecret created

# 使用公钥加密本地Secret文件
$ kubeseal --format yaml < mysecret.json > mysealedsecret.json

# 从现有Secret创建SealedSecret
$ kubectl create secret generic mysecret --dry-run=client -o json | kubeseal
```

### 内容解析
- Sealed Secrets允许在版本控制系统中安全存储加密的Secret
- 使用公钥加密，只有控制器能解密
- 支持多种输出格式

### 注意事项
- 需要Sealed Secrets控制器运行在集群中
- 一旦创建，无法解密回明文（除非有私钥）

### 生产安全风险
- 提供了安全的Secret管理方案
- 避免了在Git中存储明文Secret

## 101. kube-score

### 用途
Kubernetes配置静态分析工具，评估工作负载的安全性和健壮性。

### 输出示例
```bash
# 评估配置文件
$ kube-score score my-app.yaml
--------------------
my-app.yaml: Service/my-service
--------------------
[CRITICAL] Service Exposed
	Resource is exposed to traffic from outside the cluster
	Documentation: https://kube-score.readthedocs.io/en/stable/crit-service-exposed.html

--------------------
my-app.yaml: Deployment/my-app
--------------------
[INFO] Container Resource Requests and Limits
	No resource requests or limits defined
	Documentation: https://kube-score.readthedocs.io/en/stable/checks.html#container-resource-requests-and-limits

[MEDIUM] Container Security Context
	Container has no configured security context
	Documentation: https://kube-score.readthedocs.io/en/stable/checks.html#container-security-context

# 输出JSON格式
$ kube-score score --output-format json my-app.yaml
# JSON格式的评估结果
```

### 内容解析
- 提供安全和最佳实践评估
- 分级评分（CRITICAL, HIGH, MEDIUM, LOW, INFO）
- 提供文档链接和改进建议

### 注意事项
- 用于CI/CD流水线中的质量检查
- 可自定义评估标准

### 生产安全风险
- 帮助识别配置中的安全问题
- 促进最佳实践的采用

## 102. kubevious

### 用途
Kubernetes配置验证和文档生成工具，提供可视化的配置分析。

### 输出示例
```bash
# 分析配置并生成报告
$ kubevious analyze --file my-app.yaml
# 分析配置文件

# 启动Web界面
$ kubevious serve
# 启动可视化界面来查看和分析配置
```

### 内容解析
- 配置验证和依赖分析
- 可视化展示
- 文档生成

### 注意事项
- 提供配置的可视化视图
- 帮助理解复杂的配置关系

### 生产安全风险
- 帮助识别配置问题
- 无直接安全风险

## 103. img

### 用途
独立的Dockerfile构建器，用于构建容器镜像。

### 输出示例
```bash
# 构建镜像
$ img build -t my-app:latest .
ERRO[0000] failed to dial gRPC: cannot connect to a socket file
# img需要容器运行时

# 使用根模式构建
$ sudo img build -t my-app:latest .
# 构建过程输出
```

### 内容解析
- 基于BuildKit的镜像构建工具
- 可以在没有Docker daemon的情况下构建镜像

### 注意事项
- 需要root权限或特权访问
- 基于BuildKit技术

### 生产安全风险
- 需要适当的权限管理
- 镜像构建过程的安全性

## 104. crane

### 用途
Google提供的容器镜像工具，用于高效操作容器镜像和注册表。

### 输出示例
```bash
# 拉取镜像清单
$ crane manifest alpine:latest
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
  "config": {
    "mediaType": "application/vnd.docker.container.image.v1+json",
    "size": 1493,
    "digest": "sha256:..."
  },
  "layers": [
    {
      "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
      "size": 2795381,
      "digest": "sha256:..."
    }
  ]
}

# 复制镜像
$ crane cp alpine:latest alpine:3.12
# 复制镜像到新标签

# 获取镜像配置
$ crane config alpine:latest
# 返回镜像配置JSON
```

### 内容解析
- `manifest`: 获取镜像清单
- `config`: 获取镜像配置
- `cp`: 复制镜像
- 高效操作镜像

### 注意事项
- 无需本地容器运行时
- 直接与镜像注册表交互

### 生产安全风险
- 需要安全的镜像来源验证
- 网络传输安全

## 105. ctr

### 用途
containerd的命令行客户端，用于与containerd容器运行时交互。

### 输出示例
```bash
# 列出镜像
$ ctr images list
REF                                                                    TYPE                                                      DIGEST                                                                  SIZE      PLATFORMS   LABELS
docker.io/library/alpine:latest                                          application/vnd.docker.image.rootfs.diff.tar.gzip       sha256:21a3deaa0d32a...                                                   5.8 MiB   linux/amd64 -

# 列出容器
$ ctr containers list
CONTAINER                                                           IMAGE    RUNTIME
my-container                                                        -        io.containerd.runc.v2

# 拉取镜像
$ ctr content fetch docker.io/library/nginx:latest
# 拉取镜像内容
```

### 内容解析
- 与containerd运行时直接交互
- 管理镜像、容器和内容
- 低级别的容器操作

### 注意事项
- 主要用于调试和底层操作
- 通常由Kubernetes节点自动管理

### 生产安全风险
- 直接操作容器运行时
- 需要适当的访问控制

## 106. okteto

### 用途
Kubernetes开发环境工具，提供一键式开发环境和实时同步功能。

### 输出示例
```bash
# 初始化开发环境
$ okteto init
A okteto manifest (okteto.yml) has been written to this folder.
You can customize it to fit your development workflow.

# 启动开发环境
$ okteto up
 ✓  Development environment activated
 ✓  Files synchronized
    Namespace: user
    Name:      my-app
 ✓  Connected to your development environment.
    Your persistent volume is stored in the Okteto Cloud.
    Welcome to your development environment!
 ▶   To redeploy your development environment, hit Ctrl+C and run 'okteto deploy'

# 部署应用
$ okteto deploy
 x  okteto deploy requires the okteto manifest
    To learn more about the okteto manifest, please visit https://okteto.com/docs/reference/manifest/
```

### 内容解析
- `init`: 初始化Okteto配置
- `up`: 启动开发环境
- `deploy`: 部署应用
- 提供云端开发环境

### 注意事项
- 用于简化Kubernetes开发工作流
- 提供文件同步和端口转发

### 生产安全风险
- 需要安全的云端存储
- 访问控制和认证

## 107. kubectl plugins (如kubectx, kubens)

### 用途
kubectl的第三方插件，提供便捷的上下文和命名空间切换功能。

### 输出示例
```bash
# 列出所有上下文
$ kubectx
default
production
staging
minikube

# 切换上下文
$ kubectx production
Switched to context "production".

# 列出命名空间
$ kubens
default
kube-system
kube-public
my-app
staging
production

# 切换命名空间
$ kubens production
Context "production" modified.
Active namespace is "production".
```

### 内容解析
- `kubectx`: 切换Kubernetes上下文
- `kubens`: 切换命名空间
- 提高日常操作效率

### 注意事项
- 需要单独安装插件
- 提高操作效率但需小心避免错误操作

### 生产安全风险
- 切换错误的上下文或命名空间可能导致误操作
- 需要确认操作目标

## 108. ksniff

### 用途
Kubernetes网络流量嗅探工具，用于捕获Pod的网络数据包。

### 输出示例
```bash
# 抓取Pod的网络包
$ kubectl sniff my-pod -n my-namespace
Defaulting container name to my-app.
Pcap file being written to "/tmp/ksniff-result.pcap"
Press any key to stop sniffing

# 抓取特定容器的网络包
$ kubectl sniff my-pod -c my-container -n my-namespace -f "port 80"
# 只抓取80端口的数据包
```

### 内容解析
- 在Pod中注入tcpdump来捕获网络流量
- 用于网络故障排查
- 支持tcpdump过滤器

### 注意事项
- 需要在Pod中注入临时容器
- 可能影响性能

### 生产安全风险
- 可能捕获敏感网络数据
- 需要适当的访问控制

## 109. ktop

### 用途
Kubernetes资源监控工具，提供类似top的界面来查看Pod资源使用情况。

### 输出示例
```bash
# 交互式查看资源使用
$ ktop
# 显示交互式界面，展示各Pod的CPU、内存使用情况

# 指定命名空间
$ ktop -n production
# 仅显示生产命名空间的Pod
```

### 内容解析
- 类似top的交互式界面
- 实时显示Pod资源使用情况
- 便于快速识别资源消耗大的Pod

### 注意事项
- 需要Metrics Server
- 提供直观的资源视图

### 生产安全风险
- 显示资源使用信息
- 无直接安全风险

## 110. restic

### 用途
快速、安全、高效的备份程序，常用于Kubernetes备份解决方案。

### 输出示例
```bash
# 初始化备份仓库
$ restic init --repo /path/to/backup
created restic backend /path/to/backup
Please note that knowledge of your password is required to access the repository.
You can use the "--password-file" option while running restic to read the password from a file.
repository b1234567 opened successfully, password is correct

# 备份目录
$ restic backup --repo /path/to/backup /data/to/backup
enter password for repository:
scan [/data/to/backup]
scanned 10 directories, 50 files in 0:00
[0:01] 100.00%  1.234 MiB / 1.234 MiB  60 / 60 items  0 errors  ETA 0:00
duration: 0:01
snapshot 12345678 saved

# 列出备份
$ restic snapshots --repo /path/to/backup
enter password for repository:
ID        Time                 Host        Tags        Summary
12345678  2024-01-01 10:00:00  my-host                 60 files, 1.234 MiB
```

### 内容解析
- `init`: 初始化备份仓库
- `backup`: 执行备份
- `snapshots`: 列出备份快照
- 增量备份和去重

### 注意事项
- 用于数据备份和恢复
- 支持多种存储后端

### 生产安全风险
- 需要安全的密码管理
- 备份数据需要加密保护

## 111. dstat

### 用途
多功能系统资源统计工具，可用于监控Kubernetes节点资源使用情况。

### 输出示例
```bash
# 显示系统统计信息
$ dstat
----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system--
usr sys idl wai hiq siq| read  writ| recv  send|  in   out | int   csw
  2   1  97   0   0   0|   0     0 | 324B  456B|   0     0 |1234  5678
  1   0  99   0   0   0|   0     0 | 123B  234B|   0     0 |1122  4567

# 显示更多详细信息
$ dstat -clmnd
--cpu- -dsk-full- -net/total- ------memory-usage----- -dsk/sda- --load-
usr sys idl| read  writ| recv  send| used  free| read  writ| avg1 avg5
  2   1  97|   0     0 | 324B  456B| 1.2G 2.8G|   0     0 |0.12 0.08
```

### 内容解析
- 综合显示CPU、内存、磁盘、网络等信息
- 实时监控系统资源
- 丰富的输出选项

### 注意事项
- 用于节点级别监控
- 帮助识别性能瓶颈

### 生产安全风险
- 显示系统资源信息
- 无直接安全风险

## 112. ekubectl

### 用途
增强版kubectl，提供额外的功能和便利性改进。

### 输出示例
```bash
# ekubectl通常提供与kubectl相同的功能，但带有增强特性
$ ekubectl get pods -A --watch
# 可能提供增强的显示功能

# 集成其他便利功能
$ ekubectl cluster-info
# 显示集群信息，可能带有额外的格式化
```

### 内容解析
- 增强的kubectl体验
- 可能包括更好的输出格式、快捷方式等
- 向后兼容kubectl

### 注意事项
- 通常是kubectl的封装
- 提供额外的便利功能

### 生产安全风险
- 与kubectl相同的安全考虑
- 需要验证额外功能的安全性

## 113. nmcli

### 用途
NetworkManager命令行工具，用于配置和管理网络连接，特别是在Kubernetes节点上。

### 输出示例
```bash
# 列出网络连接
$ nmcli connection show
NAME                UUID                                  TYPE      DEVICE
eth0               abc123-...-def456                     ethernet  eth0
docker0            def456-...-ghi789                     bridge    docker0
calico-veth1       ghi789-...-jkl012                     ethernet  cali123

# 查看设备状态
$ nmcli device status
DEVICE  TYPE      STATE         CONNECTION
eth0    ethernet  connected     eth0
docker0 bridge    connected     docker0
lo      loopback  unmanaged     --

# 修改连接
$ sudo nmcli con mod eth0 ipv4.addresses 10.0.0.10/24
# 修改网络配置
```

### 内容解析
- 管理网络连接和设备
- 在Kubernetes节点上用于网络配置
- 支持多种网络类型

### 注意事项
- 用于节点网络配置
- 错误配置可能影响节点网络

### 生产安全风险
- 网络配置错误可能影响集群通信
- 需要适当的权限管理

## 114. iptables

### 用途
Linux内核的包过滤和NAT工具，Kubernetes使用它来实现服务和网络策略。

### 输出示例
```bash
# 查看规则
$ sudo iptables -L -n -v
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain FORWARD (policy DROP 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
 123K  123M KUBE-FORWARD  all  --  *      *       0.0.0.0/0            0.0.0.0/0

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

# 查看NAT表
$ sudo iptables -t nat -L -n -v
# 显示NAT规则，包括Kubernetes服务规则
```

### 内容解析
- 用于实现Kubernetes服务网络
- 处理网络地址转换(NAT)
- 实现网络策略

### 注意事项
- Kubernetes自动管理部分规则
- 手动修改可能影响集群网络

### 生产安全风险
- 直接修改可能破坏集群网络
- 需要深入了解Kubernetes网络模型

## 115. dd

### 用途
数据复制和转换工具，可用于在Kubernetes环境中进行数据操作。

### 输出示例
```bash
# 在Pod中使用dd创建测试文件
$ kubectl exec my-pod -- dd if=/dev/zero of=/tmp/large-file bs=1M count=100
100+0 records in
100+0 records out
104857600 bytes (105 MB, 100 MiB) copied, 0.567890 s, 185 MB/s

# 备份配置文件
$ dd if=/etc/kubernetes/admin.conf of=/backup/admin.conf.backup
# 复制Kubernetes配置文件
```

### 内容解析
- 数据复制和转换
- 可用于创建测试数据
- 备份重要文件

### 注意事项
- 操作需谨慎，错误使用可能损坏数据
- 在Pod中使用需注意存储限制

### 生产安全风险
- 错误操作可能导致数据丢失
- 需要适当的权限控制

## 116. sar

### 用途
系统活动报告工具，用于监控和分析系统性能。

### 输出示例
```bash
# 查看CPU使用情况
$ sar -u 1 3
Linux 5.4.0-124-generic (k8s-node-1)   01/01/2024    _x86_64_    (4 CPU)

10:00:01 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
10:00:02 AM     all      2.00      0.00      1.00      0.00      0.00     97.00
10:00:03 AM     all      1.50      0.00      0.50      0.00      0.00     98.00
10:00:04 AM     all      3.00      0.00      1.00      0.00      0.00     96.00
Average:        all      2.17      0.00      0.83      0.00      0.00     96.83

# 查看内存使用
$ sar -r 1 2
Linux 5.4.0-124-generic (k8s-node-1)   01/01/2024    _x86_64_    (4 CPU)

10:00:01 AM  kbmemfree   kbavail kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
10:00:02 AM    2097152   2516582   2097152     20.00    102400   1048576   4194304     40.00   1572864   1048576      1024
```

### 内容解析
- `sar -u`: CPU使用率
- `sar -r`: 内存使用情况
- `sar -n DEV`: 网络接口统计
- 性能监控和分析

### 注意事项
- 用于节点性能监控
- 需要安装sysstat包

### 生产安全风险
- 显示系统性能信息
- 无直接安全风险

## 117. iperf3

### 用途
网络性能测试工具，用于测量Kubernetes集群内的网络吞吐量。

### 输出示例
```bash
# 服务器端
$ iperf3 -s
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
Accepted connection from 10.1.2.3, port 50000
[  5] local 10.1.2.4 port 5201 connected to 10.1.2.3 port 50002
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-1.00   sec  112 MBytes   940 Mbits/sec
[  5]   1.00-2.00   sec  118 MBytes   990 Mbits/sec
[  5]   2.00-3.00   sec  115 MBytes   965 Mbits/sec

# 客户端
$ iperf3 -c server-pod-ip -t 10
Connecting to host server-pod-ip, port 5201
[  5] local 10.1.2.3 port 50002 connected to server-pod-ip port 5201
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  1.10 GBytes   945 Mbits/sec  345             sender
[  5]   0.00-10.00  sec  1.10 GBytes   944 Mbits/sec                  receiver
```

### 内容解析
- 网络带宽性能测试
- 测量Pod间网络性能
- 评估网络策略影响

### 注意事项
- 用于网络性能基准测试
- 需要在服务端和客户端分别运行

### 生产安全风险
- 大量网络流量可能影响服务
- 需要在维护窗口运行

## 118. chkrootkit, rkhunter

### 用途
系统安全检查工具，用于检测rootkit、后门和其他恶意软件。

### 输出示例
```bash
# chkrootkit检查
$ sudo chkrootkit
ROOTDIR is `/'
Checking `amd'...                                           not found
Checking `basename'...                                       not infected
Checking `chfn'...                                           not infected
...
INFECTED: Possible ITW0RM worm detected

# rkhunter检查
$ sudo rkhunter --check
[ Rootkit Hunter version 1.4.6 ]

Checking system commands...

/usr/bin/chfn                                               [ OK ]
/usr/bin/egrep                                              [ OK ]
...
```

### 内容解析
- `chkrootkit`: 检查rootkit感染
- `rkhunter`: Rootkit Hunter，检测恶意软件
- 定期安全扫描

### 注意事项
- 用于安全审计
- 定期运行以检测威胁

### 生产安全风险
- 检测可能的安全威胁
- 需要定期更新特征库

## 119. resize2fs

### 用途
调整ext2/ext3/ext4文件系统大小，可用于Kubernetes持久卷扩容。

### 输出示例
```bash
# 检查文件系统大小
$ df -h /data
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdc1        10G  2.0G  8.0G  20% /data

# 调整大小（需要先扩展底层存储）
$ sudo resize2fs /dev/sdc1
resize2fs 1.45.5 (07-Jan-2020)
Filesystem at /dev/sdc1 is mounted on /data; on-line resizing required
old_desc_blocks = 2, new_desc_blocks = 3
The filesystem on /dev/sdc1 is now 3145728 (4k) blocks long.
```

### 内容解析
- 动态调整ext文件系统大小
- 支持在线调整（当文件系统已挂载时）
- 用于PV扩容

### 注意事项
- 需要先扩展底层存储
- 可能需要备份数据

### 生产安全风险
- 操作错误可能导致数据丢失
- 需要适当的备份策略

## 120. groups

### 用途
显示用户的组成员身份，用于检查权限配置。

### 输出示例
```bash
# 显示当前用户组
$ groups
users docker kubernetes

# 显示特定用户组
$ groups kubelet
kubelet : kubelet systemd-journal
```

### 内容解析
- 显示用户所属的组
- 检查权限配置
- 验证服务账户权限

### 注意事项
- 用于权限调试
- 检查用户是否具有必要权限

### 生产安全风险
- 显示用户权限信息
- 无直接安全风险

## 121. cgroups

### 用途
控制组管理工具，用于资源限制和隔离，Kubernetes使用它来实现Pod资源限制。

### 输出示例
```bash
# 查看cgroup层次结构
$ ls /sys/fs/cgroup/
cpu  cpuacct  cpuset  devices  freezer  hugetlb  memory  net_cls  net_prio  perf_event  pids

# 查看特定Pod的cgroup信息
$ cat /sys/fs/cgroup/memory/kubepods/pod*/cgroup.procs
# 显示Pod中进程的PID

# 查看内存限制
$ cat /sys/fs/cgroup/memory/kubepods/pod*/memory.limit_in_bytes
9223372036854771712
```

### 内容解析
- 管理资源限制和隔离
- Kubernetes使用cgroups实现QoS
- 用于性能调优

### 注意事项
- 通常由Kubernetes自动管理
- 手动修改可能影响Pod运行

### 生产安全风险
- 直接修改可能影响Pod稳定性
- 需要深入了解cgroup机制

## 122. devspace

### 用途
Kubernetes开发工具，提供一键式开发环境和实时同步。

### 输出示例
```bash
# 初始化项目
$ devspace init
? Which DevSpace should be created? my-app
? Which namespace should be used? default
? Which deployment type do you want to use? Auto-detect
? Which container image should be used? my-app:latest
? Which ports should be exposed? 8080
? Which files should be synchronized? ./src

# 启动开发模式
$ devspace dev
[info]   Waiting for services to be ready...
[done]   Successfully deployed devspace-default
[info]   DevSpace pods are starting...
[info]   DevSpace pods are ready
[info]   Using namespace: default
[info]   Using kube context: minikube
[info]   Forwarding ports...
[info]   Starting devspace-cloud sync...
[info]   Syncing files...
```

### 内容解析
- `init`: 初始化DevSpace配置
- `dev`: 启动开发模式
- 实时同步和端口转发
- 简化Kubernetes开发

### 注意事项
- 用于开发工作流
- 提供快速迭代能力

### 生产安全风险
- 需要适当的访问控制
- 文件同步可能涉及敏感数据

## 123. garden

### 用途
开发环境编排工具，用于管理本地和远程开发环境。

### 输出示例
```bash
# 初始化项目
$ garden init
? Are you sure you want to initialize Garden in the current directory? Yes
✅ Initialized Garden config in project root

# 构建项目
$ garden build
Build ing my-service...
✅ my-service:0.1.0 built in 1.234s

# 部署服务
$ garden deploy
Deploying my-service...
✅ Deployed my-service in 2.345s
```

### 内容解析
- 简化开发环境管理
- 支持多种部署目标
- 自动化构建和部署

### 注意事项
- 用于开发和测试环境
- 提高开发效率

### 生产安全风险
- 配置文件可能包含敏感信息
- 需要适当的访问控制

## 124. conftest

### 用途
配置策略测试工具，用于验证配置文件是否符合策略。

### 输出示例
```bash
# 检查Kubernetes配置
$ conftest test deployment.yaml -p policies/
FAIL - deployment.yaml - CPU limits should be set
FAIL - deployment.yaml - Memory limits should be set
WARN - deployment.yaml - Image tag should be fixed

# 检查多个文件
$ conftest test -p policies/ k8s/
FAIL - ingress.yaml - TLS should be enabled
PASS - service.yaml

# 使用内置策略
$ conftest test --policy https://hub.conftest.dev/kubernetes.rego deployment.yaml
# 使用中心化的策略库
```

### 内容解析
- 基于OPA/Rego的策略验证
- 检查配置合规性
- CI/CD集成

### 注意事项
- 用于策略即代码
- 可与CI/CD流水线集成

### 生产安全风险
- 确保配置符合安全策略
- 无直接安全风险

## 126. polaris

### 用途
Kubernetes配置验证工具，用于检查集群配置是否符合最佳实践和安全策略。

### 输出示例
```bash
# 审计集群
$ polaris audit --audit-path manifests/
{
  "timestamp": "2024-01-01T10:00:00Z",
  "clusterName": "my-cluster",
  "results": [
    {
      "name": "my-app-deployment",
      "namespace": "default",
      "kind": "Deployment",
      "summary": {
        "critical": 1,
        "danger": 2,
        "warning": 3,
        "success": 8
      }
    }
  ]
}

# 生成报告
$ polaris audit --output-file report.html --format html
Audit completed. Report saved to report.html

# 检查配置文件
$ polaris audit --audit-path deployment.yaml
# 检查单个配置文件

# 配置检查
$ polaris dashboard
# 启动Web仪表板
```

### 内容解析
- `audit`: 审计集群或配置文件
- `dashboard`: 启动Web界面
- 检查安全和最佳实践
- 生成合规性报告

### 注意事项
- 用于持续合规性检查
- 可集成到CI/CD流水线

### 生产安全风险
- 帮助识别配置问题
- 促进安全最佳实践

## 128. nh (Nhost CLI)

### 用途
Nhost命令行工具，用于开发和部署Kubernetes原生应用，提供本地开发环境和部署功能。

### 输出示例
```bash
# 安装nh
$ nh install
Installing Nhost CLI...
Nhost CLI installed successfully

# 卸载nh
$ nh uninstall
Uninstalling Nhost CLI...
Nhost CLI uninstalled successfully

# 启动开发环境
$ nh dev start my-workload
Starting development environment for my-workload...
Development environment ready at http://localhost:8080
Syncing files...

# 在Kubernetes上下文中使用
# nh工具通常与Kubernetes开发相关
```

### 内容解析
- `install`: 安装Nhost CLI工具
- `uninstall`: 卸载Nhost CLI工具
- `dev start`: 启动开发环境
- 提供本地开发到Kubernetes的桥梁

### 注意事项
- 用于Kubernetes原生应用开发
- 提供本地开发和调试能力

### 生产安全风险
- 需要验证工具来源
- 本地开发环境可能包含敏感信息

## 129. authconfig

### 用途
认证配置工具，用于管理Kubernetes集群的认证配置。

### 输出示例
```bash
# 配置认证方式
$ authconfig --enableldap --enablekrb5 --update
Updating configuration...
Authentication configuration updated successfully

# 检查认证配置
$ authconfig --test
LDAP authentication: enabled
Kerberos authentication: enabled
Configuration is valid
```

### 内容解析
- 配置多种认证方式
- LDAP、Kerberos等认证集成
- 更新系统认证配置

### 注意事项
- 用于节点级认证配置
- 需要系统级权限

### 生产安全风险
- 认证配置错误可能影响访问控制
- 需要仔细验证配置

## 130. cosign

### 用途
容器签名工具，用于签名和验证容器镜像。

### 输出示例
```bash
# 签名镜像
$ cosign sign --key cosign.key gcr.io/project/image:tag
Pushed signature to: gcr.io/project/image:sha256-xxx.sig

# 验证镜像
$ cosign verify --key cosign.pub gcr.io/project/image:tag
Verification for gcr.io/project/image:tag --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The signatures were verified against the specified public key

# 签名并推送
$ cosign sign-blob --key cosign.key myfile.txt > myfile.sig
# 签名文件
```

### 内容解析
- 容器镜像签名和验证
- 基于密钥的验证
- 透明日志支持

### 注意事项
- 用于镜像供应链安全
- 需要安全管理密钥

### 生产安全风险
- 确保镜像来源可信
- 需要密钥安全管理

## 高级运维场景

除了基本的Kubernetes命令外，在生产环境中还需要掌握以下高级运维场景：

### 故障应急处理

在生产环境中遇到紧急故障时，需要快速响应和处理：

#### 紧急故障诊断脚本
```bash
# 创建紧急诊断脚本
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

echo "\n5. 资源压力检查:"
kubectl top nodes | awk '$3>80 || $5>80 {print "⚠️  节点资源紧张: " $0}'
EOF

chmod +x emergency-check.sh
./emergency-check.sh
```

#### Pod故障应急处理
```bash
# 检查Pod详细状态
kubectl describe pod <pod-name> -n <namespace>

# 查看Pod事件
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>

# 强制删除卡住的Pod
kubectl delete pod <pod-name> -n <namespace> --force --grace-period=0

# 重新调度Pod到特定节点
kubectl cordon <node-name>  # 标记节点不可调度
kubectl uncordon <node-name>  # 恢复节点调度

# 检查Pod启动失败原因
kubectl get pods -n <namespace> --field-selector=status.phase!=Running -o wide
```

#### 节点故障应急
```bash
# 检查节点状态
kubectl get nodes
kubectl describe node <node-name>

# 驱逐节点上的Pod
kubectl drain <node-name> --ignore-daemonsets --delete-local-data

# 恢复节点调度
kubectl uncordon <node-name>

# 检查节点资源使用
kubectl top node <node-name>

# 检查节点条件
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.conditions[*]}{.type}={.status}{" "}{end}{"\n"}{end}'
```

#### 网络故障应急
```bash
# 检查网络策略
kubectl get networkpolicy -A

# 测试Pod间连通性
kubectl exec <source-pod> -- ping <destination-pod-ip>

# 检查Service和Endpoints
kubectl get svc,ep -n <namespace>

# DNS解析测试
kubectl exec <pod-name> -- nslookup kubernetes.default

# 网络延迟测试
kubectl exec <pod-name> -- traceroute <target-service>
```

#### 存储故障应急
```bash
# 检查持久卷状态
kubectl get pv,pvc -A

# 检查存储类
kubectl get storageclass

# 强制删除卡住的PVC
kubectl patch pvc <pvc-name> -p '{"metadata":{"finalizers":null}}' -n <namespace>

# 检查CSI驱动状态
kubectl get csidriver
```

#### 集群组件故障应急
```bash
# 检查API Server状态
kubectl get componentstatuses

# 检查控制平面Pod
kubectl get pods -n kube-system

# 重启核心组件
kubectl delete pod -n kube-system -l tier=control-plane

# 检查etcd状态
kubectl exec -n kube-system etcd-$(hostname) -- etcdctl endpoint health
```

### 容灾切换演练

定期进行容灾演练以确保系统可靠性：

#### 故障切换演练
```bash
# 模拟主集群故障
kubectl cordon primary-node

# 验证应用在备用节点运行
kubectl get pods -A --field-selector spec.nodeName!=primary-node

# 测试数据一致性
kubectl exec <database-pod> -- pg_dump --check <database-name>

# 切换流量到备用集群
kubectl config use-context backup-cluster
kubectl patch service/<service-name> -n <namespace> -p '{"spec":{"selector":{"version":"backup"}}}'
```

#### 数据同步和一致性检查
```bash
# 检查跨集群数据同步状态
kubectl get pods -l app=sync-controller -A

# 验证数据一致性
kubectl exec <verification-pod> -- /verify-data.sh

# 检查备份状态
kubectl get backups -A
```

### 性能优化

#### 资源调优
```bash
# 检查资源使用情况
kubectl top pods -A
kubectl top nodes

# 设置资源限制和请求
kubectl patch deployment/<deployment-name> -n <namespace> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","resources":{"requests":{"cpu":"100m","memory":"128Mi"},"limits":{"cpu":"500m","memory":"512Mi"}}}]}}}}'
```

#### 调度优化
```bash
# 设置节点亲和性
kubectl patch deployment/<deployment-name> -n <namespace> -p '{"spec":{"template":{"spec":{"affinity":{"nodeAffinity":{"preferredDuringSchedulingIgnoredDuringExecution":[{"weight":1,"preference":{"matchExpressions":[{"key":"disktype","operator":"In","values":["ssd"]}]}]}}}}}}'

# 设置Pod反亲和性
kubectl patch deployment/<deployment-name> -n <namespace> -p '{"spec":{"template":{"spec":{"affinity":{"podAntiAffinity":{"preferredDuringSchedulingIgnoredDuringExecution":[{"weight":1,"podAffinityTerm":{"labelSelector":{"matchExpressions":[{"key":"app","operator":"In","values":["<app-name>"]}]}},"topologyKey":"kubernetes.io/hostname"}}]}}}}}'
```

### 安全加固

#### 安全扫描
```bash
# 使用Trivy扫描镜像漏洞
trivy image <image-name>:<tag>

# 扫描Kubernetes资源
trivy k8s --security-checks config,secret

# 扫描集群整体安全
trivy k8s cluster --format sarif > results.sarif
```

#### 安全配置检查
```bash
# 检查RBAC权限
kubectl get rolebindings,clusterrolebindings --all-namespaces -o yaml

# 检查Pod安全策略
kubectl get psp

# 检查网络策略
kubectl get networkpolicy -A
```

### 网络连通性管理

在Kubernetes集群中，网络连通性是关键问题，需要掌握以下诊断和管理方法：

#### 集群内部连通性验证
```bash
# 检查Pod间连通性
kubectl exec <source-pod> -n <namespace> -- ping <destination-pod-ip>

# 检查Service连通性
kubectl exec <pod-name> -n <namespace> -- nslookup <service-name>.<namespace>.svc.cluster.local

# 测试端口连通性
kubectl exec <pod-name> -n <namespace> -- nc -zv <service-name> <port>
```

#### Service网络连通性测试
```bash
# 检查Endpoints
kubectl get endpoints <service-name> -n <namespace>

# 验证负载均衡
kubectl run test-pod --image=nicolaka/netshoot -it --rm -- bash
# 在Pod内执行网络测试
nslookup <service-name>
curl http://<service-name>:<port>/health
```

#### 网络策略连通性验证
```bash
# 检查网络策略
kubectl get networkpolicy -A

# 验证网络策略效果
kubectl run test-pod --image=alpine --restart=Never -- sleep 3600
kubectl exec test-pod -- apk add curl
kubectl exec test-pod -- curl -m 5 <target-service>
```

#### 网络故障排查完整流程
```bash
# 1. 检查Pod状态
kubectl get pods -n <namespace> -o wide

# 2. 检查Service和Endpoints
kubectl get svc,ep -n <namespace>

# 3. 检查网络策略
kubectl get networkpolicy -n <namespace>

# 4. 检查CNI插件状态
kubectl get pods -n kube-system | grep -E "(calico|flannel|cilium)"

# 5. 检查DNS解析
kubectl run debug --image=infoblox/dnstools -it --rm --restart=Never
```

#### 网络性能监控
```bash
# 监控网络带宽使用
kubectl top pods -A --containers

# 检查网络延迟
kubectl exec <pod-name> -- ping -c 4 <destination>

# 监控网络连接数
kubectl exec <pod-name> -- netstat -an | grep ESTABLISHED | wc -l
```

### 存储管理与排查

Kubernetes持久化存储是关键组件，需要掌握以下管理与排查方法：

#### PV/PVC 深度操作
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

#### 存储性能监控
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

#### 存储故障排查
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

#### CSI存储插件诊断
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

### 监控诊断

在Kubernetes生产环境中，监控诊断是保障系统稳定运行的重要手段：

#### 资源监控
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

#### 日志分析
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

#### 事件监控
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

### 调试排错

在Kubernetes环境中，调试排错是运维人员必须掌握的技能：

#### 常见问题诊断
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

#### 网络问题诊断
```bash
# 测试Pod间网络连通性
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- sh

# 进入Pod调试网络
kubectl exec -it <pod-name> -- sh

# 检查DNS解析
kubectl run busybox --rm --image=busybox:1.28 -it -- nslookup <service-name>

# 检查服务连通性
kubectl run busybox --rm --image=busybox:1.28 -it -- wget -qO- http://<service-name>:<port>/health
```

#### 存储问题诊断
```bash
# 检查存储卷挂载状态
kubectl describe pod <pod-name> | grep -A 10 "Volumes"

# 检查存储卷权限
kubectl exec <pod-name> -- ls -la /mount-path

# 检查存储卷容量
kubectl exec <pod-name> -- df -h /mount-path
```

### 安全管理与合规

Kubernetes安全是生产环境的重要考虑因素：

#### RBAC 权限深度管理
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

#### 安全策略检查
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

#### 证书与密钥管理
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

#### 安全扫描与合规检查
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

#### 安全日志分析
```bash
# 查看认证失败事件
kubectl get events --field-selector reason=FailedAuthentication -A

# 监控权限变更
kubectl get events --field-selector reason=PolicyRuleResolutionErrors -A

# 查看安全相关事件
kubectl get events --field-selector type=Warning -A --sort-by='.lastTimestamp'
```

### AI/ML 特殊命令

针对AI/ML工作负载的特殊管理需求，提供专业化的运维支持：

#### GPU 管理和调度
```bash
# 查看GPU资源分配情况
$ kubectl describe nodes | grep -A 5 -B 5 "nvidia.com/gpu"
Name:               worker-gpu-01
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=worker-gpu-01
                    kubernetes.io/os=linux
Capacity:
 cpu:                32
 ephemeral-storage:  101329668Ki
 hugepages-1Gi:      0
 hugepages-2Mi:      0
 memory:             131790164Ki
 nvidia.com/gpu:     4
Allocatable:
 cpu:                31800m
 ephemeral-storage:  93382289152
 hugepages-1Gi:      0
 hugepages-2Mi:      0
 memory:             130512100Ki
 nvidia.com/gpu:     4

# 查看GPU使用情况
$ kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.nvidia\.com/gpu}{"\t"}{.status.capacity.nvidia\.com/gpu}{"\n"}{end}'
worker-gpu-01    4    4
worker-gpu-02    2    2
worker-gpu-03    0    4

# 监控GPU利用率
$ kubectl top nodes --selector='nvidia.com/gpu.present' -o custom-columns='NODE:.metadata.name,GPU_ALLOCATED:.status.allocatable.nvidia\.com/gpu,GPU_CAPACITY:.status.capacity.nvidia\.com/gpu'
NODE            GPU_ALLOCATED   GPU_CAPACITY
worker-gpu-01   4               4
worker-gpu-02   2               2

# 查看GPU工作负载
$ kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests.nvidia\.com/gpu}{"\n"}{end}' | grep -v '<no value>'
kubeflow    training-job-1    2
ai-models   inference-svc-1   1
research    experiment-abc     1
```

#### AI平台资源优化
```bash
# 模型训练资源调优
$ kubectl patch tfjob/my-training-job -n kubeflow -p '{
  "spec": {
    "tfReplicaSpecs": {
      "Worker": {
        "replicas": 4,
        "template": {
          "spec": {
            "containers": [{
              "name": "tensorflow",
              "resources": {
                "requests": {
                  "cpu": "8",
                  "memory": "32Gi",
                  "nvidia.com/gpu": "2"
                },
                "limits": {
                  "cpu": "16",
                  "memory": "64Gi",
                  "nvidia.com/gpu": "2"
                }
              }
            }]
          }
        }
      }
    }
  }
}' --type=merge

# 推理服务自动扩缩容配置
$ kubectl patch inferenceservice/my-model -n kubeflow -p '{
  "spec": {
    "predictor": {
      "minReplicas": 2,
      "maxReplicas": 10,
      "scaleTarget": 70,
      "scaleMetric": "CPUUtilization"
    }
  }
}' --type=merge

# 模型版本管理
$ kubectl get inferenceservices -n kubeflow -o custom-columns='NAME:.metadata.name,DEFAULT:.status.default.url,CANARY:.status.canary.url,READY:.status.conditions[?(@.type=="Ready")].status'
NAME           DEFAULT                          CANARY                           READY
sentiment-v1   http://sentiment-v1.kubeflow     <none>                           True
sentiment-v2   http://sentiment-v2.kubeflow     http://sentiment-canary.kubeflow False
```

#### AI平台监控和可观测性
```bash
# 模型性能监控
$ kubectl get inferenceservices -n kubeflow -o jsonpath='{
  range .items[*]
}{
  .metadata.name
}{"\t"}{
  .status.url
}{"\t"}{
  .status.modelStatus.states.activeModelState
}{"\n"}{
  end
}'
sentiment-model    http://sentiment-model.kubeflow.svc.cluster.local    Loaded

# 训练任务进度跟踪
$ kubectl get tfjobs -n kubeflow -o custom-columns='NAME:.metadata.name,STATE:.status.conditions[?(@.type=="Succeeded")].status,DURATION:.status.completionTime'
NAME              STATE     DURATION
training-job-1    True      2024-01-01T15:30:45Z
training-job-2    False     <none>

# GPU内存使用分析
$ kubectl exec -n kubeflow $(kubectl get pods -n kubeflow -l training-job-name=training-job-1 -o jsonpath='{.items[0].metadata.name}') -- nvidia-smi
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.82.01    Driver Version: 470.82.01    CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla V100-PCIE...  Off  | 00000000:00:04.0 Off |                    0 |
| N/A   45C    P0    56W / 250W |  16384MiB / 32768MiB |     85%      Default |
+-------------------------------+----------------------+----------------------+

# 模型推理延迟监控
$ kubectl exec -n kubeflow $(kubectl get pods -n kubeflow -l component=predictor -o jsonpath='{.items[0].metadata.name}') -- curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8080/v1/models/my-model:predict" -d '{"instances": [{"text": "sample input"}]}'
     time_namelookup:  0.001
        time_connect:  0.002
     time_appconnect:  0.000
    time_pretransfer:  0.002
       time_redirect:  0.000
  time_starttransfer:  0.150
                     ----------
          time_total:  0.152
```

#### AI平台安全和合规
```bash
# 模型访问控制
$ kubectl patch inferenceservice/sentiment-model -n kubeflow -p '{
  "spec": {
    "predictor": {
      "containers": [{
        "name": "kfserving-container",
        "env": [{
          "name": "AUTH_ENABLED",
          "value": "true"
        }, {
          "name": "API_KEY_HEADER",
          "value": "X-API-Key"
        }]
      }]
    }
  }
}' --type=merge

# 模型数据加密
$ kubectl create secret generic model-encryption-key -n kubeflow \
  --from-literal=encryption-key=$(openssl rand -base64 32)

$ kubectl patch inferenceservice/sensitive-model -n kubeflow -p '{
  "spec": {
    "predictor": {
      "volumes": [{
        "name": "encryption-keys",
        "secret": {
          "secretName": "model-encryption-key"
        }
      }],
      "volumeMounts": [{
        "name": "encryption-keys",
        "mountPath": "/etc/encryption"
      }]
    }
  }
}' --type=merge

# 模型版本审计
$ kubectl get inferenceservices -n kubeflow -o jsonpath='{
  range .items[*]
}{
  .metadata.name
}{"\t"}{
  .metadata.annotations.model\.kubeflow\.org/version
}{"\t"}{
  .metadata.creationTimestamp
}{"\n"}{
  end
}' | sort -k3
sentiment-v1    1.0.0    2024-01-01T10:00:00Z
sentiment-v2    1.1.0    2024-01-02T14:30:00Z
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
  
  # 检查GPU状态
  kubectl exec $TRAINING_POD -n $NAMESPACE -- nvidia-smi
  
  # 检查资源使用
  kubectl top pod $TRAINING_POD -n $NAMESPACE
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
  
  # 测试服务连通性
  kubectl exec -n $NAMESPACE $PREDICTOR_POD -- curl -s http://localhost:8080/v1/models/$SERVICE_NAME
}

# 使用示例
diagnose_training_job my-failed-training-job kubeflow
diagnose_inference_service my-model kubeflow
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
  
  # CPU使用情况
  kubectl top pod $TRAINING_POD -n $NAMESPACE
  
  # 网络I/O监控
  kubectl exec $TRAINING_POD -n $NAMESPACE -- cat /proc/net/dev
}

# 推理性能优化
optimize_inference_performance() {
  SERVICE_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "⚡ 推理性能优化: $SERVICE_NAME"
  
  # 批处理大小优化
  kubectl patch inferenceservice $SERVICE_NAME -n $NAMESPACE -p '{
    "spec": {
      "predictor": {
        "batching": {
          "maxBatchSize": 32,
          "maxLatency": "100ms"
        }
      }
    }
  }' --type=merge
  
  # 资源调整
  kubectl patch inferenceservice $SERVICE_NAME -n $NAMESPACE -p '{
    "spec": {
      "predictor": {
        "containers": [{
          "name": "kfserving-container",
          "resources": {
            "requests": {
              "cpu": "2",
              "memory": "4Gi"
            },
            "limits": {
              "cpu": "4",
              "memory": "8Gi"
            }
          }
        }]
      }
    }
  }' --type=merge
}

# 模型缓存优化
enable_model_caching() {
  SERVICE_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  kubectl patch inferenceservice $SERVICE_NAME -n $NAMESPACE -p '{
    "spec": {
      "predictor": {
        "containers": [{
          "name": "kfserving-container",
          "env": [{
            "name": "MODEL_CACHE_SIZE",
            "value": "2GB"
          }, {
            "name": "MODEL_CACHE_TTL",
            "value": "3600"
          }]
        }]
      }
    }
  }' --type=merge
}
```

#### AI平台容量规划
```bash
# 资源需求预测
calculate_ai_resource_needs() {
  echo "📈 AI平台资源需求分析"
  
  # 统计当前AI工作负载
  echo "当前训练任务资源使用:"
  kubectl get tfjobs,pytorchjobs -A -o jsonpath='{
    range .items[*]
  }{
    .metadata.namespace
  }{"\t"}{
    .metadata.name
  }{"\t"}{
    .spec.tfReplicaSpecs.Worker.replicas
  }{"\t"}{
    .spec.tfReplicaSpecs.Worker.template.spec.containers[0].resources.requests.nvidia\.com/gpu
  }{"\n"}{
    end
  }'
  
  # GPU资源规划
  echo "GPU资源规划建议:"
  kubectl get nodes -l nvidia.com/gpu.present -o jsonpath='{
    range .items[*]
  }{
    .metadata.name
  }{"\t"}{
    .status.allocatable.nvidia\.com/gpu
  }{"\n"}{
    end
  }'
  
  # 存储需求分析
  echo "模型存储需求:"
  kubectl get pvc -n kubeflow -l app=model-storage -o jsonpath='{
    range .items[*]
  }{
    .metadata.name
  }{"\t"}{
    .spec.resources.requests.storage
  }{"\n"}{
    end
  }'
}

# 自动扩缩容配置
configure_autoscaling() {
  SERVICE_NAME=$1
  NAMESPACE=${2:-kubeflow}
  
  echo "📉 配置自动扩缩容: $SERVICE_NAME"
  
  # 配置HPA
  kubectl autoscale deployment $SERVICE_NAME-predictor-default -n $NAMESPACE \
    --cpu-percent=70 \
    --min=2 \
    --max=20
  
  # 配置垂直Pod自动扩缩容
  kubectl patch vpa $SERVICE_NAME-vpa -n $NAMESPACE -p '{
    "spec": {
      "targetRef": {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "name": "'$SERVICE_NAME'-predictor-default"
      },
      "updatePolicy": {
        "updateMode": "Auto"
      }
    }
  }' --type=merge
}
```

## 补充说明

除了上述详细列出的工具外，Kubernetes生态系统还包括许多其他工具，如：

- **Tekton**: 用于在Kubernetes上构建、测试和部署管道的框架
- **Crossplane**: 用于构建平台的开源控制平面
- **Ansible & Terraform**: 用于基础设施即代码和配置管理
- **Cloud CLI工具** (gcloud, az, aws): 用于管理云提供商资源
- **安全工具** (Anchore, Clair, Sysdig等): 用于安全扫描和合规性检查
- **SSH, SCP, RSYNC**: 用于安全远程访问和文件传输
- **网络工具** (Nmap, Telnet, Netcat等): 用于网络诊断和测试

这些工具在特定场景下也非常有用，可以根据具体需求选用相应的工具。

## 96. kubectl taint

### 用途
`taint` 是Kubernetes中用于在节点上设置污点的命令，与toleration配合使用，可以控制Pod能否被调度到特定节点上。污点(Taint)是一种标记，允许节点排斥某些Pod，除非这些Pod具有相应的容忍度(Toleration)。

### 输出示例
```bash
# 为节点添加污点
$ kubectl taint nodes node-1 key1=value1:NoSchedule
node/node-1 tainted

# 为节点添加多个污点
$ kubectl taint nodes node-1 key1=value1:NoSchedule key2=value2:NoExecute
node/node-1 tainted

# 移除节点上的污点
$ kubectl taint nodes node-1 key1:NoSchedule-
node/node-1 untainted

# 移除节点上的所有污点
$ kubectl taint nodes node-1 key1-
node/node-1 untainted

# 查看节点污点信息
$ kubectl describe node node-1 | grep -i taint
Taints:             key1=value1:NoSchedule
                    key2=value2:NoExecute
```

### 内容解析
- **Taint Effect**: 污点的影响效果
  - `NoSchedule`: 不允许Pod调度到该节点，不驱逐已有Pod
  - `PreferNoSchedule`: 尽量避免调度到该节点，非强制
  - `NoExecute`: 不允许Pod调度到该节点，并驱逐不符合条件的已有Pod
- **Key=Value**: 污点的键值对标识
- **移除标识(-)**: 在键后加`-`表示移除该污点

### 注意事项
- 污点和容忍度是控制Pod调度的重要机制
- `NoExecute`会影响已经在节点上的Pod
- 污点通常用于专用节点管理（如GPU节点、监控节点等）

### 生产安全风险
- 错误的污点设置可能导致节点不可用
- `NoExecute`会驱逐节点上的Pod，需谨慎使用

## 97. kubectl version

### 用途
`version` 命令用于显示客户端(kubectl)和服务器(Kubernetes集群)的版本信息，是验证环境和排查版本兼容性问题的基础工具。

### 输出示例
```bash
# 显示客户端和服务器版本
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"28", GitVersion:"v1.28.2", GitCommit:"89200d9c78ee464c25c0d1ea8a31ef88b1d0b528", GitTreeState:"clean", BuildDate:"2023-09-20T16:22:40Z", GoVersion:"go1.21.0", Compiler:"gc", Platform:"darwin/amd64"}
Server Version: version.Info{Major:"1", Minor:"28", GitVersion:"v1.28.2", GitCommit:"89200d9c78ee464c25c0d1ea8a31ef88b1d0b528", GitTreeState:"clean", BuildDate:"2023-09-20T16:22:40Z", GoVersion:"go1.21.0", Compiler:"gc", Platform:"linux/amd64"}

# 仅显示版本号
$ kubectl version --short
Client Version: v1.28.2
Server Version: v1.28.2

# 以JSON格式输出
$ kubectl version -o json
{
  "clientVersion": {
    "major": "1",
    "minor": "28",
    "gitVersion": "v1.28.2",
    ...
  },
  "serverVersion": {
    "major": "1",
    "minor": "28",
    "gitVersion": "v1.28.2",
    ...
  }
}

# 检查版本差异
$ kubectl version --output=custom-columns='CLIENT:clientVersion.gitVersion,SERVER:serverVersion.gitVersion'
CLIENT   SERVER
v1.28.2  v1.28.2
```

### 内容解析
- **Client Version**: kubectl客户端版本信息
- **Server Version**: Kubernetes集群服务器版本信息
- **GitVersion**: Git提交版本号
- **GitCommit**: Git提交哈希值
- **BuildDate**: 构建日期
- **GoVersion**: Go语言版本
- **Platform**: 平台信息

### 注意事项
- 版本差异过大可能导致兼容性问题
- 生产环境应保持版本一致性
- 定期检查版本更新和安全补丁

### 生产安全风险
- 版本过旧可能存在安全漏洞
- 版本不一致可能导致功能异常

## 98. kubectl whoami

### 用途
`whoami` 命令用于显示当前认证用户的详细信息，包括用户名、用户ID和所属组，是验证身份认证和权限的有效工具。

### 输出示例
```bash
# 显示当前用户信息
$ kubectl whoami
NAME: system:serviceaccount:default:default
UID: 12345678-1234-1234-1234-123456789012

# 以JSON格式输出详细信息
$ kubectl whoami -o json
{
  "apiVersion": "authorization.k8s.io/v1",
  "kind": "SelfSubjectReview",
  "metadata": {
    "creationTimestamp": null
  },
  "status": {
    "userInfo": {
      "groups": [
        "system:authenticated",
        "system:masters"
      ],
      "uid": "12345678-1234-1234-1234-123456789012",
      "username": "admin@example.com"
    }
  }
}

# 显示用户组信息
$ kubectl whoami --output=custom-columns='USER:.status.userInfo.username,GROUPS:.status.userInfo.groups'
USER              GROUPS
admin@example.com [system:authenticated,system:masters]

# 检查认证状态
$ kubectl whoami 2>/dev/null && echo "认证成功" || echo "认证失败"
认证成功
```

### 内容解析
- **NAME**: 当前认证的用户名
- **UID**: 用户唯一标识符
- **Groups**: 用户所属的组列表
- **UserInfo**: 包含完整的用户认证信息

### 注意事项
- 需要启用SelfSubjectReview API
- 用于验证当前上下文的认证状态
- 在多租户环境中确认操作主体

### 生产安全风险
- 显示敏感的用户身份信息
- 确保认证信息准确无误

## 99. kubectl tree

### 用途
`tree` 命令（通常作为kubectl插件）用于以树状图形式显示资源的层次结构和依赖关系，帮助理解Kubernetes资源间的父子关系和所有权。

### 输出示例
```bash
# 显示Deployment的资源树
$ kubectl tree deploy my-app
NAMESPACE  NAME                   READY  REASON  AGE
default    Deployment/my-app      -              30d
default    ├─ReplicaSet/my-app-558bd4d5db  -           30d
default    └─ReplicaSet/my-app-7c7c7c7c7c  -           15d
           ├─Pod/my-app-558bd4d5db-2scbw  True   30d
           └─Pod/my-app-558bd4d5db-5x7x7  True   30d

# 显示StatefulSet的资源树
$ kubectl tree sts database
NAMESPACE  NAME                    READY  REASON  AGE
default    StatefulSet/database    -              45d
default    └─Pod/database-0        True           45d
default    └─Pod/database-1        True           45d

# 显示Job的资源树
$ kubectl tree job my-job
NAMESPACE  NAME              READY  REASON  AGE
default    Job/my-job        -              5d
default    └─Pod/my-job-5x7x7  True   30s   5d

# 显示PVC的资源依赖树
$ kubectl tree pvc data-volume
NAMESPACE  NAME                    READY  REASON  AGE
default    PersistentVolumeClaim/data-volume  True   60d
default    └─PersistentVolume/pvc-12345678-1234-1234-1234-123456789012  Bound  60d
```

### 内容解析
- 层次结构显示资源的所有权关系
- 显示资源的当前状态（Ready、Reason等）
- 展示父资源与其子资源的关系
- 有助于理解资源依赖和清理顺序

### 注意事项
- 需要安装kubectl-tree插件
- 显示资源的真实依赖关系
- 有助于资源清理和故障排查

### 生产安全风险
- 无显著安全风险
- 有助于理解资源依赖关系

## 100. kubectl neat

### 用途
`neat` 命令（kubectl插件）用于清理和简化Kubernetes资源配置的输出，去除冗余信息，保留核心配置，便于阅读和理解。

### 输出示例
```bash
# 简化Pod配置输出
$ kubectl get pod my-pod -o yaml | kubectl neat
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  namespace: default
spec:
  containers:
  - image: nginx:latest
    name: nginx
    ports:
    - containerPort: 80
      protocol: TCP

# 简化Deployment配置
$ kubectl get deployment my-app -o yaml | kubectl neat
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - image: nginx:latest
        name: nginx

# 与其他命令结合使用
$ kubectl describe pod my-pod | kubectl neat
Name:         my-pod
Namespace:    default
Priority:     0
Labels:       app=my-app
Annotations:  <none>
Status:       Running
IP:           10.244.1.10
Containers:
  nginx:
    Image:        nginx:latest
    Port:         80/TCP
    Host Port:    0/TCP
    State:        Running
      Started:    Mon, 01 Jan 2024 10:00:00 +0000
    Ready:        True
```

### 内容解析
- 去除自动生成的元数据（如uid、resourceVersion等）
- 保留核心配置信息
- 使配置更易于理解和分享
- 便于配置审查和版本控制

### 注意事项
- 需要安装kubectl-neat插件
- 简化后的配置不适用于apply操作
- 主要用于查看和理解配置

### 生产安全风险
- 无显著安全风险
- 有助于配置审查和理解

## 101. kubectl outdate

### 用途
`outdate` 命令（kubectl插件）用于检查集群中运行的镜像是否有可用更新，帮助维护者识别过时的镜像版本，确保安全补丁及时应用。

### 输出示例
```bash
# 检查所有命名空间的过时镜像
$ kubectl outdate
NAMESPACE    WORKLOAD-TYPE  WORKLOAD-NAME    CURRENT-IMAGE         LATEST-IMAGE          OUTDATED
default      Deployment     my-app           nginx:1.20.1          nginx:1.25.3          true
kube-system  DaemonSet      kube-proxy       k8s.gcr.io/kube-proxy:v1.24.0  k8s.gcr.io/kube-proxy:v1.28.2  true
monitoring   Deployment     prometheus       prom/prometheus:v2.35.0  prom/prometheus:v2.48.1  true

# 检查特定命名空间
$ kubectl outdate -n default
NAMESPACE    WORKLOAD-TYPE  WORKLOAD-NAME    CURRENT-IMAGE         LATEST-IMAGE          OUTDATED
default      Deployment     my-app           nginx:1.20.1          nginx:1.25.3          true

# 检查特定类型的资源
$ kubectl outdate --workload-type Deployment
NAMESPACE    WORKLOAD-TYPE  WORKLOAD-NAME    CURRENT-IMAGE         LATEST-IMAGE          OUTDATED
default      Deployment     my-app           nginx:1.20.1          nginx:1.25.3          true
monitoring   Deployment     prometheus       prom/prometheus:v2.35.0  prom/prometheus:v2.48.1  true

# 仅显示过时的镜像
$ kubectl outdate --outdated-only
NAMESPACE    WORKLOAD-TYPE  WORKLOAD-NAME    CURRENT-IMAGE         LATEST-IMAGE          DAYS-BEHIND
default      Deployment     my-app           nginx:1.20.1          nginx:1.25.3          120
kube-system  DaemonSet      kube-proxy       k8s.gcr.io/kube-proxy:v1.24.0  k8s.gcr.io/kube-proxy:v1.28.2  90
```

### 内容解析
- **CURRENT-IMAGE**: 当前运行的镜像版本
- **LATEST-IMAGE**: 最新可用的镜像版本
- **OUTDATED**: 是否存在更新
- **DAYS-BEHIND**: 落后的天数
- 帮助识别安全漏洞和功能更新

### 注意事项
- 需要网络访问以检查镜像仓库
- 仅提供信息，不自动更新镜像
- 需要测试新版本的兼容性

### 生产安全风险
- 过时镜像可能包含安全漏洞
- 需要建立镜像更新流程

## 102. kubectl who-can

### 用途
`who-can` 是Kubernetes的一个重要插件，用于查找哪些用户、服务账户或组有权执行特定的操作（动词）在特定的资源上。这是权限审计和安全检查的关键工具，可以帮助识别潜在的过度权限问题。

### 输出示例
```bash
# 检查谁有权读取Pods
$ kubectl who-can get pods
ROLEBINDING            SUBJECT            VERB   RESOURCE
kube-system/extension-apiserver-authentication-reader  SystemGroup:system:masters  get    selfsubjectaccessreviews.authorization.k8s.io
kube-system/system::leader-locking-kube-scheduler      User:system:kube-scheduler  get    configmaps
default/read-pods-binding                            ServiceAccount:default:default  get    pods

# 检查谁有权创建Deployments
$ kubectl who-can create deployments
CLUSTERROLEBINDING     SUBJECT            VERB     RESOURCE
cluster-admin          Group:system:masters  create   deployments.apps
admin                  Group:system:authenticated  create   deployments.apps

# 检查特定命名空间中的权限
$ kubectl who-can delete secrets -n production
ROLEBINDING            SUBJECT            VERB   RESOURCE
production/admin-role  User:admin@example.com  delete   secrets

# 检查谁有权访问特定资源实例
$ kubectl who-can patch deployments/my-app
CLUSTERROLEBINDING     SUBJECT            VERB   RESOURCE
cluster-admin          Group:system:masters  patch  deployments.apps/my-app

# 检查所有命名空间中的特定权限
$ kubectl who-can --all-namespaces get services
CLUSTERROLEBINDING     SUBJECT            VERB   RESOURCE
system:basic-user      Group:system:authenticated  get    services
system:discovery       Group:system:authenticated  get    services
```

### 内容解析
- **ROLEBINDING/CLUSTERROLEBINDING**: 权限绑定的名称
- **SUBJECT**: 获得权限的实体（用户、组或服务账户）
- **VERB**: 允许的操作（get, create, update, delete, patch等）
- **RESOURCE**: 受影响的资源类型
- 显示了RBAC权限的实际分配情况

### 注意事项
- 需要安装kubectl-who-can插件
- 需要足够的权限查看RBAC资源
- 结果可能受到ClusterRole和Role的不同作用范围影响
- 对于复杂权限结构，输出可能很长

### 生产安全风险
- 暴露了权限分配信息，应限制访问
- 发现过度权限应及时修正
- 定期审计权限分配情况

## 103. kubectl cluster-info

### 用途
`cluster-info` 命令用于显示Kubernetes集群的主节点和服务端点信息，包括API Server、KubeDNS或CoreDNS等关键组件的地址。这是检查集群基本状态和连接性的基础工具。

### 输出示例
```bash
# 显示集群信息
$ kubectl cluster-info
Kubernetes control plane is running at https://192.168.49.2:8443
KubeDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

# 显示集群组件状态
$ kubectl cluster-info dump
{
  "kind": "List",
  "apiVersion": "v1",
  "metadata": {},
  "items": [
    {
      "kind": "Node",
      "apiVersion": "v1",
      "metadata": {
        "name": "minikube",
        ...
      },
      ...
    }
  ]
}

# 查看特定命名空间的集群信息
$ kubectl cluster-info --output-watch-events=false
Kubernetes control plane is running at https://control-plane.minikube.internal:8443
KubeDNS is running at https://control-plane.minikube.internal:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

# 以JSON格式输出
$ kubectl cluster-info -o json
{
  "kind": "ClusterInfo",
  "apiVersion": "v1",
  "kubernetes": "https://192.168.49.2:8443",
  "kube-dns": "https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy"
}
```

### 内容解析
- **Kubernetes control plane**: API Server的访问地址
- **KubeDNS/CoreDNS**: 集群DNS服务的访问地址
- **Additional services**: 如Ingress Controller、Metrics Server等服务地址
- 提供集群关键组件的访问端点信息

### 注意事项
- 需要有访问集群的权限
- 输出的URL可能因集群配置而异
- 用于验证集群连通性
- `cluster-info dump` 会输出详细的集群状态信息

### 生产安全风险
- 暴露集群内部服务地址
- 应限制对敏感集群信息的访问

## 104. kubectl argo

### 用途
`argo` 是Argo Workflows的kubectl插件，用于管理和操作Argo工作流。它提供了创建、监控和管理工作流的完整功能集。

### 输出示例
```bash
# 列出所有工作流
$ kubectl argo list -n argo
NAME                STATUS      AGE   DURATION   PRIORITY
my-workflow-abc12   Running     5m    10m        0
data-pipeline-xyz   Succeeded   15m   8m         0
ml-training-job     Failed      20m   12m        0

# 获取工作流详细信息
$ kubectl argo get my-workflow-abc12 -n argo
Name:                my-workflow-abc12
Namespace:           argo
ServiceAccount:      default
Status:              Running
Created:             2024-01-01 10:00:00 +0000 UTC
Started:             2024-01-01 10:00:05 +0000 UTC
Duration:            5m
Progress:            3/5

# 提交新的工作流
$ kubectl argo submit workflow.yaml --watch
Name:                my-new-workflow
Namespace:           argo
ServiceAccount:      default
Status:              Pending
Created:             2024-01-01 10:15:00 +0000 UTC

# 监控工作流执行
$ kubectl argo watch my-workflow-abc12 -n argo
STEP                        TEMPLATE      PODNAME                              DURATION  MESSAGE
 ✔ my-workflow-abc12        entrypoint                                          5m        
 ├─✔ prepare-data           prepare       my-workflow-abc12-prepare-123456789  2m        
 ├─✔ process-data           process       my-workflow-abc12-process-987654321  2m        
 └─● cleanup                cleanup                                            1m        (running)

# 终止工作流
$ kubectl argo terminate my-running-workflow -n argo
workflow.argoproj.io/my-running-workflow terminated
```

### 内容解析
- **list**: 列出命名空间中的所有工作流
- **get**: 获取特定工作流的详细状态和执行信息
- **submit**: 提交新的工作流定义文件
- **watch**: 实时监控工作流执行进度
- **terminate**: 终止正在运行的工作流
- 支持多种工作流状态：Running, Succeeded, Failed, Error等

### 注意事项
- 需要安装Argo Workflows控制器
- 工作流定义使用YAML格式
- 支持复杂的DAG和步骤依赖关系
- 提供丰富的日志和调试功能

### 生产安全风险
- 工作流可能执行敏感操作，需要严格的角色控制
- 工作流定义文件应进行安全审查
- 建议限制工作流的服务账户权限

## 105. kubectl krew

### 用途
`krew` 是kubectl的插件管理器，用于发现、安装、升级和管理kubectl插件。它是Kubernetes生态系统中最重要的工具之一。

### 输出示例
```bash
# 搜索可用插件
$ kubectl krew search
PLUGIN                    DESCRIPTION
affinity                  Generates pod affinity/anti-affinity YAML manifests
ctx                       Switch between kubeconfig contexts easily
df-pv                     Show disk usage for persistent volumes
doctor                    Diagnose common Kubernetes problems
get-all                   Like `kubectl get all` but _really_ everything
grep                      Filter Kubernetes resources by matching their names
ktop                      Top-like resource usage for Kubernetes
ns                        Switch between Kubernetes namespaces
outdated                  Find outdated container images in a cluster
rbac-lookup               Reverse lookup for RBAC
resource-capacity         Show node and pod resource consumption
rolesum                   Summarize RBAC roles for subjects
support-bundle            Collect cluster information for support
tree                      Show Kubernetes object hierarchies
view-secret               Decode Kubernetes secrets

# 安装插件
$ kubectl krew install tree
Updated the local copy of plugin index.
Installing plugin: tree
Installed plugin: tree
\
 | Use this plugin:
 |      kubectl tree
 | Documentation:
 |      https://krew.sigs.k8s.io/plugins/tree/
 | Caveats:
 | \
 |  | This plugin requires a minimum kubectl version of 1.12.
 | /
/

# 列出已安装插件
$ kubectl krew list
PLUGIN    VERSION
ctx       v0.12.0
krew      v0.4.3
ns        v0.11.0
tree      v0.4.1
view-secret v0.11.0

# 升级所有插件
$ kubectl krew upgrade
Upgraded plugin: ctx
Upgraded plugin: ns
Upgraded plugin: tree
Upgraded plugin: view-secret
WARNING: Some plugins failed to upgrade, check logs above.

# 升级特定插件
$ kubectl krew upgrade tree
Upgraded plugin: tree

# 卸载插件
$ kubectl krew uninstall tree
Uninstalled plugin: tree

# 查看插件信息
$ kubectl krew info view-secret
NAME: view-secret
URI: https://github.com/elsesiy/kubectl-view-secret
SHA256: 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
VERSION: v0.11.0
HOMEPAGE: https://github.com/elsesiy/kubectl-view-secret
DESCRIPTION: Decode Kubernetes secrets
CAVEATS:
\
 | This plugin requires a minimum kubectl version of 1.12.
 | 
 | Usage:
 |   kubectl view-secret <secret-name> [key]
/
```

### 内容解析
- **search**: 搜索可用的kubectl插件
- **install**: 安装指定的插件
- **list**: 显示已安装的插件及其版本
- **upgrade**: 升级插件到最新版本
- **uninstall**: 卸载不再需要的插件
- **info**: 查看插件的详细信息和使用说明

### 注意事项
- 插件会安装到`~/.krew/bin`目录
- 需要将该目录添加到PATH环境变量
- 插件版本可能与kubectl版本有兼容性要求
- 建议定期更新插件以获得最新功能和安全修复

### 生产安全风险
- 插件来源需要可信，建议使用官方索引
- 插件具有与kubectl相同的权限级别
- 应定期审查已安装插件的安全性
- 生产环境中应限制插件安装权限

## 106. kubectl kuttl

### 用途
`kuttl` (KUbernetes Test TooL) 是专门用于Kubernetes端到端测试的强大框架，支持声明式测试定义和自动化执行。

### 输出示例
```bash
# 运行测试套件
$ kubectl kuttl test ./test/e2e
=== RUN   kuttl
=== RUN   kuttl/test-deployment
--- PASS: kuttl/test-deployment (15.23s)
=== RUN   kuttl/test-service
--- PASS: kuttl/test-service (8.45s)
=== RUN   kuttl/test-ingress
--- FAIL: kuttl/test-ingress (12.10s)
    assert.go:45: Service "test-service" not found
=== RUN   kuttl/test-configmap
--- PASS: kuttl/test-configmap (3.21s)

KUTTL TESTS COMPLETE: 3 passed, 1 failed

# 运行特定测试
$ kubectl kuttl test --test my-specific-test ./test/integration
=== RUN   kuttl
=== RUN   kuttl/my-specific-test
--- PASS: kuttl/my-specific-test (22.15s)

KUTTL TESTS COMPLETE: 1 passed, 0 failed

# 并行运行测试
$ kubectl kuttl test --parallel 4 ./test/parallel
=== RUN   kuttl
=== RUN   kuttl/test-1
=== RUN   kuttl/test-2
=== RUN   kuttl/test-3
=== RUN   kuttl/test-4
--- PASS: kuttl/test-1 (5.12s)
--- PASS: kuttl/test-2 (4.87s)
--- PASS: kuttl/test-3 (6.23s)
--- PASS: kuttl/test-4 (5.41s)

KUTTL TESTS COMPLETE: 4 passed, 0 failed

# 详细输出模式
$ kubectl kuttl test --v 3 ./test/debug
=== RUN   kuttl
=== RUN   kuttl/debug-test
    kuttl.go:123: Creating namespace: kuttl-test-debug-abc123
    kuttl.go:145: Applying manifest: test-deployment.yaml
    kuttl.go:167: Waiting for deployment to be ready...
    kuttl.go:189: Deployment is ready
    kuttl.go:201: Running assertion checks...
--- PASS: kuttl/debug-test (18.76s)

KUTTL TESTS COMPLETE: 1 passed, 0 failed

# 生成测试报告
$ kubectl kuttl test --report xml ./test/full-suite
=== RUN   kuttl
[... test execution ...]
KUTTL TESTS COMPLETE: 15 passed, 2 failed

$ ls -la kuttl-test.xml
-rw-r--r--  1 user  staff  12345  Jan 1 10:30 kuttl-test.xml
```

### 内容解析
- **test**: 执行测试套件或特定测试
- 支持声明式的测试定义(YAML格式)
- 提供丰富的断言和验证机制
- 支持测试并行执行以提高效率
- 生成详细的测试报告和日志
- 支持测试前后的清理操作

### 注意事项
- 测试文件使用YAML格式定义
- 需要配置测试环境和前置条件
- 建议在独立的测试命名空间中运行
- 支持测试超时和重试机制
- 可以集成到CI/CD流水线中

### 生产安全风险
- 测试可能影响集群状态，应在测试环境中运行
- 测试资源需要适当的清理机制
- 敏感数据不应出现在测试配置中
- 建议使用临时的测试集群

## 存储管理高级主题

### 存储类(StorageClass)管理

存储类是Kubernetes中动态供应持久化存储的关键抽象，允许管理员描述他们提供的存储"类"。

#### 存储类创建和管理
```bash
# 创建高性能SSD存储类
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  fsType: ext4
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
EOF

# 查看存储类详细信息
kubectl describe storageclass fast-ssd

# 列出所有存储类并显示参数
kubectl get storageclass -o custom-columns='NAME:.metadata.name,PROVISIONER:.provisioner,PARAMETERS:.parameters'

# 设置默认存储类
kubectl patch storageclass fast-ssd -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

# 查看默认存储类
kubectl get storageclass -o=jsonpath='{range .items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=="true")]}{.metadata.name}{"\n"}{end}'
```

#### 存储容量管理
```bash
# 查看存储容量使用情况
kubectl get pv -o custom-columns='NAME:.metadata.name,CAPACITY:.spec.capacity.storage,STATUS:.status.phase,CLAIM:.spec.claimRef.name,CLASS:.spec.storageClassName'

# 查看PVC使用情况
kubectl get pvc --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volumeName,CAPACITY:.status.capacity.storage,ACCESSMODES:.status.accessModes'

# 监控存储使用率
kubectl get pvc --all-namespaces -o json | jq -r '.items[] | {namespace: .metadata.namespace, name: .metadata.name, capacity: .status.capacity.storage, used: .status.phase} | select(.used == "Bound")'
```

### 网络策略管理高级主题

网络策略是Kubernetes中实现微分段和网络安全的重要工具，控制Pod之间的网络流量。

#### 网络策略创建和管理
```bash
# 创建限制性的默认拒绝策略
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

# 创建允许同命名空间通信的策略
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-same-namespace
  namespace: production
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector: {}
  policyTypes:
  - Ingress
EOF

# 创建允许特定端口的策略
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-web-traffic
  namespace: production
spec:
  podSelector:
    matchLabels:
      role: web
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: frontend
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
  policyTypes:
  - Ingress
EOF

# 检查网络策略实施效果
kubectl get networkpolicy --all-namespaces

# 验证网络策略
kubectl run test-pod --image=nicolaka/netshoot --rm -it --generator=run-pod/v1 -- sh
# 在测试Pod中测试网络连通性
```

### 安全管理高级主题

#### Pod安全策略和准入控制器
```bash
# 检查Pod安全标准(Pod Security Standards)配置
kubectl get namespace --show-labels

# 为命名空间设置安全级别
kubectl label namespace production pod-security.kubernetes.io/enforce=restricted
kubectl label namespace production pod-security.kubernetes.io/audit=restricted
kubectl label namespace production pod-security.kubernetes.io/warn=restricted

# 检查特权容器
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{" "}{range .spec.containers[*]}{.securityContext.privileged}{" "}{end}{"\n"}{end}' | grep true

# 检查运行特权用户容器
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{" "}{range .spec.containers[*]}{.securityContext.runAsNonRoot}{" "}{end}{"\n"}{end}' | grep false

# 检查允许权限提升的容器
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{" "}{range .spec.containers[*]}{.securityContext.allowPrivilegeEscalation}{" "}{end}{"\n"}{end}' | grep true
```

#### 安全扫描和合规检查
```bash
# 使用Polaris进行集群安全检查
kubectl polaris audit --audit-path .

# 检查资源限制配置
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{"\n"}{range .spec.containers[*]}{"  "}{.name}{": "}{.resources}{", "}{end}{"\n"}{end}'

# 检查未加密的Secret
kubectl get secrets --all-namespaces --field-selector type!=kubernetes.io/service-account-token -o json | jq -r '.items[] | select(.data.TLS_PRIVATE_KEY == null) | .metadata.namespace + " " + .metadata.name'

# 审计RBAC权限
kubectl get roles,rolebindings,clusterroles,clusterrolebindings --all-namespaces -o wide
```

## 安全管理与合规高级主题

### 安全上下文(Security Context)管理

安全上下文定义了Pod或容器的安全属性，是实现最小权限原则的关键配置。

#### Pod级别安全上下文
```bash
# 创建带有安全上下文的Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app-container
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
EOF

# 检查Pod的安全配置
kubectl get pod secure-pod -o jsonpath='{.spec.securityContext}'

# 检查容器级别的安全上下文
kubectl get pod secure-pod -o jsonpath='{.spec.containers[0].securityContext}'
```

#### 安全能力管理
```bash
# 检查所有Pod的安全能力配置
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{"\n"}{range .spec.containers[*]}{"  "}{.name}{" Capabilities: "}{.securityContext.capabilities}{"\n"}{end}{"\n"}{end}'

# 查找使用特权模式的Pod
kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(any(.spec.containers[]; .securityContext.privileged == true)) | .metadata.namespace + " " + .metadata.name + " " + (.spec.containers[] | select(.securityContext.privileged == true) | .name)'

# 检查允许权限提升的容器
kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(any(.spec.containers[]; .securityContext.allowPrivilegeEscalation == true)) | .metadata.namespace + " " + .metadata.name'
```

### 网络安全策略高级配置

#### 多层次网络策略设计
```bash
# 默认拒绝所有流量的策略（全局）
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

# 允许集群内部通信的策略
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-cluster-internal
  namespace: default
spec:
  podSelector: {}
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          purpose: cluster-internal
  policyTypes:
  - Ingress
EOF

# 允许特定服务访问的策略
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-access
  namespace: default
spec:
  podSelector: {}
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
  policyTypes:
  - Egress
EOF
```

### 安全扫描和持续监控

#### 使用Trivy进行镜像扫描
```bash
# 扫描命名空间中所有Pod使用的镜像
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u

# 使用Trivy扫描特定镜像
trivy image nginx:latest

# 创建安全扫描Job
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: Job
metadata:
  name: security-scan
  namespace: security-tools
spec:
  template:
    spec:
      containers:
      - name: trivy
        image: aquasec/trivy:latest
        command:
        - /bin/sh
        - -c
        - |
          kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u > /tmp/images.txt
          while read image; do
            echo "Scanning $image"
            trivy image --format table $image
          done < /tmp/images.txt
        env:
        - name: KUBECONFIG
          value: /root/.kube/config
        volumeMounts:
        - name: kubeconfig
          mountPath: /root/.kube
      volumes:
      - name: kubeconfig
        secret:
          secretName: kubeconfig
      restartPolicy: Never
EOF
```

#### 安全事件监控
```bash
# 监控安全相关事件
kubectl get events --all-namespaces --field-selector type=Warning --sort-by='.lastTimestamp' | grep -i security

# 查看Pod安全违规事件
kubectl get events --all-namespaces --field-selector reason=FailedPostStartHook,reason=BackOff,reason=Failed --sort-by='.lastTimestamp'

# 监控RBAC权限拒绝事件
kubectl get events --all-namespaces --field-selector reason=Forbidden --sort-by='.lastTimestamp'
```

### 安全基线和合规检查

#### 使用Kyverno进行策略管理
```bash
# 创建安全策略验证Pod不使用特权模式
kubectl apply -f - <<EOF
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-privileged-containers
spec:
  validationFailureAction: enforce
  rules:
  - name: privileged-containers
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Privileged containers are not allowed."
      pattern:
        spec:
          =(containers):
          - =(securityContext):
              =(privileged): "false"
EOF

# 检查策略执行情况
kubectl get polr --all-namespaces
```

## Linux系统运维基础命令在K8s环境中的应用

### 系统信息和状态监控
```bash
# 检查节点系统信息
kubectl get nodes -o json | jq -r '.items[] | {name: .metadata.name, kernel: .status.nodeInfo.kernelVersion, os: .status.nodeInfo.osImage, arch: .status.nodeInfo.architecture, containerRuntime: .status.nodeInfo.containerRuntimeVersion}'

# 检查节点资源使用情况
kubectl top nodes --use-protocol-buffers

# 查看节点系统日志
kubectl get pods -n kube-system -l k8s-app=kubelet
```

### 网络基础命令
```bash
# 使用netshoot工具进行网络诊断
kubectl run netshoot --image=nicolaka/netshoot --rm -it --generator=run-pod/v1 -- sh

# 在Pod中执行网络诊断命令
kubectl exec -it <pod-name> -- bash
# 在Pod内执行网络命令
nslookup kubernetes.default.svc.cluster.local
ping google.com
netstat -tuln
ss -tuln
ip route show
```

### 安全基础命令
```bash
# 检查Pod安全上下文
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{" "}{.metadata.name}{"\n"}{range .spec.containers[*]}{"  Container: "}{.name}{"\n"}{"    RunAsNonRoot: "}{.securityContext.runAsNonRoot}{"\n"}{"    Privileged: "}{.securityContext.privileged}{"\n"}{end}{"\n"}{end}'

# 检查文件权限
kubectl exec <pod-name> -- ls -la /app
kubectl exec <pod-name> -- stat /app/config.properties
```

## 107. Helm相关命令

虽然Helm不是kubectl的内置命令，但在Kubernetes生态系统中广泛使用，经常与kubectl配合使用。

### 用途
Helm是Kubernetes的包管理器，用于简化应用程序的部署和管理。它提供了Chart（预配置的Kubernetes资源包）的概念，使得复杂应用的部署变得简单。

### 常用命令

#### Helm仓库管理
```bash
# 添加仓库
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami

# 列出仓库
helm repo list

# 更新仓库
helm repo update

# 搜索Chart
helm search repo nginx
helm search hub wordpress
```

#### Release管理
```bash
# 列出所有Release
helm list -A

# 查看Release状态
helm status my-release -n production

# 获取Release值配置
helm get values my-release -n production

# 获取Release清单
helm get manifest my-release -n production
```

#### Chart部署和管理
```bash
# 安装Chart
helm install my-release bitnami/nginx --namespace production

# 升级Release
helm upgrade my-release bitnami/nginx --set replicaCount=3

# 回滚Release
helm rollback my-release 1

# 卸载Release
helm uninstall my-release -n production
```

#### Chart开发和调试
```bash
# 模板渲染测试
helm template my-chart ./my-chart --debug

# 语法检查
helm lint ./my-chart

# 依赖管理
helm dependency update ./my-chart

# 打包Chart
helm package ./my-chart
```

### 实际应用场景
1. **应用打包**：将复杂的应用程序打包成可重用的Chart
2. **配置管理**：通过values文件管理不同环境的配置
3. **版本控制**：支持Chart和Release的版本管理
4. **批量部署**：一次性部署包含多个组件的复杂应用
5. **依赖管理**：自动处理Chart之间的依赖关系

### 注意事项
- Helm v3不再需要Tiller组件，更加安全
- 建议使用明确的命名空间进行部署
- 重要的Release应该启用历史记录保存
- 定期清理旧的Release版本以节省存储空间

## 108. Istio服务网格命令

Istio是流行的服务网格实现，提供了流量管理、安全、可观测性等功能。

### 用途
Istio为微服务提供了统一的服务治理能力，包括流量路由、安全策略、监控指标等。

### 常用命令

#### 网格状态检查
```bash
# 检查Istio安装状态
istioctl version
istioctl ps
istioctl proxy-status

# 分析配置问题
istioctl analyze -A
```

#### 流量管理
```bash
# 查看虚拟服务
kubectl get virtualservices -A

# 查看目标规则
kubectl get destinationrules -A

# 查看网关
kubectl get gateways -A
```

#### 代理配置检查
```bash
# 查看代理路由配置
istioctl proxy-config routes <pod-name>.<namespace>

# 查看监听器配置
istioctl proxy-config listeners <pod-name>.<namespace>

# 查看集群配置
istioctl proxy-config clusters <pod-name>.<namespace>
```

#### 安全配置
```bash
# 查看认证策略
kubectl get peerauthentications -A
kubectl get requestauthentications -A

# 权限检查
istioctl authz check <pod-name>.<namespace>
```

#### 监控和调试
```bash
# 启动各种仪表板
istioctl dashboard prometheus
istioctl dashboard grafana
istioctl dashboard kiali

# 流量监控
istioctl experimental metrics <service-name>.<namespace>
```

### 实际应用场景
1. **金丝雀发布**：通过流量权重控制逐步发布新版本
2. **故障注入**：测试服务的容错能力
3. **安全策略**：实施mTLS和服务间认证
4. **可观测性**：获取详细的流量指标和追踪信息
5. **流量治理**：实现复杂的路由规则和重试策略

### 注意事项
- 需要在Pod中注入istio-proxy sidecar
- 某些网络配置可能需要特殊处理
- 监控会产生额外的资源开销
- 安全配置需要仔细规划和测试

## 109. Linkerd服务网格命令

Linkerd是轻量级的服务网格，专注于性能和易用性。

### 用途
Linkerd提供服务发现、负载均衡、流量加密、可观测性等服务网格核心功能。

### 常用命令

#### 安装和状态检查
```bash
# 检查Linkerd安装
linkerd check

# 查看控制平面状态
linkerd check --proxy

# 查看版本信息
linkerd version
```

#### 服务网格化应用
```bash
# 将应用注入到服务网格
kubectl get -n emojivoto deploy -o yaml \
  | linkerd inject - \
  | kubectl apply -f -

# 检查注入状态
linkerd stat deploy -n emojivoto
```

#### 流量监控
```bash
# 查看服务统计
linkerd viz stat deploy

# 实时流量监控
linkerd viz tap deploy/<deployment-name>

# Top线路视图
linkerd viz top deploy
```

#### 可视化界面
```bash
# 启动仪表板
linkerd viz dashboard

# 查看服务图
linkerd viz edges deploy
```

### 实际应用场景
1. **零配置网格化**：简单的命令即可将应用加入服务网格
2. **性能监控**：获取详细的延迟、成功率等指标
3. **故障诊断**：通过tap命令实时查看请求流量
4. **安全通信**：自动启用mTLS加密服务间通信
5. **渐进式采用**：可以选择性地将部分服务网格化

### 注意事项
- 注入sidecar会增加Pod的资源消耗
- 需要足够的RBAC权限进行注入操作
- 某些应用可能需要特殊的注入配置
- 建议在非生产环境先进行测试

## 110. Flux CD GitOps工具命令

Flux是流行的GitOps工具，实现了基于Git的持续交付。

### 用途
Flux通过监控Git仓库的变化来自动化Kubernetes资源的部署和更新，实现Infrastructure as Code。

### 常用命令

#### 基础操作
```bash
# 检查Flux状态
flux check

# 查看所有Flux资源
flux get all -A

# 查看Git仓库源
flux get sources git -A

# 查看Kustomization
flux get kustomizations -A

# 查看Helm Release
flux get helmreleases -A
```

#### 资源管理
```bash
# 创建Git仓库源
flux create source git my-app \
  --url=https://github.com/example/my-app \
  --branch=main

# 创建Kustomization
flux create kustomization my-app \
  --source=my-app \
  --path="./kustomize" \
  --prune=true \
  --interval=5m

# 手动同步
flux reconcile kustomization my-app
```

#### 故障排查
```bash
# 查看资源详情
flux describe kustomization my-app

# 查看资源事件
flux events --for Kustomization/my-app

# 暂停同步
flux suspend kustomization my-app

# 恢复同步
flux resume kustomization my-app
```

### 实际应用场景
1. **GitOps流水线**：实现完全基于Git的部署流程
2. **多环境管理**：通过不同分支管理不同环境
3. **自动同步**：Git仓库变化自动触发部署
4. **回滚机制**：通过Git历史轻松回滚到任意版本
5. **审计跟踪**：所有变更都有Git提交记录

### 注意事项
- 需要配置正确的Git仓库访问权限
- 建议使用SSH密钥而非用户名密码
- 敏感信息应使用Sealed Secrets等方式加密
- 定期清理旧的历史记录
- 监控Flux控制器的运行状态

## 总结

本文档全面覆盖了Kubernetes CLI的核心命令和高级运维技能，从基础的资源管理到复杂的集群运维，为Kubernetes管理员和开发者提供了完整的学习和参考指南。

### 文档特点

1. **完整性**：包含110个kubectl及相关生态工具的详细说明，涵盖所有核心功能
2. **实用性**：每个命令都配有实际使用场景、输出示例和注意事项
3. **专业性**：深入解析命令参数、工作机制和最佳实践
4. **安全性**：重点标注安全风险和生产环境注意事项
5. **现代性**：包含AI/ML平台、服务网格、GitOps等前沿技术内容

### 核心技能覆盖

- **基础操作**：Pod、Service、Deployment等核心资源管理
- **集群管理**：节点维护、集群健康检查、版本升级
- **网络管理**：网络策略、服务发现、Ingress配置
- **存储管理**：持久卷、存储类、CSI插件管理
- **安全管理**：RBAC、网络策略、安全扫描
- **监控诊断**：资源监控、日志分析、故障排查
- **高级运维**：蓝绿部署、金丝雀发布、容灾演练
- **生态集成**：Helm、Istio、Linkerd、Flux等工具集成

### 学习路径建议

1. **入门阶段**：掌握基础命令（1-20号）和日常操作
2. **进阶阶段**：学习网络、存储、安全管理（21-60号）
3. **专家阶段**：精通高级运维和生态工具（61-110号）
4. **实践应用**：结合实际场景综合运用各项技能

### 生产环境最佳实践

- 始终使用命名空间隔离不同环境
- 充分利用标签和注解进行资源管理
- 定期进行安全扫描和合规检查
- 建立完善的监控告警体系
- 实施备份和灾难恢复策略
- 保持工具和集群版本更新

### 持续学习建议

Kubernetes生态系统快速发展，建议：
- 关注官方文档和版本更新
- 参与社区讨论和技术分享
- 定期实践新特性和最佳实践
- 结合实际项目积累经验

通过系统学习和实践本文档内容，您将具备专业的Kubernetes运维能力，能够在生产环境中高效、安全地管理和维护Kubernetes集群。