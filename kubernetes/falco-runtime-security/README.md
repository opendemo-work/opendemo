# Falco Runtime Security

Falco容器运行时安全监控演示。

## 什么是Falco

Falco是开源的云原生运行时安全工具：

```
Falco架构:
┌─────────────────────────────────────────────────────────┐
│  Application / Container                                │
├─────────────────────────────────────────────────────────┤
│  System Calls (syscalls)                                │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │  Falco Probe (内核模块/eBPF)                     │   │
│  │  - 系统调用捕获                                  │   │
│  │  - 事件过滤                                      │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  Falco Engine (规则引擎)                                 │
│  - 规则匹配                                             │
│  - 异常检测                                             │
├─────────────────────────────────────────────────────────┤
│  Outputs (Alerts/Logs)                                  │
│  - stdout                                               │
│  - File                                                 │
│  - Webhook                                              │
│  - gRPC                                                 │
└─────────────────────────────────────────────────────────┘
```

## 安装Falco

```bash
# Helm安装
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace \
  --set driver.kind=ebpf

# 验证
kubectl get pods -n falco
kubectl logs -n falco -l app.kubernetes.io/name=falco
```

## Falco规则示例

```yaml
# 自定义规则
- rule: Unauthorized Container Privilege Escalation
  desc: Detect privilege escalation in containers
  condition: >
    spawned_process and
    container and
    (user.uid != 0 and user.euid = 0)
  output: >
    Privilege escalation detected
    (user=%user.name command=%proc.cmdline)
  priority: CRITICAL

- rule: Sensitive File Access
  desc: Detect access to sensitive files
  condition: >
    open_read and
    (fd.name contains "/etc/shadow" or
     fd.name contains "/etc/passwd")
  output: >
    Sensitive file accessed
    (file=%fd.name user=%user.name)
  priority: WARNING
```

## 学习要点

1. 运行时安全概念
2. Falco规则编写
3. 异常检测配置
4. 告警响应
5. 与SIEM集成
