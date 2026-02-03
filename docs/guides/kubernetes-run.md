# Kubernetes 案例运行说明

## 环境要求

- Kubernetes 集群（v1.20+）
- kubectl 命令行工具（版本与集群匹配）
- 适当的集群权限（根据案例需求）

## 运行步骤

1. **选择要运行的案例**
   - 浏览 `opendemo_output/kubernetes/` 目录，选择感兴趣的案例
   - 每个案例都有独立的目录，包含完整的配置文件和 README.md

2. **查看案例说明**
   ```bash
   cd opendemo_output/kubernetes/<案例目录>
   cat README.md
   ```

3. **应用配置文件**
   - 对于大多数案例，可以使用 `kubectl apply` 命令应用配置
   ```bash
   kubectl apply -f <配置文件>
   ```
   - 或者根据 README.md 中的特定说明执行

4. **验证部署**
   ```bash
   # 查看 Pod 状态
   kubectl get pods
   
   # 查看服务状态
   kubectl get services
   
   # 查看部署状态
   kubectl get deployments
   ```

5. **访问应用**（如果适用）
   - 对于有外部访问的应用，可以通过 Service 的 EXTERNAL-IP 访问
   ```bash
   kubectl get service <service-name>
   ```
   - 或者使用端口转发
   ```bash
   kubectl port-forward <pod-name> <本地端口>:<容器端口>
   ```

6. **清理资源**
   ```bash
   kubectl delete -f <配置文件>
   # 或删除整个命名空间（如果案例使用了独立命名空间）
   kubectl delete namespace <namespace-name>
   ```

## 常见问题

1. **权限不足**
   - 确保你有足够的集群权限来创建和管理资源
   - 对于需要集群级权限的操作（如 RBAC、CRD），可能需要 cluster-admin 角色

2. **资源不足**
   - 确保集群有足够的资源（CPU、内存、存储）来运行案例
   - 对于大型案例（如 EFK、ELK），可能需要多个节点

3. **版本兼容性**
   - 大多数案例兼容 Kubernetes v1.20+，但某些高级特性可能需要更高版本
   - 查看案例 README.md 中的版本兼容性说明

4. **网络问题**
   - 确保集群网络插件正常工作
   - 对于网络相关案例，确保网络策略、CNI 插件等配置正确

## 示例：运行 Prometheus 案例

```bash
# 进入案例目录
cd opendemo_output/kubernetes/prometheus/basic-prometheus/

# 查看说明
cat README.md

# 应用配置
kubectl apply -f prometheus.yaml

# 验证部署
kubectl get pods -n monitoring
kubectl get services -n monitoring

# 访问 Prometheus UI
kubectl port-forward service/prometheus 9090:9090 -n monitoring
# 然后在浏览器中访问 http://localhost:9090

# 清理资源
kubectl delete -f prometheus.yaml
```

## 示例：运行 Operator 案例

```bash
# 进入案例目录
cd opendemo_output/kubernetes/operator/basic-operator/

# 查看说明
cat README.md

# 应用 CRD
kubectl apply -f crd.yaml

# 应用 RBAC 配置
kubectl apply -f rbac.yaml

# 应用 Operator 部署
kubectl apply -f operator.yaml

# 验证部署
kubectl get pods
kubectl get crds

# 清理资源
kubectl delete -f operator.yaml
kubectl delete -f rbac.yaml
kubectl delete -f crd.yaml
```

## 注意事项

- 建议在测试集群中运行案例，避免影响生产环境
- 某些案例（如故障排查、灾难恢复）可能会影响集群状态
- 始终先查看案例的 README.md，了解详细的运行说明和注意事项
- 对于复杂案例，可能需要按照特定顺序应用配置文件

所有 Kubernetes 案例都经过测试，可以在符合要求的环境中正常运行。如果遇到问题，请参考案例的故障排查部分或查看 Kubernetes 集群日志。