<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# RAG 基础架构

> 本案例详解 RAG (Retrieval-Augmented Generation) 的核心架构、检索策略和实现方案

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAG 完整架构                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Query                                                      │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Query Processing                         │   │
│  │   • Query Rewriting                                      │   │
│  │   • Query Expansion                                      │   │
│  │   • HyDE (Hypothetical Document Embedding)               │   │
│  └─────────────────────────────────────────────────────────┘   │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Retrieval                             │   │
│  │                                                          │   │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │   │
│  │   │ Dense      │    │ Sparse     │    │ Hybrid     │ │   │
│  │   │ Retrieval  │    │ Retrieval  │    │ Retrieval  │ │   │
│  │   │ (Vector)   │    │ (BM25)     │    │            │ │   │
│  │   └──────┬──────┘    └──────┬──────┘    └──────┬────┘ │   │
│  │          │                  │                  │       │   │
│  │          └──────────────────┼──────────────────┘       │   │
│  │                             ▼                             │   │
│  │                    ┌─────────────┐                        │   │
│  │                    │   Reranker  │                        │   │
│  │                    └─────────────┘                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Context Augmentation                    │   │
│  │                                                          │   │
│  │   Retrieved Chunks + User Query → Prompt Template        │   │
│  └─────────────────────────────────────────────────────────┘   │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      LLM Generation                       │   │
│  │                                                          │   │
│  │   [Context] + [Query] → [Generated Answer]               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

向量数据库检索流程:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Document Collection                                             │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                                │
│  │  Chunking   │  ←─ 滑动窗口 / 句子 / 段落                      │
│  └─────────────┘                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                                │
│  │ Embedding   │  ←─ OpenAI / BGE / E5 / Jina                  │
│  └─────────────┘                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                                │
│  │  Vector DB  │  ←─ Milvus / Qdrant / Pinecone / Weaviate    │
│  │  Indexing   │                                                │
│  └─────────────┘                                                │
│       │                                                         │
│       ▼                                                         │
│  Query = "What is Python?"                                       │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────┐                                                │
│  │ ANN Search  │                                                │
│  └─────────────┘                                                │
│       │                                                         │
│       ▼                                                         │
│  Top-K Chunks                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. RAG 工作流程

```
1. Indexing (离线)
   Document → Chunking → Embedding → Vector DB

2. Retrieval (在线)
   Query → Embedding → Vector Search → Top-K Chunks

3. Generation (在线)
   Query + Chunks → LLM → Answer
```

### 2. 文档分块策略

| 策略 | 块大小 | 适用场景 | 优缺点 |
|------|--------|----------|--------|
| 固定窗口 | 512 tokens | 通用 | 简单，可能切断语义 |
| 句子级 | 1 句子 | 精确匹配 | 丢失上下文 |
| 段落级 | 1 段落 | 长文档 | 上下文完整 |
| 滑动窗口 | 可重叠 | 平衡 | 推荐默认 |

### 3. 检索策略

| 策略 | 原理 | 适用场景 |
|------|------|----------|
| Dense (向量) | 语义相似度 | 语义查询 |
| Sparse (BM25) | 关键词匹配 | 精确术语 |
| Hybrid | 向量 + BM25 | 两者兼顾 |

## 💻 完整实现

### RAG Pipeline 实现

```python
from langchain.document_loaders import PDFPlumberLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Milvus
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

class RAGPipeline:
    def __init__(self, embedding_model="text-embedding-ada-002"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_documents(self, file_paths: list):
        """加载文档"""
        documents = []
        for path in file_paths:
            if path.endswith('.pdf'):
                loader = PDFPlumberLoader(path)
            elif path.endswith('.txt'):
                loader = TextLoader(path)
            else:
                raise ValueError(f"Unsupported file type: {path}")
            documents.extend(loader.load())
        return documents

    def split_documents(self, documents):
        """分割文档"""
        return self.text_splitter.split_documents(documents)

    def build_index(self, documents, collection_name="rag"):
        """构建向量索引"""
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        self.vectorstore = Milvus.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            collection_name=collection_name,
            connection_args={"host": "localhost", "port": "19530"}
        )
        return self.vectorstore

    def create_retriever(self, search_type="mmr", k=4, fetch_k=10):
        """创建检索器"""
        if self.vectorstore is None:
            raise ValueError("Index not built. Call build_index first.")

        if search_type == "similarity":
            return self.vectorstore.as_retriever(
                search_kwargs={"k": k}
            )
        elif search_type == "mmr":
            return self.vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={"k": k, "fetch_k": fetch_k}
            )
        else:
            raise ValueError(f"Unknown search type: {search_type}")

    def create_hybrid_retriever(self, documents, k=4):
        """创建混合检索器"""
        bm25_retriever = BM25Retriever.from_texts(
            [doc.page_content for doc in documents]
        )
        bm25_retriever.k = k

        vector_retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})

        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            weights=[0.3, 0.7]
        )
        return ensemble_retriever

    def query(self, question: str, retriever, use_compression=False):
        """执行 RAG 查询"""
        if use_compression:
            compressor = LLMChainExtractor.from_llm(OpenAI(temperature=0))
            retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=retriever
            )

        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

        result = qa_chain({"query": question})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"]
        }


def example_usage():
    """使用示例"""
    rag = RAGPipeline()

    # 1. 加载文档
    documents = rag.load_documents(["./docs/manual.pdf", "./docs/faq.txt"])

    # 2. 分割文档
    chunks = rag.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # 3. 构建索引
    rag.build_index(chunks)

    # 4. 创建检索器 (使用 MMR)
    retriever = rag.create_retriever(search_type="mmr", k=4, fetch_k=10)

    # 5. 查询
    result = rag.query("How do I reset the device?", retriever)
    print(f"Answer: {result['answer']}")
    print(f"Sources: {[doc.metadata for doc in result['source_documents']]}")
```

### 高级检索：Hybrid Search + Rerank

```python
from sentence_transformers import CrossEncoder
from rank_bm25 import BM25Okapi

class AdvancedRAGPipeline:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')
        self.vectorstore = None

    def hybrid_search_with_rerank(
        self, 
        query: str, 
        vector_results: list, 
        bm25_results: list, 
        top_k=5
    ):
        """混合搜索 + 重排序"""
        
        # 1. 融合向量和 BM25 结果
        all_chunks = []
        seen = set()
        
        for chunk, score in vector_results:
            if chunk not in seen:
                all_chunks.append(chunk)
                seen.add(chunk)
                
        for chunk, score in bm25_results:
            if chunk not in seen:
                all_chunks.append(chunk)
                seen.add(chunk)

        # 2. Cross-Encoder 重排序
        pairs = [[query, chunk] for chunk in all_chunks]
        scores = self.cross_encoder.predict(pairs)

        # 3. 按分数排序
        ranked_results = sorted(
            zip(all_chunks, scores), 
            key=lambda x: x[1], 
            reverse=True
        )

        return ranked_results[:top_k]

    def query_with_hybrid_rerank(self, question: str, top_k=5):
        """完整的混合搜索 + 重排序查询"""
        # 向量搜索
        vector_results = self.vectorstore.similarity_search_with_score(
            question, k=20
        )

        # BM25 搜索
        bm25_results = self.bm25_index.get_scores(question)
        top_bm25 = sorted(
            enumerate(bm25_results), 
            key=lambda x: x[1], 
            reverse=True
        )[:20]

        # 融合 + 重排序
        results = self.hybrid_search_with_rerank(
            question, 
            vector_results, 
            top_bm25,
            top_k=top_k
        )

        return results
```

## 📊 RAG 评估指标

| 指标 | 说明 | 评估方式 |
|------|------|----------|
| Context Precision | 上下文块的相关性 | RAGAS |
| Answer Faithfulness | 答案对上下文的忠实度 | RAGAS |
| Answer Relevance | 答案与问题的相关性 | RAGAS |
| Hit Rate | Top-K 召回率 | 人工/自动 |

## 📋 命令速查

```bash
# 启动向量数据库
docker run -d -p 19530:19530 milvusdb/milvus

# 安装依赖
pip install langchain openai pymilvus rank-bm25 sentence-transformers

# 运行 RAG 示例
python rag_fundamentals/rag_pipeline.py --documents ./docs

# 运行评估
python rag_fundamentals/evaluate.py --dataset ragas_benchmark.json
```

## 📚 学习要点

1. **Chunk 策略影响大**：选择合适的 chunk size 和 overlap
2. **Embedding 模型关键**：使用针对中文/特定领域优化的模型
3. **Hybrid Search 更鲁棒**：结合向量和关键词检索
4. **Rerank 提升精度**：Cross-Encoder 可以显著提升相关性

## 🔗 相关案例

- `hybrid-search` - 混合搜索实战
- `rag-retrieval-optimization` - 检索优化技术
- `reranking-optimization` - 重排序优化
- `embedding-model-selection` - Embedding 模型选择

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

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

```bash
python code/main.py
```
