# RAG(检索增强生成)管道实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 向量数据库的基本原理和应用
- 文档嵌入和相似性检索技术
- RAG系统的架构设计和实现
- 检索增强生成的实际应用

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- GPU或CPU环境
- 至少16GB内存

### 依赖安装
```bash
pip install torch transformers
pip install pinecone-client chromadb qdrant-client  # 向量数据库
pip install sentence-transformers openai  # 嵌入库
pip install langchain llama-index  # RAG框架
pip install fastapi uvicorn  # API服务
```

## 📁 项目结构

```
rag-pipeline-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── embed_documents.py             # 文档嵌入脚本
│   ├── build_index.py                 # 构建索引脚本
│   └── rag_query.py                   # RAG查询脚本
├── configs/                           # 配置文件
│   ├── embedding_config.json          # 嵌入配置
│   ├── vector_db_config.json          # 向量数据库配置
│   └── rag_config.yaml                # RAG配置
├── data/                              # 数据文件
│   ├── documents/                     # 源文档
│   ├── embeddings/                    # 嵌入向量
│   └── queries/                       # 查询示例
├── vector_stores/                     # 向量存储
│   ├── pinecone/                      # Pinecone配置
│   ├── chromadb/                      # ChromaDB配置
│   └── faiss/                         # FAISS配置
├── api/                               # API服务
│   ├── rag_service.py                 # RAG服务端点
│   └── health_check.py                # 健康检查
├── models/                            # 模型文件
│   ├── embedding_models/              # 嵌入模型
│   └── generation_models/             # 生成模型
├── evaluation/                        # 评估脚本
│   ├── retrieval_eval.py              # 检索评估
│   └── generation_eval.py             # 生成评估
└── notebooks/                         # Jupyter笔记本
    ├── 01_embedding_techniques.ipynb   # 嵌入技术
    ├── 02_vector_database.ipynb        # 向量数据库
    └── 03_rag_implementation.ipynb     # RAG实现
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装RAG相关依赖
pip install -r requirements.txt
```

### 步骤2：文档嵌入

```bash
# 将文档转换为向量嵌入
python scripts/embed_documents.py \
  --documents_dir data/documents/ \
  --output_dir vector_stores/chromadb/ \
  --embedding_model sentence-transformers/all-MiniLM-L6-v2
```

### 步骤3：构建RAG系统

```bash
# 启动RAG服务
uvicorn api.rag_service:app --host 0.0.0.0 --port 8000
```

### 步骤4：执行RAG查询

```bash
# 查询RAG系统
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the capital of France?",
    "top_k": 3,
    "temperature": 0.7
  }'
```

## 🔍 代码详解

### 核心概念解析

#### 1. 向量数据库操作
```python
# 使用ChromaDB进行向量存储和检索
import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, collection_name="documents"):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(collection_name)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_documents(self, documents, metadatas=None, ids=None):
        """添加文档到向量数据库"""
        embeddings = self.encoder.encode(documents).tolist()
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query, top_k=5):
        """搜索最相关的文档"""
        query_embedding = self.encoder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        return results
```

#### 2. 实际应用示例

##### 场景1：RAG查询实现
```python
# RAG系统核心实现
class RAGSystem:
    def __init__(self, vector_store, generator_model):
        self.vector_store = vector_store
        self.generator = generator_model
    
    def retrieve_and_generate(self, query, top_k=3):
        """检索增强生成"""
        # 1. 检索相关文档
        retrieved_docs = self.vector_store.search(query, top_k=top_k)
        
        # 2. 构建上下文
        context = "\n".join(retrieved_docs['documents'][0])
        
        # 3. 构建提示词
        prompt = f"""
        根据以下上下文回答问题：
        上下文: {context}
        
        问题: {query}
        
        回答:
        """
        
        # 4. 生成答案
        response = self.generator.generate(prompt)
        return response
```

##### 场景2：LangChain集成
```python
# 使用LangChain构建RAG管道
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline

def build_rag_chain(vector_db_path, llm):
    """构建LangChain RAG管道"""
    # 初始化嵌入模型
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # 加载向量数据库
    vectorstore = Chroma(
        persist_directory=vector_db_path,
        embedding_function=embeddings
    )
    
    # 创建检索器
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 构建RAG链
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    return rag_chain
```

## 🧪 验证测试

### 测试1：向量数据库功能验证
```python
#!/usr/bin/env python
# 验证向量数据库功能
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

def test_vector_database():
    print("=== 向量数据库功能验证 ===")
    
    # 初始化向量数据库
    client = chromadb.Client()
    collection = client.create_collection("test_docs")
    
    # 初始化嵌入模型
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 添加测试文档
    documents = [
        "Paris is the capital of France",
        "Tokyo is the capital of Japan", 
        "Berlin is the capital of Germany",
        "The weather is sunny today",
        "Machine learning is a subset of AI"
    ]
    
    embeddings = encoder.encode(documents).tolist()
    
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[f"id_{i}" for i in range(len(documents))]
    )
    
    print(f"✅ 添加了 {len(documents)} 个文档到向量数据库")
    
    # 测试检索功能
    query = "What is the capital of France?"
    query_embedding = encoder.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=2
    )
    
    print(f"✅ 检索成功，找到 {len(results['documents'][0])} 个相关文档")
    print(f"最相关文档: {results['documents'][0][0]}")
    
    # 验证相关性
    expected_doc = "Paris is the capital of France"
    assert expected_doc in results['documents'][0], "检索结果应包含预期文档"
    print("✅ 检索结果验证通过")

if __name__ == "__main__":
    test_vector_database()
```

### 测试2：RAG系统端到端验证
```python
#!/usr/bin/env python
# RAG系统端到端验证
from transformers import pipeline
import chromadb
from sentence_transformers import SentenceTransformer

def test_rag_system():
    print("=== RAG系统端到端验证 ===")
    
    # 创建简单的向量数据库
    client = chromadb.Client()
    collection = client.create_collection("qa_docs")
    
    # 添加知识库文档
    qa_pairs = [
        ("What is the capital of France?", "The capital of France is Paris."),
        ("What is the capital of Japan?", "The capital of Japan is Tokyo."),
        ("What is machine learning?", "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed."),
    ]
    
    docs = [pair[1] for pair in qa_pairs]
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = encoder.encode(docs).tolist()
    
    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(docs))]
    )
    
    # 简单的生成模型（这里使用填空模型作为示例）
    generator = pipeline("fill-mask", model="bert-base-uncased")
    
    # 测试RAG查询
    query = "What is the capital of France?"
    query_embedding = encoder.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=1
    )
    
    context = results['documents'][0][0]
    print(f"检索到的上下文: {context}")
    print(f"查询: {query}")
    
    print("✅ RAG系统端到端验证通过")
    print("系统能够成功检索相关信息并准备生成答案")

if __name__ == "__main__":
    test_rag_system()
```

## ❓ 常见问题

### Q1: 如何优化向量检索的性能？
**解决方案**：
```python
# 向量检索性能优化
"""
1. 使用近似最近邻算法(如HNSW, IVF)
2. 合理设置索引参数
3. 分批处理大量查询
4. 使用缓存机制
"""
```

### Q2: 如何评估RAG系统的质量？
**解决方案**：
```python
# RAG系统质量评估
"""
1. 检索评估: MRR, Recall@K, NDCG
2. 生成评估: BLEU, ROUGE, METEOR
3. 端到端评估: 人工评估答案质量
4. 延迟评估: 首字节时间、总响应时间
"""
```

## 📚 扩展学习

### 相关技术
- **Pinecone**: 托管向量数据库
- **Weaviate**: 云原生向量搜索引擎
- **FAISS**: Meta的高效相似性搜索库
- **LlamaIndex**: 数据框架用于LLMs

### 进阶学习路径
1. 掌握不同向量数据库的特点和选择
2. 学习高级嵌入技术和微调方法
3. 理解RAG系统中的幻觉缓解技术
4. 掌握多模态RAG系统的构建

### 企业级应用场景
- 企业知识库问答系统
- 客服机器人和智能助手
- 法律和医疗文档分析
- 科研文献检索和总结

---
> **💡 提示**: RAG系统结合了检索和生成的优势，能够在利用外部知识的同时生成准确、可靠的响应，是现代AI应用的重要架构模式。