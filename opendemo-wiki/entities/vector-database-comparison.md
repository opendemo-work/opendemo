---
title: Vector Database Comparison
summary: Comparison of mainstream vector databases (Milvus, Qdrant, Pinecone, Weaviate, Chroma) performance and use cases.
updated: 2026-06-05
tags:
  - llm
  - application
  - vector-database-comparison
sources:
  - /ai-ml/llm/application/vector-database-comparison/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Vector Database Comparison

Comparison of mainstream vector databases including Milvus, Qdrant, Pinecone, Weaviate, and Chroma.

## Database Comparison

| Database | Open Source | Deployment | Index Algorithm | Scale | Features |
|----------|-------------|------------|-----------------|-------|----------|
| Milvus | ✓ | Self-hosted/K8s | HNSW/IVF | Billion | Full-featured, industrial |
| Qdrant | ✓ | Self-hosted/Docker | HNSW/IVF | 100M | High performance, Rust |
| Pinecone | ✗ | Cloud | Proprietary | Any | Managed, easy start |
| Weaviate | ✓ | Self-hosted/K8s | HNSW | 10M | Strong hybrid search |
| Chroma | ✓ | Local/Server | HNSW | 1M | Lightweight, simple |
| FAISS | ✓ | Library | IVF/HNSW | 10M | Fastest, self-managed |

## Key Implementations

### Unified Interface

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

### Milvus Implementation

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

### Qdrant Implementation

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

### Chroma Implementation

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

## Related Cases

- [[entities/rag-retrieval-optimization]] - RAG Retrieval Optimization
- [[entities/rag-chunking-strategies]] - RAG Chunking Strategies
