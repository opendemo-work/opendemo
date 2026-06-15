---
title: Reranking Optimization
summary: RAG重排序技术包括Cross-Encoder、Diversity Reranking、LLM-based Reranking等策略优化检索结果。
updated: 2026-06-05
tags:
  - llm
  - application
  - reranking-optimization
sources:
  - /ai-ml/llm/application/reranking-optimization/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Reranking Optimization

Reranking techniques in RAG including Cross-Encoder, Diversity Reranking, and LLM-based Reranking strategies.

## Reranking Flow

```
Initial Retrieval (Top-100) → Reranking → Final Top-K
         │                       │
         ▼                       ▼
    粗排阶段                   精排阶段
    ANN/BM25                Cross-Encoder
```

## Core Strategies

### Cross-Encoder Reranking

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| ms-marco-MiniLM | Fast | Medium | Real-time |
| ms-marco-MiniLM-L-12 | Medium | High | Standard |
| bge-reranker | Slow | Very High | High Precision |

### Diversity Reranking (MMR)

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

## Key Implementations

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

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| NDCG@K | Normalized Discounted Cumulative Gain |
| MRR | Mean Reciprocal Rank |
| MAP | Mean Average Precision |

## Related Cases

- [[entities/rag-retrieval-optimization]] - RAG Retrieval Optimization
- [[entities/rag-chunking-strategies]] - RAG Chunking Strategies
