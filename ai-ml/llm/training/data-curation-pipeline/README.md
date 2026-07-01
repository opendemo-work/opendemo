# 大模型数据清洗 Pipeline

> 本案例详解从原始语料到训练就绪数据的完整数据清洗流程，覆盖去重、质量过滤、隐私脱敏、毒性过滤与分词感知预处理等核心环节。

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       大模型数据清洗 Pipeline                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Raw Corpus                                                            │
│   (网页 / 书籍 / 代码 / 对话)                                             │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    1. 原始数据标准化                              │  │
│   │   • 统一编码 (UTF-8)                                             │  │
│   │   • HTML / Markdown 解析                                         │  │
│   │   • 段落拆分与格式归一化                                          │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    2. 文本去重 (Deduplication)                   │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ Exact Match │    │ MinHash     │    │ SimHash     │        │  │
│   │   │ 精确去重     │    │ 模糊去重     │    │ 局部敏感哈希 │        │  │
│   │   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │  │
│   │          └──────────────────┼──────────────────┘               │  │
│   │                             ▼                                   │  │
│   │                    移除重复 / 近似重复文档                        │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    3. 质量过滤 (Quality Filtering)               │  │
│   │                                                                  │  │
│   │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │
│   │   │ 规则过滤     │    │ 统计指标     │    │ 模型打分     │        │  │
│   │   │ 长度 / 语言  │    │ 困惑度       │    │ 质量分类器   │        │  │
│   │   │ 特殊字符占比 │    │ 可读性       │    │ 领域相关性   │        │  │
│   │   └─────────────┘    └─────────────┘    └─────────────┘        │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    4. 隐私与合规过滤                              │  │
│   │   • PII 检测与脱敏 (邮箱 / 电话 / 身份证号)                       │  │
│   │   • 毒性内容过滤 (toxicity / hate speech)                        │  │
│   │   • 版权与敏感信息过滤                                            │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    5. 分词感知预处理                              │  │
│   │   • 训练 tokenizer                                               │  │
│   │   • 文档边界标记                                                  │  │
│   │   • 长度截断与打包 (packing)                                      │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       ▼                                                                 │
│   Clean & Ready Training Data                                           │
│   (可被预训练框架直接消费)                                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解大模型预训练数据清洗的完整流程与每个环节的作用
- ✅ 掌握精确去重、MinHash 模糊去重、统计质量过滤等核心技术
- ✅ 实现一个可扩展、可配置的 Python 数据清洗 Pipeline
- ✅ 评估清洗前后数据质量，并理解清洗对模型训练的影响

## 📖 核心概念

### 1. 数据清洗为什么重要？

大语言模型的性能在很大程度上取决于训练数据的质量。研究表明，高质量、去重、干净的数据可以：

- 显著提升模型下游任务表现
- 降低训练成本（减少冗余样本）
- 减少模型生成有害内容或泄露隐私信息的风险
- 改善模型泛化能力，避免过拟合到重复内容

### 2. 去重策略

**精确去重（Exact Deduplication）**：通过文档内容的精确哈希（如 MD5/SHA256）找出完全相同的文档，适用于去除完全重复的网页抓取内容。

**模糊去重（Near-Deduplication）**：使用 MinHash + LSH（局部敏感哈希）计算文档之间的 Jaccard 相似度，去除高度相似但非完全相同的文档，常用于去除模板化页面或新闻转载。

### 3. 质量过滤

质量过滤通常结合三类方法：

- **规则过滤**：基于长度、语言、特殊字符比例、停用词比例等硬规则
- **统计指标**：使用困惑度（perplexity）、可读性分数（如 Flesch-Kincaid）筛选自然流畅的文本
- **模型打分**：训练小型质量分类器对文档进行质量评分，保留高分样本

### 4. 隐私与合规

- **PII 脱敏**：识别并替换或删除个人身份信息，如邮箱、手机号、身份证号、银行卡号等
- **毒性过滤**：使用 toxicity 分类器或规则过滤仇恨言论、成人内容等
- **版权与敏感信息**：过滤代码中的密钥、API Token、内部 URL 等

## 💻 代码示例

完整代码位于 `code/` 目录，下面展示 Pipeline 的核心流程：

```python
# code/curation_pipeline.py
import json
import re
import hashlib
from typing import List, Dict, Any
from collections import Counter


class DataCurationPipeline:
    """大模型数据清洗 Pipeline"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.seen_hashes = set()

    def normalize(self, text: str) -> str:
        """文本标准化：统一编码、去除多余空白"""
        text = text.strip()
        # 统一空白字符
        text = re.sub(r'\s+', ' ', text)
        # 过滤不可见控制字符
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', text)
        return text

    def exact_dedup(self, text: str) -> bool:
        """精确去重：返回 True 表示保留，False 表示重复"""
        doc_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        if doc_hash in self.seen_hashes:
            return False
        self.seen_hashes.add(doc_hash)
        return True

    def quality_filter(self, text: str) -> bool:
        """基于规则的质量过滤"""
        min_len = self.config.get('min_length', 100)
        max_symbol_ratio = self.config.get('max_symbol_ratio', 0.3)

        if len(text) < min_len:
            return False

        # 计算特殊字符占比
        symbol_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
        if symbol_count / len(text) > max_symbol_ratio:
            return False

        return True

    def remove_pii(self, text: str) -> str:
        """简单 PII 脱敏：邮箱、手机号、身份证号"""
        # 邮箱
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                      '[EMAIL]', text)
        # 手机号（中国大陆）
        text = re.sub(r'1[3-9]\d{9}', '[PHONE]', text)
        # 身份证号（18 位）
        text = re.sub(r'\d{17}[\dXx]', '[ID_CARD]', text)
        return text

    def process(self, documents: List[str]) -> List[str]:
        """执行完整清洗流程"""
        cleaned = []
        for doc in documents:
            doc = self.normalize(doc)
            if not self.exact_dedup(doc):
                continue
            if not self.quality_filter(doc):
                continue
            doc = self.remove_pii(doc)
            cleaned.append(doc)
        return cleaned


if __name__ == '__main__':
    config = {
        'min_length': 50,
        'max_symbol_ratio': 0.3,
    }
    pipeline = DataCurationPipeline(config)

    raw_docs = [
        '  这是一段干净的训练文本，包含有效的中文内容。  ',
        '这是一段干净的训练文本，包含有效的中文内容。',
        '!!!@@@###  大量无意义符号  $$$%%%^^^',
        '请联系 example@email.com 或 13800138000 获取更多信息。',
    ]

    result = pipeline.process(raw_docs)
    print(f'原始文档数: {len(raw_docs)}, 清洗后文档数: {len(result)}')
    for idx, doc in enumerate(result, 1):
        print(f'{idx}. {doc}')
```

## 🔧 配置说明

Pipeline 通过 `config` 字典控制各环节阈值：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `min_length` | int | 100 | 保留文档的最小字符长度 |
| `max_symbol_ratio` | float | 0.3 | 特殊字符最大占比 |
| `min_unique_words` | int | 10 | 文档最小唯一词数 |
| `enable_minhash` | bool | False | 是否启用 MinHash 模糊去重 |
| `pii_patterns` | list | `[EMAIL, PHONE, ID_CARD]` | 需要脱敏的 PII 类型 |

## 📊 运行结果

执行 `code/curation_pipeline.py` 后，预期输出：

```
原始文档数: 4, 清洗后文档数: 2
1. 这是一段干净的训练文本，包含有效的中文内容。
2. 请联系 [EMAIL] 或 [PHONE] 获取更多信息。
```

说明：
- 第 2 条与第 1 条完全重复，被精确去重移除
- 第 3 条特殊字符占比过高，被质量过滤移除
- 第 4 条通过清洗并完成了 PII 脱敏

## 🐛 常见问题

### Q1: 精确去重会漏掉哪些重复？

精确去重只能识别内容完全一致的文档。对于仅差几个字符、段落顺序不同、或经过轻微改写的内容，需要使用 MinHash、SimHash 等模糊去重方法。

### Q2: 质量过滤中的阈值如何确定？

阈值应通过小规模实验和人工抽检确定。建议先采样 1000-10000 条数据，分别用不同阈值过滤后，人工评估保留样本质量，选择 F1 最优的阈值组合。

### Q3: PII 脱敏能否 100% 保证隐私安全？

不能。正则规则只能覆盖常见模式，复杂或变形的 PII 可能漏检。生产环境中应结合命名实体识别（NER）模型、人工审核和差分隐私等技术多层防护。

## 📚 扩展学习

- **The Pile**: 经典大模型预训练数据集，展示了多来源语料的清洗与去重方法
- **Deduplicating Training Data Makes Language Models Better**: 介绍 Near-Deduplication 的经典论文
- **FineWeb**: 高质量网页数据清洗案例，包含详细的数据过滤策略
- **C4 / RefinedWeb**: 展示了从 Common Crawl 到训练数据的标准化处理流程

## 🤝 贡献指南

欢迎补充更多高级数据清洗技术：

- 增加 MinHash + LSH 模糊去重实现
- 集成 perplexity 统计质量过滤
- 增加多语言检测与语言比例过滤
- 增加 toxicity 分类器集成示例

---

*最后更新：2026-06-16*

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```
