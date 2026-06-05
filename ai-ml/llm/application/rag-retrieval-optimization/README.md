# RAG 检索优化

> 本案例详解 RAG 检索阶段的优化技术，包括 query rewriting、multi-representation indexing、adaptive retrieval 等策略。

## 📐 核心优化策略

### 1. Query Rewriting

```
用户原始Query → Query Expansion → HyDE → 多角度Query → 并行检索
```

### 2. Multi-Representation Indexing

```
Document → Summary Embedding → 摘要向量索引
        → Chunk Embedding → 块级向量索引
```

### 3. Adaptive Retrieval

| 策略 | 触发条件 | 检索方式 |
|------|----------|----------|
| Self-RAG | 低置信度 | 按需检索 |
| FLARE | 遇到未知词 | 主动检索 |
| Corrective-RAG | 检测到幻觉 | 回退检索 |

## 💻 核心实现

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
        hypothetical_doc = self.llm.invoke(hyde_prompt)
        return hypothetical_doc
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

## 📋 命令速查

```bash
pip install langchain openai faiss-cpu

# 运行检索优化示例
python rag_optimization/query_rewrite.py

# 测试自适应检索
python rag_optimization/adaptive_retrieval.py
```

## 🔗 相关案例

- `rag-fundamentals` - RAG 基础
- `reranking-optimization` - 重排序优化
- `embedding-model-selection` - Embedding 模型选择
