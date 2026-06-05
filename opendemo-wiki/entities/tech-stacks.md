---
title: Technology Stacks
category: entities
tags: [technology, programming, infrastructure]
sources: [/Users/allengaller/Documents/GitHub/opendemo-work/opendemo/README.md, /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/DETAILED_STRUCTURE.md]
summary: The 12 technology stacks covered by OpenDemo, including 4 programming language stacks (288 cases), 5 infrastructure stacks (154 cases), and 2 operations/security stacks (41 cases).
provenance:
  extracted: 0.9
  inferred: 0.1
  ambiguous: 0.0
base_confidence: 0.75
lifecycle: draft
lifecycle_changed: 2026-06-03
tier: core
created: 2026-06-03T05:33:46Z
updated: 2026-06-03T05:33:46Z
---

# Technology Stacks

OpenDemo covers 12 major technology stacks organized into three categories.

## Programming Languages (4 stacks, 288 cases)

### Go (93 cases)
Microservices architecture, concurrent programming, cloud-native tools, CLI development, design patterns, performance optimization, testing practices.

### Java (70 cases)
Spring ecosystem complete coverage, microservices, distributed systems, GoF design patterns, DDD, TDD, JVM internals.

### Node.js (70 cases)
Express/NestJS full-stack development, real-time applications, design patterns, asynchronous programming, testing frameworks.

### Python (55 cases)
Django/FastAPI web development, data science, design patterns, pytest TDD, performance optimization.

## AI/ML (1 stack, 120+ cases)

### LLM/AI (120+ cases)
Covers 8 major domains:
- **Architecture**: Transformer, Attention, RoPE, MoE, SSM
- **Training**: Pretraining, SFT, RLHF, LoRA, distributed training
- **Inference**: vLLM, TGI, Continuous Batching, Speculative Decoding
- **Optimization**: Quantization (FP8/INT4), pruning, distillation
- **Application**: RAG, Function Calling, Prompt Engineering
- **Agentic**: ReAct, Multi-Agent, Memory, Agent frameworks
- **Harness**: Eval Harness, Testing Framework, Benchmark
- **Evaluation**: MMLU, HumanEval, BBH, MT-Bench, Safety

## Infrastructure (5 stacks, 154 cases)

### Kubernetes (80 cases)
Container orchestration, service mesh (Istio/Linkerd/Cilium), GitOps (ArgoCD/Flux), multi-cluster (Karmada), security (Falco/OPA), Serverless (Knative), storage (Rook Ceph/Longhorn), chaos engineering.

### Database (37 cases)
SQL (MySQL/PostgreSQL), NoSQL (MongoDB/Redis), performance optimization, high availability, sharding clusters.

### Networking (15 cases)
TCP/IP protocol, virtual private networks, protocol analysis, network security, BGP routing.

### KVM (11 cases)
Virtualization, performance tuning, high availability architecture, backup and recovery, VM templates.

### Virtualization (11 cases)
Docker vs VM comparison, containerd runtime, namespace isolation, Kata containers, LXC system containers.

## Operations & Security (2 stacks, 41 cases)

### SRE (10 cases)
SLO/SLI management, error budgets, chaos engineering, incident management, postmortem analysis, capacity planning, runbook automation, canary deployment, feature flags.

### Security (31 cases)
- **Full Disk Encryption**: LUKS, BitLocker, FileVault, encryption algorithms (AES/XTS/ChaCha20)
- **Trusted Computing**: TPM 2.0, HSM, secure boot, measured boot, remote attestation
- **Key Management**: HashiCorp Vault, AWS/Azure/GCP KMS, key rotation
- **Cloud Security**: Cloud FDE, BYOK/HYOK, automated encryption
- **Compliance**: GDPR, HIPAA, PCI-DSS, SOC2, automated compliance checking

## Distribution

```
Programming Languages  ████████████████████████████  288 cases (62%)
Infrastructure        ████████████████████          154 cases (33%)
Operations/Security    ███                            41 cases (5%)
```

## Related

- [[references/opendemo-project]] — Project overview
- [[concepts/five-star-standard]] — Quality standard
- [[concepts/vibe-coding]] — Learning methodology using these stacks
