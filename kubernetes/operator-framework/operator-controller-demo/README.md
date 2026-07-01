# Kubernetes Operator控制器开发演示

> 使用Kubebuilder框架开发完整的Kubernetes Operator，实现自定义资源的自动化管理

![Difficulty](https://img.shields.io/badge/难度-中级-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-≥1.24-blue)
![Go](https://img.shields.io/badge/Go-≥1.20-00ADD8)
![Kubebuilder](https://img.shields.io/badge/Kubebuilder-3.x-green)

---

##📋 功能概述

本Demo演示如何使用Kubebuilder框架开发Kubernetes Operator，实现AppDeployment自定义资源的自动化管理。

**核心功能**：
- ✅ 使用Kubebuilder快速搭建Operator项目
- ✅ 实现Reconcile调谐循环逻辑
- ✅ 自动创建/更新Deployment和Service
- ✅ 监听资源变化并同步状态
- ✅ 实现Finalizer资源清理机制

**Operator功能**：
- 监听AppDeployment资源创建
- 自动创建对应的Deployment和Service
- 同步副本数变化
- 更新Status状态
- 资源删除时清理关联资源

**学习目标**：
- 掌握Kubebuilder项目结构
- 理解Reconcile调谐循环原理
- 熟悉client-go API使用
- 了解Operator开发最佳实践

---

## 🔧 前置要求

| 类别 | 要求 | 说明 |
|------|------|------|
| **Kubernetes集群** | v1.24+ | 本地minikube或云端集群 |
| **kubectl** | v1.24+ | Kubernetes命令行工具 |
| **Go** | 1.20+ | Operator开发语言 |
| **Kubebuilder** | 3.x | Operator开发框架 |
| **Make** | - | 构建工具 |
| **权限** | cluster-admin | 部署CRD和RBAC |

**环境准备**：

```bash
# 安装Go
# 从 https://golang.org/dl/ 下载安装

# 安装Kubebuilder
curl -L -o kubebuilder "https://go.kubebuilder.io/dl/latest/$(go env GOOS)/$(go env GOARCH)"
chmod +x kubebuilder
sudo mv kubebuilder /usr/local/bin/

# 验证安装
kubebuilder version
```

---

## 🚀 快速开始

### 步骤1：初始化Operator项目

**目标**：使用Kubebuilder创建项目脚手架

**执行命令**：
```bash
# 创建项目目录
mkdir appdeployment-operator
cd appdeployment-operator

# 初始化项目
kubebuilder init --domain demo.opendemo.io --repo github.com/opendemo/appdeployment-operator

# 创建API和Controller
kubebuilder create api --group demo --version v1 --kind AppDeployment --resource --controller

# 项目结构将自动生成
```

**生成的项目结构**：
```
appdeployment-operator/
├── api/v1/                    # API定义
│   └── appdeployment_types.go
├── controllers/               # 控制器实现
│   └── appdeployment_controller.go
├── config/                    # 部署配置
│   ├── crd/                  # CRD定义
│   ├── rbac/                 # RBAC权限
│   └── manager/              # Manager配置
├── go.mod                     # Go依赖
├── Makefile                   # 构建脚本
└── main.go                    # 程序入口
```

### 步骤2：定义API资源类型

编辑`api/v1/appdeployment_types.go`：

```go
// AppDeploymentSpec defines the desired state of AppDeployment
type AppDeploymentSpec struct {
    // 应用副本数量
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=10
    Replicas int32 `json:"replicas"`
    
    // 容器镜像
    // +kubebuilder:validation:Pattern=`^[a-zA-Z0-9\.\-\/\:]+$`
    Image string `json:"image"`
    
    // 服务端口
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=65535
    Port int32 `json:"port"`
}

// AppDeploymentStatus defines the observed state of AppDeployment
type AppDeploymentStatus struct {
    // 当前阶段
    // +optional
    Phase string `json:"phase,omitempty"`
    
    // 准备就绪的副本数
    // +optional
    ReadyReplicas int32 `json:"readyReplicas,omitempty"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status
//+kubebuilder:printcolumn:name="Replicas",type=integer,JSONPath=`.spec.replicas`
//+kubebuilder:printcolumn:name="Ready",type=integer,JSONPath=`.status.readyReplicas`
//+kubebuilder:printcolumn:name="Phase",type=string,JSONPath=`.status.phase`
//+kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`

// AppDeployment is the Schema for the appdeployments API
type AppDeployment struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   AppDeploymentSpec   `json:"spec,omitempty"`
    Status AppDeploymentStatus `json:"status,omitempty"`
}
```

### 步骤3：实现Reconcile逻辑

编辑`controllers/appdeployment_controller.go`：

```go
func (r *AppDeploymentReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    
    // 1. 获取AppDeployment资源
    var appDeploy demov1.AppDeployment
    if err := r.Get(ctx, req.NamespacedName, &appDeploy); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // 2. 检查是否正在删除
    if !appDeploy.DeletionTimestamp.IsZero() {
        return r.handleDeletion(ctx, &appDeploy)
    }
    
    // 3. 添加Finalizer
    if !controllerutil.ContainsFinalizer(&appDeploy, finalizerName) {
        controllerutil.AddFinalizer(&appDeploy, finalizerName)
        if err := r.Update(ctx, &appDeploy); err != nil {
            return ctrl.Result{}, err
        }
    }
    
    // 4. 创建或更新Deployment
    deploy := r.constructDeployment(&appDeploy)
    if err := r.createOrUpdateDeployment(ctx, &appDeploy, deploy); err != nil {
        return ctrl.Result{}, err
    }
    
    // 5. 创建或更新Service
    svc := r.constructService(&appDeploy)
    if err := r.createOrUpdateService(ctx, &appDeploy, svc); err != nil {
        return ctrl.Result{}, err
    }
    
    // 6. 更新Status
    if err := r.updateStatus(ctx, &appDeploy); err != nil {
        return ctrl.Result{}, err
    }
    
    log.Info("Successfully reconciled AppDeployment")
    return ctrl.Result{}, nil
}
```

### 步骤4：生成CRD和部署配置

```bash
# 生成CRD manifests
make manifests

# 生成代码
make generate

# 安装CRD到集群
make install

# 查看生成的CRD
kubectl get crd appdeployments.demo.demo.opendemo.io
```

### 步骤5：本地运行Operator

```bash
# 方式1：本地运行（开发调试）
make run

# 方式2：构建镜像并部署到集群
make docker-build docker-push IMG=<your-registry>/appdeployment-operator:tag
make deploy IMG=<your-registry>/appdeployment-operator:tag
```

### 步骤6：测试Operator

创建测试资源`config/samples/demo_v1_appdeployment.yaml`：

```yaml
apiVersion: demo.demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-app
spec:
  replicas: 3
  image: nginx:1.21
  port: 80
```

应用资源并观察：
```bash
# 创建资源
kubectl apply -f config/samples/demo_v1_appdeployment.yaml

# 查看AppDeployment
kubectl get appdeployments

# 查看Operator自动创建的Deployment
kubectl get deployments

# 查看Operator自动创建的Service
kubectl get services

# 查看Operator日志
kubectl logs -f <operator-pod-name>
```

---

## 📖 核心概念详解

### 1. Reconcile调谐循环

Reconcile是Operator的核心，负责将实际状态调谐到期望状态：

```
期望状态（Spec） → Reconcile → 实际状态（Status）
                      ↓
                  创建/更新/删除资源
```

**核心原则**：
- 幂等性：多次执行结果相同
- 边缘触发：资源变化时触发
- 最终一致性：不断重试直到成功

### 2. Finalizer机制

Finalizer用于在资源删除前执行清理逻辑：

```go
const finalizerName = "appdeployment.demo.opendemo.io/finalizer"

func (r *AppDeploymentReconciler) handleDeletion(ctx context.Context, appDeploy *demov1.AppDeployment) (ctrl.Result, error) {
    // 清理外部资源
    if err := r.cleanupExternalResources(ctx, appDeploy); err != nil {
        return ctrl.Result{}, err
    }
    
    // 移除Finalizer
    controllerutil.RemoveFinalizer(appDeploy, finalizerName)
    if err := r.Update(ctx, appDeploy); err != nil {
        return ctrl.Result{}, err
    }
    
    return ctrl.Result{}, nil
}
```

### 3. OwnerReference关联

通过OwnerReference建立资源关联关系：

```go
func (r *AppDeploymentReconciler) constructDeployment(appDeploy *demov1.AppDeployment) *appsv1.Deployment {
    deploy := &appsv1.Deployment{
        // ...
    }
    
    // 设置OwnerReference
    ctrl.SetControllerReference(appDeploy, deploy, r.Scheme)
    return deploy
}
```

好处：
- 父资源删除时自动删除子资源
- `kubectl describe`可以看到关联关系
- 避免孤儿资源

### 4. Status更新策略

Status应该反映实际状态，与Spec分离更新：

```go
func (r *AppDeploymentReconciler) updateStatus(ctx context.Context, appDeploy *demov1.AppDeployment) error {
    // 获取关联的Deployment
    var deploy appsv1.Deployment
    if err := r.Get(ctx, types.NamespacedName{
        Name:      appDeploy.Name,
        Namespace: appDeploy.Namespace,
    }, &deploy); err != nil {
        return err
    }
    
    // 更新Status
    appDeploy.Status.ReadyReplicas = deploy.Status.ReadyReplicas
    if deploy.Status.ReadyReplicas == appDeploy.Spec.Replicas {
        appDeploy.Status.Phase = "Running"
    } else {
        appDeploy.Status.Phase = "Pending"
    }
    
    // 只更新Status子资源
    return r.Status().Update(ctx, appDeploy)
}
```

---

## ✅ 测试验证

### 单元测试

Kubebuilder生成测试框架：

```go
var _ = Describe("AppDeployment Controller", func() {
    Context("When reconciling a resource", func() {
        It("Should create Deployment and Service", func() {
            ctx := context.Background()
            
            appDeploy := &demov1.AppDeployment{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      "test-app",
                    Namespace: "default",
                },
                Spec: demov1.AppDeploymentSpec{
                    Replicas: 3,
                    Image:    "nginx:1.21",
                    Port:     80,
                },
            }
            
            Expect(k8sClient.Create(ctx, appDeploy)).Should(Succeed())
            
            // 验证Deployment创建
            deploy := &appsv1.Deployment{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-app",
                    Namespace: "default",
                }, deploy)
            }).Should(Succeed())
            
            Expect(*deploy.Spec.Replicas).Should(Equal(int32(3)))
        })
    })
})
```

运行测试：
```bash
make test
```

### 集成测试

```bash
# 创建测试资源
kubectl apply -f config/samples/demo_v1_appdeployment.yaml

# 验证Deployment创建
kubectl get deployment test-app
# 应该显示 READY 3/3

# 验证Service创建
kubectl get service test-app
# 应该显示端口80

# 测试副本数更新
kubectl patch appdeployment test-app -p '{"spec":{"replicas":5}}' --type=merge

# 验证Deployment副本数同步
kubectl get deployment test-app
# 应该显示 READY 5/5

# 测试删除
kubectl delete appdeployment test-app

# 验证关联资源被清理
kubectl get deployment test-app
# 应该显示 NotFound
```

---

## 🎓 进阶使用

### 1. 添加Webhook验证

```bash
kubebuilder create webhook --group demo --version v1 --kind AppDeployment --defaulting --programmatic-validation
```

### 2. 实现多版本API

```bash
kubebuilder create api --group demo --version v2 --kind AppDeployment
```

### 3. 添加监控指标

```go
import "sigs.k8s.io/controller-runtime/pkg/metrics"

var (
    reconcileCounter = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "appdeployment_reconcile_total",
            Help: "Total number of reconciliations",
        },
        []string{"result"},
    )
)

func init() {
    metrics.Registry.MustRegister(reconcileCounter)
}
```

### 4. 实现Leader Election

已默认启用，配置在`main.go`：

```go
mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
    LeaderElection:   true,
    LeaderElectionID: "appdeployment-operator.demo.opendemo.io",
})
```

---

## 🔍 故障排查

| 现象 | 可能原因 | 解决方法 |
|------|----------|----------|
| **Operator启动失败** | CRD未安装 | 执行`make install`安装CRD |
| **Reconcile未触发** | RBAC权限不足 | 检查`config/rbac/`配置 |
| **资源创建失败** | OwnerReference错误 | 检查Scheme注册 |
| **Status未更新** | 未使用Status()子资源 | 使用`r.Status().Update()` |
| **资源删除卡住** | Finalizer未清理 | 检查`handleDeletion`逻辑 |

**查看日志**：
```bash
# 本地运行时直接显示
make run

# 集群部署后查看Pod日志
kubectl logs -n appdeployment-operator-system deployment/appdeployment-operator-controller-manager
```

---

## 🧹 清理资源

```bash
# 删除示例资源
kubectl delete -f config/samples/demo_v1_appdeployment.yaml

# 卸载Operator
make undeploy

# 删除CRD
make uninstall
```

---

## 📚 参考资料

### 官方文档
- [Kubebuilder Book](https://book.kubebuilder.io/)
- [Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [client-go Documentation](https://github.com/kubernetes/client-go)

### 学习资源
- [Operator SDK](https://sdk.operatorframework.io/)
- [controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
- [Sample Controller](https://github.com/kubernetes/sample-controller)

### 本项目相关
- [CRD基础使用](../crd-basic-usage/) - 前置知识
- [KubeSkoop Operator](../../kubeskoop/) - 生产级示例

---

**Created**: 2026-01-06  
**Version**: 1.0.0  
**License**: MIT
# Kubernetes Operator控制器开发演示

> 使用Kubebuilder框架开发完整的Kubernetes Operator，实现自定义资源的自动化管理

![Difficulty](https://img.shields.io/badge/难度-中级-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-≥1.24-blue)
![Go](https://img.shields.io/badge/Go-≥1.20-00ADD8)
![Kubebuilder](https://img.shields.io/badge/Kubebuilder-3.x-green)

---

##📋 功能概述

本Demo演示如何使用Kubebuilder框架开发Kubernetes Operator，实现AppDeployment自定义资源的自动化管理。

**核心功能**：
- ✅ 使用Kubebuilder快速搭建Operator项目
- ✅ 实现Reconcile调谐循环逻辑
- ✅ 自动创建/更新Deployment和Service
- ✅ 监听资源变化并同步状态
- ✅ 实现Finalizer资源清理机制

**Operator功能**：
- 监听AppDeployment资源创建
- 自动创建对应的Deployment和Service
- 同步副本数变化
- 更新Status状态
- 资源删除时清理关联资源

**学习目标**：
- 掌握Kubebuilder项目结构
- 理解Reconcile调谐循环原理
- 熟悉client-go API使用
- 了解Operator开发最佳实践

---

## 🔧 前置要求

| 类别 | 要求 | 说明 |
|------|------|------|
| **Kubernetes集群** | v1.24+ | 本地minikube或云端集群 |
| **kubectl** | v1.24+ | Kubernetes命令行工具 |
| **Go** | 1.20+ | Operator开发语言 |
| **Kubebuilder** | 3.x | Operator开发框架 |
| **Make** | - | 构建工具 |
| **权限** | cluster-admin | 部署CRD和RBAC |

**环境准备**：

```bash
# 安装Go
# 从 https://golang.org/dl/ 下载安装

# 安装Kubebuilder
curl -L -o kubebuilder "https://go.kubebuilder.io/dl/latest/$(go env GOOS)/$(go env GOARCH)"
chmod +x kubebuilder
sudo mv kubebuilder /usr/local/bin/

# 验证安装
kubebuilder version
```

---

## 🚀 快速开始

### 步骤1：初始化Operator项目

**目标**：使用Kubebuilder创建项目脚手架

**执行命令**：
```bash
# 创建项目目录
mkdir appdeployment-operator
cd appdeployment-operator

# 初始化项目
kubebuilder init --domain demo.opendemo.io --repo github.com/opendemo/appdeployment-operator

# 创建API和Controller
kubebuilder create api --group demo --version v1 --kind AppDeployment --resource --controller

# 项目结构将自动生成
```

**生成的项目结构**：
```
appdeployment-operator/
├── api/v1/                    # API定义
│   └── appdeployment_types.go
├── controllers/               # 控制器实现
│   └── appdeployment_controller.go
├── config/                    # 部署配置
│   ├── crd/                  # CRD定义
│   ├── rbac/                 # RBAC权限
│   └── manager/              # Manager配置
├── go.mod                     # Go依赖
├── Makefile                   # 构建脚本
└── main.go                    # 程序入口
```

### 步骤2：定义API资源类型

编辑`api/v1/appdeployment_types.go`：

```go
// AppDeploymentSpec defines the desired state of AppDeployment
type AppDeploymentSpec struct {
    // 应用副本数量
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=10
    Replicas int32 `json:"replicas"`
    
    // 容器镜像
    // +kubebuilder:validation:Pattern=`^[a-zA-Z0-9\.\-\/\:]+$`
    Image string `json:"image"`
    
    // 服务端口
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=65535
    Port int32 `json:"port"`
}

// AppDeploymentStatus defines the observed state of AppDeployment
type AppDeploymentStatus struct {
    // 当前阶段
    // +optional
    Phase string `json:"phase,omitempty"`
    
    // 准备就绪的副本数
    // +optional
    ReadyReplicas int32 `json:"readyReplicas,omitempty"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status
//+kubebuilder:printcolumn:name="Replicas",type=integer,JSONPath=`.spec.replicas`
//+kubebuilder:printcolumn:name="Ready",type=integer,JSONPath=`.status.readyReplicas`
//+kubebuilder:printcolumn:name="Phase",type=string,JSONPath=`.status.phase`
//+kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`

// AppDeployment is the Schema for the appdeployments API
type AppDeployment struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   AppDeploymentSpec   `json:"spec,omitempty"`
    Status AppDeploymentStatus `json:"status,omitempty"`
}
```

### 步骤3：实现Reconcile逻辑

编辑`controllers/appdeployment_controller.go`：

```go
func (r *AppDeploymentReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    
    // 1. 获取AppDeployment资源
    var appDeploy demov1.AppDeployment
    if err := r.Get(ctx, req.NamespacedName, &appDeploy); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    
    // 2. 检查是否正在删除
    if !appDeploy.DeletionTimestamp.IsZero() {
        return r.handleDeletion(ctx, &appDeploy)
    }
    
    // 3. 添加Finalizer
    if !controllerutil.ContainsFinalizer(&appDeploy, finalizerName) {
        controllerutil.AddFinalizer(&appDeploy, finalizerName)
        if err := r.Update(ctx, &appDeploy); err != nil {
            return ctrl.Result{}, err
        }
    }
    
    // 4. 创建或更新Deployment
    deploy := r.constructDeployment(&appDeploy)
    if err := r.createOrUpdateDeployment(ctx, &appDeploy, deploy); err != nil {
        return ctrl.Result{}, err
    }
    
    // 5. 创建或更新Service
    svc := r.constructService(&appDeploy)
    if err := r.createOrUpdateService(ctx, &appDeploy, svc); err != nil {
        return ctrl.Result{}, err
    }
    
    // 6. 更新Status
    if err := r.updateStatus(ctx, &appDeploy); err != nil {
        return ctrl.Result{}, err
    }
    
    log.Info("Successfully reconciled AppDeployment")
    return ctrl.Result{}, nil
}
```

### 步骤4：生成CRD和部署配置

```bash
# 生成CRD manifests
make manifests

# 生成代码
make generate

# 安装CRD到集群
make install

# 查看生成的CRD
kubectl get crd appdeployments.demo.demo.opendemo.io
```

### 步骤5：本地运行Operator

```bash
# 方式1：本地运行（开发调试）
make run

# 方式2：构建镜像并部署到集群
make docker-build docker-push IMG=<your-registry>/appdeployment-operator:tag
make deploy IMG=<your-registry>/appdeployment-operator:tag
```

### 步骤6：测试Operator

创建测试资源`config/samples/demo_v1_appdeployment.yaml`：

```yaml
apiVersion: demo.demo.opendemo.io/v1
kind: AppDeployment
metadata:
  name: test-app
spec:
  replicas: 3
  image: nginx:1.21
  port: 80
```

应用资源并观察：
```bash
# 创建资源
kubectl apply -f config/samples/demo_v1_appdeployment.yaml

# 查看AppDeployment
kubectl get appdeployments

# 查看Operator自动创建的Deployment
kubectl get deployments

# 查看Operator自动创建的Service
kubectl get services

# 查看Operator日志
kubectl logs -f <operator-pod-name>
```

---

## 📖 核心概念详解

### 1. Reconcile调谐循环

Reconcile是Operator的核心，负责将实际状态调谐到期望状态：

```
期望状态（Spec） → Reconcile → 实际状态（Status）
                      ↓
                  创建/更新/删除资源
```

**核心原则**：
- 幂等性：多次执行结果相同
- 边缘触发：资源变化时触发
- 最终一致性：不断重试直到成功

### 2. Finalizer机制

Finalizer用于在资源删除前执行清理逻辑：

```go
const finalizerName = "appdeployment.demo.opendemo.io/finalizer"

func (r *AppDeploymentReconciler) handleDeletion(ctx context.Context, appDeploy *demov1.AppDeployment) (ctrl.Result, error) {
    // 清理外部资源
    if err := r.cleanupExternalResources(ctx, appDeploy); err != nil {
        return ctrl.Result{}, err
    }
    
    // 移除Finalizer
    controllerutil.RemoveFinalizer(appDeploy, finalizerName)
    if err := r.Update(ctx, appDeploy); err != nil {
        return ctrl.Result{}, err
    }
    
    return ctrl.Result{}, nil
}
```

### 3. OwnerReference关联

通过OwnerReference建立资源关联关系：

```go
func (r *AppDeploymentReconciler) constructDeployment(appDeploy *demov1.AppDeployment) *appsv1.Deployment {
    deploy := &appsv1.Deployment{
        // ...
    }
    
    // 设置OwnerReference
    ctrl.SetControllerReference(appDeploy, deploy, r.Scheme)
    return deploy
}
```

好处：
- 父资源删除时自动删除子资源
- `kubectl describe`可以看到关联关系
- 避免孤儿资源

### 4. Status更新策略

Status应该反映实际状态，与Spec分离更新：

```go
func (r *AppDeploymentReconciler) updateStatus(ctx context.Context, appDeploy *demov1.AppDeployment) error {
    // 获取关联的Deployment
    var deploy appsv1.Deployment
    if err := r.Get(ctx, types.NamespacedName{
        Name:      appDeploy.Name,
        Namespace: appDeploy.Namespace,
    }, &deploy); err != nil {
        return err
    }
    
    // 更新Status
    appDeploy.Status.ReadyReplicas = deploy.Status.ReadyReplicas
    if deploy.Status.ReadyReplicas == appDeploy.Spec.Replicas {
        appDeploy.Status.Phase = "Running"
    } else {
        appDeploy.Status.Phase = "Pending"
    }
    
    // 只更新Status子资源
    return r.Status().Update(ctx, appDeploy)
}
```

---

## ✅ 测试验证

### 单元测试

Kubebuilder生成测试框架：

```go
var _ = Describe("AppDeployment Controller", func() {
    Context("When reconciling a resource", func() {
        It("Should create Deployment and Service", func() {
            ctx := context.Background()
            
            appDeploy := &demov1.AppDeployment{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      "test-app",
                    Namespace: "default",
                },
                Spec: demov1.AppDeploymentSpec{
                    Replicas: 3,
                    Image:    "nginx:1.21",
                    Port:     80,
                },
            }
            
            Expect(k8sClient.Create(ctx, appDeploy)).Should(Succeed())
            
            // 验证Deployment创建
            deploy := &appsv1.Deployment{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-app",
                    Namespace: "default",
                }, deploy)
            }).Should(Succeed())
            
            Expect(*deploy.Spec.Replicas).Should(Equal(int32(3)))
        })
    })
})
```

运行测试：
```bash
make test
```

### 集成测试

```bash
# 创建测试资源
kubectl apply -f config/samples/demo_v1_appdeployment.yaml

# 验证Deployment创建
kubectl get deployment test-app
# 应该显示 READY 3/3

# 验证Service创建
kubectl get service test-app
# 应该显示端口80

# 测试副本数更新
kubectl patch appdeployment test-app -p '{"spec":{"replicas":5}}' --type=merge

# 验证Deployment副本数同步
kubectl get deployment test-app
# 应该显示 READY 5/5

# 测试删除
kubectl delete appdeployment test-app

# 验证关联资源被清理
kubectl get deployment test-app
# 应该显示 NotFound
```

---

## 🎓 进阶使用

### 1. 添加Webhook验证

```bash
kubebuilder create webhook --group demo --version v1 --kind AppDeployment --defaulting --programmatic-validation
```

### 2. 实现多版本API

```bash
kubebuilder create api --group demo --version v2 --kind AppDeployment
```

### 3. 添加监控指标

```go
import "sigs.k8s.io/controller-runtime/pkg/metrics"

var (
    reconcileCounter = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "appdeployment_reconcile_total",
            Help: "Total number of reconciliations",
        },
        []string{"result"},
    )
)

func init() {
    metrics.Registry.MustRegister(reconcileCounter)
}
```

### 4. 实现Leader Election

已默认启用，配置在`main.go`：

```go
mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
    LeaderElection:   true,
    LeaderElectionID: "appdeployment-operator.demo.opendemo.io",
})
```

---

## 🔍 故障排查

| 现象 | 可能原因 | 解决方法 |
|------|----------|----------|
| **Operator启动失败** | CRD未安装 | 执行`make install`安装CRD |
| **Reconcile未触发** | RBAC权限不足 | 检查`config/rbac/`配置 |
| **资源创建失败** | OwnerReference错误 | 检查Scheme注册 |
| **Status未更新** | 未使用Status()子资源 | 使用`r.Status().Update()` |
| **资源删除卡住** | Finalizer未清理 | 检查`handleDeletion`逻辑 |

**查看日志**：
```bash
# 本地运行时直接显示
make run

# 集群部署后查看Pod日志
kubectl logs -n appdeployment-operator-system deployment/appdeployment-operator-controller-manager
```

---

## 🧹 清理资源

```bash
# 删除示例资源
kubectl delete -f config/samples/demo_v1_appdeployment.yaml

# 卸载Operator
make undeploy

# 删除CRD
make uninstall
```

---

## 📚 参考资料

### 官方文档
- [Kubebuilder Book](https://book.kubebuilder.io/)
- [Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
- [client-go Documentation](https://github.com/kubernetes/client-go)

### 学习资源
- [Operator SDK](https://sdk.operatorframework.io/)
- [controller-runtime](https://pkg.go.dev/sigs.k8s.io/controller-runtime)
- [Sample Controller](https://github.com/kubernetes/sample-controller)

### 本项目相关
- [CRD基础使用](../crd-basic-usage/) - 前置知识
- [KubeSkoop Operator](../../kubeskoop/) - 生产级示例

---

**Created**: 2026-01-06  
**Version**: 1.0.0  
**License**: MIT

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 Kubernetes 核心概念
- ✅ 掌握相关的资源配置与命令
- ✅ 能够在本地集群中复现

## 💻 代码示例

### 基本命令

```bash
# 请根据实际场景替换
kubectl apply -f manifests/
```
