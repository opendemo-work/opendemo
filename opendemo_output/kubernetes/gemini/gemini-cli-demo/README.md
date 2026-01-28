# Gemini CLI 基础演示

## 概述

Gemini CLI 是一个命令行工具，用于与 Google 的 Gemini AI 模型进行交互。Gemini 是 Google 开发的多模态AI模型，能够处理文本、图像、音频等多种类型的数据。Gemini CLI 提供了在终端中直接访问和使用 Gemini 模型的能力，支持多种功能和应用场景。

## 架构

Gemini CLI 架构主要包括以下几个组件：

- **CLI 客户端**：命令行界面，处理用户输入和显示输出
- **API 适配器**：与 Gemini API 进行通信
- **认证管理器**：处理 API 密钥和身份验证
- **内容处理器**：处理不同类型的内容（文本、图片、音频等）

## 快速开始

### 环境准备

确保您的系统满足以下要求：
- Node.js v16+ 或 Python 3.8+
- 有效的 Google Cloud 项目
- Gemini API 密钥

### 安装 Gemini CLI

```bash
# 使用 npm 安装
npm install -g @google/generative-ai-cli

# 或者使用 Python 安装
pip install google-generativeai-cli
```

### 配置 API 密钥

```bash
# 设置 API 密钥
export GEMINI_API_KEY="your-api-key-here"

# 或者通过配置命令
gemini config set api_key "your-api-key-here"
```

### 基础使用

```bash
# 简单查询
gemini generate "Hello, how are you?"

# 使用特定模型
gemini generate --model gemini-pro "Explain quantum computing in simple terms"

# 处理图片
gemini generate -i image.jpg "Describe this image"

# 交互模式
gemini chat
```

## 在 Kubernetes 中部署 Gemini CLI 服务

### 1. 创建命名空间

```bash
kubectl create namespace gemini-system
```

### 2. 部署 Gemini CLI 服务

```bash
kubectl apply -f gemini-deployment.yaml
```

### 3. 检查部署状态

```bash
kubectl get pods -n gemini-system
kubectl get svc -n gemini-system
```

## 示例配置

### Gemini CLI 服务部署配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gemini-cli
  namespace: gemini-system
  labels:
    app: gemini-cli
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gemini-cli
  template:
    metadata:
      labels:
        app: gemini-cli
    spec:
      containers:
      - name: gemini-cli
        image: node:18-alpine
        command: ["/bin/sh", "-c"]
        args:
        - |
          # 安装 Gemini CLI
          npm install -g @google/generative-ai-cli
          
          # 保持容器运行
          tail -f /dev/null
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-secret
              key: api-key
        - name: GOOGLE_CLOUD_PROJECT
          value: "your-project-id"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        volumeMounts:
        - name: gemini-config
          mountPath: /root/.config/gemini
      volumes:
      - name: gemini-config
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: gemini-cli-service
  namespace: gemini-system
spec:
  selector:
    app: gemini-cli
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: v1
kind: Secret
metadata:
  name: gemini-secret
  namespace: gemini-system
type: Opaque
data:
  api-key: <base64-encoded-api-key>
```

### Gemini 任务配置

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: gemini-task
  namespace: gemini-system
spec:
  template:
    spec:
      containers:
      - name: gemini-task
        image: node:18-alpine
        command: ["/bin/sh", "-c"]
        args:
        - |
          # 安装依赖
          npm install -g @google/generative-ai-cli
          
          # 运行 Gemini 命令
          echo "Running Gemini task..."
          gemini generate "Summarize the benefits of Kubernetes" > /tmp/output.txt
          
          # 输出结果
          cat /tmp/output.txt
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-secret
              key: api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      restartPolicy: Never
  backoffLimit: 4
```

## 高级功能

### 多模态支持

Gemini 支持多种输入类型：

```bash
# 文本 + 图片
gemini generate -i image.jpg "What's happening in this image?"

# 音频处理（如果模型支持）
gemini generate -a audio.mp3 "Transcribe this audio"

# 视频处理（如果模型支持）
gemini generate -v video.mp4 "Summarize this video"
```

### 对话模式

```bash
# 开始对话
gemini chat

# 或者使用特定模型
gemini chat --model gemini-pro-vision
```

### 模型选择

```bash
# 使用不同模型
gemini generate --model gemini-pro "Advanced query"
gemini generate --model gemini-pro-vision "Vision-based query"
```

## 配置选项

### 基础配置

```bash
# 查看当前配置
gemini config list

# 设置默认模型
gemini config set model gemini-pro

# 设置输出格式
gemini config set output_format json
```

### 高级参数

```bash
# 设置温度参数
gemini generate --temperature 0.7 "Creative response"

# 设置最大输出长度
gemini generate --max-output-tokens 1024 "Long-form content"
```

## 使用场景

1. **自动化内容生成**：批量生成文章、摘要或翻译
2. **数据分析**：处理和分析大量文本数据
3. **代码辅助**：生成代码、解释代码或重构代码
4. **多模态处理**：处理图像、文本等混合内容
5. **API 集成**：与其他系统集成进行AI处理

## 最佳实践

- 保护 API 密钥安全，使用 Kubernetes Secrets 存储
- 合理设置资源限制以优化成本
- 使用适当的模型以平衡性能和成本
- 实施适当的错误处理和重试机制
- 监控 API 使用量和成本

## 故障排除

### API 密钥错误

检查密钥是否正确设置：

```bash
kubectl get secrets -n gemini-system
kubectl describe secret gemini-secret -n gemini-system
```

### 模型访问问题

确认您的 API 密钥有访问所需模型的权限：

```bash
# 检查模型列表
gemini models list
```

## 扩展阅读

- [Gemini API 官方文档](https://ai.google.dev/tutorials/get_started)
- [Google AI SDK](https://github.com/google/generative-ai-js)
- [Google Cloud 认证指南](https://cloud.google.com/docs/authentication)
- [Kubernetes 最佳实践](https://cloud.google.com/kubernetes-engine/docs/best-practices)