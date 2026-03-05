# 向量数据库与RAG

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **数据库**: Milvus, Weaviate, Qdrant

---

## 概述

向量数据库是RAG(检索增强生成)架构的核心组件，用于存储和检索文本嵌入向量，实现语义搜索和知识检索。

---

## Milvus部署

### 集群部署

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: milvus
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: milvus
  namespace: milvus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: milvus
  template:
    metadata:
      labels:
        app: milvus
    spec:
      containers:
        - name: milvus
          image: milvusdb/milvus:v2.3.0
          args:
            - milvus
            - run
            - standalone
          ports:
            - containerPort: 19530
              name: grpc
            - containerPort: 9091
              name: metrics
          resources:
            limits:
              memory: 8Gi
              cpu: 4
            requests:
              memory: 4Gi
              cpu: 2
          volumeMounts:
            - name: milvus-storage
              mountPath: /var/lib/milvus
      volumes:
        - name: milvus-storage
          persistentVolumeClaim:
            claimName: milvus-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: milvus
  namespace: milvus
spec:
  selector:
    app: milvus
  ports:
    - port: 19530
      name: grpc
      targetPort: 19530
    - port: 9091
      name: metrics
      targetPort: 9091
```

---

## RAG应用部署

### RAG服务

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-service
  namespace: llm-serving
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rag-service
  template:
    metadata:
      labels:
        app: rag-service
    spec:
      containers:
        - name: rag
          image: rag-service:latest
          ports:
            - containerPort: 8000
          env:
            - name: MILVUS_HOST
              value: "milvus.milvus.svc.cluster.local"
            - name: MILVUS_PORT
              value: "19530"
            - name: EMBEDDING_MODEL
              value: "BAAI/bge-large-zh-v1.5"
            - name: LLM_ENDPOINT
              value: "http://vllm-service:8000"
          resources:
            limits:
              memory: 8Gi
              cpu: 4
            requests:
              memory: 4Gi
              cpu: 2
```

### RAG应用代码示例

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from langchain.llms import VLLM
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5"
)

vectorstore = Milvus(
    embedding_function=embeddings,
    collection_name="knowledge_base",
    connection_args={
        "host": "milvus.milvus.svc.cluster.local",
        "port": "19530"
    }
)

llm = VLLM(
    model="meta-llama/Llama-2-7b-chat-hf",
    endpoint="http://vllm-service:8000"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )
)

def query_rag(question: str) -> str:
    return qa_chain.run(question)
```

---

## Weaviate部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: weaviate
  namespace: vector-db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: weaviate
  template:
    metadata:
      labels:
        app: weaviate
    spec:
      containers:
        - name: weaviate
          image: semitechnologies/weaviate:1.21.0
          env:
            - name: QUERY_DEFAULTS_LIMIT
              value: "25"
            - name: AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED
              value: "true"
            - name: PERSISTENCE_DATA_PATH
              value: "/var/lib/weaviate"
            - name: ENABLE_MODULES
              value: "text2vec-openai,text2vec-cohere,text2vec-huggingface"
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: weaviate-storage
              mountPath: /var/lib/weaviate
      volumes:
        - name: weaviate-storage
          persistentVolumeClaim:
            claimName: weaviate-pvc
```

---

## Qdrant部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qdrant
  namespace: vector-db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: qdrant
  template:
    metadata:
      labels:
        app: qdrant
    spec:
      containers:
        - name: qdrant
          image: qdrant/qdrant:v1.6.0
          ports:
            - containerPort: 6333
              name: http
            - containerPort: 6334
              name: grpc
          volumeMounts:
            - name: qdrant-storage
              mountPath: /qdrant/storage
      volumes:
        - name: qdrant-storage
          persistentVolumeClaim:
            claimName: qdrant-pvc
```

---

## 向量数据库监控

### Prometheus监控

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: milvus-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: milvus
  endpoints:
    - port: metrics
      interval: 30s
```

---

## 相关案例

- [LLM推理服务](../17-llm-inference-serving/) - 模型推理
- [LLM数据管道](../15-llm-data-pipeline/) - 数据处理
- [AI平台可观测性](../13-ai-platform-observability/) - 监控体系

---

**维护者**: OpenDemo Team | **许可证**: MIT
