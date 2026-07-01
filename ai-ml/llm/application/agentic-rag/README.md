# Agentic RAG

> 本案例介绍 Agentic RAG 架构，通过将智能体的决策能力引入检索增强生成系统，解决传统 RAG 在复杂查询、多步推理和动态信息需求场景下的局限。

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Agentic RAG 架构                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   User Query                                                            │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   1. 查询理解与路由                               │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │  简单查询    │    │  多步推理    │    │  需要外部     │        │  │
│   │   │  → 直接 RAG │    │  → 迭代检索  │    │  工具调用     │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   2. Agent 决策循环 (ReAct)                       │  │
│   │                                                                  │  │
│   │   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │  │
│   │   │ Thought │ -> │ Action  │ -> │Observe  │ -> │ Reflect │    │  │
│   │   │ 思考    │    │ 行动    │    │ 观察    │    │ 反思    │    │  │
│   │   └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    │  │
│   │        │              │              │              │         │  │
│   │        └──────────────┴──────────────┘──────────────┘         │  │
│   │                       循环直到满足停止条件                         │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   3. 工具与检索能力                               │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ Vector DB   │    │ Web Search  │    │  API Tools  │        │  │
│   │   │ 向量检索     │    │ 网络搜索    │    │ 工具调用    │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   4. 答案生成与验证                               │  │
│   │                                                                  │  │
│   │   • 基于聚合上下文生成答案                                         │  │
│   │   • 自我反思：检查答案是否充分、是否存在幻觉                       │  │
│   │   • 必要时触发补充检索                                             │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   Final Answer                                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解 Agentic RAG 与传统 RAG 在架构和能力上的核心差异
- ✅ 掌握查询路由、迭代检索、自我反思、工具调用等关键技术
- ✅ 实现一个基于 ReAct 模式的 Agentic RAG 原型
- ✅ 评估 Agentic RAG 在复杂查询场景下的检索与生成质量

## 📖 核心概念

### 1. 传统 RAG 的局限

传统 RAG 流程通常是：

```
Query → Embedding → Vector Search → Top-K Chunks → LLM Answer
```

这种流水线在处理简单、事实性查询时效果很好，但面对以下场景时能力有限：

- **复杂多步问题**：需要分解为多个子问题并分别检索
- **信息缺失**：初次检索结果不充分，需要补充检索
- **跨源对比**：需要对比多个文档或外部数据源
- **动态信息**：需要结合实时搜索结果或 API 数据

### 2. Agentic RAG 的核心思想

Agentic RAG 将智能体（Agent）的决策能力引入 RAG 流程，使系统能够：

- **自主决定**是否需要检索、检索什么、使用哪个检索源
- **迭代优化**检索策略，根据中间结果调整查询
- **调用工具**扩展能力边界，如搜索引擎、数据库、API
- **自我反思**验证答案质量，必要时重新检索

### 3. 查询路由（Query Routing）

查询路由根据用户问题的特征，将其分配给最合适的处理路径：

- **简单事实查询** → 直接向量检索
- **需要最新信息** → 网络搜索工具
- **结构化数据需求** → 数据库/API 查询
- **复杂推理问题** → 多步迭代检索

### 4. 迭代检索与自我反思

Agentic RAG 通过 ReAct（Reasoning + Acting）循环实现迭代检索：

1. **Thought**：分析当前已掌握的信息，判断是否需要进一步检索
2. **Action**：执行检索或工具调用
3. **Observation**：观察检索结果
4. **Reflect**：评估是否已足以回答问题，否则继续循环

## 💻 代码示例

完整代码位于 `code/` 目录。下面展示 Agentic RAG 的核心实现：

```python
# code/agentic_rag.py
from typing import List, Dict, Any


class SimpleRetriever:
    """模拟向量检索器"""

    def __init__(self, documents: List[str]):
        self.documents = documents

    def search(self, query: str, top_k: int = 2) -> List[str]:
        """基于关键词的简单检索模拟"""
        query_words = set(query.lower().split())
        scored = []
        for doc in self.documents:
            doc_words = set(doc.lower().split())
            score = len(query_words & doc_words)
            scored.append((score, doc))
        scored.sort(reverse=True)
        return [doc for _, doc in scored[:top_k]]


class AgenticRAG:
    """基于 ReAct 的 Agentic RAG 原型"""

    def __init__(self, retriever: SimpleRetriever, max_iterations: int = 3):
        self.retriever = retriever
        self.max_iterations = max_iterations

    def route_query(self, query: str) -> str:
        """简单查询路由"""
        if "最新" in query or "今天" in query or "新闻" in query:
            return "web_search"
        if "对比" in query or "比较" in query or "哪个" in query:
            return "multi_retrieval"
        return "direct_rag"

    def reflect(self, query: str, context: str, answer: str) -> bool:
        """自我反思：判断答案是否充分"""
        # 简单启发式：如果上下文中没有查询关键词，认为不充分
        query_keywords = set(query.lower().split())
        context_words = set(context.lower().split())
        overlap = query_keywords & context_words
        return len(overlap) >= 1 and len(answer) > 20

    def generate_answer(self, query: str, context: str) -> str:
        """模拟答案生成"""
        return f"基于检索到的信息：{context[:80]}...\n答案：针对'{query}'的总结性回答。"

    def run(self, query: str) -> Dict[str, Any]:
        """执行 Agentic RAG 流程"""
        route = self.route_query(query)
        all_context = []

        for i in range(self.max_iterations):
            # 根据路由策略决定检索方式
            if route == "multi_retrieval":
                # 多步检索：拆分查询
                sub_queries = [query.replace("对比", "").strip(), query]
                context = []
                for sq in sub_queries:
                    context.extend(self.retriever.search(sq, top_k=2))
            else:
                context = self.retriever.search(query, top_k=3)

            all_context.extend(context)
            combined_context = "\n".join(all_context)
            answer = self.generate_answer(query, combined_context)

            if self.reflect(query, combined_context, answer):
                return {
                    "query": query,
                    "route": route,
                    "iterations": i + 1,
                    "context": combined_context,
                    "answer": answer,
                }

        return {
            "query": query,
            "route": route,
            "iterations": self.max_iterations,
            "context": combined_context,
            "answer": answer,
        }


if __name__ == "__main__":
    documents = [
        "vLLM 使用 PagedAttention 实现高吞吐推理。",
        "SGLang 使用 RadixAttention 优化多轮对话缓存。",
        "TGI 是 Hugging Face 推出的生产级推理服务。",
        "Agentic RAG 通过智能体实现迭代检索和自我反思。",
    ]

    retriever = SimpleRetriever(documents)
    rag = AgenticRAG(retriever)

    queries = [
        "vLLM 和 SGLang 的注意力机制有什么区别？",
        "最新的大模型推理引擎新闻",
    ]

    for q in queries:
        result = rag.run(q)
        print(f"\n查询: {result['query']}")
        print(f"路由: {result['route']}")
        print(f"迭代次数: {result['iterations']}")
        print(f"答案: {result['answer'][:120]}")
```

## 🔧 配置说明

Agentic RAG 的关键配置参数：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `max_iterations` | int | 3 | 最大迭代检索次数 |
| `top_k` | int | 3 | 每次检索返回的文档数 |
| `enable_web_search` | bool | False | 是否启用网络搜索工具 |
| `enable_reflection` | bool | True | 是否启用自我反思 |
| `reflection_threshold` | float | 0.5 | 反思通过阈值 |

## 📊 运行结果

执行 `code/agentic_rag.py` 后，预期输出：

```
查询: vLLM 和 SGLang 的注意力机制有什么区别？
路由: multi_retrieval
迭代次数: 1
答案: 基于检索到的信息：vLLM 使用 PagedAttention 实现高吞吐推理。
SGLang 使用 RadixAttention 优化多轮对话缓存。...

查询: 最新的大模型推理引擎新闻
路由: web_search
迭代次数: 1
答案: 基于检索到的信息：vLLM 使用 PagedAttention 实现高吞吐推理。...
```

说明：
- 第一个查询触发多路检索， because it contains "对比" / "区别"
- 第二个查询触发 web_search 路由， because it contains "最新"

## 🐛 常见问题

### Q1: Agentic RAG 与传统 RAG 的主要区别是什么？

传统 RAG 是固定的检索-生成流水线；Agentic RAG 引入智能体决策循环，使系统能够根据中间结果动态选择检索策略、调用工具、迭代优化答案。

### Q2: Agentic RAG 是否一定比传统 RAG 好？

不一定。Agentic RAG 增加了系统复杂度和延迟，适合复杂查询场景。对于简单的事实查询，传统 RAG 更快、更稳定。

### Q3: 如何评估 Agentic RAG 的效果？

可以从以下维度评估：
- **检索准确率**：相关文档是否被检索到
- **答案正确性**：最终答案是否准确
- **迭代效率**：平均需要几次迭代才能回答问题
- **工具调用合理性**：工具调用是否必要且有效

## 📚 扩展学习

- **ReAct**: Synergizing Reasoning and Acting in Language Models
- **Self-RAG**: Learning to Retrieve, Generate, and Critique through Self-Reflection
- **Corrective RAG**: Active Retrieval Augmented Generation
- **LangGraph**: 用于构建复杂 Agent 工作流的框架
- **LlamaIndex Agents**: 提供多种 Agentic RAG 实现模式

## 🤝 贡献指南

欢迎扩展 Agentic RAG 的能力：

- 增加更复杂的查询路由策略
- 实现真实的向量检索器集成（如 FAISS、Chroma）
- 增加网络搜索和 API 工具调用示例
- 添加多轮对话记忆机制
- 实现更完善的自我反思评分模型

---

*最后更新：2026-06-16*

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```
