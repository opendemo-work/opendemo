# 🤖 大模型 (LLM) 技术栈

> OpenDemo 大模型技术栈核心目录，覆盖架构、训练、推理、优化、应用、Agentic、Harness、评估 8 大领域

## 📋 概览

本目录是 OpenDemo 大模型技术的核心重点方向，包含 **120+** 个高质量案例，全面覆盖大模型从理论到实践的完整技术体系。

## 📊 技术栈全景

| 领域 | 英文 | 案例数 | 核心内容 |
|------|------|--------|----------|
| **架构** | Architecture | 15+ | Transformer、Attention、RoPE、MoE、SSM |
| **训练** | Training | 20+ | 预训练、SFT、RLHF、LoRA、分布式训练 |
| **推理** | Inference | 15+ | vLLM、TGI、Continuous Batching、Speculative Decoding |
| **优化** | Optimization | 15+ | 量化(FP8/INT4)、剪枝、蒸馏、编译优化 |
| **应用** | Application | 15+ | RAG、Function Calling、Prompt Engineering |
| **Agentic** | Agentic AI | 15+ | ReAct、Multi-Agent、Memory、Agent框架 |
| **Harness** | Harness Engineering | 10+ | Eval Harness、Testing Framework、Benchmark |
| **评估** | Evaluation | 15+ | MMLU、HumanEval、BBH、MT-Bench、Safety |

**总计: 120+ 案例**

---

## 📁 目录结构

```
llm/
├── LLM_TECH_STACK_PLAN.md    # 完整技术栈规划文档
├── README.md                 # 本文件
├── architecture/             # 架构篇 (15+)
│   ├── transformer-scratch/  # 从零实现Transformer
│   ├── multi-head-attention/ # Multi-Head Attention
│   ├── flash-attention/      # Flash Attention
│   ├── rotary-embedding/     # RoPE 旋转位置编码
│   ├── mixture-of-experts/   # MoE 混合专家
│   └── ...
├── training/                 # 训练篇 (20+)
│   ├── llm-pretraining-from-scratch/  # 从零预训练
│   ├── distributed-training/ # 分布式训练
│   ├── sft-fundamentals/     # SFT 基础
│   ├── lora-fine-tuning/     # LoRA 微调
│   ├── rlhf-introduction/    # RLHF 对齐
│   └── ...
├── inference/                # 推理篇 (15+)
│   ├── vllm-inference/       # vLLM 高吞吐推理
│   ├── text-generation-inference/  # TGI 部署
│   ├── continuous-batching/   # Continuous Batching
│   ├── speculative-decoding/ # 投机解码
│   └── ...
├── optimization/             # 优化篇 (15+)
│   ├── fp8-quantization/     # FP8 量化
│   ├── int4-quantization/    # INT4 量化
│   ├── wanda-pruning/        # Wanda 剪枝
│   ├── knowledge-distillation/  # 知识蒸馏
│   └── ...
├── application/               # 应用篇 (15+)
│   ├── rag-fundamentals/     # RAG 基础
│   ├── hybrid-search/        # 混合搜索
│   ├── function-calling/     # Function Calling
│   ├── chain-of-thought/     # 思维链
│   └── ...
├── agentic/                  # Agentic 工程篇 (15+)
│   ├── react-agent/          # ReAct 推理框架
│   ├── multi-agent-collaboration/  # 多智能体协作
│   ├── memory-systems/       # 记忆系统
│   ├── langchain-agent/      # LangChain Agent
│   └── ...
├── harness/                  # Harness 工程篇 (10+)
│   ├── lm-evaluation-harness/  # LM-Eval Harness
│   ├── llm-testing-framework/ # 测试框架
│   └── ...
└── evaluation/               # 评估测评篇 (15+)
    ├── mmlu-evaluation/      # MMLU 评测
    ├── humaneval-evaluation/  # HumanEval 评测
    ├── mt-bench-evaluation/   # MT-Bench 对话
    ├── safety-evaluation/     # 安全评测
    └── ...
```

---

## 🚀 快速开始

### 查看所有 LLM 案例

```bash
opendemo search llm
```

### 按领域获取案例

```bash
# 架构类
opendemo get llm transformer-scratch
opendemo get llm flash-attention

# 训练类
opendemo get llm lora-fine-tuning
opendemo get llm rlhf-introduction

# 推理类
opendemo get llm vllm-inference
opendemo get llm continuous-batching

# 优化类
opendemo get llm fp8-quantization
opendemo get llm knowledge-distillation

# 应用类
opendemo get llm rag-fundamentals
opendemo get llm function-calling

# Agentic
opendemo get llm react-agent
opendemo get llm multi-agent-collaboration

# 评估类
opendemo get llm mmlu-evaluation
opendemo get llm humaneval-evaluation
```

---

## 🎯 学习路径

### 路径 1: LLM 全栈工程师

```
架构基础 → 训练实战 → 推理优化 → 应用部署
```

### 路径 2: LLM 应用开发者

```
RAG 基础 → Function Calling → Agent 开发 → 应用集成
```

### 路径 3: LLM 研究工程师

```
模型架构 → 训练优化 → RLHF 对齐 → 评估体系
```

---

## 📚 核心技术栈

### 框架与工具

| 类别 | 工具 |
|------|------|
| **训练框架** | DeepSpeed, Megatron-LM, NeMo, FlashAttention |
| **推理引擎** | vLLM, Text Generation Inference, llama.cpp, TensorRT |
| **微调工具** | LoRA, QLoRA, PEFT, Axotl |
| **应用框架** | LangChain, LlamaIndex, CrewAI, AutoGen |
| **评估工具** | LM-Evaluation-Harness, HELICONE, Promptfoo |

### 主流模型

| 模型系列 | 代表模型 | 应用场景 |
|----------|----------|----------|
| **LLaMA** | LLaMA 3, LLaMA 2 | 通用对话 |
| **Mistral** | Mistral 7B, Mixtral 8x22B | 效率优先 |
| **Qwen** | Qwen 2, Qwen 2.5 | 中文优化 |
| **DeepSeek** | DeepSeek V2, DeepSeek Coder | 代码专用 |
| **Yi** | Yi 1.5, Yi Large | 中英双语 |

---

## 📈 实现计划

### Phase 1: 核心基础 (2026 Q3)

- [ ] 架构篇核心案例 (8+)
- [ ] 训练篇基础案例 (10+)
- [ ] 推理篇核心案例 (8+)

### Phase 2: 能力扩展 (2026 Q4)

- [ ] Agentic 工程完整体系 (15+)
- [ ] RAG 与应用实战 (10+)
- [ ] 评估测评体系 (10+)

### Phase 3: 高级优化 (2027 Q1)

- [ ] RLHF/DPO 等对齐技术 (8+)
- [ ] 量化压缩高级技术 (8+)
- [ ] Multi-Agent 复杂系统 (8+)

---

## 🤝 贡献指南

欢迎提交新的 LLM 技术案例：

1. 遵循统一的目录结构和文档格式
2. 每个案例包含 README.md (≥3000字符) + metadata.json
3. 提供完整的代码实现和运行说明
4. 包含架构图、代码示例、学习要点
5. 遵循 OpenDemo 五星案例标准

---

> **💡 提示**: 大模型技术发展迅速，建议关注最新的研究成果和技术趋势，保持持续学习的态度。
