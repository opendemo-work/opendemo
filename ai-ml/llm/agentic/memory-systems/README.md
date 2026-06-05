# Memory Systems 记忆系统

> 本案例详解 Agent 记忆系统：短期记忆、长期记忆、语义记忆

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Memory 架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Working Memory                         │   │
│  │                   (当前上下文)                           │   │
│  │                                                          │   │
│  │   Conversation History ──▶ Current Session Context       │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Episodic Memory                           │   │
│  │                 (情景记忆)                                │   │
│  │                                                          │   │
│  │   [Episode 1] [Episode 2] [Episode 3] ...               │   │
│  │   每次重要交互作为一个 episode                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Semantic Memory                           │   │
│  │                 (语义记忆)                                │   │
│  │                                                          │   │
│  │   Facts ──▶ Concepts ──▶ Knowledge Graph                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### 记忆管理器

```python
class MemoryManager:
    def __init__(self):
        self.working_memory = []  # 当前上下文
        self.episodic_memory = []  # 历史 episodes
        self.semantic_memory = {}  # 知识图谱
    
    def add_working(self, item):
        self.working_memory.append(item)
        if len(self.working_memory) > MAX_WORKING_SIZE:
            # 压缩到 episodic
            self.compress_to_episode()
    
    def compress_to_episode(self):
        """将工作记忆压缩到情景记忆"""
        if self.working_memory:
            episode = {
                "content": self.working_memory.copy(),
                "timestamp": datetime.now()
            }
            self.episodic_memory.append(episode)
            self.working_memory = []
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Any]:
        """检索记忆"""
        # 结合 working + episodic + semantic
        pass
```

## 🔗 相关案例

- `react-agent` - ReAct Agent
- `plan-and-execute` - Plan-and-Execute
- `multi-agent-collaboration` - Multi-Agent
