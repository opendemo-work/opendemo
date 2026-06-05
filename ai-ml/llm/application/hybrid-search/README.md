# Hybrid Search 混合搜索

> 本案例详解 RAG 中的混合搜索技术，结合向量检索和关键词检索

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Hybrid Search 架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Query: "Python programming best practices"                     │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Query Processing                           │   │
│  │  ┌─────────────────┐  ┌─────────────────┐             │   │
│  │  │ Dense Embedding │  │ Keyword Extract │             │   │
│  │  │   (向量化)       │  │    (分词)       │             │   │
│  │  └─────────────────┘  └─────────────────┘             │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Retrieval                              │   │
│  │  ┌─────────────────┐  ┌─────────────────┐             │   │
│  │  │ Vector Search   │  │  BM25 Search   │             │   │
│  │  │ (语义相似度)    │  │  (关键词匹配)   │             │   │
│  │  └────────┬────────┘  └────────┬────────┘             │   │
│  │           │                    │                       │   │
│  │           └──────────┬─────────┘                       │   │
│  │                      ▼                                  │   │
│  │              ┌─────────────┐                          │   │
│  │              │   RRF Fusion │  ← Reciprocal Rank Fusion│   │
│  │              └─────────────┘                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                      │                                         │
│                      ▼                                         │
│              Top-K Results                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### RRF 融合

```python
def reciprocal_rank_fusion(results_list, k=60):
    """RRF 融合多个检索结果"""
    scores = {}
    
    for results in results_list:
        for rank, doc in enumerate(results):
            doc_id = doc['id']
            # RRF 分数
            score = 1 / (k + rank + 1)
            scores[doc_id] = scores.get(doc_id, 0) + score
    
    # 排序
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs
```

## 🔗 相关案例

- `rag-fundamentals` - RAG 基础
- `reranking-optimization` - 重排序优化
- `embedding-model-selection` - Embedding 模型选择
