---
title: RAG Chunking Strategies
summary: Document chunking techniques for RAG including fixed window, semantic, parent-child, and LLM-assisted strategies.
updated: 2026-06-05
tags:
  - llm
  - application
  - rag-chunking-strategies
sources:
  - /ai-ml/llm/application/rag-chunking-strategies/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# RAG Chunking Strategies

Document chunking techniques for RAG systems covering fixed window, semantic, parent-child, and LLM-assisted strategies.

## Strategy Comparison

| Strategy | Chunk Size | Context Preservation | Use Case |
|----------|------------|---------------------|----------|
| Fixed Window | 512 tokens | Low | General |
| Semantic | Variable | High | QA Systems |
| Parent-Child | Variable | Very High | Complex Documents |
| LLM-Assisted | Variable | Highest | Precise QA |

## Key Implementations

### Fixed Window Chunking

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def fixed_chunking(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)
```

### Semantic Chunking

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import OpenAIEmbeddings

def semantic_chunking(documents, threshold=0.5):
    splitter = SemanticChunker(
        OpenAIEmbeddings(),
        breakpoint_threshold_threshold=threshold
    )
    return splitter.split_documents(documents)
```

### Parent-Child Strategy

```python
class ParentChunker:
    def __init__(self, parent_chunk_size=4000, child_chunk_size=500):
        self.parent_size = parent_chunk_size
        self.child_size = child_chunk_size
    
    def chunk_hierarchy(self, document):
        parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.parent_size
        )
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.child_size
        )
        
        parent_chunks = parent_splitter.split_documents([document])
        child_chunks = child_splitter.split_documents([document])
        
        return {
            "parents": parent_chunks,
            "children": child_chunks,
            "mapping": self._create_mapping(parent_chunks, child_chunks)
        }
```

## Selection Guide

```
Long/Technical Docs → Parent-Child / Semantic
Short Docs/FAQ → Fixed Window / Sentence-level
Tables/Structured → Special handling
```

## Related Cases

- [[entities/rag-retrieval-optimization]] - RAG Retrieval Optimization
- [[entities/reranking-optimization]] - Reranking Optimization
