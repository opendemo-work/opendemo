# Loki日志事件接收器配置演示

## 简介
本演示展示了如何在Kubernetes集群中部署并配置Grafana Loki作为日志聚合系统，使应用能够将日志发送至Loki进行集中存储与查询。通过本示例，您将学习到Loki的基本架构、日志路径配置以及Promtail的部署方法。

## 学习目标
- 理解Loki在Kubernetes中的角色与优势
- 掌握使用Helm部署Loki和Promtail的方法
- 配置Pod日志自动收集并发送至Loki
- 查询和验证日志是否成功摄入

## 环境要求
- `kubectl` >= 1.20
- `helm` >= 3.0.0
- Kubernetes 集群（Minikube、Kind、EKS、AKS等均可）
- 可选：`minikube` >= 1.0.0（用于本地测试）

## 安装依赖的详细步骤

### 1. 安装kubectl
```bash
# Linux/macOS
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Windows: 下载 https://dl.k8s.io/release/v1.29.0/bin/windows/amd64/kubectl.exe
```

### 2. 安装Helm
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### 3. 启动Kubernetes集群（以Minikube为例）
```bash
minikube start --memory=4096 --cpus=2
```

## 文件说明
- `loki-values.yaml`: Helm自定义配置文件，用于定制Loki部署参数
- `promtail-config.yaml`: Promtail的配置文件，定义日志采集规则

## 逐步实操指南

### 步骤1：添加Grafana Helm仓库
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

**预期输出**：`"grafana" has been added to your repositories`

### 步骤2：部署Loki
```bash
helm install loki grafana/loki --version 5.30.1 -f loki-values.yaml
```

**预期输出**：显示Loki服务、StatefulSet等资源创建成功

### 步骤3：部署Promtail
```bash
helm install promtail grafana/promtail --version 6.16.2 -f promtail-config.yaml
```

**预期输出**：Promtail DaemonSet 和 ConfigMap 创建成功

### 步骤4：验证Pod状态
```bash
kubectl get pods -l app=loki
kubectl get pods -l app=promtail
```

**预期输出**：所有Pod处于 `Running` 状态

### 步骤5：查看日志摄入情况
```bash
kubectl logs -l app=promtail --tail=10
```

应看到类似 `level=info msg="Sending batch of entries" ...` 的日志，表示日志已发送至Loki

## 代码解析

### `loki-values.yaml`
- 设置 `ingester.replication_factor: 1` 适用于单节点环境
- 启用 `auth_enabled: false` 简化本地测试流程
- 使用 `inmemory` 作为索引存储，适合演示

### `promtail-config.yaml`
- `clients.url`: 指向Loki服务的内部ClusterIP地址
- `scrape_configs.job_name: kubernetes-pods`: 自动发现所有命名空间的Pod日志
- `pipeline_stages`: 提取Pod标签作为日志流标签（如job, namespace, pod）

## 预期输出示例
```bash
$ kubectl get svc loki
NAME   TYPE        CLUSTER-IP      PORT(S)
loki   ClusterIP   10.96.123.45    3100/TCP

$ kubectl logs promtail-abcde
... level=info msg="Starting Promtail" ...
... level=info msg="Sending batch" ...
```

## 常见问题解答

**Q: Promtail无法连接Loki？**
A: 检查服务名称是否为`loki`且在同一命名空间，或使用FQDN `loki.default.svc.cluster.local`

**Q: 日志未出现在Loki中？**
A: 查看Promtail日志是否有错误；确认容器日志路径为`/var/log/pods/*/*/*.log`

**Q: 如何查询Loki中的日志？**
A: 使用`logcli`工具或部署Grafana并添加Loki数据源进行可视化查询

## 扩展学习建议
- 将Loki与Grafana集成实现日志仪表板
- 使用持久化存储（如S3、GCS）替换内存存储
- 配置RBAC和多租户支持用于生产环境
- 实现日志保留策略和压缩设置
