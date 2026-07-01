<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Distributed Training 分布式训练

> 本案例详解 LLM 分布式训练技术：Data Parallel、Tensor Parallel、Pipeline Parallel

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    分布式训练策略对比                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Data Parallel (DP):                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  GPU 0: [Model] ──── gradient ──── sync ────→          │   │
│  │  GPU 1: [Model] ──── gradient ──── sync ────→          │   │
│  │  GPU 2: [Model] ──── gradient ──── sync ────→          │   │
│  │  GPU 3: [Model] ──── gradient ──── sync ────→          │   │
│  │  (每个 GPU 有完整模型副本)                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Tensor Parallel (TP):                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │       Layer N                                            │   │
│  │  ┌────┐  ┌────┐  ┌────┐  ┌────┐                      │   │
│  │  │ W0 │  │ W1 │  │ W2 │  │ W3 │  ← 分列切割         │   │
│  │  └────┘  └────┘  └────┘  └────┘                      │   │
│  │     ↓        ↓        ↓        ↓                        │   │
│  │   AllReduce AllReduce AllReduce AllReduce                │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Pipeline Parallel (PP):                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  GPU 0: Layer 0-12   → GPU 1: Layer 13-24  →          │   │
│  │  GPU 2: Layer 25-36  → GPU 3: Layer 37-48            │   │
│  │  (每个 GPU 只有部分层)                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

DeepSpeed ZeRO 优化:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ZeRO Stage 0: 无优化 (DDP)                                    │
│  ZeRO Stage 1: 分片 optimizer states                           │
│  ZeRO Stage 2: + 分片 gradients                               │
│  ZeRO Stage 3: + 分片 parameters                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### DeepSpeed 配置

```json
{
  "train_batch_size": 32,
  "gradient_accumulation_steps": 4,
  "fp16": {"enabled": true},
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {"device": "cpu"},
    "offload_param": {"device": "cpu"},
    "overlap_comm": true,
    "contiguous_gradients": true
  }
}
```

### 训练启动

```bash
deepspeed --num_gpus=8 train.py \
    --model_name meta-llama/Llama-2-70b-hf \
    --deepspeed_config ds_config.json
```

## 🔗 相关案例

- `llm-pretraining-scratch` - 预训练基础
- `lora-fine-tuning` - LoRA 微调
- `flash-attention` - Flash Attention

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
python code/main.py
```
