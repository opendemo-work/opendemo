# ModelScope Model Serving

魔搭社区模型服务化部署演示。

## 什么是ModelScope

阿里巴巴开源的模型即服务(MaaS)平台：

```bash
# 安装ModelScope
pip install modelscope

# 下载模型
from modelscope import snapshot_download
model_dir = snapshot_download('damo/nlp_structbert_siamese-uie_chinese-base')

# 加载使用
from modelscope.pipelines import pipeline
p = pipeline('information-extraction', model=model_dir)
result = p('阿里巴巴是一家科技公司')
```

## K8s部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: modelscope-serving
spec:
  replicas: 2
  selector:
    matchLabels:
      app: modelscope
  template:
    spec:
      containers:
      - name: model
        image: modelscope-serving:latest
        resources:
          limits:
            nvidia.com/gpu: 1
        volumeMounts:
        - name: models
          mountPath: /models
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: model-pvc
```

## 学习要点

1. 模型下载与管理
2. 推理服务封装
3. K8s弹性伸缩
4. 多模型调度
