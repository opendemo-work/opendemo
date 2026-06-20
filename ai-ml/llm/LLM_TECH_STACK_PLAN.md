# 大模型 (LLM) 技术栈完整规划

> 本文档定义了 OpenDemo 大模型技术栈的完整体系结构，覆盖从基础架构到上层应用的 8 大核心领域。

---

## 📋 概览

大模型技术栈是 OpenDemo 的核心重点方向，覆盖以下 8 大领域。

### 当前落地状态（截至 2026-06-16）

`ai-ml/llm/` 下已实际落地 **88 个 demo**，各方向分布如下：

| 领域 | 英文 | 已落地数量 | 代表 demo |
|------|------|-----------|-----------|
| **训练** | Training | 15 | `lora-fine-tuning`、`rlhf-introduction`、`dpo-training`、`q-lora-tuning`、`fsdp-training`、`llm-pretraining-scratch` |
| **优化** | Optimization | 12 | `fp8-quantization`、`int4-quantization`、`awq-quantization`、`gptq-quantization`、`knowledge-distillation`、`torch-compile` |
| **评估** | Evaluation | 11 | `mmlu-evaluation`、`humaneval-evaluation`、`mt-bench-evaluation`、`llm-as-judge`、`safety-evaluation`、`truthfulqa-evaluation` |
| **应用** | Application | 11 | `rag-fundamentals`、`function-calling`、`chain-of-thought`、`vector-database-comparison`、`few-shot-learning`、`prompt-patterns` |
| **Agentic** | Agentic AI | 11 | `react-agent`、`langchain-agent`、`multi-agent-collaboration`、`plan-and-execute`、`reflexion-agent`、`web-search-agent` |
| **推理** | Inference | 10 | `vllm-inference`、`tgi-deployment`、`speculative-decoding`、`continuous-batching`、`paged-attention`、`kv-cache-optimization` |
| **架构** | Architecture | 10 | `transformer-scratch`、`gpt-architecture`、`llama-architecture`、`flash-attention`、`mixture-of-experts`、`state-space-models` |
| **Harness** | Harness Engineering | 8 | `lm-evaluation-harness`、`open-llm-leaderboard`、`promptfoo-evaluation`、`llm-testing-framework`、`regression-testing` |
| **总计** | | **88** | |

### 目标规划

| 领域 | 英文 | 核心内容 | 目标案例数 |
|------|------|----------|-----------|
| **架构** | Architecture | Transformer、Attention、Positional Encoding、MoE | 15+ |
| **训练** | Training | 预训练、SFT、RLHF、Distributed Training、Alignment | 20+ |
| **推理** | Inference | vLLM、TGI、Continuous Batching、Speculative Decoding | 15+ |
| **优化** | Optimization | Quantization、Pruning、Distillation、Compilation | 15+ |
| **应用** | Application | RAG、Function Calling、Prompt Engineering、Tool Use | 15+ |
| **Agentic** | Agentic AI | ReAct、Plan-and-Execute、Multi-Agent、Memory | 15+ |
| **Harness** | Harness Engineering | Eval Harness、Testing Framework、Benchmark | 10+ |
| **评估** | Evaluation | MMLU、HumanEval、BBH、MT-Bench、Safety | 15+ |

**目标总计: 120+ 案例**

### 已识别缺口清单

按优先级排序的待补齐方向：

- **架构**：KV 压缩、专家路由可视化、Mamba/RetNet 实战、编码器-解码器架构、ALiBi/RoPE 对比
- **训练**：数据清洗 pipeline、Dora/RS-LoRA、模型 soups、长上下文微调、故障容错训练
- **推理**：推理引擎对比（vLLM vs TGI vs SGLang）、动态批调度、前缀缓存工程化、多模型服务编排
- **优化**：GGUF、SmoothQuant、AutoGPTQ、ONNX/TensorRT-LLM 端到端、多教师蒸馏
- **应用**：Agentic RAG、Text2SQL、代码生成工作流、多语言 RAG、Graph RAG、多模态 RAG
- **Agentic**：工具调用安全、Agent 评估基准、人机协作循环、CrewAI/AutoGen/Swarm 框架实战
- **评估**：BBH、Arena、自定义评估 Harness、红队测试、隐私/偏见评测
- **Harness**：CI 集成评估、A/B 测试框架、生产监控与回滚、模糊测试

---

## 🏗️ 一、架构篇 (Architecture)

### 1.1 Transformer 核心组件

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `transformer-scratch` | 从零实现 Transformer 架构 | ⭐⭐⭐ |
| `multi-head-attention` | Multi-Head Attention 实现与可视化 | ⭐⭐⭐ |
| `self-attention-cuda` | CUDA 加速的自注意力机制 | ⭐⭐⭐⭐ |
| `flash-attention` | Flash Attention 原理与实现 | ⭐⭐⭐⭐ |
| `rotary-embedding` | RoPE 旋转位置编码详解 | ⭐⭐⭐⭐ |

### 1.2 位置编码 (Positional Encoding)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `absolute-positional-encoding` | 绝对位置编码实现 | ⭐⭐⭐ |
| `relative-positional-encoding` | 相对位置编码 (Shaw, XLNet) | ⭐⭐⭐⭐ |
| `alibi-positional-encoding` | ALiBi 无注意力偏置位置编码 | ⭐⭐⭐⭐ |
| `positional-encoding-comparison` | 各种位置编码对比分析 | ⭐⭐⭐⭐ |

### 1.3 模型架构变体

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `encoder-only-architecture` | Encoder-Only (BERT 系列) | ⭐⭐⭐ |
| `decoder-only-architecture` | Decoder-Only (GPT 系列) | ⭐⭐⭐ |
| `encoder-decoder-architecture` | Encoder-Decoder (T5, BART) | ⭐⭐⭐ |
| `mixture-of-experts` | MoE 混合专家架构详解 | ⭐⭐⭐⭐⭐ |
| `state-space-models` | SSM (Mamba) 状态空间模型 | ⭐⭐⭐⭐ |

### 1.4 主流模型解读

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `llama-architecture` | LLaMA 模型架构详解 | ⭐⭐⭐⭐ |
| `gpt-architecture` | GPT-2/3/4 架构演进 | ⭐⭐⭐⭐ |
| `mistral-architecture` | Mistral 7B 技术分析 | ⭐⭐⭐⭐ |
| `qwen-architecture` | Qwen 模型架构解读 | ⭐⭐⭐⭐ |
| `deepseek-architecture` | DeepSeek MoE 架构 | ⭐⭐⭐⭐⭐ |

---

## 🏋️ 二、训练篇 (Training)

### 2.1 预训练 (Pre-training)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `llm-pretraining-from-scratch` | 从零开始预训练 LLM | ⭐⭐⭐⭐⭐ |
| `tokenizer-training` | BPE/WordPiece 分词器训练 | ⭐⭐⭐ |
| `dataset-processing` | 大规模数据集处理 (湖仓架构) | ⭐⭐⭐⭐ |
| `curation-quality` | 数据清洗与质量控制 | ⭐⭐⭐⭐ |
| `dynamic-batching` | 动态批处理策略 | ⭐⭐⭐⭐ |

### 2.2 分布式训练 (Distributed Training)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `data-parallel-training` | Data Parallel 实战 | ⭐⭐⭐⭐ |
| `tensor-parallel-training` | Tensor Parallel 详解 | ⭐⭐⭐⭐⭐ |
| `pipeline-parallel-training` | Pipeline Parallel 实现 | ⭐⭐⭐⭐⭐ |
| `zero-redundancy-optimizer` | ZeRO 优化器原理与实践 | ⭐⭐⭐⭐⭐ |
| `fsdp-training` | FSDP 全分片数据并行 | ⭐⭐⭐⭐⭐ |
| `mixed-precision-training` | 混合精度训练 (FP16/BF16/FP8) | ⭐⭐⭐⭐ |
| `gradient-checkpointing` | 梯度检查点节省显存 | ⭐⭐⭐⭐ |
| `distributed-training-trainer` | DeepSpeed / Megatron-LM 实战 | ⭐⭐⭐⭐⭐ |

### 2.3 有监督微调 (SFT)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `sft-fundamentals` | SFT 基础与最佳实践 | ⭐⭐⭐ |
| `lora-fine-tuning` | LoRA 低秩适配微调 | ⭐⭐⭐⭐ |
| `q-lora-tuning` | QLoRA 高效微调 | ⭐⭐⭐⭐ |
| `adalora-fine-tuning` | AdaLoRA 自适应秩分配 | ⭐⭐⭐⭐⭐ |
| `long-context-finetuning` | 长上下文微调技术 | ⭐⭐⭐⭐ |
| `instruction-formatting` | Instruction 格式设计 | ⭐⭐⭐ |

### 2.4 对齐训练 (Alignment)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `rlhf-introduction` | RLHF 人类反馈强化学习 | ⭐⭐⭐⭐ |
| `reward-model-training` | 奖励模型训练 | ⭐⭐⭐⭐ |
| `ppo-training` | PPO 算法实现与调优 | ⭐⭐⭐⭐⭐ |
| `dpo-training` | DPO 直接偏好优化 | ⭐⭐⭐⭐ |
| `kto-training` | KTO 认知权衡优化 | ⭐⭐⭐⭐ |
| `orpo-training` | ORPO 反对率优化 | ⭐⭐⭐⭐ |
| `constitutional-ai` | Constitutional AI 对齐方法 | ⭐⭐⭐⭐⭐ |

### 2.5 训练基础设施

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `training-cluster-setup` | GPU 集群配置与管理 | ⭐⭐⭐⭐ |
| `fault-tolerance-training` | 训练容错与检查点 | ⭐⭐⭐⭐⭐ |
| `hyperparameter-tuning` | 超参数调优策略 | ⭐⭐⭐⭐ |
| `learning-rate-scheduler` | 学习率调度器对比 | ⭐⭐⭐⭐ |

---

## 🚀 三、推理篇 (Inference)

### 3.1 推理引擎

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `vllm-inference` | vLLM 高吞吐量推理 | ⭐⭐⭐⭐ |
| `text-generation-inference` | TGI 部署实战 | ⭐⭐⭐⭐ |
| `lightllm-inference` | LightLLM 轻量推理 | ⭐⭐⭐⭐ |
| `llama-cpp-inference` | llama.cpp CPU 推理 | ⭐⭐⭐ |
| `gptq-inference` | GPTQ 量化推理 | ⭐⭐⭐⭐ |
| `awq-inference` | AWQ 激活感知量化 | ⭐⭐⭐⭐ |

### 3.2 推理优化技术

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `continuous-batching` | Continuous Batching 详解 | ⭐⭐⭐⭐⭐ |
| `paged-attention` | PagedAttention 内存管理 | ⭐⭐⭐⭐⭐ |
| `speculative-decoding` | 投机解码加速推理 | ⭐⭐⭐⭐⭐ |
| `prefix-caching` | 前缀缓存优化 | ⭐⭐⭐⭐ |
| `kv-cache-optimization` | KV Cache 优化策略 | ⭐⭐⭐⭐ |
| `tensor-parallel-inference` | 推理 Tensor Parallel | ⭐⭐⭐⭐ |

### 3.3 推理服务化

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `openai-compatible-api` | OpenAI 兼容 API 部署 | ⭐⭐⭐ |
| `batch-inference` | 批量推理处理 | ⭐⭐⭐⭐ |
| `streaming-inference` | 流式输出实现 | ⭐⭐⭐ |
| `multi-model-serving` | 多模型服务编排 | ⭐⭐⭐⭐ |
| `inference-load-balancing` | 推理负载均衡 | ⭐⭐⭐⭐ |

---

## ⚡ 四、优化篇 (Optimization)

### 4.1 量化 (Quantization)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `fp8-quantization` | FP8 量化原理与实践 | ⭐⭐⭐⭐⭐ |
| `int8-quantization` | INT8 量化实战 | ⭐⭐⭐⭐ |
| `int4-quantization` | INT4 量化技术 | ⭐⭐⭐⭐ |
| `gptq-quantization` | GPTQ 后训练量化 | ⭐⭐⭐⭐ |
| `awq-quantization` | AWQ 激活感知量化 | ⭐⭐⭐⭐ |
| `bnb-quantization` | BitsAndBytes 量化 | ⭐⭐⭐⭐ |
| `quip-quantization` | QuIP 最近量子化 | ⭐⭐⭐⭐⭐ |
| `quantization-evaluation` | 量化效果评估与选择 | ⭐⭐⭐⭐ |

### 4.2 剪枝 (Pruning)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `magnitude-pruning` | 幅度剪枝实现 | ⭐⭐⭐ |
| `wanda-pruning` | Wanda 结构化剪枝 | ⭐⭐⭐⭐⭐ |
| `sparsegpt-pruning` | SparseGPT 一次性剪枝 | ⭐⭐⭐⭐⭐ |
| ` JamCut-bruning` | JamCut 剪枝方法 | ⭐⭐⭐⭐⭐ |
| `pruning-recovery` | 剪枝后恢复训练 | ⭐⭐⭐⭐ |

### 4.3 知识蒸馏 (Distillation)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `knowledge-distillation` | 经典知识蒸馏 | ⭐⭐⭐⭐ |
| `minimax-distillation` | MiniMax 洛希模型 | ⭐⭐⭐⭐⭐ |
| `gdm-distillation` | GDM 通用蒸馏方法 | ⭐⭐⭐⭐ |
| `self-distillation` | 自蒸馏实战 | ⭐⭐⭐⭐ |
| `multi-teacher-distillation` | 多教师蒸馏 | ⭐⭐⭐⭐⭐ |

### 4.4 编译优化 (Compilation)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `torch.compile` | PyTorch 编译优化 | ⭐⭐⭐⭐ |
| `tensorrt-inference` | TensorRT 推理加速 | ⭐⭐⭐⭐ |
| `onnx-optimization` | ONNX 模型优化 | ⭐⭐⭐⭐ |
| `tvm- compilation` | TVM 自动编译调优 | ⭐⭐⭐⭐⭐ |
| `flashinfer-kernel` | FlashInfer CUDA Kernel 优化 | ⭐⭐⭐⭐⭐ |

---

## 📚 五、应用篇 (Application)

### 5.1 RAG (Retrieval-Augmented Generation)

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `rag-fundamentals` | RAG 基础架构 | ⭐⭐⭐ |
| `rag-retrieval-optimization` | 检索优化技术 | ⭐⭐⭐⭐ |
| `rag-chunking-strategies` | 文档分块策略 | ⭐⭐⭐⭐ |
| `hybrid-search` | 混合搜索实战 | ⭐⭐⭐⭐ |
| `reranking-optimization` | 重排序优化 | ⭐⭐⭐⭐ |
| `rag-evaluation` | RAG 效果评估 | ⭐⭐⭐⭐ |
| `multi-modal-rag` | 多模态 RAG | ⭐⭐⭐⭐⭐ |
| `graph-rag` | Graph RAG 知识图谱增强 | ⭐⭐⭐⭐⭐ |

### 5.2 Function Calling / Tool Use

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `function-calling-basics` | Function Calling 基础 | ⭐⭐⭐ |
| `tool-schema-design` | 工具 schema 设计 | ⭐⭐⭐⭐ |
| `multi-tool-orchestration` | 多工具编排 | ⭐⭐⭐⭐ |
| `tool-choice-strategies` | 工具选择策略 | ⭐⭐⭐⭐ |

### 5.3 Prompt Engineering

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `prompt-patterns` | 高级 Prompt 模式 | ⭐⭐⭐ |
| `chain-of-thought` | CoT 思维链 | ⭐⭐⭐⭐ |
| `tree-of-thought` | ToT 思维树 | ⭐⭐⭐⭐ |
| `few-shot-learning` | Few-shot 学习技巧 | ⭐⭐⭐ |
| `prompt-injection-defense` | Prompt 注入防御 | ⭐⭐⭐⭐ |

### 5.4 向量数据库

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `vector-database-comparison` | 向量数据库对比 (Milvus/Pinecone/Qdrant) | ⭐⭐⭐ |
| `embedding-model-selection` | Embedding 模型选择 | ⭐⭐⭐⭐ |
| `approximate-nearest-neighbor` | ANN 算法原理 | ⭐⭐⭐⭐⭐ |
| `vector-index-optimization` | 向量索引优化 | ⭐⭐⭐⭐ |

---

## 🤖 六、Agentic 工程篇 (Agentic AI)

### 6.1 Agent 核心范式

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `react-agent` | ReAct 推理+行动框架 | ⭐⭐⭐⭐ |
| `plan-and-execute` | Plan-and-Execute 模式 | ⭐⭐⭐⭐ |
| `reflexion-agent` | Reflexion 自我反思 | ⭐⭐⭐⭐⭐ |
| `self-ask-agent` | Self-Ask 自我提问 | ⭐⭐⭐⭐ |
| `chain-of-thought-agent` | CoT Agent 实现 | ⭐⭐⭐⭐ |

### 6.2 Multi-Agent 系统

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `multi-agent-collaboration` | 多智能体协作 | ⭐⭐⭐⭐ |
| `multi-agent-competition` | 多智能体竞争 | ⭐⭐⭐⭐ |
| `agent-hierarchy` | 智能体层级架构 | ⭐⭐⭐⭐⭐ |
| `agent-debate` | 智能体辩论系统 | ⭐⭐⭐⭐⭐ |
| `agent-swarm` | Agent Swarm 大规模协作 | ⭐⭐⭐⭐⭐ |

### 6.3 Memory 系统

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `short-term-memory` | 短期记忆实现 | ⭐⭐⭐ |
| `long-term-memory` | 长期记忆系统 | ⭐⭐⭐⭐ |
| `semantic-memory` | 语义记忆管理 | ⭐⭐⭐⭐ |
| `episodic-memory` | 情景记忆系统 | ⭐⭐⭐⭐⭐ |
| `memory-consolidation` | 记忆整合与检索 | ⭐⭐⭐⭐⭐ |

### 6.4 Agent 工具生态

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `web-search-agent` | 网页搜索智能体 | ⭐⭐⭐⭐ |
| `code-execution-agent` | 代码执行智能体 | ⭐⭐⭐⭐ |
| `file-operations-agent` | 文件操作智能体 | ⭐⭐⭐⭐ |
| `api-integration-agent` | API 集成智能体 | ⭐⭐⭐⭐ |
| `database-query-agent` | 数据库查询智能体 | ⭐⭐⭐⭐ |

### 6.5 Agent 框架

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `langchain-agent` | LangChain Agent 开发 | ⭐⭐⭐⭐ |
| `llamaindex-agent` | LlamaIndex Agent 开发 | ⭐⭐⭐⭐ |
| `crewai-multi-agent` | CrewAI 多智能体框架 | ⭐⭐⭐⭐ |
| `autogen-agent` | AutoGen 多智能体框架 | ⭐⭐⭐⭐ |
| `swarm-agent` | OpenAI Swarm 框架 | ⭐⭐⭐⭐ |

---

## 🧪 七、Harness 工程篇 (Harness Engineering)

### 7.1 Eval Harness 框架

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `lm-evaluation-harness` | LM-Evaluation-Harness 实战 | ⭐⭐⭐⭐ |
| `big-bench-evaluation` | Big Bench 评估体系 | ⭐⭐⭐⭐ |
| `helicone-evaluation` | Helicone 评估平台 | ⭐⭐⭐ |
| `promptfoo-evaluation` | Promptfoo 自动化评估 | ⭐⭐⭐⭐ |

### 7.2 测试框架

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `llm-unit-testing` | LLM 单元测试框架 | ⭐⭐⭐ |
| `llm-integration-testing` | LLM 集成测试 | ⭐⭐⭐⭐ |
| `llm-e2e-testing` | LLM 端到端测试 | ⭐⭐⭐⭐ |
| `regression-testing` | 回归测试体系建设 | ⭐⭐⭐⭐ |
| `fuzz-testing-llm` | LLM 模糊测试 | ⭐⭐⭐⭐⭐ |

### 7.3 Benchmark 平台

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `open-llm-leaderboard` | Open LLM Leaderboard 分析 | ⭐⭐⭐⭐ |
| `chatbot-arena` | Chatbot Arena 原理 | ⭐⭐⭐⭐ |
| `live-code-bench` | Live Code Bench 实时评测 | ⭐⭐⭐⭐⭐ |
| `mmlu-pro-bench` | MMLU-Pro 高难度评测 | ⭐⭐⭐⭐⭐ |

---

## 📏 八、评估测评篇 (Evaluation)

### 8.1 基础评测基准

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `mmlu-evaluation` | MMLU 多任务语言理解 | ⭐⭐⭐⭐ |
| `mmlu-pro-evaluation` | MMLU-Pro 高难度评测 | ⭐⭐⭐⭐⭐ |
| `humaneval-evaluation` | HumanEval 代码评测 | ⭐⭐⭐⭐ |
| `mbpp-evaluation` | MBPP 编程基础评测 | ⭐⭐⭐⭐ |
| `math-evaluation` | MATH 数学评测 | ⭐⭐⭐⭐⭐ |

### 8.2 高级评测基准

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `bbh-evaluation` | BBH BIG-Bench Hard | ⭐⭐⭐⭐⭐ |
| `gsm8k-evaluation` | GSM8K 数学推理 | ⭐⭐⭐⭐ |
| `gpqa-evaluation` | GPQA 研究生水平评测 | ⭐⭐⭐⭐⭐ |
| `arc-c-evaluation` | ARC-Challenge 科学推理 | ⭐⭐⭐⭐ |
| `truthfulqa-evaluation` | TruthfulQA 真实性评测 | ⭐⭐⭐⭐ |

### 8.3 对话评测

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `mt-bench-evaluation` | MT-Bench 多轮对话 | ⭐⭐⭐⭐ |
| `alpaca-farm-evaluation` | AlpacaFarm 对话评估 | ⭐⭐⭐⭐ |
| `vicuna-bench` | Vicuna Bench 对话评估 | ⭐⭐⭐⭐ |
| `llms-full-spectrum` | LLM 全谱系评测 | ⭐⭐⭐⭐⭐ |

### 8.4 安全与对齐评测

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `safety-evaluation` | Safety 安全性评测 | ⭐⭐⭐⭐ |
| `toxicity-evaluation` | Toxicity 有害内容检测 | ⭐⭐⭐⭐ |
| `bias-evaluation` | Bias 偏见评测 | ⭐⭐⭐⭐ |
| `fairness-evaluation` | Fairness 公平性评测 | ⭐⭐⭐⭐ |
| `privacy-evaluation` | Privacy 隐私保护评测 | ⭐⭐⭐⭐⭐ |

### 8.5 评测方法论

| 案例名称 | 描述 | 难度 |
|----------|------|------|
| `llm-as-judge` | LLM-as-a-Judge 评估法 | ⭐⭐⭐⭐ |
| `pairwise-comparison` | 成对比较评估 | ⭐⭐⭐⭐ |
| `calibration-evaluation` | 校准度评估 | ⭐⭐⭐⭐ |
| `robustness-evaluation` | 对抗鲁棒性评估 | ⭐⭐⭐⭐⭐ |

---

## 📁 目录结构

```
ai-ml/
├── llm/
│   ├── architecture/          # 架构篇
│   │   ├── transformer-scratch/
│   │   ├── multi-head-attention/
│   │   ├── flash-attention/
│   │   ├── rotary-embedding/
│   │   ├── mixture-of-experts/
│   │   └── [10+ more]
│   │
│   ├── training/              # 训练篇
│   │   ├── llm-pretraining-from-scratch/
│   │   ├── distributed-training/
│   │   ├── sft-fundamentals/
│   │   ├── lora-fine-tuning/
│   │   ├── rlhf-introduction/
│   │   └── [15+ more]
│   │
│   ├── inference/             # 推理篇
│   │   ├── vllm-inference/
│   │   ├── text-generation-inference/
│   │   ├── continuous-batching/
│   │   ├── speculative-decoding/
│   │   └── [10+ more]
│   │
│   ├── optimization/         # 优化篇
│   │   ├── fp8-quantization/
│   │   ├── int4-quantization/
│   │   ├── wanda-pruning/
│   │   ├── knowledge-distillation/
│   │   └── [10+ more]
│   │
│   ├── application/           # 应用篇
│   │   ├── rag-fundamentals/
│   │   ├── hybrid-search/
│   │   ├── function-calling/
│   │   ├── chain-of-thought/
│   │   └── [10+ more]
│   │
│   ├── agentic/              # Agentic 工程篇
│   │   ├── react-agent/
│   │   ├── multi-agent-collaboration/
│   │   ├── memory-systems/
│   │   ├── langchain-agent/
│   │   └── [10+ more]
│   │
│   ├── harness/              # Harness 工程篇
│   │   ├── lm-evaluation-harness/
│   │   ├── llm-testing-framework/
│   │   └── [8+ more]
│   │
│   └── evaluation/           # 评估测评篇
│       ├── mmlu-evaluation/
│       ├── humaneval-evaluation/
│       ├── mt-bench-evaluation/
│       ├── safety-evaluation/
│       └── [10+ more]
```

---

## 🎯 实现优先级

### Phase 1: 核心基础 (2026 Q3)
1. 架构篇核心案例 (Transformer, Attention, RoPE)
2. 训练篇基础 (SFT, LoRA, 分布式训练)
3. 推理篇核心 (vLLM, TGI, Continuous Batching)

### Phase 2: 能力扩展 (2026 Q4)
1. Agentic 工程完整体系
2. RAG 与应用实战
3. 评估测评体系

### Phase 3: 高级优化 (2027 Q1)
1. RLHF/DPO 等对齐技术
2. 量化压缩高级技术
3. Multi-Agent 复杂系统

---

## 📝 命名规范

每个案例遵循以下命名规范：
- 使用 kebab-case (如 `llm-pretraining-from-scratch`)
- 前缀统一为 `llm-` 或具体领域前缀
- 避免使用缩写，保持清晰可读

---

*最后更新: 2026-06-01*
