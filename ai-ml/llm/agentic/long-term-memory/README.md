# Long-Term Memory 长期记忆系统

> 本案例详解长期记忆架构：跨会话持久化知识存储与检索

## 架构图

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

## 核心实现

### 长期记忆管理

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

## 相关案例

- `semantic-memory` - 语义记忆
- `memory-systems` - 记忆系统
