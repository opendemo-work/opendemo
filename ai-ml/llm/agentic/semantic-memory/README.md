# Semantic Memory 语义记忆管理

> 本案例详解语义记忆架构：基于语义相似性的动态记忆组织

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Semantic Memory 架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Content    │───▶│   Semantic   │───▶│   Concept    │      │
│  │   Input      │    │   Embedding  │    │   Graph      │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                  │                   │               │
│         ▼                  ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Forget    │◀───│   Similarity  │◀───│   Associate  │      │
│  │   Filter    │    │   Match       │    │   Linking    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心实现

### 语义记忆管理

```python
class SemanticMemory:
    def __init__(self, embedding_model):
        self.embedder = embedding_model
        self.concepts = {}
        
    def add(self, content):
        embedding = self.embedder.encode(content)
        concept_id = self.link_to_concepts(embedding)
        self.concepts[concept_id] = {
            'content': content,
            'embedding': embedding
        }
        return concept_id
    
    def retrieve(self, query, threshold=0.8):
        query_emb = self.embedder.encode(query)
        matches = []
        for cid, data in self.concepts.items():
            sim = cosine_similarity(query_emb, data['embedding'])
            if sim > threshold:
                matches.append((cid, sim))
        return sorted(matches, key=lambda x: x[1], reverse=True)
```

## 相关案例

- `long-term-memory` - 长期记忆
- `memory-systems` - 记忆系统
