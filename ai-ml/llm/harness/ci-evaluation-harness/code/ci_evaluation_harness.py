"""
LLM CI 集成评估 Harness

本脚本演示如何将大模型评估嵌入持续集成流程，包括：
- 加载黄金数据集
- 运行模型评测
- 与基线对比检测回归
- 生成 Markdown 报告

注意：本示例仅使用标准库，便于在无网络环境下运行。
生产环境可替换为真实 LLM API、专业评估指标和 CI 平台。
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class EvalSample:
    """评测样本"""

    id: str
    input: str
    expected: str
    category: str


@dataclass
class EvalResult:
    """单个样本评测结果"""

    sample_id: str
    prediction: str
    score: float
    latency_ms: float


class SimpleLLMClient:
    """模拟 LLM 客户端

    生产环境中应替换为真实 API 调用或本地模型推理。
    """

    def generate(self, prompt: str) -> str:
        """模拟生成"""
        prompt_lower = prompt.lower()
        if "北京" in prompt or "首都" in prompt:
            return "北京是中国的首都。"
        if "python" in prompt_lower:
            return "Python 是一种流行的编程语言。"
        if "应用场景" in prompt or "大语言模型" in prompt:
            return "大语言模型可用于文本生成、问答、代码生成等任务。"
        return "这是一个模拟回答。"


class CIEvaluationHarness:
    """CI 集成评估 Harness"""

    def __init__(self, model_client: SimpleLLMClient, threshold: float = -0.05):
        """
        初始化 Harness

        Args:
            model_client: LLM 客户端实例
            threshold: 允许的最大分数下降（负数表示下降）
        """
        self.model_client = model_client
        self.threshold = threshold

    def load_golden_dataset(self, path: str) -> List[EvalSample]:
        """从 JSON 文件加载黄金数据集"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [EvalSample(**item) for item in data["samples"]]

    def score_prediction(self, expected: str, prediction: str) -> float:
        """简单评分：基于关键词重叠

        生产环境中可替换为 BLEU、ROUGE、LLM-as-a-Judge 等。
        """
        expected_words = set(expected.lower().split())
        prediction_words = set(prediction.lower().split())
        if not expected_words:
            return 0.0
        overlap = expected_words & prediction_words
        return len(overlap) / len(expected_words)

    def run_evaluation(self, dataset: List[EvalSample]) -> Dict[str, Any]:
        """运行完整评估

        Args:
            dataset: 评测样本列表

        Returns:
            包含平均分、延迟、详细结果的字典
        """
        results: List[EvalResult] = []
        start_time = time.time()

        for sample in dataset:
            t0 = time.time()
            prediction = self.model_client.generate(sample.input)
            latency_ms = (time.time() - t0) * 1000
            score = self.score_prediction(sample.expected, prediction)
            results.append(
                EvalResult(
                    sample_id=sample.id,
                    prediction=prediction,
                    score=score,
                    latency_ms=latency_ms,
                )
            )

        avg_score = sum(r.score for r in results) / len(results) if results else 0.0
        avg_latency = (
            sum(r.latency_ms for r in results) / len(results) if results else 0.0
        )
        total_time = time.time() - start_time

        return {
            "avg_score": round(avg_score, 4),
            "avg_latency_ms": round(avg_latency, 2),
            "total_time_s": round(total_time, 2),
            "num_samples": len(results),
            "details": [asdict(r) for r in results],
        }

    def check_regression(
        self, current_score: float, baseline_score: float
    ) -> Dict[str, Any]:
        """检查是否发生回归

        Args:
            current_score: 当前版本分数
            baseline_score: 基线分数

        Returns:
            包含 current_score、baseline_score、delta、threshold、passed 的字典
        """
        delta = current_score - baseline_score
        passed = delta >= self.threshold
        return {
            "current_score": round(current_score, 4),
            "baseline_score": round(baseline_score, 4),
            "delta": round(delta, 4),
            "threshold": self.threshold,
            "passed": passed,
        }

    def generate_report(
        self, eval_result: Dict[str, Any], regression: Dict[str, Any]
    ) -> str:
        """生成 Markdown 评估报告"""
        status = "✅ 通过" if regression["passed"] else "❌ 失败"
        conclusion = (
            "模型表现符合预期，可以合并。"
            if regression["passed"]
            else "检测到性能回归，请检查模型变更。"
        )

        report = f"""# LLM CI 评估报告

## 摘要

| 指标 | 数值 |
|------|------|
| 平均分数 | {eval_result['avg_score']} |
| 基线分数 | {regression['baseline_score']} |
| 回归差值 | {regression['delta']} |
| 阈值 | {regression['threshold']} |
| 平均延迟 | {eval_result['avg_latency_ms']} ms |
| 总耗时 | {eval_result['total_time_s']} s |
| 样本数 | {eval_result['num_samples']} |
| 状态 | {status} |

## 结论

{conclusion}
"""
        return report


def main():
    """主函数：演示 CI 评估流程"""
    client = SimpleLLMClient()
    harness = CIEvaluationHarness(client, threshold=-0.05)

    # 构造示例数据集
    dataset = [
        EvalSample("q1", "中国的首都是哪里？", "北京是中国的首都。", "geography"),
        EvalSample("q2", "Python 是什么？", "Python 是一种流行的编程语言。", "tech"),
        EvalSample(
            "q3",
            "请简述大语言模型的应用场景。",
            "大语言模型可用于文本生成、问答、代码生成等任务。",
            "general",
        ),
    ]

    eval_result = harness.run_evaluation(dataset)
    regression = harness.check_regression(
        eval_result["avg_score"], baseline_score=0.75
    )
    report = harness.generate_report(eval_result, regression)

    print(report)
    print("\n详细结果:")
    print(json.dumps(eval_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
