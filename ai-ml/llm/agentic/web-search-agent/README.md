# Web Search Agent 网页搜索 Agent

> 本案例详解网页搜索 Agent：实时信息获取与知识更新

## 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Web Search Agent 架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Query      │───▶│   Search     │───▶│   Extract    │      │
│  │   Formulate  │    │   Engine     │    │   Content    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                  │                   │               │
│         ▼                  ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Result    │◀───│   Ranking    │◀───│   Summarize  │      │
│  │   Filter    │    │   & Score    │    │   & Answer   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心实现

### 网页搜索 Agent

```python
import search_api

class WebSearchAgent:
    def __init__(self, llm):
        self.llm = llm
        self.search = search_api
        
    def formulate_query(self, question):
        prompt = f"为以下问题生成搜索关键词：{question}"
        return self.llm.generate(prompt).strip()
    
    def search_web(self, query, top_k=5):
        results = self.search(query, num_results=top_k)
        return self.extract_content(results)
    
    def answer(self, question):
        query = self.formulate_query(question)
        content = self.search_web(query)
        summary = self.summarize(content)
        return self.llm.generate(f"基于以下信息回答：{summary}\n问题：{question}")
```

## 相关案例

- `react-agent` - ReAct Agent
- `langchain-agent` - LangChain Agent
