---
title: AWQ Quantization
summary: Activation-Aware Weight Quantization considers both weight and activation distributions for higher accuracy than weight-only methods like GPTQ.
updated: 2026-06-05
tags:
  - llm
  - optimization
  - quantization
sources:
  - /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/ai-ml/llm/optimization/awq-quantization/README.md
base_confidence: 0.7
lifecycle: draft
tier: supporting
---

# AWQ Quantization

AWQ (Activation-Aware Weight Quantization) considers both weight and activation distributions, achieving better accuracy than weight-only quantization methods like GPTQ.

## Core Principle

```
GPTQ: Only considers weight distribution, ignores activation statistics
AWQ:  Weight × Activation distribution, considers quantization error jointly

AWQ Core Insight:
- Not all weights are equally important
- Channels with larger activation values need higher weight precision
- Scale factors auto-adjusted based on activation ratios
```

## Quantization Formula

```python
def compute_awq_scale(weight, activation):
    act_scale = activation.abs().max(dim=0)[0]
    scale = (act_scale / act_scale.max()).sqrt()
    scaled_weight = weight / scale
    return scaled_weight, scale
```

## Implementation

```python
class AWQQuantizer:
    def __init__(self, w_bit=4, group_size=128):
        self.w_bit = w_bit
        self.group_size = group_size
        
    def quantize_awq(self, weight, activation):
        scale = self.compute_scale(weight, activation)
        scaled_w = weight / scale
        quantized = self.group_quantize(scaled_w)
        return quantized, scale
    
    def compute_scale(self, weight, activation):
        act_scale = activation.abs().mean(dim=0)
        weight_scale = weight.abs().mean(dim=0)
        combined = act_scale * weight_scale
        scale = (combined / combined.max()).clamp(min=1e-4)
        return scale
    
    def group_quantize(self, tensor):
        shape = tensor.shape
        tensor = tensor.view(-1, self.group_size)
        max_val = tensor.abs().max(dim=-1, keepdim=True)[0]
        scale = (max_val * 2 / (2**self.w_bit - 1)).clamp(min=1e-8)
        quantized = (tensor / scale).round().to(torch.int8)
        return quantized, scale
```

## Accuracy Comparison

| Method | WikiText-2 PPL | MMLU | Memory Reduction |
|--------|---------------|------|------------------|
| FP16 | 12.5 | 68.2 | 1.0x |
| GPTQ INT4 | 14.2 | 63.5 | 4.0x |
| AWQ INT4 | 13.1 | 66.8 | 4.0x |

## Usage

```bash
pip install autoawq
python -m awq.quantize model --w_bit 4 --group_size 128
python evaluate.py --model awq_model --task mmlu
```

## Key Takeaways

1. **AWQ advantage**: Activation-aware quantization, higher accuracy than weight-only methods
2. **vs GPTQ**: AWQ preserves activation distribution while quantizing weights
3. **4-bit quantization**: Smaller group_size = higher accuracy, more memory
4. **Use cases**: High-accuracy quantization deployment for LLaMA/Vicuna models

## Related

- [[entities/kv-cache-optimization]] - KV Cache quantization
- [[entities/sparsegpt-pruning]] - Structured pruning methods
- [[entities/tensorrt-inference]] - Inference optimization
- [[entities/tech-stacks]] - LLM optimization stack
