# Katib超参数调优基础

## 概述

本Demo演示如何使用Kubeflow Katib进行自动化超参数搜索和调优。Katib是Kubeflow的AutoML组件，支持多种搜索算法和并行试验执行。

**所属组件**: Kubeflow Katib  
**难度级别**: beginner  
**核心功能**: 超参数搜索、试验管理、结果分析

## 前置条件

### 环境要求
- Kubernetes集群：v1.26+
- Kubeflow平台：v1.8+
- Katib组件：v0.16+
- kubectl：已配置

### 资源要求
- CPU: 至少2核
- 内存: 至少4GB
- 并行试验数×资源需求

## 资源清单说明

### manifests/experiment.yaml
Katib Experiment CRD定义，包含：
- 实验配置
- 搜索空间定义
- 优化目标
- 搜索算法配置
- 试验模板

## 部署步骤

### 1. 创建命名空间

```bash
kubectl create namespace kubeflow
```

### 2. 应用Experiment配置

```bash
kubectl apply -f manifests/experiment.yaml
```

### 3. 查看实验状态

```bash
kubectl get experiment -n kubeflow
```

**预期输出**：
```
NAME                    TYPE     STATUS    AGE
random-search-example   Created  Running   30s
```

### 4. 监控试验执行

查看正在运行的试验：

```bash
kubectl get trials -n kubeflow
```

## 验证和测试

### 1. 检查Experiment状态

查看实验详情：

```bash
kubectl describe experiment random-search-example -n kubeflow
```

关键信息：
- Trials Running: 当前运行的试验数
- Trials Succeeded: 成功的试验数
- Current Optimal Trial: 当前最优试验
- Best Metrics: 最佳指标值

### 2. 查看试验结果

列出所有试验：

```bash
kubectl get trials -n kubeflow -l experiment=random-search-example
```

查看特定试验详情：

```bash
kubectl describe trial <trial-name> -n kubeflow
```

### 3. 获取最优超参数

```bash
kubectl get experiment random-search-example -n kubeflow -o yaml | grep -A 10 "currentOptimalTrial"
```

### 4. 通过Dashboard查看

1. 登录Kubeflow Dashboard
2. 进入Katib页面
3. 查看实验列表
4. 点击实验查看详细结果图表

## 超参数搜索空间

本Demo示例的搜索空间：

```yaml
parameters:
- name: learning_rate
  parameterType: double
  feasibleSpace:
    min: "0.001"
    max: "0.1"
- name: num_layers
  parameterType: int
  feasibleSpace:
    min: "2"
    max: "5"
- name: optimizer
  parameterType: categorical
  feasibleSpace:
    list:
    - sgd
    - adam
    - rmsprop
```

## 搜索算法

### Random Search（随机搜索）
- 优点: 简单易用，适合初步探索
- 缺点: 效率较低
- 适用场景: 参数空间较小，初步调优

### Grid Search（网格搜索）
- 优点: 全面覆盖参数空间
- 缺点: 计算成本高
- 适用场景: 参数空间小且离散

### Bayesian Optimization（贝叶斯优化）
- 优点: 智能采样，效率高
- 缺点: 计算开销较大
- 适用场景: 参数空间连续，需要高效搜索

## 监控和日志

### 查看实验进度

```bash
# 实时监控实验状态
watch kubectl get experiment random-search-example -n kubeflow

# 查看试验列表
kubectl get trials -n kubeflow -l experiment=random-search-example --sort-by=.status.startTime
```

### 查看试验日志

```bash
# 获取试验对应的Pod
kubectl get pods -n kubeflow -l trial=<trial-name>

# 查看训练日志
kubectl logs -n kubeflow <pod-name> -c training-container
```

### 指标监控

Katib会自动收集并记录：
- 训练损失
- 验证准确率
- 训练时长
- 资源使用情况

## 故障排查

### 问题1：实验无法启动

**症状**：Experiment状态为Failed或Pending

**排查步骤**：
1. 检查YAML配置语法
2. 验证资源配额
3. 查看Katib controller日志

```bash
kubectl logs -n kubeflow -l app=katib-controller
```

### 问题2：试验执行失败

**症状**：Trial状态为Failed

**排查步骤**：
1. 查看试验详情
2. 检查训练容器日志
3. 验证训练脚本正确性
4. 检查资源限制

```bash
kubectl describe trial <trial-name> -n kubeflow
```

### 问题3：指标未正确收集

**症状**：无法获取最优结果

**排查步骤**：
1. 确认训练脚本正确输出指标
2. 检查指标收集器配置
3. 验证指标名称匹配

## 清理步骤

### 删除实验

```bash
kubectl delete experiment random-search-example -n kubeflow
```

这会自动删除所有关联的试验。

### 手动删除试验

如果需要单独删除某个试验：

```bash
kubectl delete trial <trial-name> -n kubeflow
```

## 扩展参考

### 官方文档
- [Katib官方文档](https://www.kubeflow.org/docs/components/katib/)
- [超参数调优指南](https://www.kubeflow.org/docs/components/katib/user-guides/)

### 进阶配置
- Early Stopping策略
- 自定义搜索算法
- 神经架构搜索(NAS)
- 多目标优化
- 分布式训练集成

### 关联Demo
- [Katib随机搜索算法]
- [Katib贝叶斯优化]
- [Katib Early Stopping策略]
- [Trainer PyTorchJob训练]

## 最佳实践

1. **搜索空间设计**
   - 先用粗粒度搜索探索
   - 再用细粒度搜索优化
   - 合理设置参数范围

2. **资源管理**
   - 设置并行试验数限制
   - 配置合适的资源请求和限制
   - 使用节点选择器优化调度

3. **指标选择**
   - 选择合适的优化目标
   - 考虑多个评估指标
   - 注意过拟合风险

4. **实验管理**
   - 使用有意义的实验名称
   - 记录实验参数和结果
   - 定期清理历史实验

## 版本说明

本Demo基于：
- Kubeflow: v1.8+
- Katib: v0.16+
- Kubernetes: v1.26+
