# Kubernetes Troubleshooting

Kubernetes故障排查实战演示，涵盖常见问题诊断与解决方案。

## 排查方法论

```
分层排查法:
┌─────────────┐
│  应用层      │  Pod状态、日志、Events
├─────────────┤
│  控制层      │  Controller、Scheduler
├─────────────┤
│  网络层      │  Service、DNS、CNI
├─────────────┤
│  存储层      │  PV、PVC、CSI
├─────────────┤
│  节点层      │  Node状态、资源、Kubelet
├─────────────┤
│  基础设施    │  etcd、API Server
└─────────────┘
```

## Pod故障排查

### Pod状态诊断
```bash
# 查看Pod状态
kubectl get pod <pod-name> -o yaml | grep -A 10 status

# 查看Events
kubectl get events --field-selector involvedObject.name=<pod-name>

# 常见状态及解决
Pending:    # 资源不足、调度失败
  kubectl describe node  # 查看节点资源
  
CrashLoopBackOff:  # 应用崩溃
  kubectl logs --previous <pod-name>
  
ImagePullBackOff:  # 镜像拉取失败
  kubectl describe pod <pod-name> | grep -i error
  
OOMKilled:  # 内存溢出
  kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].lastState}'
```

### 网络排查
```bash
# 测试DNS解析
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default

# 测试Service连通性
kubectl get endpoints <service-name>

# 进入Pod网络命名空间
kubectl debug -it <pod-name> --image=nicolaka/netshoot --target=<container>
```

## 节点故障排查

```bash
# 查看节点状态
kubectl get nodes -o wide

# 查看节点详情
kubectl describe node <node-name>

# 检查Kubelet
ssh <node-ip>
systemctl status kubelet
journalctl -u kubelet -f

# 检查容器运行时
crictl ps
crictl logs <container-id>
```

## 控制平面故障

```bash
# 检查API Server
kubectl get --raw /healthz

# 检查etcd
kubectl exec -it etcd-<node> -n kube-system -- etcdctl endpoint health

# 检查Controller Manager
kubectl get pods -n kube-system -l component=kube-controller-manager

# 检查Scheduler
kubectl get pods -n kube-system -l component=kube-scheduler
```

## 常用诊断工具

```bash
# k9s - 交互式管理工具
k9s

# stern - 多Pod日志查看
stern <pod-name-pattern>

# kube-bench - 安全检查
kube-bench

# kubectl-debug
kubectl debug node/<node-name> -it --image=mcr.microsoft.com/dotnet/runtime-deps:6.0
```

## 学习要点

1. 系统化排查思路
2. 日志分析技巧
3. 网络连通性诊断
4. 性能瓶颈定位
5. 根因分析方法
