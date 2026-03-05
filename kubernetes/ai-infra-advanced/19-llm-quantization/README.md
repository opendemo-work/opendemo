# LLM量化压缩

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **方法**: AWQ, GPTQ, INT8, INT4

---

## 概述

大语言模型量化是降低模型部署成本的关键技术，通过降低模型精度减少显存占用和推理延迟。

---

## AWQ量化

### AWQ量化Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: awq-quantization
  namespace: llm-training
spec:
  template:
    spec:
      containers:
        - name: quantize
          image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
          command:
            - python
            - quantize_awq.py
            - --model_path
            - /models/llama-2-7b-hf
            - --output_path
            - /models/llama-2-7b-awq
            - --w_bit
            - "4"
            - --q_group_size
            - "128"
          resources:
            limits:
              nvidia.com/gpu: 1
              memory: 24Gi
          volumeMounts:
            - name: model-storage
              mountPath: /models
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: models-pvc
      restartPolicy: Never
```

### AWQ量化脚本

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "/models/llama-2-7b-hf"
output_path = "/models/llama-2-7b-awq"

model = AutoAWQForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_path)

quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM"
}

model.quantize(
    tokenizer,
    quant_config=quant_config,
    calib_data="pileval"
)

model.save_quantized(output_path)
tokenizer.save_pretrained(output_path)
```

---

## GPTQ量化

### GPTQ量化配置

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: gptq-quantization
  namespace: llm-training
spec:
  template:
    spec:
      containers:
        - name: quantize
          image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
          command:
            - python
            - quantize_gptq.py
            - --model
            - /models/llama-2-7b-hf
            - --output_dir
            - /models/llama-2-7b-gptq
            - --bits
            - "4"
            - --groupsize
            - "128"
            - --act-order
          resources:
            limits:
              nvidia.com/gpu: 1
              memory: 24Gi
```

### GPTQ量化脚本

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig

model_path = "/models/llama-2-7b-hf"
output_path = "/models/llama-2-7b-gptq"

quantization_config = GPTQConfig(
    bits=4,
    group_size=128,
    desc_act=True,
    sym=False,
    true_sequential=True,
    dataset="c4"
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quantization_config,
    torch_dtype=torch.float16,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_path)

model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)
```

---

## vLLM量化推理

### INT4量化推理

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-quantized
  namespace: llm-serving
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-quantized
  template:
    metadata:
      labels:
        app: vllm-quantized
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:latest
          args:
            - --model
            - /models/llama-2-7b-awq
            - --quantization
            - awq
            - --dtype
            - half
            - --max-model-len
            - "4096"
            - --gpu-memory-utilization
            - "0.8"
          resources:
            limits:
              nvidia.com/gpu: 1
              memory: 12Gi
            requests:
              nvidia.com/gpu: 1
              memory: 8Gi
          volumeMounts:
            - name: model-storage
              mountPath: /models
      volumes:
        - name: model-storage
          persistentVolumeClaim:
            claimName: quantized-models-pvc
```

---

## 量化效果对比

| 量化方法 | 精度 | 显存占用 | 推理速度 | 精度损失 |
|---------|------|---------|---------|---------|
| FP16 | 16bit | 14GB | 基准 | 0% |
| INT8 | 8bit | 7GB | +20% | <1% |
| INT4 (AWQ) | 4bit | 4GB | +30% | 1-2% |
| INT4 (GPTQ) | 4bit | 4GB | +25% | 1-3% |

---

## 相关案例

- [LLM微调训练](../16-llm-finetuning/) - 模型微调
- [LLM推理服务](../17-llm-inference-serving/) - 模型推理
- [AI成本分析](../12-ai-cost-analysis-finops/) - 成本优化

---

**维护者**: OpenDemo Team | **许可证**: MIT
