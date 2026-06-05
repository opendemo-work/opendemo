# Few-Shot Learning

> 本案例详解 LLM Few-Shot Learning 技术，包括 In-Context Learning、示例选择策略、示例格式设计。

## 📐 Few-Shot 分类

```
┌──────────────────────────────────────────────────────┐
│                   Few-Shot Learning                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Zero-Shot ─────── 无示例，仅靠指令                    │
│       │                                               │
│       ▼                                               │
│  One-Shot ─────── 1 个示例                            │
│       │                                               │
│       ▼                                               │
│  Few-Shot ─────── K 个示例 (通常 3-10)                │
│       │                                               │
│       ▼                                               │
│  Multi-Shot ───── 大量示例，接近微调效果               │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 核心策略

### 1. 示例选择

| 策略 | 方法 | 优缺点 |
|------|------|--------|
| Random | 随机选择 | 简单，可能不佳 |
| Similarity | 找相似样本 | 需要样本库 |
| Coverage | 多样性覆盖 | 更全面 |
| LLM-based | LLM 选择 | 最优但慢 |

### 2. 示例格式

```python
# 问答格式
qa_template = """Q: {question}
A: {answer}

Q: {new_question}
A:"""

# 链式格式
cot_template = """Problem: {problem}
Step 1: {step1}
Step 2: {step2}
Conclusion: {conclusion}

Problem: {new_problem}
Step 1:"""
```

## 💻 核心实现

### Semantic Similarity 示例选择

```python
from langchain.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticExampleSelector:
    def __init__(self, examples: list, embeddings_model):
        self.examples = examples
        self.embeddings_model = embeddings_model
        self.example_embeddings = embeddings_model.embed_documents(
            [ex["text"] for ex in examples]
        )
    
    def select(self, query: str, k=5):
        query_embedding = self.embeddings_model.embed_query(query)
        
        similarities = cosine_similarity(
            [query_embedding],
            self.example_embeddings
        )[0]
        
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        return [self.examples[i] for i in top_k_indices]
```

### Diverse Example Selection

```python
class DiverseExampleSelector:
    def __init__(self, examples: list, embeddings_model, max_examples=10):
        self.examples = examples
        self.embeddings_model = embeddings_model
        self.max_examples = max_examples
    
    def select(self, query: str, k=5):
        query_embedding = self.embeddings_model.embed_query(query)
        
        selected = []
        remaining = self.examples.copy()
        query_emb = query_embedding
        
        while len(selected) < min(k, len(remaining)):
            best_idx = 0
            best_score = -float('inf')
            
            for i, ex in enumerate(remaining):
                ex_emb = self.embeddings_model.embed_query(ex["text"])
                relevance = cosine_similarity([query_emb], [ex_emb])[0][0]
                diversity = min(
                    cosine_similarity([ex_emb], [self.embeddings_model.embed_query(s["text"])])[0][0]
                    for s in selected
                ) if selected else 1
                
                score = 0.5 * relevance + 0.5 * diversity
                
                if score > best_score:
                    best_score = score
                    best_idx = i
            
            selected.append(remaining.pop(best_idx))
        
        return selected
```

### Dynamic Few-Shot Prompt

```python
class DynamicFewShotPrompter:
    def __init__(self, example_selector, template):
        self.example_selector = example_selector
        self.template = template
    
    def build_prompt(self, query: str, k=5):
        examples = self.example_selector.select(query, k=k)
        
        example_texts = []
        for ex in examples:
            example_texts.append(self.template.format(**ex))
        
        return "\n\n".join(example_texts) + f"\n\nQuery: {query}\nAnswer:"
    
    def invoke(self, query: str, llm, k=5):
        prompt = self.build_prompt(query, k=k)
        return llm.invoke(prompt)
```

## 📊 Few-Shot 最佳实践

| 场景 | 推荐示例数 | 格式建议 |
|------|------------|----------|
| 分类 | 3-5 | Input-Output |
| 问答 | 2-3 | Q-A |
| 推理 | 1-2 | CoT 格式 |
| 代码生成 | 1 | 完整函数 |

## 📋 命令速查

```bash
pip install langchain openai scikit-learn

# 运行示例选择对比
python few_shot/selectors.py

# 测试动态 Few-Shot
python few_shot/dynamic.py
```

## 🔗 相关案例

- `chain-of-thought` - 思维链
- `prompt-patterns` - Prompt 工程
- `tree-of-thought` - 思维树
