"""
推理引擎横向对比基准测试框架

本脚本提供一个可复现的对比框架，使用模拟数据展示 vLLM、TGI、SGLang
在吞吐量、延迟、显存占用等维度的差异。

生产环境中，可将 simulate_engine_inference 替换为真实引擎调用。
"""

import random
from dataclasses import dataclass
from typing import List


@dataclass
class BenchmarkResult:
    """基准测试结果"""

    engine: str
    throughput: float  # tokens/sec
    avg_latency: float  # ms
    p99_latency: float  # ms
    gpu_memory_gb: float


def simulate_engine_inference(
    engine: str,
    num_requests: int,
    avg_input_len: int,
    avg_output_len: int,
) -> BenchmarkResult:
    """
    模拟不同推理引擎的性能特征。

    参数:
        engine: 引擎名称 (vllm / tgi / sglang)
        num_requests: 请求数量
        avg_input_len: 平均输入长度
        avg_output_len: 平均输出长度

    返回:
        BenchmarkResult 对象
    """
    # 基于各引擎公开技术特点的模拟参数
    # vLLM: PagedAttention 带来高吞吐，显存利用率高
    # TGI: 功能全面但吞吐略低，企业级特性带来一定开销
    # SGLang: RadixAttention 和结构化生成优化，延迟较低
    engine_profiles = {
        "vllm": {
            "throughput_factor": 1.25,
            "latency_factor": 0.9,
            "memory_overhead": 1.1,
        },
        "tgi": {
            "throughput_factor": 1.0,
            "latency_factor": 1.0,
            "memory_overhead": 1.2,
        },
        "sglang": {
            "throughput_factor": 1.15,
            "latency_factor": 0.85,
            "memory_overhead": 1.05,
        },
    }

    if engine not in engine_profiles:
        raise ValueError(f"不支持的引擎: {engine}")

    profile = engine_profiles[engine]

    # 基础耗时：总 token 数 / 1000（模拟每秒处理 1000 tokens 的基线）
    total_tokens = num_requests * (avg_input_len + avg_output_len)
    base_time = total_tokens / 1000.0
    elapsed = base_time / profile["throughput_factor"]

    throughput = total_tokens / max(elapsed, 0.001)
    avg_latency = (elapsed * 1000) / num_requests * profile["latency_factor"]
    p99_latency = avg_latency * (1.5 + random.uniform(0, 0.3))
    gpu_memory = 14.0 * profile["memory_overhead"]

    return BenchmarkResult(
        engine=engine,
        throughput=round(throughput, 2),
        avg_latency=round(avg_latency, 2),
        p99_latency=round(p99_latency, 2),
        gpu_memory_gb=round(gpu_memory, 2),
    )


def run_comparison(
    num_requests: int = 1000,
    avg_input_len: int = 512,
    avg_output_len: int = 256,
) -> List[BenchmarkResult]:
    """
    运行三大引擎对比实验。

    参数:
        num_requests: 请求数量
        avg_input_len: 平均输入长度
        avg_output_len: 平均输出长度

    返回:
        各引擎的 BenchmarkResult 列表
    """
    engines = ["vllm", "tgi", "sglang"]
    results = []
    for engine in engines:
        result = simulate_engine_inference(
            engine=engine,
            num_requests=num_requests,
            avg_input_len=avg_input_len,
            avg_output_len=avg_output_len,
        )
        results.append(result)
    # 按吞吐量降序排列
    results.sort(key=lambda x: x.throughput, reverse=True)
    return results


def print_results(results: List[BenchmarkResult]):
    """打印对比结果表格"""
    header = (
        f"{'Engine':<10} {'Throughput':<15} {'Avg Latency':<15} "
        f"{'P99 Latency':<15} {'GPU Memory':<12}"
    )
    print(header)
    print("-" * len(header))
    for r in results:
        print(
            f"{r.engine:<10} {r.throughput:<15} {r.avg_latency:<15} "
            f"{r.p99_latency:<15} {r.gpu_memory_gb:<12}"
        )


def recommend_engine(scenario: str) -> str:
    """
    根据场景推荐合适的推理引擎。

    参数:
        scenario: 场景描述 (throughput / latency / structured / ecosystem)

    返回:
        推荐引擎名称
    """
    recommendations = {
        "throughput": "vllm",
        "latency": "sglang",
        "structured": "sglang",
        "ecosystem": "tgi",
    }
    return recommendations.get(scenario.lower(), "vllm")


if __name__ == "__main__":
    random.seed(42)
    results = run_comparison()
    print_results(results)

    print("\n场景推荐:")
    for scenario in ["throughput", "latency", "structured", "ecosystem"]:
        print(f"  {scenario:<12} -> {recommend_engine(scenario)}")
