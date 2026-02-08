# 🔄 Kubernetes 本地开发 CI/CD 集成最佳实践

> 本地 Kubernetes 环境与 CI/CD 流水线的无缝集成指南

## 🎯 CI/CD 集成概述

将本地 Kubernetes 开发环境与 CI/CD 流水线集成，可以实现从代码提交到生产部署的自动化流程，提高开发效率和软件质量。

### 📋 核心目标
- **自动化构建**：代码变更自动触发构建流程
- **持续测试**：自动化测试确保代码质量
- **快速部署**：一键部署到不同环境
- **环境一致性**：保证开发、测试、生产环境一致性
- **快速反馈**：及时获得构建和测试结果

## 🛠️ 本地开发环境准备

### 1. 工具链配置

```bash
# 安装必要的 CI/CD 工具
install_cicd_tools() {
    # GitHub Actions 本地测试工具
    brew install act
    
    # GitLab CI 本地测试工具
    brew install gitlab-runner
    
    # Jenkins CLI
    wget -O jenkins-cli.jar http://localhost:8080/jnlpJars/jenkins-cli.jar
    
    # Helm (用于包管理)
    brew install helm
    
    # Kustomize (用于配置管理)
    brew install kustomize
    
    # Argo CD CLI (GitOps 工具)
    brew install argocd
    
    echo "CI/CD 工具安装完成"
}

# 验证工具安装
verify_cicd_tools() {
    echo "=== CI/CD 工具验证 ==="
    
    command -v act && echo "✅ act 已安装" || echo "❌ act 未安装"
    command -v gitlab-runner && echo "✅ gitlab-runner 已安装" || echo "❌ gitlab-runner 未安装"
    command -v helm && echo "✅ helm 已安装" || echo "❌ helm 未安装"
    command -v kustomize && echo "✅ kustomize 已安装" || echo "❌ kustomize 未安装"
    command -v argocd && echo "✅ argocd 已安装" || echo "❌ argocd 未安装"
}
```

### 2. 本地开发环境配置

```yaml
# 本地开发环境配置文件 .devcontainer/devcontainer.json
{
  "name": "Kubernetes Dev Environment",
  "image": "mcr.microsoft.com/devcontainers/go:1.21",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "redhat.vscode-yaml",
        "ms-azuretools.vscode-docker"
      ]
    }
  },
  "forwardPorts": [8080],
  "postCreateCommand": "make setup-dev-environment"
}
```

## 🚀 GitHub Actions 集成

### 1. 基础 CI/CD 工作流

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'
    
    - name: Run unit tests
      run: go test -v ./...
    
    - name: Run integration tests
      run: |
        kind create cluster --name test-cluster
        kubectl cluster-info --context kind-test-cluster
        make integration-test
        kind delete cluster --name test-cluster

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-dev:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to development cluster
      run: |
        kubectl config use-context development-cluster
        kustomize build k8s/overlays/dev | kubectl apply -f -
        kubectl rollout status deployment/app-deployment -n development

  deploy-prod:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to production cluster
      run: |
        kubectl config use-context production-cluster
        kustomize build k8s/overlays/prod | kubectl apply -f -
        kubectl rollout status deployment/app-deployment -n production
```

### 2. 本地测试 GitHub Actions

```bash
# 使用 act 在本地测试 GitHub Actions
test_github_actions_locally() {
    # 安装 act
    brew install act
    
    # 列出所有工作流
    act -l
    
    # 运行特定事件的工作流
    act push  # 模拟 push 事件
    act pull_request  # 模拟 PR 事件
    
    # 运行特定工作流
    act -j test  # 只运行 test 作业
    
    # 使用自定义环境变量
    act -e test-env.json push
    
    # 挂载本地目录
    act -b . push  # 绑定当前目录
}

# 创建本地测试环境配置
create_test_env() {
    cat <<EOF > test-env.json
{
  "act": true,
  "github": {
    "actor": "developer",
    "repository": "owner/repo"
  },
  "secrets": {
    "DOCKER_USERNAME": "test-user",
    "DOCKER_PASSWORD": "test-password"
  }
}
EOF
}
```

## 🦊 GitLab CI 集成

### 1. GitLab CI 配置

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  KUBE_CONTEXT: "kind-local"

before_script:
  - docker info
  - kubectl cluster-info

test:
  stage: test
  image: golang:1.21
  services:
    - name: docker:dind
      alias: docker
  script:
    - go test -v ./...
    - kind create cluster --name test-cluster
    - kubectl cluster-info --context kind-test-cluster
    - make integration-test
  after_script:
    - kind delete cluster --name test-cluster
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "develop" || $CI_COMMIT_BRANCH == "main"

build:
  stage: build
  image: docker:20.10.16
  services:
    - name: docker:dind
      alias: docker
  variables:
    DOCKER_HOST: tcp://docker:2376
    DOCKER_TLS_VERIFY: 1
    DOCKER_CERT_PATH: "/certs/client"
  script:
    - docker build --pull -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
  rules:
    - if: $CI_COMMIT_BRANCH == "develop" || $CI_COMMIT_BRANCH == "main"

deploy-dev:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context $KUBE_CONTEXT
    - kustomize build k8s/overlays/dev | kubectl apply -f -
    - kubectl rollout status deployment/app-deployment -n development
  environment:
    name: development
    url: https://dev.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-prod:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production-cluster
    - kustomize build k8s/overlays/prod | kubectl apply -f -
    - kubectl rollout status deployment/app-deployment -n production
  environment:
    name: production
    url: https://example.com
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### 2. 本地 GitLab Runner

```bash
# 注册本地 GitLab Runner
setup_local_gitlab_runner() {
    # 下载并安装 runner
    curl -L --output /usr/local/bin/gitlab-runner \
        "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-darwin-amd64"
    chmod +x /usr/local/bin/gitlab-runner
    
    # 注册 runner
    gitlab-runner register \
        --non-interactive \
        --url "https://gitlab.com/" \
        --registration-token "REGISTRATION_TOKEN" \
        --executor "shell" \
        --description "local-dev-runner" \
        --tag-list "local,dev" \
        --run-untagged="true" \
        --locked="false"
    
    # 启动 runner
    gitlab-runner install
    gitlab-runner start
}

# 本地测试 GitLab CI 配置
test_gitlab_ci_locally() {
    # 使用 gitlab-ci-local 工具
    npm install -g gitlab-ci-local
    
    # 列出所有作业
    gitlab-ci-local --list
    
    # 运行特定作业
    gitlab-ci-local test
    gitlab-ci-local build
    
    # 运行整个流水线
    gitlab-ci-local
}
```

## 🌊 GitOps 实践

### 1. Argo CD 集成

```yaml
# Argo CD Application 配置
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/owner/my-app-config.git
    targetRevision: HEAD
    path: k8s/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: development
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
```

### 2. 本地 GitOps 开发流程

```bash
# 设置本地 GitOps 环境
setup_local_gitops() {
    # 安装 Argo CD CLI
    brew install argocd
    
    # 部署 Argo CD 到本地集群
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    
    # 等待 Argo CD 就绪
    kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=300s
    
    # 获取初始密码
    argocd_password=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
    echo "Argo CD 初始密码: $argocd_password"
    
    # 端口转发访问 Argo CD UI
    kubectl port-forward svc/argocd-server -n argocd 8080:443 &
}

# 本地 GitOps 开发工作流
gitops_development_workflow() {
    # 1. 创建应用配置仓库结构
    mkdir -p my-app-config/{base,overlays/{dev,staging,prod}}
    
    # 2. 创建基础配置
    cat <<EOF > my-app-config/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
- configmap.yaml
EOF
    
    # 3. 创建开发环境覆盖
    cat <<EOF > my-app-config/overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases:
- ../../base
namePrefix: dev-
patchesStrategicMerge:
- patch.yaml
EOF
    
    # 4. 创建 Argo CD Application
    cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-dev
  namespace: argocd
spec:
  project: default
  source:
    repoURL: file:///workspace/my-app-config
    targetRevision: HEAD
    path: overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: development
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
EOF
}

# GitOps 本地开发脚本
create_gitops_scripts() {
    # 创建同步脚本
    cat <<'EOF' > sync-app.sh
#!/bin/bash
# 应用配置同步脚本

APP_NAME=$1
ENVIRONMENT=$2

if [ -z "$APP_NAME" ] || [ -z "$ENVIRONMENT" ]; then
    echo "用法: $0 <app-name> <environment>"
    exit 1
fi

# 提交配置更改
git add .
git commit -m "Update $APP_NAME configuration for $ENVIRONMENT"
git push origin main

# 触发 Argo CD 同步
argocd app sync $APP_NAME-$ENVIRONMENT --prune
argocd app wait $APP_NAME-$ENVIRONMENT --health
EOF

    chmod +x sync-app.sh
    
    # 创建环境切换脚本
    cat <<'EOF' > switch-env.sh
#!/bin/bash
# 环境切换脚本

ENV=$1

case $ENV in
    "dev")
        kubectl config use-context kind-dev
        export KUBECONFIG=~/.kube/kind-dev-config
        ;;
    "staging")
        kubectl config use-context kind-staging
        export KUBECONFIG=~/.kube/kind-staging-config
        ;;
    "prod")
        kubectl config use-context kind-prod
        export KUBECONFIG=~/.kube/kind-prod-config
        ;;
    *)
        echo "支持的环境: dev, staging, prod"
        exit 1
        ;;
esac

echo "已切换到 $ENV 环境"
EOF

    chmod +x switch-env.sh
}
```

## 🧪 自动化测试策略

### 1. 测试层次结构

```bash
# 创建测试框架
setup_testing_framework() {
    # 单元测试
    cat <<'EOF' > Makefile.test
.PHONY: unit-test
unit-test:
	go test -v ./... -short

.PHONY: integration-test
integration-test:
	kind create cluster --name integration-test
	kubectl cluster-info --context kind-integration-test
	go test -v ./integration/...
	kind delete cluster --name integration-test

.PHONY: e2e-test
e2e-test:
	kind create cluster --name e2e-test
	kubectl apply -f k8s/base/
	kubectl wait --for=condition=available deployment/app-deployment --timeout=300s
	go test -v ./e2e/...
	kind delete cluster --name e2e-test
EOF

    # 创建集成测试示例
    mkdir -p integration
    cat <<'EOF' > integration/deployment_test.go
package integration

import (
    "testing"
    "time"
    
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/clientcmd"
)

func TestDeploymentHealth(t *testing.T) {
    // 加载 kubeconfig
    config, err := clientcmd.BuildConfigFromFlags("", "/tmp/kind-integration-test-config")
    if err != nil {
        t.Fatalf("无法加载 kubeconfig: %v", err)
    }
    
    // 创建客户端
    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        t.Fatalf("无法创建客户端: %v", err)
    }
    
    // 等待部署就绪
    timeout := time.After(5 * time.Minute)
    ticker := time.NewTicker(10 * time.Second)
    defer ticker.Stop()
    
    for {
        select {
        case <-timeout:
            t.Fatal("部署超时未就绪")
        case <-ticker.C:
            deployment, err := clientset.AppsV1().Deployments("default").Get(context.TODO(), "app-deployment", metav1.GetOptions{})
            if err != nil {
                t.Logf("获取部署信息失败: %v", err)
                continue
            }
            
            if deployment.Status.ReadyReplicas == *deployment.Spec.Replicas {
                t.Log("部署已就绪")
                return
            }
            
            t.Logf("部署状态: %d/%d Pods 就绪", deployment.Status.ReadyReplicas, *deployment.Spec.Replicas)
        }
    }
}
EOF
}

# 性能测试集成
setup_performance_testing() {
    # 安装性能测试工具
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/perf-tests/master/network/benchmarks/netperf/manifests/netperf-daemonset.yaml
    
    # 创建性能测试脚本
    cat <<'EOF' > performance-test.sh
#!/bin/bash
# 性能测试脚本

echo "=== 性能测试 ==="

# 网络性能测试
echo "1. 网络延迟测试"
kubectl exec -it $(kubectl get pods -l app=netperf -o jsonpath='{.items[0].metadata.name}') -- \
    netperf -H $(kubectl get pods -l app=netperf -o jsonpath='{.items[1].status.podIP}') -t TCP_RR

# 存储性能测试
echo "2. 存储 I/O 测试"
kubectl run storage-test --image=busybox --rm -it --restart=Never -- \
    dd if=/dev/zero of=/data/test.dat bs=1M count=100 oflag=dsync

# API 服务器性能测试
echo "3. API 服务器响应时间测试"
for i in {1..10}; do
    time kubectl get nodes > /dev/null
done
EOF

    chmod +x performance-test.sh
}
```

### 2. 测试报告生成

```bash
# 测试报告生成工具
generate_test_reports() {
    # 创建 JUnit XML 报告
    cat <<'EOF' > test-report.sh
#!/bin/bash
# 测试报告生成脚本

REPORT_DIR="test-reports"
mkdir -p $REPORT_DIR

# 运行测试并生成报告
go test -v ./... -json > $REPORT_DIR/test-results.json

# 转换为 JUnit 格式
go install github.com/jstemmer/go-junit-report/v2@latest
cat $REPORT_DIR/test-results.json | go-junit-report > $REPORT_DIR/junit-report.xml

# 生成覆盖率报告
go test -coverprofile=$REPORT_DIR/coverage.out ./...
go tool cover -html=$REPORT_DIR/coverage.out -o $REPORT_DIR/coverage.html

echo "测试报告已生成到 $REPORT_DIR/"
EOF

    chmod +x test-report.sh
    
    # 创建 HTML 测试报告模板
    cat <<'EOF' > test-report-template.html
<!DOCTYPE html>
<html>
<head>
    <title>测试报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .summary { background: #f5f5f5; padding: 15px; border-radius: 5px; }
        .test-suite { margin: 20px 0; border: 1px solid #ddd; }
        .test-case { padding: 10px; border-bottom: 1px solid #eee; }
        .passed { background: #dff0d8; }
        .failed { background: #f2dede; }
        .coverage { width: 100%; background: #f5f5f5; height: 20px; border-radius: 10px; overflow: hidden; }
        .coverage-bar { height: 100%; background: #5cb85c; }
    </style>
</head>
<body>
    <h1>CI/CD 测试报告</h1>
    
    <div class="summary">
        <h2>测试摘要</h2>
        <p>总测试数: <span id="total-tests">0</span></p>
        <p>通过测试: <span id="passed-tests">0</span></p>
        <p>失败测试: <span id="failed-tests">0</span></p>
        <p>测试覆盖率: <span id="coverage-percent">0%</span></p>
        <div class="coverage">
            <div class="coverage-bar" id="coverage-bar" style="width: 0%"></div>
        </div>
    </div>
    
    <div id="test-results"></div>
    
    <script>
        // 这里可以添加解析测试结果 JSON 并渲染到页面的 JavaScript 代码
    </script>
</body>
</html>
EOF
}
```

## 🚀 部署策略和蓝绿部署

### 1. 蓝绿部署配置

```yaml
# 蓝绿部署配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
      version: blue
  template:
    metadata:
      labels:
        app: app
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:blue-version
        ports:
        - containerPort: 8080

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 0  # 初始状态为0
  selector:
    matchLabels:
      app: app
      version: green
  template:
    metadata:
      labels:
        app: app
        version: green
    spec:
      containers:
      - name: app
        image: myapp:green-version
        ports:
        - containerPort: 8080

---
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: app
    version: blue  # 初始指向蓝色环境
  ports:
  - port: 80
    targetPort: 8080
```

### 2. 部署切换脚本

```bash
# 蓝绿部署切换脚本
blue_green_deploy() {
    local new_version=$1  # blue 或 green
    local current_version=""
    
    # 检测当前版本
    current_svc_selector=$(kubectl get service app-service -o jsonpath='{.spec.selector.version}')
    if [ "$current_svc_selector" = "blue" ]; then
        current_version="blue"
    else
        current_version="green"
    fi
    
    echo "当前版本: $current_version"
    echo "新版本: $new_version"
    
    # 部署新版本
    echo "部署新版本..."
    kubectl scale deployment app-$new_version --replicas=3
    
    # 等待新版本就绪
    echo "等待新版本就绪..."
    kubectl rollout status deployment/app-$new_version --timeout=300s
    
    # 测试新版本
    echo "测试新版本..."
    if ! curl -f http://app-service/health; then
        echo "新版本健康检查失败，回滚..."
        kubectl scale deployment app-$new_version --replicas=0
        exit 1
    fi
    
    # 切换流量
    echo "切换流量到新版本..."
    kubectl patch service app-service -p '{"spec":{"selector":{"version":"'$new_version'"}}}'
    
    # 验证切换
    echo "验证流量切换..."
    sleep 30
    if curl -f http://app-service/version | grep -q "$new_version"; then
        echo "流量切换成功"
        # 缩减旧版本
        kubectl scale deployment app-$current_version --replicas=0
    else
        echo "流量切换验证失败，回滚..."
        kubectl patch service app-service -p '{"spec":{"selector":{"version":"'$current_version'"}}}'
        kubectl scale deployment app-$new_version --replicas=0
        exit 1
    fi
    
    echo "蓝绿部署完成"
}

# 滚动更新配置
rolling_update_config() {
    cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rolling-update-app
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: rolling-app
  template:
    metadata:
      labels:
        app: rolling-app
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
EOF
}
```

## 📊 监控和反馈

### 1. 构建状态监控

```bash
# CI/CD 状态监控仪表板
create_cicd_dashboard() {
    # 创建简单的状态监控脚本
    cat <<'EOF' > cicd-monitor.sh
#!/bin/bash
# CI/CD 状态监控脚本

REPO_URL="https://api.github.com/repos/owner/repo/actions/runs"
WEBHOOK_URL="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

# 获取最近的运行状态
get_latest_run_status() {
    curl -s -H "Authorization: token $GITHUB_TOKEN" $REPO_URL | \
        jq -r '.workflow_runs[0] | "\(.status) \(.conclusion) \(.created_at)"'
}

# 发送通知
send_notification() {
    local status=$1
    local message=$2
    
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"CI/CD 状态: $status - $message\"}" \
        $WEBHOOK_URL
}

# 监控循环
while true; do
    status=$(get_latest_run_status)
    echo "当前状态: $status"
    
    if echo "$status" | grep -q "completed success"; then
        send_notification "✅ 成功" "构建和部署成功完成"
    elif echo "$status" | grep -q "completed failure"; then
        send_notification "❌ 失败" "构建或部署失败，请检查日志"
    fi
    
    sleep 300  # 每5分钟检查一次
done
EOF

    chmod +x cicd-monitor.sh
}

# 本地开发反馈集成
setup_local_feedback() {
    # 创建本地通知脚本
    cat <<'EOF' > local-notify.sh
#!/bin/bash
# 本地开发通知脚本

notify_build_success() {
    osascript -e "display notification \"构建成功!\" with title \"CI/CD\""
}

notify_build_failure() {
    osascript -e "display notification \"构建失败!\" with title \"CI/CD\" sound name \"Glass\""
}

notify_deployment_complete() {
    osascript -e "display notification \"部署完成!\" with title \"CI/CD\""
}

# 集成到 Makefile
cat <<'MAKEFILE' >> Makefile

.PHONY: notify-success
notify-success:
	./local-notify.sh notify_build_success

.PHONY: notify-failure
notify-failure:
	./local-notify.sh notify_build_failure

.PHONY: notify-deploy
notify-deploy:
	./local-notify.sh notify_deployment_complete
MAKEFILE
EOF

    chmod +x local-notify.sh
}
```

## 🎯 CI/CD 最佳实践总结

### 实施建议
1. **渐进式实施**：从简单的 CI 开始，逐步添加 CD 功能
2. **环境分离**：明确区分开发、测试、生产环境
3. **自动化测试**：建立完善的测试体系
4. **快速反馈**：优化流水线执行时间
5. **安全控制**：保护敏感信息和生产环境

### 关键成功因素
- 团队协作和沟通
- 持续改进和优化
- 监控和度量
- 文档和知识共享
- 工具链的稳定性

---

> **💡 提示**: CI/CD 集成是一个持续演进的过程，需要根据团队需求和项目特点不断调整优化。

**版本**: v1.0.0  
**更新时间**: 2026年2月6日