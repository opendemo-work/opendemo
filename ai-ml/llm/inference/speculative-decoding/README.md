# Speculative Decoding 投机解码

> 本案例详解 Speculative Decoding (推测解码) 原理，实现推理加速

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Speculative Decoding 流程                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  传统 Decoding (自回归):                                          │
│                                                                 │
│  Step 1: Q → Token_1                                           │
│  Step 2: Q + T1 → Token_2                                       │
│  Step 3: Q + T1 + T2 → Token_3                                  │
│  ...                                                            │
│  每个 Step 都需要完整 Attention 计算                               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Speculative Decoding:                                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Phase 1: Speculative (Draft Model 小模型快速生成)        │   │
│  │                                                          │   │
│  │  Q → t1 → t2 → t3 → t4  (Draft 模型快速生成 4 个 token)  │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Phase 2: Verification (Target 模型验证)                  │   │
│  │                                                          │   │
│  │  Target(Q + t1 + t2 + t3 + t4) → [p1, p2, p3, p4]      │   │
│  │  与 Draft 的 t1-t4 对比，接受/拒绝                        │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Phase 3: Output                                        │   │
│  │                                                          │   │
│  │  接受: t1, t2, t3  拒绝: t4, 生成: t5                   │   │
│  │  3 个 token 一次生成 + 1 个 新 token                     │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

算法细节:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Draft Model: 小模型 (如 7B)                                    │
│  Target Model: 大模型 (如 70B)                                   │
│                                                                 │
│  for i in range(draft_len):                                    │
│      # Draft 模型生成 k 个 token                                 │
│      t_i = draft_model.generate(Q + t_0..t_{i-1})              │
│                                                                 │
│      # Target 模型验证                                           │
│      p_i = target_model.forward(Q + t_0..t_{i})                 │
│                                                                 │
│      # 接受/拒绝决策                                            │
│      if accept(t_i, p_i):                                       │
│          accepted.append(t_i)                                   │
│      else:                                                      │
│          # 从 p_i 采样一个新 token                               │
│          t_new = sample(p_i)                                    │
│          accepted.append(t_new)                                 │
│          break                                                  │
│                                                                 │
│  return accepted                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

加速比分析:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  假设:                                                          │
│  - Draft 模型比 Target 快 10x                                    │
│  - 接受率 80%                                                   │
│                                                                 │
│  理想加速比 = Draft 速度 × 接受率                               │
│            = 10x × 0.8 = 8x                                    │
│                                                                 │
│  实际开销: Target 模型需要处理所有 draft tokens                  │
│  有效加速 ≈ Draft 速度 / 平均处理 token 数                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 核心概念

### 1. 为什么需要投机解码

```
传统 Decoding 问题:
- 每个 token 生成都需要完整 Transformer 前向
- KV Cache 很长时，Attention 计算量大
- GPU 利用率低（大量矩阵乘是小矩阵）

解决方案:
- 用小模型快速生成多个候选 token
- 大模型并行验证，一次性决定接受哪些
```

### 2. 接受策略

```python
def accept_token(draft_token, draft_prob, target_prob):
    """
    接受/拒绝策略
    draft_token: draft 模型生成的 token
    draft_prob: draft 模型给的概率
    target_prob: target 模型给的概率
    """
    
    # 策略 1: 贪婪接受
    # if draft_token == argmax(target_prob):
    #     accept
    
    # 策略 2: 概率接受 (常用)
    # 以 q(t)/p(t) 的概率接受
    ratio = draft_prob / (target_prob + 1e-10)
    if random.random() < ratio:
        accept
    else:
        reject
```

### 3. 自适应 draft 长度

```python
# 根据接受率动态调整 draft 长度
def get_adaptive_draft_len(accept_rate, base_len=4):
    if accept_rate > 0.9:
        return base_len + 2  # 增加
    elif accept_rate > 0.7:
        return base_len
    else:
        return max(1, base_len - 1)  # 减少
```

## 💻 完整实现

### 投机解码核心

```python
import torch
import torch.nn.functional as F
from typing import List, Tuple, Optional

class SpeculativeDecoder:
    """投机解码器"""
    
    def __init__(
        self,
        draft_model,
        target_model,
        tokenizer,
        draft_len: int = 4,
        temperature: float = 1.0,
    ):
        self.draft_model = draft_model
        self.target_model = target_model
        self.tokenizer = tokenizer
        self.draft_len = draft_len
        self.temperature = temperature
        
    @torch.no_grad()
    def generate(
        self,
        prompt_ids: torch.Tensor,
        max_new_tokens: int = 100,
        eos_token_id: int = None,
    ) -> List[int]:
        """生成文本"""
        
        target_model = self.target_model
        draft_model = self.draft_model
        
        # 初始输入
        input_ids = prompt_ids.clone()
        generated = []
        
        while len(generated) < max_new_tokens:
            
            # Phase 1: Draft 模型生成
            draft_tokens = []
            draft_probs = []
            
            for _ in range(self.draft_len):
                # Draft 前向
                draft_output = draft_model(input_ids)
                draft_logits = draft_output.logits[:, -1, :]
                
                if self.temperature > 0:
                    draft_probs_step = F.softmax(draft_logits / self.temperature, dim=-1)
                else:
                    draft_probs_step = F.softmax(draft_logits, dim=-1)
                
                # 采样
                draft_token = torch.multinomial(draft_probs_step, 1).squeeze(-1)
                draft_prob = draft_probs_step.gather(-1, draft_token.unsqueeze(-1)).squeeze(-1)
                
                draft_tokens.append(draft_token.item())
                draft_probs.append(draft_prob.item())
                
                # 如果是 EOS，停止
                if eos_token_id and draft_token.item() == eos_token_id:
                    break
                
                # 扩展输入
                input_ids = torch.cat([input_ids, draft_token.unsqueeze(0)], dim=-1)
            
            # Phase 2: Target 模型验证
            # 扩展 prompt 以包含 draft tokens
            target_output = target_model(input_ids)
            target_logits = target_output.logits[:, -len(draft_tokens):, :]
            
            if self.temperature > 0:
                target_probs = F.softmax(target_logits / self.temperature, dim=-1)
            else:
                target_probs = F.softmax(target_logits, dim=-1)
            
            # Phase 3: 接受/拒绝
            accepted = []
            for i, (draft_token, draft_prob) in enumerate(zip(draft_tokens, draft_probs)):
                target_prob = target_probs[:, i, draft_token].item()
                
                # 概率接受
                if draft_prob <= target_prob:
                    accepted.append(draft_token)
                else:
                    # 拒绝，从 target 分布采样
                    new_token = torch.multinomial(target_probs[:, i, :], 1).item()
                    accepted.append(new_token)
                    break
            
            generated.extend(accepted)
            
            # 更新 input_ids
            input_ids = torch.cat([input_ids, torch.tensor([accepted], device=input_ids.device)], dim=-1)
            
            # 检查是否生成 EOS
            if eos_token_id and accepted[-1] == eos_token_id:
                break
        
        return generated
```

### vLLM 投机解码

```python
# vLLM 支持投机解码
from vllm import LLM, SamplingParams

# 需要一个小模型作为 draft
llm = LLM(
    model="meta-llama/Llama-2-70b-hf",
    speculative_model="meta-llama/Llama-2-7b-hf",  # Draft 模型
    num_speculative_tokens=5,  # 每次投机 5 个 token
    tensor_parallel_size=4,
)

outputs = llm.generate(["Hello, world!"], SamplingParams(temperature=0.8))
```

### HuggingFace 实现

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from accelerate import init_empty_weights
import torch

def setup_speculative_decoding(
    target_model_name: str,
    draft_model_name: str,
):
    """设置投机解码"""
    
    tokenizer = AutoTokenizer.from_pretrained(target_model_name)
    
    # Target 模型 (大模型)
    target_model = AutoModelForCausalLM.from_pretrained(
        target_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Draft 模型 (小模型)
    draft_model = AutoModelForCausalLM.from_pretrained(
        draft_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    target_model.eval()
    draft_model.eval()
    
    return SpeculativeDecoder(
        draft_model=draft_model,
        target_model=target_model,
        tokenizer=tokenizer,
        draft_len=5,
    )
```

## 📊 性能对比

| 配置 | 延迟/Token | 吞吐量 | 加速比 |
|------|------------|---------|--------|
| 自回归 (70B) | 50ms | 20 tok/s | 1x |
| **Speculative (7B→70B)** | 15ms | 65 tok/s | **3-4x** |
| Speculative (13B→70B) | 20ms | 50 tok/s | 2.5x |

## 📋 命令速查

```bash
# vLLM 投机解码
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-70b-hf \
    --speculative-model meta-llama/Llama-2-7b-hf \
    --num-speculative-tokens 5

# 测试加速效果
python speculative_decoding/benchmark.py \
    --target_model 70b \
    --draft_model 7b
```

## 📚 学习要点

1. **核心思想**：小模型快速生成，大模型并行验证
2. **接受率关键**：决定实际加速效果
3. **自适用调整**：根据接受率动态调整 draft 长度
4. **内存开销**：需要同时加载两个模型

## 🔗 相关案例

- `vllm-inference` - vLLM 高吞吐推理
- `continuous-batching` - Continuous Batching
- `prefix-caching` - 前缀缓存优化
- `torch-compile` - PyTorch 编译优化
