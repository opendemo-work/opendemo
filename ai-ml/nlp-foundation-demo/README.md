# 自然语言处理基础实战演示

## 🎯 学习目标

通过本案例你将掌握：
- 自然语言处理的基础概念和核心技术
- 文本预处理和特征提取方法
- 经典NLP任务的实现（分类、序列标注、生成）
- 现代NLP模型（BERT、GPT等）的应用

## 🛠️ 环境准备

### 系统要求
- Python 3.8+
- GPU或CPU环境
- 至少16GB内存

### 依赖安装
```bash
pip install torch transformers scikit-learn
pip install nltk spacy gensim  # NLP库
pip install datasets tokenizers  # 数据处理
pip install sentencepiece protobuf  # 分词工具
pip install matplotlib seaborn  # 可视化
pip install pytest  # 测试工具
```

## 📁 项目结构

```
nlp-foundation-demo/
├── README.md                           # 本说明文档
├── metadata.json                       # 元数据配置
├── scripts/                           # 实用脚本
│   ├── preprocess_text.py             # 文本预处理脚本
│   ├── train_classifier.py            # 分类模型训练脚本
│   ├── train_tagger.py                # 序列标注训练脚本
│   └── evaluate_nlp.py                # NLP评估脚本
├── configs/                           # 配置文件
│   ├── preprocessing_config.json      # 预处理配置
│   ├── model_config.json              # 模型配置
│   └── training_config.yaml           # 训练配置
├── models/                            # 模型文件
│   ├── architectures/                 # 模型架构
│   │   ├── lstm.py                  # LSTM架构
│   │   ├── transformer.py             # Transformer架构
│   │   ├── bert.py                   # BERT架构
│   │   └── gpt.py                    # GPT架构
│   ├── pretrained/                    # 预训练模型
│   └── checkpoints/                   # 训练检查点
├── data/                              # 数据文件
│   ├── raw/                           # 原始文本
│   ├── processed/                     # 处理后数据
│   ├── vocab/                         # 词汇表
│   └── samples/                       # 示例文本
├── preprocessing/                     # 预处理模块
│   ├── tokenizer.py                   # 分词器
│   ├── normalizer.py                  # 标准化
│   ├── cleaner.py                     # 文本清洗
│   └── featurizer.py                  # 特征提取
├── tasks/                             # NLP任务
│   ├── classification/                # 文本分类
│   ├── tagging/                       # 序列标注
│   ├── generation/                    # 文本生成
│   └── translation/                   # 机器翻译
├── evaluation/                        # 评估模块
│   ├── metrics.py                     # 评估指标
│   ├── scorers.py                     # 评分器
│   └── analysis.py                    # 分析工具
├── utils/                             # 工具函数
│   ├── data_utils.py                  # 数据工具
│   ├── model_utils.py                 # 模型工具
│   └── visualization.py               # 可视化工具
└── notebooks/                         # Jupyter笔记本
    ├── 01_text_preprocessing.ipynb     # 文本预处理
    ├── 02_word_embeddings.ipynb        # 词嵌入
    └── 03_transformer_architecture.ipynb # Transformer架构
```

## 🚀 快速开始

### 步骤1：环境设置

```bash
# 安装NLP相关依赖
pip install -r requirements.txt

# 下载NLTK数据
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 步骤2：文本预处理

```bash
# 预处理文本数据
python scripts/preprocess_text.py \
  --input_file data/raw/sample_texts.txt \
  --output_dir data/processed/ \
  --tokenizer_type bert \
  --max_length 512
```

### 步骤3：训练文本分类模型

```bash
# 训练BERT分类器
python scripts/train_classifier.py \
  --model_name bert-base-uncased \
  --train_file data/processed/train.json \
  --validation_file data/processed/validation.json \
  --output_dir models/checkpoints/classifier/ \
  --num_epochs 3 \
  --batch_size 16 \
  --learning_rate 2e-5
```

### 步骤4：运行NLP评估

```bash
# 评估模型性能
python scripts/evaluate_nlp.py \
  --model_path models/checkpoints/classifier/ \
  --test_file data/processed/test.json \
  --task classification \
  --output_dir results/evaluation/
```

## 🔍 代码详解

### 核心概念解析

#### 1. Transformer架构实现
```python
# models/architectures/transformer.py
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        matmul_qk = torch.matmul(Q, K.transpose(-2, -1))
        dk = K.size()[-1]
        scaled_attention_logits = matmul_qk / math.sqrt(dk)
        
        if mask is not None:
            scaled_attention_logits += (mask * -1e9)
        
        attention_weights = torch.softmax(scaled_attention_logits, dim=-1)
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights
    
    def split_heads(self, x):
        batch_size = x.size(0)
        seq_len = x.size(1)
        
        x = x.view(batch_size, seq_len, self.num_heads, self.d_k)
        return x.transpose(1, 2)
    
    def forward(self, Q, K, V, mask=None):
        Q = self.W_q(Q)
        K = self.W_k(K)
        V = self.W_v(V)
        
        Q = self.split_heads(Q)
        K = self.split_heads(K)
        V = self.split_heads(V)
        
        scaled_attention, attention_weights = self.scaled_dot_product_attention(
            Q, K, V, mask)
        
        scaled_attention = scaled_attention.transpose(1, 2).contiguous()
        original_size = scaled_attention.size()
        concat_attention = scaled_attention.view(
            original_size[0], original_size[1], self.d_model)
        
        output = self.W_o(concat_attention)
        
        return output, attention_weights

class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super(PositionwiseFeedForward, self).__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.ReLU()
    
    def forward(self, x):
        x = self.dropout(self.activation(self.linear1(x)))
        x = self.linear2(x)
        return x

class EncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super(EncoderLayer, self).__init__()
        self.self_attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionwiseFeedForward(d_model, d_ff, dropout)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Self-attention
        attended, attention_weights = self.self_attention(x, x, x, mask)
        x = self.norm1(x + self.dropout1(attended))
        
        # Feed-forward
        ff_out = self.feed_forward(x)
        x = self.norm2(x + self.dropout2(ff_out))
        
        return x, attention_weights
```

#### 2. 实际应用示例

##### 场景1：文本分类实现
```python
# tasks/classification/classifier.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import BertModel, BertTokenizer

class TextClassificationDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

class BERTClassifier(nn.Module):
    def __init__(self, model_name, num_classes, dropout=0.3):
        super(BERTClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_classes)
    
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        pooled_output = outputs.pooler_output
        output = self.dropout(pooled_output)
        return self.classifier(output)

def train_classifier(model, train_dataloader, val_dataloader, epochs=3, lr=2e-5):
    """训练分类器"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for batch in train_dataloader:
            optimizer.zero_grad()
            
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        avg_train_loss = total_loss / len(train_dataloader)
        
        # 验证
        model.eval()
        val_accuracy = evaluate_model(model, val_dataloader, device)
        model.train()
        
        print(f'Epoch {epoch+1}/{epochs}')
        print(f'Train Loss: {avg_train_loss:.4f}')
        print(f'Validation Accuracy: {val_accuracy:.4f}')
        print('-' * 50)
```

##### 场景2：序列标注实现（NER）
```python
# tasks/tagging/ner_tagger.py
import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer

class NERModel(nn.Module):
    def __init__(self, model_name, num_labels, dropout=0.1):
        super(NERModel, self).__init__()
        self.bert = BertModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)
        self.num_labels = num_labels
    
    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        sequence_output = outputs.last_hidden_state
        sequence_output = self.dropout(sequence_output)
        logits = self.classifier(sequence_output)
        
        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            # Only keep active parts of the loss
            if attention_mask is not None:
                active_loss = attention_mask.view(-1) == 1
                active_logits = logits.view(-1, self.num_labels)
                active_labels = torch.where(
                    active_loss, labels.view(-1), torch.tensor(loss_fct.ignore_index).type_as(labels)
                )
                loss = loss_fct(active_logits, active_labels)
            else:
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
        
        return {
            'loss': loss,
            'logits': logits
        }

# NER标签映射
NER_LABELS = {
    'O': 0,        # Outside of a named entity
    'B-PER': 1,    # Beginning of a person name
    'I-PER': 2,    # Inside of a person name
    'B-ORG': 3,    # Beginning of an organization name
    'I-ORG': 4,    # Inside of an organization name
    'B-LOC': 5,    # Beginning of a location name
    'I-LOC': 6,    # Inside of a location name
    'B-MISC': 7,   # Beginning of a miscellaneous name
    'I-MISC': 8    # Inside of a miscellaneous name
}
```

## 🧪 验证测试

### 测试1：模型构建验证
```python
#!/usr/bin/env python
# 验证NLP模型构建
import torch
from transformers import BertTokenizer, BertModel

def test_nlp_model():
    print("=== NLP模型构建验证 ===")
    
    # 测试BERT模型
    model_name = 'bert-base-uncased'
    try:
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertModel.from_pretrained(model_name)
        
        print(f"✅ BERT模型加载成功")
        print(f"模型参数数量: {sum(p.numel() for p in model.parameters()):,}")
        
        # 测试文本编码
        test_text = "Hello, how are you doing today?"
        encoded = tokenizer(test_text, return_tensors='pt', padding=True, truncation=True)
        
        print(f"✅ 文本编码成功")
        print(f"输入IDs形状: {encoded['input_ids'].shape}")
        print(f"注意力掩码形状: {encoded['attention_mask'].shape}")
        
        # 测试前向传播
        with torch.no_grad():
            outputs = model(**encoded)
        
        print(f"✅ 前向传播正常")
        print(f"序列输出形状: {outputs.last_hidden_state.shape}")
        print(f"池化输出形状: {outputs.pooler_output.shape}")
        
    except Exception as e:
        print(f"❌ 模型验证失败: {e}")
        print("可能需要检查网络连接或安装transformers库")
    
    print("✅ NLP模型验证完成")

if __name__ == "__main__":
    test_nlp_model()
```

### 测试2：文本预处理验证
```python
#!/usr/bin/env python
# 验证文本预处理管道
import re
import string
from collections import Counter

def test_text_preprocessing():
    print("=== 文本预处理管道验证 ===")
    
    # 测试文本
    raw_text = "Hello World! This is a SAMPLE text with numbers 123 and symbols @#$%."
    
    # 基础预处理步骤
    print(f"原始文本: {raw_text}")
    
    # 1. 转换为小写
    lower_text = raw_text.lower()
    print(f"转小写后: {lower_text}")
    
    # 2. 移除标点符号
    no_punct_text = lower_text.translate(str.maketrans('', '', string.punctuation))
    print(f"移除标点后: {no_punct_text}")
    
    # 3. 分词
    tokens = no_punct_text.split()
    print(f"分词后: {tokens}")
    
    # 4. 移除停用词（简化版）
    stop_words = {'is', 'a', 'with', 'and'}
    filtered_tokens = [token for token in tokens if token not in stop_words]
    print(f"移除停用词后: {filtered_tokens}")
    
    # 5. 统计词频
    word_freq = Counter(filtered_tokens)
    print(f"词频统计: {dict(word_freq)}")
    
    print("✅ 文本预处理管道验证通过")

if __name__ == "__main__":
    test_text_preprocessing()
```

## ❓ 常见问题

### Q1: 如何选择合适的NLP模型架构？
**解决方案**：
```python
# NLP模型架构选择指南
"""
1. 文本分类: BERT, RoBERTa, DistilBERT
2. 序列标注: BERT+CRF, BiLSTM-CRF
3. 文本生成: GPT, T5, BART
4. 机器翻译: Transformer, MarianMT
"""
```

### Q2: 如何处理长文本序列？
**解决方案**：
```python
# 长文本处理策略
"""
1. 分块处理: 将长文本分割为固定长度块
2. 滑动窗口: 使用重叠窗口捕捉上下文
3. 层次建模: 先句子级再文档级建模
4. 稀疏注意力: 使用Longformer, BigBird等
"""
```

## 📚 扩展学习

### 相关技术
- **spaCy**: 工业级NLP库
- **NLTK**: 自然语言工具包
- **Transformers**: Hugging Face模型库
- **AllenNLP**: 深度学习NLP平台

### 进阶学习路径
1. 掌握经典NLP任务的实现方法
2. 学习预训练模型的微调技巧
3. 理解多语言NLP和跨语言迁移
4. 掌握大语言模型的对齐技术

### 企业级应用场景
- 情感分析和舆情监控
- 命名实体识别和信息抽取
- 文本摘要和内容生成
- 机器翻译和多语言支持

---
> **💡 提示**: 自然语言处理是AI的重要分支，通过深度学习技术实现了文本理解、生成和转换等复杂任务，是构建智能对话系统和内容处理平台的基础。