# Gemini AI Integration

Google Gemini AI模型Kubernetes集成演示。

## Gemini API

```python
import google.generativeai as genai

# 配置API
api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 创建模型
model = genai.GenerativeModel('gemini-pro')

# 生成内容
response = model.generate_content("Explain Kubernetes to a beginner")
print(response.text)

# 多模态
vision_model = genai.GenerativeModel('gemini-pro-vision')
image = PIL.Image.open('architecture.png')
response = vision_model.generate_content(["Describe this diagram", image])
```

## K8s部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gemini-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gemini
  template:
    spec:
      containers:
      - name: api
        image: gemini-service:latest
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: gemini-secret
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Secret
metadata:
  name: gemini-secret
type: Opaque
stringData:
  api-key: <your-api-key>
```

## 学习要点

1. Gemini API调用
2. 多模态应用开发
3. K8s集成部署
4. 提示工程优化
