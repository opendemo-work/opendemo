# OpenDemo 技术演示平台 🚀

## 🎯 项目简介

OpenDemo 是一个综合性技术学习和演示平台，涵盖多种主流编程语言、基础设施、运维实践和安全技术的实战案例。本项目致力于提供高质量的技术示例和最佳实践指南，帮助开发者快速掌握各种技术栈的核心概念和实际应用。

> **项目规模**: 959 个技术演示案例 | **覆盖技术栈**: 18 大类别 | **全部达成五星标准** ⭐⭐⭐⭐⭐

---

## 🌟 项目里程碑

### 🎉 全项目五星达成 (2026-07-01)

我们激动地宣布：OpenDemo 所有 **18** 个技术栈、**959** 个有效案例全部达到 **⭐⭐⭐⭐⭐ 五星标准**！

```
五星标准定义:
✅ 每个案例均包含 metadata.json 且符合 schema 1.0
✅ README.md 长度 ≥ 3000 字符，含学习目标、快速开始、核心概念、代码示例
✅ 至少包含一个可运行产物（脚本 / YAML / 代码 / 测试）
✅ README 引用的本地文件真实存在
✅ 目录非空壳，除 README 和 metadata 外还有其他实质文件
```

---

## ⚠️ 生产环境安全声明

OpenDemo 中的命令和脚本主要用于**学习、测试和演示**。为了保障生产环境安全：

- 所有代码块均已标注风险等级：**🔴 高风险** / **🟡 中风险** / **🟢 低风险**
- 🔴 **高风险**命令可能导致数据丢失、服务中断或不可逆破坏，**禁止在生产环境直接执行**
- 🟡 **中风险**命令会修改环境状态，请在隔离测试环境先验证
- 🟢 **低风险**命令通常为只读操作，可安全在学习环境中执行

> 详细安全使用指南请参阅：[docs/guides/PRODUCTION-SAFETY.md](./docs/guides/PRODUCTION-SAFETY.md)

---

## 📊 技术栈全景图

| 技术栈 | 案例数 | 星级 | 核心内容 |
|--------|--------|------|----------|
| **Go** | 97 | ⭐⭐⭐⭐⭐ | 系统编程、微服务、云原生工具 |
| **Java** | 108 | ⭐⭐⭐⭐⭐ | 企业级开发、Spring生态、微服务 |
| **Node.js** | 83 | ⭐⭐⭐⭐⭐ | 全栈开发、API设计、实时应用 |
| **Python** | 60 | ⭐⭐⭐⭐⭐ | AI/ML、数据科学、自动化脚本 |
| **AI/ML** | 15 | ⭐⭐⭐⭐⭐ | 机器学习、深度学习、MLOps、AutoML |
| **LLM** | 96+ | ⭐⭐⭐⭐⭐ | 大模型架构、训练、推理、优化、应用、Agentic、Harness、评估 |
| **Database** | 37 | ⭐⭐⭐⭐⭐ | SQL/NoSQL、性能优化、高可用 |
| **Kubernetes** | 84 | ⭐⭐⭐⭐⭐ | 容器编排、云原生、可观测性 |
| **Networking** | 15 | ⭐⭐⭐⭐⭐ | TCP/IP、协议分析、网络安全 |
| **KVM** | 11 | ⭐⭐⭐⭐⭐ | 虚拟化、性能调优、高可用 |
| **Virtualization** | 11 | ⭐⭐⭐⭐⭐ | 容器、虚拟机、隔离技术 |
| **Container** | 14 | ⭐⭐⭐⭐⭐ | Docker、containerd、runc、容器网络与存储 |
| **Linux** | 18 | ⭐⭐⭐⭐⭐ | 系统管理、性能监控、网络工具、Shell 脚本 |
| **SRE** | 10 | ⭐⭐⭐⭐⭐ | 可靠性工程、混沌工程、事件管理 |
| **Security** | 31 | ⭐⭐⭐⭐⭐ | FDE全盘加密、合规审计、云安全、密钥管理 |
| **Monitoring** | 7 | ⭐⭐⭐⭐⭐ | Prometheus、Grafana、Kibana、可观测性 |
| **Messaging** | 5 | ⭐⭐⭐⭐⭐ | RocketMQ 生产者/消费者、延迟消息、事务消息 |
| **Traffic** | 8 | ⭐⭐⭐⭐⭐ | Nginx、HAProxy、Higress 负载均衡与网关 |
| **BigData** | 7 | ⭐⭐⭐⭐⭐ | Spark、Flink、ClickHouse、Kafka、数据仓库、数据湖 |

**总案例数: 959** | **文档覆盖率: 100%** | **元数据覆盖率: 100%** | **五星通过率: 100%**

---

## 🚀 快速入门

### 技术栈分类导航

#### 💻 编程语言 (4个栈)
- **[Go](./go/)** - 97个案例：微服务、并发编程、云原生工具
- **[Java](./java/)** - 108个案例：Spring Boot、微服务、分布式系统
- **[Node.js](./nodejs/)** - 83个案例：Express、NestJS、全栈开发
- **[Python](./python/)** - 60个案例：Django、FastAPI、数据科学

#### 🤖 AI/大模型 (2个栈)
- **[AI/ML](./ai-ml/)** - 15个案例：机器学习、深度学习、MLOps、AutoML
- **[LLM](./ai-ml/llm/)** - 96+个案例：大模型架构、训练、推理、优化、应用、Agentic、Harness、评估

#### 🏗️ 基础设施 (7个栈)
- **[Database](./database/)** - 37个案例：MySQL、PostgreSQL、MongoDB、Redis
- **[Kubernetes](./kubernetes/)** - 84个案例：容器编排、服务网格、GitOps
- **[Networking](./networking/)** - 15个案例：TCP/IP、HTTP/2、Wireshark
- **[KVM](./kvm/)** - 11个案例：虚拟化、性能调优、高可用架构
- **[Virtualization](./virtualization/)** - 11个案例：Docker、Kata、Namespace
- **[Container](./container/)** - 14个案例：Docker、containerd、runc
- **[Linux](./linux/)** - 18个案例：系统管理、性能监控、网络工具

#### 📊 数据与消息 (3个栈)
- **[BigData](./bigdata/)** - 7个案例：Spark、Flink、ClickHouse、Kafka
- **[Monitoring](./monitoring/)** - 7个案例：Prometheus、Grafana、Kibana
- **[Messaging](./messaging/)** - 5个案例：RocketMQ 消息队列

#### 🔧 运维与安全 (2个栈)
- **[SRE](./sre/)** - 10个案例：SLO管理、混沌工程、容量规划
- **[Security](./security/)** - 31个案例：FDE全盘加密、合规审计、云安全、密钥管理

#### 🌐 流量与网关 (1个栈)
- **[Traffic](./traffic/)** - 8个案例：Nginx、HAProxy、Higress 负载均衡与网关

---

## 🛠️ OpenDemo CLI 命令清单

### 主命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `get <language> <keywords...>` | 获取已有 demo；找不到时用 AI 生成 | `opendemo get python logging` |
| `search [language] [keywords...]` | 搜索 demo | `opendemo search python` |
| `new <language> <topic...>` | 创建新 demo | `opendemo new go goroutines` |
| `check` | 运行质量检查（单元测试 + CLI 测试） | `opendemo check -v` |
| `config` | 配置管理（含子命令） | `opendemo config set ai.api_key xxx` |

### `config` 子命令

| 子命令 | 说明 | 示例 |
|--------|------|------|
| `init` | 初始化配置 | `opendemo config init` |
| `set <key> <value>` | 设置配置项 | `opendemo config set ai.api_key sk-xxx` |
| `get <key>` | 获取配置项 | `opendemo config get ai.model` |
| `list` | 列出所有配置 | `opendemo config list` |

### 常用选项

- `--version`：显示版本（当前 `0.3.0`）
- `--verify`（`get` / `new`）：启用自动验证
- `--difficulty {beginner|intermediate|advanced}`（`new`）：指定生成难度

### 支持的语言

`python`、`java`、`go`、`nodejs`、`kubernetes`、`database`、`networking`、`kvm`、`virtualization`、`container`、`linux`、`sre`、`security`、`monitoring`、`messaging`、`traffic`、`bigdata`、`ai-ml`

---

## 📚 文档标准

### 五星案例文档规范

每个技术案例都包含以下标准化内容：

```
案例结构:
┌─────────────────────────────────────────┐
│ 1. 架构图 (ASCII艺术)                    │
│    - 系统架构、数据流程、组件关系         │
├─────────────────────────────────────────┤
│ 2. 核心概念解释                          │
│    - 原理说明、关键术语、设计思想         │
├─────────────────────────────────────────┤
│ 3. 配置与代码示例                        │
│    - 可运行的配置、完整代码片段           │
├─────────────────────────────────────────┤
│ 4. 命令速查表                            │
│    - 常用命令、参数说明、使用场景         │
├─────────────────────────────────────────┤
│ 5. 学习要点总结                          │
│    - 核心知识点、最佳实践、常见问题       │
└─────────────────────────────────────────┘

质量标准:
- README长度: ≥3000字符 (平均4500+)
- metadata.json: 完整元数据信息
- 代码可运行: 经过验证的配置和脚本
```

---

## 📈 项目统计

### 按类型分布

```
案例类型分布:
编程语言    ████████████████████████████  358个 (37%)
基础设施    ████████████████████          276个 (29%)
AI/LLM      ██████████████                111个 (12%)
数据与消息  ██████                         55个  (6%)
运维安全    ████                           41个  (4%)
容器与虚拟化 ███                           36个  (4%)
其他工具链   ██                            82个  (8%)
```

### 成长轨迹

| 时间节点 | Demo总数 | 里程碑 |
|----------|----------|--------|
| 2024年初 | 85 | 项目启动 |
| 2024年中 | 185 | 核心技术栈建立 |
| 2025年初 | 265 | AI/ML技术栈引入 |
| 2025年底 | 320 | 云原生深度扩展 |
| 2026-02 | 442 | **全五星标准达成** |
| 2026-04 | 518 | **FDE安全+编程专家+云原生架构** |
| 2026-07 | 959 | **18 个技术栈全项目五星达成** |

---

## 🎯 技术亮点

### 新领域突破 (2026 Q1)

#### 1. SRE (站点可靠性工程)
完整的SRE实践体系：
- **sre-fundamentals**: SRE核心原则与错误预算
- **slo-sli-management**: 服务级别目标管理
- **chaos-engineering**: Chaos Mesh混沌工程
- **incident-management**: 事件响应与指挥体系
- **capacity-planning**: 容量规划与预测

#### 2. Security (信息安全) - 31案例
全栈FDE与云安全技术覆盖：

**全磁盘加密 (FDE)**: LUKS, BitLocker, FileVault, 加密算法 (AES/XTS/ChaCha20), 密钥派生 (Argon2/PBKDF2)
**可信计算**: TPM 2.0, HSM硬件安全模块, 安全启动, 测量启动, 远程证明
**密钥管理**: HashiCorp Vault, AWS KMS, Azure Key Vault, GCP Cloud KMS, 密钥轮换
**云安全**: AWS/Azure/GCP云FDE, BYOK/HYOK, 云端密钥管理, 自动化加密
**合规与审计**: GDPR, HIPAA, PCI-DSS, SOC2, 数据分类, 自动化合规检测
**安全自动化**: Ansible加密部署, 自动化配置, 集中监控, 实时告警

经典案例:
- **fde-luks-production**: 企业级LUKS部署与密钥托管
- **fde-tpm-unified**: TPM+PIN统一安全架构
- **cloud-fde-aws**: AWS云实例全盘加密实践
- **compliance-automation-gdpr**: GDPR合规自动化检测
- **fde-field-automation**: 现场设备FDE自动化部署

---

## 🤖 大模型 (LLM) 技术栈 - 核心重点方向

> **后续主要重点**: 全面覆盖大模型的架构、训练、推理、优化、应用、Agentic、Harness、评估等 8 大领域

### 📊 LLM 技术栈全景

当前 `ai-ml/llm/` 下已落地 **92 个 demo**，覆盖 8 大领域：

| 领域 | 数量 | 代表 demo |
|------|------|-----------|
| **训练 (training)** | 16 | `lora-fine-tuning`、`rlhf-introduction`、`dpo-training`、`q-lora-tuning`、`fsdp-training`、`llm-pretraining-scratch`、`data-curation-pipeline` |
| **优化 (optimization)** | 13 | `fp8-quantization`、`int4-quantization`、`awq-quantization`、`gptq-quantization`、`knowledge-distillation`、`torch-compile`、`gguf-quantization` |
| **评估 (evaluation)** | 12 | `mmlu-evaluation`、`humaneval-evaluation`、`mt-bench-evaluation`、`llm-as-judge`、`safety-evaluation`、`truthfulqa-evaluation`、`bbh-evaluation` |
| **应用 (application)** | 13 | `rag-fundamentals`、`function-calling`、`chain-of-thought`、`vector-database-comparison`、`few-shot-learning`、`prompt-patterns`、`agentic-rag`、`text2sql` |
| **Agentic (agentic)** | 11 | `react-agent`、`langchain-agent`、`multi-agent-collaboration`、`plan-and-execute`、`reflexion-agent`、`web-search-agent` |
| **推理 (inference)** | 11 | `vllm-inference`、`tgi-deployment`、`speculative-decoding`、`continuous-batching`、`paged-attention`、`kv-cache-optimization`、`inference-engine-comparison` |
| **架构 (architecture)** | 11 | `transformer-scratch`、`gpt-architecture`、`llama-architecture`、`flash-attention`、`mixture-of-experts`、`state-space-models`、`kv-cache-compression` |
| **评测框架 (harness)** | 9 | `lm-evaluation-harness`、`open-llm-leaderboard`、`promptfoo-evaluation`、`llm-testing-framework`、`regression-testing`、`ci-evaluation-harness` |

### 🚀 快速开始

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 查看所有 LLM 案例
opendemo search llm

# 获取架构类案例
opendemo get llm transformer-scratch

# 获取训练类案例
opendemo get llm lora-fine-tuning

# 获取推理优化案例
opendemo get llm vllm-inference

# 获取 Agentic AI 案例
opendemo get llm react-agent
```

### 🎯 里程碑目标与补齐计划

当前 LLM 8 大领域已初步覆盖，近期已补齐 4 个高优先级缺口，剩余方向持续深化中。

| 阶段 | 时间 | 目标 | 计划新增/深化的 demo 方向 |
|------|------|------|---------------------------|
| **短期** | 2026 Q2 | 夯实基础 + 补齐缺口 | 增加基础预训练、数据工程、模型合并（model merging）、长上下文推理等 |
| **中期** | 2026 Q3-Q4 | 深化应用与 Agentic | RAG 高级主题（routing、agentic-rag）、Multi-Agent 编排框架（AutoGen、CrewAI）、可视化/可解释评估 |
| **长期** | 2027 Q1 | 前沿与平台化 | 多模态大模型、MoE 训练、推理系统调度、企业级 LLMOps、在线实验环境配套 |

### 本次补齐（2026-06-16）

- `training/data-curation-pipeline`：大模型数据清洗 Pipeline
- `inference/inference-engine-comparison`：vLLM / TGI / SGLang 推理引擎横向对比
- `application/agentic-rag`：Agentic RAG 架构与实现
- `harness/ci-evaluation-harness`：LLM CI 集成评估与质量门禁
- `architecture/kv-cache-compression`：KV Cache 压缩技术
- `optimization/gguf-quantization`：GGUF 量化与 llama.cpp 部署
- `evaluation/bbh-evaluation`：BBH 复杂推理评测
- `application/text2sql`：自然语言转 SQL

### 剩余缺口清单

- **架构**：~~KV 压缩~~ ✅；专家路由可视化、Mamba/RetNet 实战
- **训练**：~~数据清洗 pipeline~~ ✅；Dora/RS-LoRA、模型 soups
- **推理**：~~推理引擎对比~~ ✅；动态批调度、前缀缓存工程化
- **优化**：~~GGUF~~ ✅；SmoothQuant、AutoGPTQ、ONNX/TensorRT-LLM 端到端
- **应用**：~~Agentic RAG~~ ✅；~~Text2SQL~~ ✅；代码生成工作流、多语言 RAG
- **Agentic**：工具调用安全、Agent 评估基准、人机协作循环
- **评估**：~~BBH~~ ✅；Arena、自定义评估 Harness、红队测试
- **Harness**：~~CI 集成评估~~ ✅；A/B 测试框架、生产监控与回滚

---

## 🔐 安全说明

### 使用规范

```
学习环境:
✅ 仅用于技术学习和技能提升
✅ 在隔离环境(VM/容器)中运行示例
✅ 理解代码逻辑后再执行操作
✅ 定期清理测试产生的临时数据

生产环境:
⚠️ 必须进行充分的测试验证
⚠️ 遵循企业安全标准和合规要求
⚠️ 配置适当的监控和告警机制
⚠️ 建立完善的备份恢复方案
```

### 安全检查

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 项目提供安全扫描脚本
./scripts/security/run_full_scan.sh
./scripts/security/check_dependencies.sh
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献：

- 📝 **文档改进**: 完善现有案例的文档
- 💡 **新案例**: 添加新的技术演示
- 🐛 **Bug修复**: 报告和修复问题
- 🌐 **翻译**: 将文档翻译成其他语言

### 贡献标准

新案例需满足五星标准：
1. 完整的README.md (≥3000字符)
2. 完整的metadata.json
3. 包含架构图和代码示例
4. 经过本地测试验证

---

## 📚 学习路径推荐

### 路径1: 全栈开发工程师
```
Node.js/Python → Database → Kubernetes → SRE
```

### 路径2: 基础设施工程师
```
Linux → Networking → KVM → Kubernetes → Security
```

### 路径3: 云原生架构师
```
Go → Kubernetes → Networking → SRE → Security
```

### 路径4: 安全工程师
```
Security → Networking → Kubernetes SRE → 全栈
```

---

## 📞 联系我们

- **项目主页**: [GitHub Repository](https://github.com/yourusername/opendemo)
- **问题反馈**: [Issues](https://github.com/yourusername/opendemo/issues)
- **讨论交流**: [Discussions](https://github.com/yourusername/opendemo/discussions)

---

<p align="center">
  <strong>🌟 959 技术案例 | 18 个五星技术栈 | 100% 文档覆盖 | 100% 五星通过</strong><br><br>
  <strong>👨‍💻 欢迎贡献代码，一起打造最好的技术学习平台！</strong><br><br>
  <strong>如果这个项目对你有帮助，请给个 ⭐ Star 支持我们！</strong>
</p>

---

*最后更新：2026年7月1日*  
*版本: v2.2.0 - Full Quality Edition (全项目 959 个案例五星达成)*
