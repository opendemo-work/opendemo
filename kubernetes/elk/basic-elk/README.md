# Kubernetes ELK 日志管理基础案例

## 什么是 ELK？

ELK 是 Elasticsearch、Logstash 和 Kibana 的组合，用于 Kubernetes 集群的日志管理解决方案：

- **Elasticsearch**: 分布式搜索引擎，用于存储和索引日志数据
- **Logstash**: 日志处理管道，用于收集、转换和发送日志数据
- **Kibana**: 数据可视化平台，用于查询和分析 Elasticsearch 中的日志

## 本案例包含的内容

- **elasticsearch.yaml**: Elasticsearch 部署配置
- **logstash.yaml**: Logstash Deployment 配置
- **kibana.yaml**: Kibana 部署配置

## 快速开始

### 1. 部署 Elasticsearch

```bash
kubectl apply -f elasticsearch.yaml
```

### 2. 验证 Elasticsearch 部署

```bash
# 检查 Elasticsearch Pod 状态
kubectl get pods -n elk -l app=elasticsearch

# 等待 Elasticsearch 就绪
kubectl wait --for=condition=ready pod -l app=elasticsearch -n elk --timeout=300s
```

### 3. 部署 Logstash

```bash
kubectl apply -f logstash.yaml
```

### 4. 验证 Logstash 部署

```bash
# 检查 Logstash Pod 状态
kubectl get pods -n elk -l app=logstash
```

### 5. 部署 Kibana

```bash
kubectl apply -f kibana.yaml
```

### 6. 验证 Kibana 部署

```bash
# 检查 Kibana Pod 状态
kubectl get pods -n elk -l app=kibana

# 等待 Kibana 就绪
kubectl wait --for=condition=ready pod -l app=kibana -n elk --timeout=300s
```

### 7. 访问 Kibana UI

#### 7.1 使用 NodePort 访问

```bash
# 获取 Node IP（根据你的 Kubernetes 环境调整）
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 访问 Kibana UI
echo "http://$NODE_IP:30062"
```

#### 7.2 使用 Port Forward 访问

```bash
kubectl port-forward svc/kibana 5601:5601 -n elk
```

然后访问：http://localhost:5601

## 基本使用

### 1. 配置 Kibana 索引模式

首次登录 Kibana 后，需要配置索引模式：

1. 点击左侧菜单栏的 **Management** > **Stack Management** > **Data** > **Index Patterns**
2. 点击 **Create index pattern**
3. 输入索引模式名称：`logstash-*`
4. 选择时间字段：`@timestamp`
5. 点击 **Create index pattern**

### 2. 发送测试日志到 Logstash

你可以使用以下方法向 Logstash 发送测试日志：

#### 2.1 使用 HTTP 发送日志

```bash
# 端口转发 Logstash HTTP 端口
kubectl port-forward svc/logstash 5043:5043 -n elk

# 发送测试日志
curl -X POST -H "Content-Type: application/json" -d '{"message": "This is a test log from curl", "type": "test"}' http://localhost:5043
```

#### 2.2 使用 TCP 发送日志

```bash
# 端口转发 Logstash TCP 端口
kubectl port-forward svc/logstash 5000:5000 -n elk

# 发送测试日志
echo "This is a test log via TCP" | nc localhost 5000
```

### 3. 查看日志

1. 点击左侧菜单栏的 **Analytics** > **Discover**
2. 选择刚刚创建的索引模式 `logstash-*`
3. 你可以看到发送到 Logstash 的日志数据
4. 使用搜索栏和过滤器可以查询特定的日志

### 4. 创建可视化和仪表盘

参考 EFK 案例中的相关步骤，创建自定义可视化和仪表盘。

## 日志查询示例

### 1. 查询测试日志

```
type: "test"
```

### 2. 查询包含特定关键词的日志

```
message: "test"
```

### 3. 查询特定时间段的日志

使用 Kibana 界面上的时间选择器，或者在查询中指定时间范围：

```
@timestamp > "2024-01-20T00:00:00.000Z" AND @timestamp < "2024-01-21T00:00:00.000Z"
```

## 清理资源

```bash
kubectl delete -f kibana.yaml
kubectl delete -f logstash.yaml
kubectl delete -f elasticsearch.yaml
```

## ELK vs EFK

| 特性 | ELK | EFK |
|------|-----|-----|
| 日志收集 | Logstash | Fluentd |
| 性能 | 较重，资源消耗大 | 轻量，资源消耗小 |
| 配置复杂度 | 较高 | 较低 |
| 插件生态 | 丰富 | 丰富 |
| Kubernetes 集成 | 良好 | 优秀 |

## 扩展建议

1. **添加 Filebeat**: 部署 Filebeat 作为日志收集器，发送日志到 Logstash
2. **添加持久化存储**: 为 Elasticsearch 添加持久化存储
3. **配置高可用性**: 扩展 Elasticsearch 和 Logstash 到多个节点
4. **添加安全配置**: 为 ELK 堆栈配置 TLS 和认证
5. **配置日志保留策略**: 为 Elasticsearch 配置索引生命周期管理

## 相关链接

- [ELK 官方文档](https://www.elastic.co/guide/en/elastic-stack-overview/current/index.html)
- [Logstash 官方文档](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana 官方文档](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Filebeat 官方文档](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
- [Kubernetes 日志管理最佳实践](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
