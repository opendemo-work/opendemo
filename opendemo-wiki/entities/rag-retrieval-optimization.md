---
title: RAG Retrieval Optimization
summary: Optimize RAG retrieval with query rewriting, multi-representation indexing, and adaptive retrieval strategies.
updated: 2026-06-05
tags:
  - llm
  - application
  - rag-retrieval-optimization
sources:
  - /ai-ml/llm/application/rag-retrieval-optimization/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# RAG Retrieval Optimization

Optimizes the retrieval stage of RAG systems using query rewriting, multi-representation indexing, and adaptive retrieval.

## Core Strategies

### Query Rewriting

```
User Query → Query Expansion → HyDE → Multi-angle Query → Parallel Retrieval
```

### Multi-Representation Indexing

```
Document → Summary Embedding → Summary Vector Index
         → Chunk Embedding → Chunk-level Vector Index
```

### Adaptive Retrieval

| Strategy | Trigger | Method |
|----------|---------|--------|
| Self-RAG | Low confidence | On-demand retrieval |
| FLARE | Unknown tokens | Proactive retrieval |
| Corrective-RAG | Hallucination detected | Fallback retrieval |

## Key Implementations

### Query Rewriting

```python
class QueryRewriter:
    def __init__(self, llm):
        self.llm = llm
    
    def rewrite(self, query):
        prompt = f"""Rewrite this query to improve retrieval:
        Original: {query}
        Rewrite:"""
        return self.llm.invoke(prompt)
    
    def expand(self, query):
        expansion_prompt = f"""Generate 3 different versions of this query:
        Query: {query}
        Variations:"""
        return self.llm.invoke(expansion_prompt).split('\n')
    
    def hyde(self, query):
        hyde_prompt = f"""Write a hypothetical document that answers:
        {query}
        Document:"""
        return self.llm.invoke(hyde_prompt)
```

### Adaptive Retrieval

```python
class AdaptiveRetriever:
    def __init__(self, base_retriever, llm):
        self.retriever = base_retriever
        self.llm = llm
    
    def should_retrieve(self, context, question):
        confidence_prompt = f"""Rate confidence that context answers:
        Question: {question}
        Context: {context}
        Confidence (0-1):"""
        score = float(self.llm.invoke(confidence_prompt))
        return score < 0.7
    
    def retrieve_if_needed(self, context, question):
        if self.should_retrieve(context, question):
            return self.retriever.get_relevant_docs(question)
        return []
```

## Related Cases

- [[entities/rag-chunking-strategies]] - RAG Chunking Strategies
- [[entities/reranking-optimization]] - Reranking Optimization
