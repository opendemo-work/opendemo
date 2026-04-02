# Operator Framework

Operator开发框架与工具链演示。

## Operator SDK

```bash
# 安装Operator SDK
curl -LO https://github.com/operator-framework/operator-sdk/releases/latest/download/operator-sdk_linux_amd64
chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/local/bin/operator-sdk

# 验证安装
operator-sdk version
```

## 创建Operator

```bash
# 初始化项目
operator-sdk init --domain example.com --repo github.com/example/my-operator

# 创建API
operator-sdk create api --group app --version v1 --kind MyApp --resource --controller

# 定义CRD结构体
type MyAppSpec struct {
    Replicas int32  `json:"replicas,omitempty"`
    Image    string `json:"image,omitempty"`
}

# 实现Reconcile逻辑
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 获取MyApp实例
    myapp := &appv1.MyApp{}
    if err := r.Get(ctx, req.NamespacedName, myapp); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // 创建Deployment
    deployment := r.deploymentForMyApp(myapp)
    if err := r.Create(ctx, deployment); err != nil {
        return ctrl.Result{}, err
    }
    
    return ctrl.Result{}, nil
}
```

## OLM集成

```bash
# 生成bundle
make bundle

# 测试bundle
operator-sdk run bundle my-registry/my-operator:v1.0.0

# 发布到OperatorHub
make catalog-build catalog-push
```

## 学习要点

1. Operator SDK使用
2. Controller开发模式
3. OLM生命周期管理
4. 测试与调试
