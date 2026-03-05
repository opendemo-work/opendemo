# LLM微调训练

> **适用版本**: v1.25 - v1.32 | **最后更新**: 2026-03 | **方法**: LoRA, QLoRA, Full Fine-tuning

---

## 概述

大语言模型微调是AI基础设施的核心应用场景，涵盖全量微调、LoRA、QLoRA等多种微调方法。

---

## LoRA微调

### LoRA训练Job

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: lora-finetuning
  namespace: llm-training
spec:
  schedulerName: volcano
  minAvailable: 1
  tasks:
    - replicas: 1
      name: worker
      policies:
        - event: TaskCompleted
          action: CompleteJob
      template:
        spec:
          containers:
            - name: finetune
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - python
                - train_lora.py
                - --model_name_or_path
                - /models/llama-2-7b-hf
                - --data_path
                - /data/train.json
                - --output_dir
                - /output/lora-adapter
                - --num_train_epochs
                - "3"
                - --per_device_train_batch_size
                - "4"
                - --gradient_accumulation_steps
                - "4"
                - --learning_rate
                - "2e-4"
                - --lora_r
                - "16"
                - --lora_alpha
                - "32"
                - --lora_dropout
                - "0.05"
              resources:
                limits:
                  nvidia.com/gpu: 1
                  memory: 24Gi
                requests:
                  nvidia.com/gpu: 1
                  memory: 16Gi
              volumeMounts:
                - name: model-storage
                  mountPath: /models
                - name: data-storage
                  mountPath: /data
                - name: output-storage
                  mountPath: /output
          volumes:
            - name: model-storage
              persistentVolumeClaim:
                claimName: llama2-models-pvc
            - name: data-storage
              persistentVolumeClaim:
                claimName: training-data-pvc
            - name: output-storage
              persistentVolumeClaim:
                claimName: lora-output-pvc
```

### LoRA训练脚本

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer
from datasets import load_dataset

model_name = "/models/llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
)

model = get_peft_model(model, lora_config)

dataset = load_dataset("json", data_files="/data/train.json")

training_args = TrainingArguments(
    output_dir="/output/lora-adapter",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=100,
    save_total_limit=3
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
    max_seq_length=512
)

trainer.train()
model.save_pretrained("/output/lora-adapter")
```

---

## QLoRA微调

### QLoRA配置

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: qlora-finetuning
  namespace: llm-training
spec:
  schedulerName: volcano
  minAvailable: 1
  tasks:
    - replicas: 1
      name: worker
      template:
        spec:
          containers:
            - name: finetune
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - python
                - train_qlora.py
                - --model_name_or_path
                - /models/llama-2-70b-hf
                - --data_path
                - /data/train.json
                - --output_dir
                - /output/qlora-adapter
                - --bits
                - "4"
                - --quant_type
                - nf4
                - --double_quant
                - "true"
              resources:
                limits:
                  nvidia.com/gpu: 4
                  memory: 48Gi
                requests:
                  nvidia.com/gpu: 4
                  memory: 48Gi
```

### QLoRA训练脚本

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "/models/llama-2-70b-hf",
    quantization_config=quantization_config,
    device_map="auto"
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
```

---

## 分布式微调

### 多GPU微调

```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: distributed-finetuning
  namespace: llm-training
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - torchrun
                - --nproc_per_node=8
                - --nnodes=2
                - train_distributed.py
              resources:
                limits:
                  nvidia.com/gpu: 8
                  memory: 256Gi
    Worker:
      replicas: 1
      template:
        spec:
          containers:
            - name: pytorch
              image: pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
              command:
                - torchrun
                - --nproc_per_node=8
                - --nnodes=2
                - train_distributed.py
              resources:
                limits:
                  nvidia.com/gpu: 8
                  memory: 256Gi
```

---

## 相关案例

- [分布式训练框架](../05-distributed-training-frameworks/) - 训练框架
- [LLM推理服务](../17-llm-inference-serving/) - 模型推理
- [LLM量化压缩](../19-llm-quantization/) - 模型优化

---

**维护者**: OpenDemo Team | **许可证**: MIT
