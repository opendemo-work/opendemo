---
title: Long-Term Memory
summary: Cross-session persistent knowledge storage and retrieval architecture for AI agents.
updated: 2026-06-05
tags:
  - llm
  - agentic
  - long-term-memory
sources:
  - /ai-ml/llm/agentic/long-term-memory/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# Long-Term Memory

Cross-session persistent knowledge storage and retrieval architecture for AI agents.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Long-Term Memory 架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Session    │───▶│   Memory     │───▶│   Vector     │      │
│  │   Input      │    │   Store      │    │   Index      │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                  │                   │               │
│         ▼                  ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Compress    │◀───│   Retrieve   │◀───│   Semantic   │      │
│  │   & Save     │    │             │    │   Search     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Implementation

### Long-Term Memory Management

```python
import vectorstore

class LongTermMemory:
    def __init__(self, vector_dim=1536):
        self.store = vectorstore.VectorStore(dim=vector_dim)
        
    def add(self, content, metadata):
        embedding = self.embed(content)
        self.store.add(embedding, content, metadata)
        
    def retrieve(self, query, top_k=5):
        query_emb = self.embed(query)
        return self.store.search(query_emb, top_k)
    
    def compress(self, memories):
        prompt = f"总结以下记忆要点：{memories}"
        return self.llm.generate(prompt)
```

## Related Cases

- [[entities/reflexion-agent]] - Reflexion Agent
