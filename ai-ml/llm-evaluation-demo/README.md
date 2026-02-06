# 大语言模型评估实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 大语言模型评估的基本指标和方法
- 人类反馈强化学习(RLHF)和基于人类反馈的强化学习(RLAIF)
- 模型对齐和安全性评估
- 评估框架和工具的使用

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- GPU或CPU环境
- 至少16GB内存

### 依赖安装
```bash
pip install torch transformers datasets
pip install evaluate nltk rouge-score  # 评估指标
pip install openai anthropic  # API评估
pip install gradio  # 人工评估界面
```

## 📁 项目结构

```
llm-evaluation-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── eval_generation.py             # 生成质量评估脚本
│   ├── eval_safety.py                 # 安全性评估脚本
│   └── eval_bias.py                   # 偏见评估脚本
├── configs/                           # 配置文件
│   ├── evaluation_config.json         # 评估配置
│   └── metrics_config.json            # 指标配置
├── metrics/                           # 评估指标
│   ├── automatic_metrics.py           # 自动化指标
│   ├── human_eval_metrics.py          # 人工评估指标
│   └── safety_metrics.py              # 安全指标
├── data/                              # 评估数据
│   ├── benchmarks/                    # 基准测试数据
│   ├── prompts/                       # 提示词数据
│   └── reference_responses/           # 参考回复
├── models/                            # 模型文件
│   ├── target_models/                 # 待评估模型
│   └── reference_models/              # 参考模型
└── notebooks/                         # Jupyter笔记本
    ├── 01_automatic_evaluation.ipynb  # 自动评估
    ├── 02_human_evaluation.ipynb      # 人工评估
    └── 03_safety_assessment.ipynb     # 安全评估
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装评估依赖
pip install -r requirements.txt
```

### 步骤2：运行自动评估

```bash
# 运行自动化评估
python scripts/eval_generation.py \
  --model_path facebook/opt-350m \
  --benchmark hellaswag \
  --metrics bleu,rouge,perplexity \
  --output_dir results/automatic_eval/
```

### 步骤3：运行安全性评估

```bash
# 运行安全性评估
python scripts/eval_safety.py \
  --model_path facebook/opt-350m \
  --attack_prompts data/attack_prompts.txt \
  --metrics toxicity,jailbreak \
  --output_dir results/safety_eval/
```

## 🔍 代码详解

### 核心概念解析

#### 1. 评估指标实现
```python
# BLEU分数计算
from evaluate import load
bleu = load("bleu")

def calculate_bleu_score(predictions, references):
    """计算BLEU分数"""
    results = bleu.compute(predictions=predictions, references=references)
    return results["bleu"]

# ROUGE分数计算
rouge = load("rouge")

def calculate_rouge_score(predictions, references):
    """计算ROUGE分数"""
    results = rouge.compute(predictions=predictions, references=references)
    return results
```

#### 2. 实际应用示例

##### 场景1：RLHF评估
```python
# 基于人类反馈的评估
def rlhf_evaluation(model, reward_model, prompts, references):
    """RLHF评估流程"""
    # 1. 收集模型生成
    generations = []
    for prompt in prompts:
        generation = model.generate(prompt)
        generations.append(generation)
    
    # 2. 使用奖励模型评分
    scores = []
    for gen, ref in zip(generations, references):
        score = reward_model.predict(gen, ref)
        scores.append(score)
    
    # 3. 计算平均奖励
    avg_reward = sum(scores) / len(scores)
    return avg_reward
```

##### 场景2：安全性评估
```python
# 安全性评估实现
def safety_evaluation(model, attack_prompts, safety_checker):
    """安全性评估"""
    unsafe_count = 0
    total_count = len(attack_prompts)
    
    for prompt in attack_prompts:
        response = model.generate(prompt)
        is_safe = safety_checker.check(response)
        
        if not is_safe:
            unsafe_count += 1
    
    safety_rate = (total_count - unsafe_count) / total_count
    return safety_rate
```

## 🧪 验证测试

### 测试1：评估指标验证
```python
#!/usr/bin/env python
# 验证评估指标
from evaluate import load

def test_evaluation_metrics():
    print("=== 评估指标验证 ===")
    
    # 测试BLEU
    try:
        bleu = load("bleu")
        predictions = ["hello world", "good morning"]
        references = [["hello world"], ["good morning"]]
        score = bleu.compute(predictions=predictions, references=references)
        print(f"✅ BLEU指标正常: {score['bleu']:.3f}")
    except Exception as e:
        print(f"⚠️ BLEU指标异常: {e}")
    
    # 测试ROUGE
    try:
        rouge = load("rouge")
        score = rouge.compute(predictions=predictions, references=references)
        print(f"✅ ROUGE指标正常: {score}")
    except Exception as e:
        print(f"⚠️ ROUGE指标异常: {e}")
    
    # 测试准确率
    try:
        accuracy = load("accuracy")
        predictions = [0, 1, 0, 1]
        references = [0, 1, 1, 1]
        score = accuracy.compute(predictions=predictions, references=references)
        print(f"✅ 准确率指标正常: {score['accuracy']:.3f}")
    except Exception as e:
        print(f"⚠️ 准确率指标异常: {e}")

if __name__ == "__main__":
    test_evaluation_metrics()
```

### 测试2：模型评估流程验证
```python
#!/usr/bin/env python
# 验证模型评估流程
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def test_model_evaluation():
    print("=== 模型评估流程验证 ===")
    
    # 加载模型和tokenizer
    model_name = "facebook/opt-350m"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # 设置pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # 测试生成
    test_prompt = "The capital of France is"
    inputs = tokenizer(test_prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=len(inputs.input_ids[0]) + 20,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✅ 生成测试通过")
    print(f"输入: {test_prompt}")
    print(f"输出: {generated_text[len(test_prompt):]}")
    
    # 计算困惑度
    with torch.no_grad():
        logits = model(**inputs).logits
        shift_logits = logits[..., :-1, :].contiguous()
        shift_labels = inputs.input_ids[..., 1:].contiguous()
        
        loss_fct = torch.nn.CrossEntropyLoss()
        loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
        perplexity = torch.exp(loss)
        
    print(f"✅ 困惑度计算: {perplexity:.2f}")

if __name__ == "__main__":
    test_model_evaluation()
```

## ❓ 常见问题

### Q1: 如何设计有效的评估基准？
**解决方案**：
```python
# 评估基准设计原则
"""
1. 多样性: 覆盖不同领域和任务类型
2. 代表性: 反映真实使用场景
3. 可重复性: 结果可复现和比较
4. 全面性: 涵盖功能性、安全性、公平性等方面
"""
```

### Q2: 如何处理评估中的偏差问题？
**解决方案**：
```python
# 偏差处理策略
"""
1. 多样化测试集: 包含不同群体、文化背景的数据
2. 偏差检测: 使用专门的偏差检测工具
3. 对比评估: 与基线模型进行对比
4. 人工审核: 结合人工判断进行评估
"""
```

## 📚 扩展学习

### 相关技术
- **HELM**: Holistic Evaluation of Language Models
- **BIG-bench**: Beyond the Imitation Game Benchmark
- **MT-Bench**: 多轮对话评估基准
- **TruthfulQA**: 真实性评估基准

### 进阶学习路径
1. 掌握不同评估方法的优缺点
2. 学习评估结果的统计分析方法
3. 理解模型对齐和价值观一致性
4. 掌握自动化评估系统的构建

### 企业级应用场景
- 大模型产品上线前的安全评估
- 模型迭代过程中的性能对比
- 客户定制模型的合规性验证
- AI系统的风险管控和审计

---
> **💡 提示**: 大语言模型评估是确保模型质量和安全性的关键环节，需要综合考虑性能、安全、伦理等多个维度，是负责任AI发展的重要保障。