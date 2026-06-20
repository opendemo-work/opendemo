# 大模型 (LLM) 技术栈缺口分析与补齐路线

> 本文档汇总 OpenDemo LLM 技术栈当前已落地 demo 清单、已识别缺口，以及后续高质量补齐计划。
> 
> **生成时间**: 2026-06-16  
> **对应目录**: `opendemo/ai-ml/llm/`
> **最新补齐**: 2026-06-16 新增 4 个 demo（`data-curation-pipeline`、`inference-engine-comparison`、`agentic-rag`、`ci-evaluation-harness`）

---

## 📊 当前落地状态

`ai-ml/llm/` 下已实际落地 **92 个 demo**，覆盖 8 大领域：

| 领域 | 英文 | 已落地数量 | 占比 | 代表 demo |
|------|------|-----------|------|-----------|
| **训练** | Training | 16 | 17.4% | `lora-fine-tuning`、`rlhf-introduction`、`dpo-training`、`q-lora-tuning`、`fsdp-training`、`llm-pretraining-scratch`、`data-curation-pipeline` |
| **优化** | Optimization | 12 | 13.0% | `fp8-quantization`、`int4-quantization`、`awq-quantization`、`gptq-quantization`、`knowledge-distillation`、`torch-compile` |
| **评估** | Evaluation | 11 | 12.0% | `mmlu-evaluation`、`humaneval-evaluation`、`mt-bench-evaluation`、`llm-as-judge`、`safety-evaluation`、`truthfulqa-evaluation` |
| **应用** | Application | 12 | 13.0% | `rag-fundamentals`、`function-calling`、`chain-of-thought`、`vector-database-comparison`、`few-shot-learning`、`prompt-patterns`、`agentic-rag` |
| **Agentic** | Agentic AI | 11 | 12.0% | `react-agent`、`langchain-agent`、`multi-agent-collaboration`、`plan-and-execute`、`reflexion-agent`、`web-search-agent` |
| **推理** | Inference | 11 | 12.0% | `vllm-inference`、`tgi-deployment`、`speculative-decoding`、`continuous-batching`、`paged-attention`、`kv-cache-optimization`、`inference-engine-comparison` |
| **架构** | Architecture | 10 | 10.9% | `transformer-scratch`、`gpt-architecture`、`llama-architecture`、`flash-attention`、`mixture-of-experts`、`state-space-models` |
| **Harness** | Harness Engineering | 9 | 9.8% | `lm-evaluation-harness`、`open-llm-leaderboard`、`promptfoo-evaluation`、`llm-testing-framework`、`regression-testing`、`ci-evaluation-harness` |
| **总计** | | **92** | 100% | |

### 与目标差距

| 指标 | 当前 | 目标 | 缺口 |
|------|------|------|------|
| 总案例数 | 92 | 120+ | ~28+ |
| 五星覆盖率 | 100% | 100% | 保持 |
| 文档覆盖率 | 100% | 100% | 保持 |

---

## 🔍 已识别缺口清单

按优先级与领域分类的待补齐方向：

### 1. 架构 (Architecture)

| 缺口方向 | 优先级 | 说明 |
|----------|--------|------|
| KV 压缩 (KV Cache Compression) | 高 | 降低推理显存占用，含 GQA、MLA、量化 KV 等 |
| 专家路由可视化 (MoE Routing Visualization) | 中 | 展示 MoE 负载均衡与专家选择机制 |
| Mamba / RetNet 实战 | 中 | 非 Transformer 架构的替代方案 |
| 编码器-解码器架构 (Encoder-Decoder) | 中 | T5、BART 等 seq2seq 架构 |
| 位置编码对比 (ALiBi vs RoPE) | 低 | 系统对比主流位置编码方案 |

### 2. 训练 (Training)

| 缺口方向 | 优先级 | 说明 | 状态 |
|----------|--------|------|------|
| ~~数据清洗 Pipeline (Data Curation)~~ | 高 | 从原始语料到训练数据的完整处理流程 | ✅ 已补齐：`data-curation-pipeline` |
| Dora / RS-LoRA | 中 | 更高效的参数高效微调方法 | 待补齐 |
| 模型合并 (Model Soups / SLERP) | 中 | 多模型权重融合技术 | 待补齐 |
| 长上下文微调 (Long-Context Fine-tuning) | 中 | 位置编码外推、NTK-aware 训练 | 待补齐 |
| 故障容错训练 (Fault Tolerance) | 低 | 大规模训练中的 checkpoint 与恢复 | 待补齐 |

### 3. 推理 (Inference)

| 缺口方向 | 优先级 | 说明 | 状态 |
|----------|--------|------|------|
| ~~推理引擎对比 (vLLM vs TGI vs SGLang)~~ | 高 | 横向评测主流推理引擎 | ✅ 已补齐：`inference-engine-comparison` |
| 动态批调度 (Dynamic Batching) | 中 | 优化吞吐与延迟的调度策略 | 待补齐 |
| 前缀缓存工程化 (Prefix Caching) | 中 | 共享 prompt 前缀的缓存机制 | 待补齐 |
| 多模型服务编排 (Multi-Model Serving) | 中 | 同一集群部署多个模型的路由与资源分配 | 待补齐 |
| OpenAI 兼容 API 部署 | 低 | 标准化 API 接口封装 | 待补齐 |

### 4. 优化 (Optimization)

| 缺口方向 | 优先级 | 说明 |
|----------|--------|------|
| GGUF 量化与 llama.cpp 部署 | 高 | 端侧与 CPU 推理的完整流程 |
| SmoothQuant | 中 | 激活与权重联合量化 |
| AutoGPTQ | 中 | GPTQ 量化自动化工具 |
| ONNX / TensorRT-LLM 端到端 | 中 | 生产环境推理加速 |
| 多教师蒸馏 (Multi-Teacher Distillation) | 低 | 多模型知识迁移 |

### 5. 应用 (Application)

| 缺口方向 | 优先级 | 说明 | 状态 |
|----------|--------|------|------|
| ~~Agentic RAG~~ | 高 | Agent 与 RAG 结合的高级检索生成 | ✅ 已补齐：`agentic-rag` |
| Text2SQL | 中 | 自然语言转 SQL 的完整工作流 | 待补齐 |
| 代码生成工作流 (Code Generation Pipeline) | 中 | 从需求到代码生成的工程化实践 | 待补齐 |
| 多语言 RAG | 中 | 跨语言检索与生成 | 待补齐 |
| Graph RAG | 低 | 知识图谱增强 RAG | 待补齐 |
| 多模态 RAG | 低 | 图文混合检索 | 待补齐 |

### 6. Agentic

| 缺口方向 | 优先级 | 说明 |
|----------|--------|------|
| 工具调用安全 (Tool Calling Safety) | 高 | Agent 工具调用的权限控制与沙箱 |
| Agent 评估基准 | 中 | Agent 任务成功率、步骤效率评估 |
| 人机协作循环 (Human-in-the-Loop) | 中 | 人工介入与 Agent 迭代 |
| CrewAI 多智能体框架 | 中 | 角色扮演与任务委托 |
| AutoGen 多智能体框架 | 中 | 对话式多 Agent 编排 |
| OpenAI Swarm 框架 | 低 | 轻量级多 Agent 系统 |

### 7. 评估 (Evaluation)

| 缺口方向 | 优先级 | 说明 |
|----------|--------|------|
| BBH (BIG-Bench Hard) | 高 | 复杂推理能力评测 |
| Chatbot Arena | 中 | 人工偏好对战评测 |
| 自定义评估 Harness | 中 | 面向业务的私有评估框架 |
| 红队测试 (Red Teaming) | 中 | 安全对抗评测 |
| 隐私 / 偏见评测 | 低 | 公平性与隐私保护评估 |

### 8. Harness

| 缺口方向 | 优先级 | 说明 | 状态 |
|----------|--------|------|------|
| ~~CI 集成评估 (CI Evaluation)~~ | 高 | 将评估嵌入持续集成流程 | ✅ 已补齐：`ci-evaluation-harness` |
| A/B 测试框架 | 中 | 模型版本对比实验 | 待补齐 |
| 生产监控与回滚 | 中 | 线上模型性能监控与自动回滚 | 待补齐 |
| 模糊测试 (Fuzz Testing) | 低 | 输入扰动下的鲁棒性测试 | 待补齐 |

---

## 🗓️ 补齐路线

| 阶段 | 时间 | 目标 | 重点方向 |
|------|------|------|----------|
| **短期** | 2026 Q2 | 夯实基础 + 补齐高优先级缺口 | 数据清洗 Pipeline、推理引擎对比、Agentic RAG、BBH 评估、CI 集成评估、GGUF 量化 |
| **中期** | 2026 Q3-Q4 | 深化应用与 Agentic | Multi-Agent 框架实战、RAG 高级主题、Agent 评估、可视化评估 |
| **长期** | 2027 Q1 | 前沿与平台化 | 多模态大模型、MoE 训练、推理系统调度、企业级 LLMOps、在线实验环境配套 |

---

## ✅ 验收标准

每个新补齐的 demo 需满足 OpenDemo 五星标准：

1. `README.md` ≥ 3000 字符，含架构图、代码示例、学习要点
2. `metadata.json` 完整且格式正确
3. 代码可运行，附运行说明
4. 包含测试或验证脚本
5. 中文注释与文档

---

## 📚 相关文档

- [`LLM_TECH_STACK_PLAN.md`](./LLM_TECH_STACK_PLAN.md) — 完整技术栈规划
- [`README.md`](./README.md) — LLM 技术栈入口说明
- [项目级 `README.md`](../../README.md) — OpenDemo 全局介绍

---

*最后更新：2026-06-16*
