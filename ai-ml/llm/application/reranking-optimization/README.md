# Reranking 优化

> 本案例详解 RAG 中重排序技术，包括 Cross-Encoder、Diversity Reranking、LLM-based Reranking 等策略。

## 📐 Reranking 流程

```
Initial Retrieval (Top-100) → Reranking → Final Top-K
        │                       │
        ▼                       ▼
   粗排阶段                 精排阶段
   ANN/BM25                Cross-Encoder
```

## 核心策略

### 1. Cross-Encoder Reranking

| 模型 | 速度 | 精度 | 适用场景 |
|------|------|------|----------|
| ms-marco-MiniLM | 快 | 中 | 实时系统 |
| ms-marco-MiniLM-L-12 | 中 | 高 | 标准场景 |
| bge-reranker | 慢 | 极高 | 高精度场景 |

### 2. Diversity Reranking

```python
def mmr_rerank(query, docs, k=5, lambda_param=0.5):
    selected = []
    remaining = docs.copy()
    
    while len(selected) < k and remaining:
        best_score = -float('inf')
        best_doc = None
        
        for doc in remaining:
            relevance = cosine_similarity(query, doc.embedding)
            diversity = min([cosine_similarity(doc.embedding, s.embedding) 
                          for s in selected]) if selected else 1
            
            score = lambda_param * relevance + (1 - lambda_param) * diversity
            
            if score > best_score:
                best_score = score
                best_doc = doc
        
        selected.append(best_doc)
        remaining.remove(best_doc)
    
    return selected
```

## 💻 核心实现

### Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-12-v2"):
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query, documents, top_k=5):
        pairs = [[query, doc.page_content] for doc in documents]
        scores = self.model.predict(pairs)
        
        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [doc for doc, _ in ranked[:top_k]]
```

### LLM-based Reranking

```python
class LLMReranker:
    def __init__(self, llm):
        self.llm = llm
    
    def rerank(self, query, documents, top_k=5):
        doc_list = "\n".join(
            [f"{i+1}. {doc.page_content[:200]}..." 
             for i, doc in enumerate(documents)]
        )
        
        prompt = f"""Rank these documents by relevance to the query.
        Query: {query}
        
        Documents:
        {doc_list}
        
        Return top {top_k} document numbers in order (e.g., 1,3,5):"""
        
        result = self.llm.invoke(prompt)
        indices = self._parse_indices(result)
        return [documents[i] for i in indices if i < len(documents)]
```

## 📊 评估指标

| 指标 | 说明 | 计算方式 |
|------|------|----------|
| NDCG@K | 折损累积增益 | 标准化DCG |
| MRR | 平均倒数排名 | 1/rank |
| MAP | 平均精度 | Precision@K |

## 📋 命令速查

```bash
pip install sentence-transformers rank-bm25

# 运行重排序对比
python reranking/compare.py

# 测试 Cross-Encoder
python reranking/cross_encoder.py
```

## 🔗 相关案例

- `rag-fundamentals` - RAG 基础
- `rag-retrieval-optimization` - 检索优化
- `hybrid-search` - 混合搜索
