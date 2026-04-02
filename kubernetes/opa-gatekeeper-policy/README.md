# OPA/Gatekeeper Policy

OPA/Gatekeeper策略管理演示。

## 什么是OPA/Gatekeeper

Open Policy Agent (OPA) 是通用的策略引擎：

```
策略执行流程:
Admission Request -> Gatekeeper -> OPA/Rego -> Allow/Deny
```

## 安装Gatekeeper

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# 验证
kubectl get pods -n gatekeeper-system
```

## 约束模板示例

```yaml
# 限制镜像仓库
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sallowedrepos
spec:
  crd:
    spec:
      names:
        kind: K8sAllowedRepos
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sallowedrepos
        
        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          satisfied := [good | repo = input.parameters.repos[_] ; good = startswith(container.image, repo)]
          not any(satisfied)
          msg := sprintf("container <%v> has invalid image repo <%v>", [container.name, container.image])
        }
```

## 学习要点

1. OPA/Rego语言
2. Gatekeeper约束
3. 策略模板开发
4. 准入控制
5. 合规检查
