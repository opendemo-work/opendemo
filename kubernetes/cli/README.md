# Kubernetes CLI

Kubectl命令行工具高级使用技巧演示。

## 常用命令速查

```bash
# 资源查询
kubectl get all -n namespace
kubectl get pods -o wide --show-labels
kubectl get events --sort-by='.lastTimestamp'

# 资源操作
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml --grace-period=0 --force
kubectl rollout restart deployment/app

# 调试诊断
kubectl logs pod-name -f --previous
kubectl exec -it pod-name -- /bin/sh
kubectl port-forward svc/service 8080:80
kubectl top nodes
kubectl top pods
```

## 插件工具

```bash
# krew插件管理
kubectl krew install ctx
kubectl krew install ns
kubectl krew install tree

# 常用插件
kubectl ctx    # 上下文切换
kubectl ns     # 命名空间切换
kubectl tree   # 资源树展示
kubectl sniff  # 网络抓包
```

## 学习要点

1. 高效资源查询
2. 调试诊断技巧
3. 插件生态使用
4. 脚本自动化
