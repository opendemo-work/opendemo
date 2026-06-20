"""
Agentic RAG 单元测试

使用标准库 unittest，无需额外安装 pytest 即可运行。
"""

import sys
import unittest
from pathlib import Path

# 添加 code 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from agentic_rag import AgenticRAG, SimpleRetriever


class TestSimpleRetriever(unittest.TestCase):
    """SimpleRetriever 测试"""

    def setUp(self):
        self.documents = [
            "vLLM 使用 PagedAttention 实现高吞吐推理。",
            "SGLang 使用 RadixAttention 优化多轮对话缓存。",
            "TGI 是 Hugging Face 推出的生产级推理服务。",
        ]
        self.retriever = SimpleRetriever(self.documents)

    def test_search_returns_top_k_results(self):
        """测试检索返回指定数量的结果"""
        results = self.retriever.search("vLLM", top_k=2)
        self.assertEqual(len(results), 2)

    def test_search_ranking(self):
        """测试检索结果按相关性排序"""
        results = self.retriever.search("vLLM PagedAttention", top_k=1)
        self.assertIn("vLLM", results[0])


class TestAgenticRAG(unittest.TestCase):
    """AgenticRAG 测试"""

    def setUp(self):
        documents = [
            "vLLM 使用 PagedAttention 实现高吞吐推理。",
            "SGLang 使用 RadixAttention 优化多轮对话缓存。",
            "TGI 是 Hugging Face 推出的生产级推理服务。",
            "Agentic RAG 通过智能体实现迭代检索和自我反思。",
        ]
        self.retriever = SimpleRetriever(documents)
        self.rag = AgenticRAG(self.retriever, max_iterations=3)

    def test_route_query_direct_rag(self):
        """测试简单查询路由到 direct_rag"""
        route = self.rag.route_query("什么是 RAG")
        self.assertEqual(route, "direct_rag")

    def test_route_query_web_search(self):
        """测试最新信息查询路由到 web_search"""
        route = self.rag.route_query("最新的大模型新闻")
        self.assertEqual(route, "web_search")

    def test_route_query_multi_retrieval(self):
        """测试对比查询路由到 multi_retrieval"""
        route = self.rag.route_query("vLLM 和 SGLang 有什么区别")
        self.assertEqual(route, "multi_retrieval")

    def test_reflect_passes_with_relevant_context(self):
        """测试有相关上下文时反思通过"""
        result = self.rag.reflect(
            query="vLLM",
            context="vLLM 使用 PagedAttention",
            answer="vLLM 是一个高性能大模型推理引擎，使用 PagedAttention 技术。",
        )
        self.assertTrue(result)

    def test_reflect_fails_with_short_answer(self):
        """测试答案过短时反思不通过"""
        result = self.rag.reflect(
            query="vLLM",
            context="vLLM 使用 PagedAttention",
            answer="短",
        )
        self.assertFalse(result)

    def test_run_returns_expected_keys(self):
        """测试运行结果包含必要字段"""
        result = self.rag.run("什么是 Agentic RAG")
        expected_keys = {"query", "route", "iterations", "context", "answer"}
        self.assertEqual(set(result.keys()), expected_keys)
        self.assertLessEqual(result["iterations"], 3)
        self.assertGreater(len(result["answer"]), 0)


if __name__ == "__main__":
    unittest.main()
