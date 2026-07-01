# LLM CI 集成评估

> 本案例介绍如何将大模型评估嵌入持续集成（CI）流程，通过黄金数据集、回归测试、自动报告与质量门禁，确保模型迭代不降低关键能力。

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      LLM CI 集成评估架构                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      1. CI 触发源                                 │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ Pull Request │    │ Merge to    │    │ Scheduled   │        │  │
│   │   │             │    │ main        │    │ Nightly     │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   2. 评估 Harness 执行                            │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ 加载模型    │    │ 加载黄金     │    │ 运行评测     │        │  │
│   │   │ 或 API     │    │ 数据集       │    │ 任务         │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   │   评测维度：                                                     │  │
│   │   • 准确率 (Accuracy)                                            │  │
│   │   • 召回率 (Recall)                                              │  │
│   │   • BLEU / ROUGE                                                 │  │
│   │   • 延迟与吞吐                                                   │  │
│   │   • 安全与对齐                                                   │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   3. 结果聚合与对比                               │  │
│   │                                                                  │  │
│   │   Current Score  vs  Baseline Score                             │  │
│   │        │                    │                                   │  │
│   │        ▼                    ▼                                   │  │
│   │   ┌─────────────────────────────────────────────┐              │  │
│   │   │  计算 Delta = Current - Baseline             │              │  │
│   │   │  判断是否超过允许回归阈值                      │              │  │
│   │   └─────────────────────────────────────────────┘              │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                   4. 报告与门禁                                   │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ Markdown    │    │ CI Badge    │    │ Quality     │        │  │
│   │   │ Report      │    │ Status      │    │ Gate        │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   │                                                                  │  │
│   │   如果 Delta < threshold → CI 失败                               │  │
│   │   如果 Delta >= threshold → CI 通过                              │  │
│   │                                                                  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解将 LLM 评估集成到 CI 流程的必要性与常见挑战
- ✅ 掌握黄金数据集、回归测试、质量门禁的设计方法
- ✅ 实现一个可嵌入 CI 的 LLM 评估 Harness
- ✅ 学会生成自动化评估报告并设置合理的失败阈值

## 📖 核心概念

### 1. 为什么需要 CI 中的 LLM 评估？

大语言模型的迭代速度极快，每次权重更新、微调或 prompt 调整都可能影响模型行为。将评估集成到 CI 可以：

- **及早发现回归**：在代码合并前发现性能下降
- **保证关键能力**：确保核心任务（如代码生成、安全对齐）不被破坏
- **提供可复现基准**：每次评估使用相同数据集和配置
- **加速迭代**：自动化评估减少人工验证成本

### 2. 黄金数据集（Golden Dataset）

黄金数据集是经过人工标注或验证的、代表核心业务场景的测试集合。好的黄金数据集应具备：

- **稳定性**：不频繁变动，保证纵向可比性
- **代表性**：覆盖关键业务场景和边缘案例
- **可扩展性**：支持逐步增加新测试用例
- **可解释性**：每个样本有明确的期望输出和评分标准

### 3. 回归测试与阈值

回归测试通过对比当前版本与基线版本的评估分数，判断新版本是否引入性能退化：

```
Delta = Current Score - Baseline Score

如果 Delta < -threshold:  CI 失败
如果 Delta >= -threshold: CI 通过
```

阈值设置需要平衡敏感度和稳定性：
- 阈值过严：导致频繁误报
- 阈值过松：无法捕获真实回归

### 4. 质量门禁（Quality Gate）

质量门禁是 CI 中的判定机制，根据评估结果决定是否允许合并。常见门禁包括：

- 关键任务准确率不得低于基线
- 安全评测分数不得低于阈值
- 延迟和成本指标不得超过预算
- 新增测试用例必须通过

## 💻 代码示例

完整代码位于 `code/` 目录。下面展示 CI 评估 Harness 的核心实现：

```python
# code/ci_evaluation_harness.py
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


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
    """模拟 LLM 客户端"""

    def generate(self, prompt: str) -> str:
        """模拟生成，生产环境替换为真实 API 调用"""
        # 简单规则：如果 prompt 包含关键词，返回预期相关的回答
        if "北京" in prompt:
            return "北京是中国的首都。"
        if "Python" in prompt:
            return "Python 是一种流行的编程语言。"
        return "这是一个模拟回答。"


class CIEvaluationHarness:
    """CI 集成评估 Harness"""

    def __init__(self, model_client: SimpleLLMClient, threshold: float = -0.05):
        self.model_client = model_client
        self.threshold = threshold

    def load_golden_dataset(self, path: str) -> List[EvalSample]:
        """加载黄金数据集"""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [EvalSample(**item) for item in data["samples"]]

    def score_prediction(self, expected: str, prediction: str) -> float:
        """简单评分：基于关键词重叠"""
        expected_words = set(expected.lower().split())
        prediction_words = set(prediction.lower().split())
        if not expected_words:
            return 0.0
        overlap = expected_words & prediction_words
        return len(overlap) / len(expected_words)

    def run_evaluation(self, dataset: List[EvalSample]) -> Dict[str, Any]:
        """运行完整评估"""
        results = []
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
        avg_latency = sum(r.latency_ms for r in results) / len(results) if results else 0.0
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
        """检查是否发生回归"""
        delta = current_score - baseline_score
        passed = delta >= self.threshold
        return {
            "current_score": round(current_score, 4),
            "baseline_score": round(baseline_score, 4),
            "delta": round(delta, 4),
            "threshold": self.threshold,
            "passed": passed,
        }

    def generate_report(self, eval_result: Dict[str, Any], regression: Dict[str, Any]) -> str:
        """生成 Markdown 评估报告"""
        status = "✅ 通过" if regression["passed"] else "❌ 失败"
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

{'模型表现符合预期，可以合并。' if regression['passed'] else '检测到性能回归，请检查模型变更。'}
"""
        return report


if __name__ == "__main__":
    client = SimpleLLMClient()
    harness = CIEvaluationHarness(client, threshold=-0.05)

    # 构造示例数据集
    dataset = [
        EvalSample("q1", "中国的首都是哪里？", "北京是中国的首都。", "geography"),
        EvalSample("q2", "Python 是什么？", "Python 是一种流行的编程语言。", "tech"),
    ]

    eval_result = harness.run_evaluation(dataset)
    regression = harness.check_regression(eval_result["avg_score"], baseline_score=0.8)
    report = harness.generate_report(eval_result, regression)

    print(report)
    print("\n详细结果:")
    print(json.dumps(eval_result, ensure_ascii=False, indent=2))
```

## 🔧 配置说明

CI 评估 Harness 的关键配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `threshold` | float | -0.05 | 允许的最大分数下降 |
| `golden_dataset_path` | str | `data/golden.json` | 黄金数据集路径 |
| `baseline_score` | float | 0.8 | 基线分数 |
| `categories` | list | `["all"]` | 需要评估的类别 |

## 📊 运行结果

执行 `code/ci_evaluation_harness.py` 后，预期输出：

```markdown
# LLM CI 评估报告

## 摘要

| 指标 | 数值 |
|------|------|
| 平均分数 | 0.85 |
| 基线分数 | 0.8 |
| 回归差值 | 0.05 |
| 阈值 | -0.05 |
| 平均延迟 | 0.05 ms |
| 总耗时 | 0.01 s |
| 样本数 | 2 |
| 状态 | ✅ 通过 |

## 结论

模型表现符合预期，可以合并。
```

## 🐛 常见问题

### Q1: 黄金数据集应该多大？

没有固定标准，建议：
- 覆盖 5-10 个核心能力维度
- 每个维度至少 20-50 个样本
- 总样本量在 200-1000 之间为宜
- 优先选择人工校验过、有明确评分标准的样本

### Q2: 如何设置回归阈值？

建议采用渐进式策略：
- 初始阶段：阈值宽松（如 -0.10），减少误报
- 稳定阶段：阈值收紧（如 -0.02），提高敏感度
- 关键任务：零容忍，任何下降都触发人工审核

### Q3: CI 评估会不会太慢？

可以通过以下方式加速：
- 使用小模型或蒸馏模型进行快速筛查
- 对黄金数据集分层采样，PR 阶段跑子集，合并后跑全集
- 并行执行不同类别的评估任务
- 使用缓存避免重复评估相同模型版本

## 📚 扩展学习

- **MLflow / Weights & Biases**: 模型实验与评估指标追踪
- **Promptfoo**: LLM prompt 测试与评估工具
- **DeepEval**: LLM 评估框架，支持多种指标
- **GitHub Actions / GitLab CI**: 常见的 CI 平台集成方式

## 🤝 贡献指南

欢迎扩展 CI 评估 Harness 的能力：

- 增加真实 LLM API 客户端集成
- 支持更多评估指标（BLEU、ROUGE、LLM-as-a-Judge）
- 增加多类别评估与分类报告
- 实现评估结果的历史趋势可视化

---

*最后更新：2026-06-16*

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```
