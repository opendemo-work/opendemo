"""
Agentic RAG 原型实现

本脚本演示一个基于 ReAct 思想的 Agentic RAG 系统，包含：
- 查询路由
- 迭代检索
- 自我反思
- 模拟答案生成

注意：本示例仅使用标准库，便于在无网络环境下运行。
生产环境可替换为真实向量数据库、LLM API 和搜索工具。
"""

from typing import Any, Dict, List


class SimpleRetriever:
    """模拟向量检索器

    使用关键词重叠作为相似度分数，便于本地演示。
    """

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
        # 按分数降序排列，分数相同保持原始顺序
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]


class AgenticRAG:
    """基于 ReAct 的 Agentic RAG 原型"""

    def __init__(self, retriever: SimpleRetriever, max_iterations: int = 3):
        """
        初始化 Agentic RAG

        Args:
            retriever: 检索器实例
            max_iterations: 最大迭代检索次数
        """
        self.retriever = retriever
        self.max_iterations = max_iterations

    def route_query(self, query: str) -> str:
        """简单查询路由

        根据查询关键词决定处理策略：
        - web_search: 需要最新信息
        - multi_retrieval: 需要对比或多方面信息
        - direct_rag: 简单事实查询
        """
        query_lower = query.lower()
        if any(kw in query_lower for kw in ["最新", "今天", "新闻", "实时"]):
            return "web_search"
        if any(kw in query_lower for kw in ["对比", "比较", "区别", "哪个", "差异"]):
            return "multi_retrieval"
        return "direct_rag"

    def reflect(self, query: str, context: str, answer: str) -> bool:
        """自我反思：判断答案是否充分

        简单启发式：上下文中包含查询关键词，且答案长度足够。
        """
        query_keywords = set(query.lower().split())
        context_words = set(context.lower().split())
        overlap = query_keywords & context_words
        return len(overlap) >= 1 and len(answer) > 20

    def generate_answer(self, query: str, context: str) -> str:
        """模拟答案生成

        生产环境中应替换为真实 LLM 调用。
        """
        return (
            f"基于检索到的信息：{context[:80]}...\n"
            f"答案：针对'{query}'的总结性回答。"
        )

    def run(self, query: str) -> Dict[str, Any]:
        """执行 Agentic RAG 流程

        Args:
            query: 用户查询

        Returns:
            包含查询、路由、迭代次数、上下文和答案的字典
        """
        route = self.route_query(query)
        all_context: List[str] = []
        combined_context = ""
        answer = ""

        for i in range(self.max_iterations):
            # 根据路由策略决定检索方式
            if route == "multi_retrieval":
                # 多步检索：对原始查询和简化查询分别检索
                sub_queries = [query, query.replace("对比", "").replace("区别", "").strip()]
                context = []
                for sq in sub_queries:
                    if sq:
                        context.extend(self.retriever.search(sq, top_k=2))
            else:
                context = self.retriever.search(query, top_k=3)

            all_context.extend(context)
            # 去重并保持顺序
            seen = set()
            unique_context = []
            for doc in all_context:
                if doc not in seen:
                    seen.add(doc)
                    unique_context.append(doc)
            all_context = unique_context

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


def main():
    """主函数：演示 Agentic RAG 效果"""
    documents = [
        "vLLM 使用 PagedAttention 实现高吞吐推理。",
        "SGLang 使用 RadixAttention 优化多轮对话缓存。",
        "TGI 是 Hugging Face 推出的生产级推理服务。",
        "Agentic RAG 通过智能体实现迭代检索和自我反思。",
        "传统 RAG 适用于简单事实查询，Agentic RAG 适合复杂推理。",
    ]

    retriever = SimpleRetriever(documents)
    rag = AgenticRAG(retriever, max_iterations=3)

    queries = [
        "vLLM 和 SGLang 的注意力机制有什么区别？",
        "最新的大模型推理引擎新闻",
        "什么是 Agentic RAG？",
    ]

    for q in queries:
        result = rag.run(q)
        print(f"\n查询: {result['query']}")
        print(f"路由: {result['route']}")
        print(f"迭代次数: {result['iterations']}")
        print(f"答案: {result['answer'][:120]}")


if __name__ == "__main__":
    main()
