<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Vector Database Comparison

> 本案例对比主流向量数据库（Milvus、Qdrant、Pinecone、Weaviate、Chroma）的性能、特性与适用场景。

## 📊 主流向量数据库对比

| 数据库 | 开源 | 部署方式 | 索引算法 | 适用规模 | 特点 |
|--------|------|----------|----------|----------|------|
| Milvus | ✓ | 自托管/K8s | HNSW/IVF | 十亿级 | 功能全面，工业级 |
| Qdrant | ✓ | 自托管/Docker | HNSW/IVF | 亿级 | 高性能，Rust实现 |
| Pinecone | ✗ | 云服务 | 私有 | 任意规模 | 免运维，快速上手 |
| Weaviate | ✓ | 自托管/K8s | HNSW | 千万级 | 混合搜索强 |
| Chroma | ✓ | 本地/Server | HNSW | 百万级 | 轻量，简单 |
| FAISS | ✓ | 库集成 | IVF/HNSW | 千万级 | 最快，需自建 |

## 💻 核心实现

### 统一接口封装

```python
from abc import ABC, abstractmethod

class VectorStore(ABC):
    @abstractmethod
    def add_documents(self, texts, embeddings, metadatas=None):
        pass
    
    @abstractmethod
    def similarity_search(self, query_embedding, k=5):
        pass
    
    @abstractmethod
    def delete(self, ids=None):
        pass
```

### Milvus 实现

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

class MilvusStore(VectorStore):
    def __init__(self, host="localhost", port="19530", collection_name="default"):
        connections.connect(host=host, port=port)
        self.collection_name = collection_name
        self.collection = None
    
    def create_collection(self, dimension=1536):
        if utility.collection_exists(self.collection_name):
            self.collection = Collection(self.collection_name)
            return
        
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=65535)
        ]
        schema = CollectionSchema(fields=fields)
        self.collection = Collection(name=self.collection_name, schema=schema)
        
        index_params = {"index_type": "HNSW", "params": {"M": 16, "efConstruction": 200}, "metric_type": "L2"}
        self.collection.create_index("embedding", index_params)
    
    def add_documents(self, texts, embeddings, metadatas=None):
        import json
        entities = [
            embeddings,
            texts,
            [json.dumps(m) if m else "{}" for m in (metadatas or [None] * len(texts))]
        ]
        self.collection.insert(entities)
        self.collection.flush()
    
    def similarity_search(self, query_embedding, k=5):
        search_params = {"metric_type": "L2", "params": {"ef": 200}}
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=k
        )
        return results[0]
```

### Qdrant 实现

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class QdrantStore(VectorStore):
    def __init__(self, host="localhost", port=6333, collection_name="default"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
    
    def create_collection(self, dimension=1536):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
        )
    
    def add_documents(self, texts, embeddings, metadatas=None):
        points = [
            PointStruct(id=i, vector=emb, payload={"text": text, "metadata": meta})
            for i, (text, emb, meta) in enumerate(zip(texts, embeddings, metadatas or [{}]*len(texts)))
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)
    
    def similarity_search(self, query_embedding, k=5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k
        )
        return results
```

### Chroma 实现

```python
import chromadb
from chromadb.config import Settings

class ChromaStore(VectorStore):
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = None
    
    def create_collection(self, name="default"):
        self.collection = self.client.get_or_create_collection(name=name)
    
    def add_documents(self, texts, embeddings, metadatas=None):
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=[f"doc_{i}" for i in range(len(texts))]
        )
    
    def similarity_search(self, query_embedding, k=5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results["documents"][0] if results["documents"] else []
```

## 📋 性能基准测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 运行基准测试
python vector_db/benchmark.py --num-vectors=100000 --dimension=1536

# 测试不同索引
python vector_db/benchmark.py --index-type=hnsw,ivf
```

## 📋 命令速查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# Milvus
docker run -d -p 19530:19530 milvusdb/milvus

# Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# Chroma
pip install chromadb

# 运行对比
python vector_db/compare.py
```

## 🔗 相关案例

- `rag-fundamentals` - RAG 基础
- `embedding-model-selection` - Embedding 模型选择
- `hybrid-search` - 混合搜索

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
python code/main.py
```
